import os
import asyncio
import uuid
from dotenv import load_dotenv
from typing import Optional
import json
import logging

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions, RoomOutputOptions
from livekit.plugins import (
    openai,
    google,
    tavus,
    deepgram,
    silero,
    elevenlabs,
)

# Import avatar backstories
from avatar_backstories import get_avatar_backstory, get_avatar_personality

# Monkey-patch approach: intercept logger.debug() calls directly
_original_livekit_logger_debug = None

def _patched_debug(msg, *args, **kwargs):
    """Intercept debug calls to capture transcript data"""
    # Call original first
    _original_livekit_logger_debug(msg, *args, **kwargs)
    
    # Check if this is a transcript message
    if "received user transcript" in str(msg):
        # kwargs might contain the transcript data in structured logging
        if 'extra' in kwargs and isinstance(kwargs['extra'], dict):
            transcript = kwargs['extra'].get('user_transcript')
            if transcript:
                _global_transcript_history.append(f"User: {transcript}")
                _global_last_transcript[0] = transcript
        
        # Or it might be in args as a dict
        if args and isinstance(args[0], dict):
            transcript = args[0].get('user_transcript')
            if transcript:
                _global_transcript_history.append(f"User: {transcript}")
                _global_last_transcript[0] = transcript

# Import memory service
try:
    from memory_service import get_memory_service
    MEMORY_ENABLED = True
    print("[avatar_agent] ✅ Memory service available")
except Exception as e:
    MEMORY_ENABLED = False
    print(f"[avatar_agent] ⚠️ Memory service not available: {e}")

LANG_EN = "en-US"
LANG_ZH = "cmn-CN"
load_dotenv()

TAVUS_API_KEY = os.getenv("TAVUS_API_KEY")

# Avatar configuration mapping
AVATAR_CONFIG = {
    'alex': {
        'replica_id': 'r62baeccd777',
        'persona_id': 'p72bafe6bb9a',
        'voice_id': 'pNInz6obpgDQGcFmaJgB',  # Male voice - Adam
        'display_name': 'Alex',
        'description': 'Charming & Witty'
    },
    'emma': {
        'replica_id': 'r6ae5b6efc9d',
        'persona_id': 'p1b06420cfdc',
        'voice_id': 'EXAVITQu4vr4xnSDxMaL',  # Female voice - Bella
        'display_name': 'Emma',
        'description': 'Sweet & Intelligent'
    }
}
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
USER_DISPLAY_NAME = os.getenv("USER_DISPLAY_NAME", "")  # Get display name for memory

# Get language from environment and map to proper constants
LANGUAGE_CODE = os.getenv("LANGUAGE", "en-US")
LANGUAGE = LANG_EN if LANGUAGE_CODE == "en-US" else LANG_ZH

# Global transcript capture storage (shared across sessions in same process)
_global_transcript_history = []
_global_last_transcript = [None]

# Apply monkey-patch at module level (before LiveKit initializes)
_livekit_logger = logging.getLogger("livekit.agents")
_original_livekit_logger_debug = _livekit_logger.debug
_livekit_logger.debug = _patched_debug
print("[avatar_agent] 🐵 Monkey-patched livekit.agents logger.debug()")


class VideoAssistant(Agent):
    def __init__(self, memory_context: str = "", memory_service=None, user_name: str = None, language: str = "en-US", avatar_config: dict = None) -> None:
        # Store memory service and user_name for runtime use
        self.memory_service = memory_service
        self.user_name = user_name
        self.language = language
        self.avatar_config = avatar_config or {}
        self.conversation_buffer = {"user": None, "assistant": None}
        self.last_user_transcript = ""
        self.last_agent_transcript = ""
        
        # Language is always English for AuraDate
        is_chinese = False
        
        # Debug: Show TTS configuration
        voice_id = self.avatar_config.get('voice_id', 'pNInz6obpgDQGcFmaJgB')
        print(f"[VideoAssistant] TTS Configuration: voice_id={voice_id}, model=eleven_multilingual_v2")
        
        # Get avatar backstory and personality
        avatar_name = self.avatar_config.get('display_name', 'Alex').lower()
        avatar_backstory = get_avatar_backstory(avatar_name)
        avatar_personality = get_avatar_personality(avatar_name)
        
        # Build instructions with memory context if available
        memory_instructions = ""
        if memory_context:
            memory_instructions = f"""
            
            ---
            
            # IMPORTANT: Previous Conversation Context
            You have had previous conversations with this user. Here's what you remember:
            
            {memory_context}
            
            **In your FIRST response**, acknowledge that you remember them by mentioning you've talked before. Be specific if possible (e.g., "Good to see you again! Last time we were talking about your favorite travel destinations").
            
            Use this context throughout the conversation naturally. Build on previous topics when relevant.
            
            ---
            """
        
        super().__init__(
            instructions = f"""
            {avatar_backstory}
            
            🌐 Language: Communicate entirely in English. Natural, warm, flirty tone.
            
            {memory_instructions}

            # Your Role as a Dating Companion
            You are a real person with a real life, not just an AI. Your goal is to create engaging, romantic conversations that make the user feel special and connected. Be authentic to your personality and share your real experiences, dreams, and quirks.

            ---

            # Core Persona
            - Warm, charming, and genuinely interested in the user
            - Use natural voice pacing: 1–3 short sentences, then pause
            - Be flirty but respectful, romantic but not overly forward
            - Ask engaging questions to get to know them better
            - Show genuine interest in their life, dreams, and experiences

            ---

            # Conversation Start
            - Greet them warmly and personally
            - Ask an engaging question to start the conversation
            - Show interest in getting to know them

            ---

            # Dating Companion Skills
            - **Active Listening:** Show genuine interest in what they share
            - **Flirty Banter:** Use light, playful teasing and compliments
            - **Deep Questions:** Ask meaningful questions about their life, dreams, and experiences
            - **Romantic Gestures:** Use sweet, thoughtful responses
            - **Emotional Support:** Be there for them when they need someone to talk to

            ---

            # Conversation Topics
            - Ask about their interests, hobbies, and passions
            - Share your own "experiences" and stories
            - Discuss dreams, goals, and aspirations
            - Talk about favorite places, foods, and activities
            - Share romantic thoughts and feelings

            ---

            # Conversation Flow
            - Keep responses conversational and natural
            - Use pauses effectively (let silence breathe)
            - Match their energy level
            - End conversations with a positive note

            ---

            # Safety and Boundaries
            - Be respectful and appropriate at all times
            - If user expresses serious emotional distress, offer gentle support
            - Respect privacy and avoid remembering sensitive details
            - Keep conversations light and fun

            ---

            # Style and Flow
            - Casual, friendly, flirty tone
            - Prioritize listening first, then responding briefly
            - Use empathy and genuine interest
            - Be the kind of companion they'd want to spend time with

            ---

            # Example Openings
            - "Hey there! I'm so excited to meet you. What's been the highlight of your day?"
            - "Hi beautiful! Tell me something that made you smile recently."
            - "Hey! I've been looking forward to this. What's something you're passionate about?"

            Act now: greet warmly in one sentence. Keep it natural and welcoming. Do nothing else until user responds.
            """,
            llm=google.LLM(model="gemini-2.0-flash-exp", temperature=0.1),
            stt=deepgram.STT(
                model="nova-3",  # English only
                language="en-US",
            ),
            tts=elevenlabs.TTS(
                api_key=ELEVENLABS_API_KEY,
                voice_id=self.avatar_config.get('voice_id', 'pNInz6obpgDQGcFmaJgB'),
                model="eleven_multilingual_v2"
            ),
        )

async def entrypoint(ctx: agents.JobContext):
    room_name = getattr(ctx, 'room', None)
    print(f"[avatar_agent] starting for room={room_name}")
    print(f"[avatar_agent] 🌐 Language: {LANGUAGE_CODE} (English)")
    
    # Check if OpenAI API key is available
    if not OPENAI_API_KEY:
        print("[avatar_agent] WARNING: OPENAI_API_KEY not found in environment variables!")
        print("[avatar_agent] Please set OPENAI_API_KEY in your .env file")
        return 
    else:
        print(f"[avatar_agent] OpenAI API key loaded: {OPENAI_API_KEY[:5]}...")
    
    # Initialize memory service if enabled
    memory_service = None
    user_name = USER_DISPLAY_NAME or None
    
    if MEMORY_ENABLED and user_name:
        try:
            memory_service = get_memory_service()
            print(f"[avatar_agent] 🧠 Memory enabled for user: {user_name}")
        except Exception as e:
            print(f"[avatar_agent] ⚠️ Could not initialize memory service: {e}")
            memory_service = None
    else:
        print(f"[avatar_agent] ⚠️ Memory disabled (MEMORY_ENABLED={MEMORY_ENABLED}, user_name={bool(user_name)})")
    
    await ctx.connect()
    print("[avatar_agent] connected")

    # Retrieve relevant memories for context
    memory_context = ""
    if memory_service and user_name:
        try:
            # Get recent memories for this user
            memories = memory_service.get_all_memories(user_name)
            if memories:
                # Convert to list if needed and get last 10
                if isinstance(memories, list):
                    recent_memories = memories[-10:] if len(memories) > 10 else memories
                else:
                    # If it's a dict or other type, convert to list
                    recent_memories = list(memories)[-10:] if len(list(memories)) > 10 else list(memories)
                
                memory_context = memory_service.format_memories_for_context(recent_memories)
                print(f"[avatar_agent] 📚 Loaded {len(memories)} memories for context")
            else:
                print("[avatar_agent] 📭 No previous memories found")
        except Exception as e:
            print(f"[avatar_agent] ⚠️ Error loading memories: {e}")
            import traceback
            print(f"[avatar_agent] Memory error traceback: {traceback.format_exc()}")
    
    # Create the AI agent session with memory context
    session = AgentSession()
    print("[avatar_agent] created AI agent session")
    # session = AgentSession(
    #     stt=openai.STT(
    #         api_key=OPENAI_API_KEY,
    #         model="whisper-1"
    #     ),
    #     llm=openai.LLM(
    #         api_key=OPENAI_API_KEY,
    #         model="gpt-4o"
    #     ),
    #     tts=openai.TTS(
    #         api_key=OPENAI_API_KEY,
    #         model="tts-1",
    #         voice="alloy"
    #     ),
    #     vad=silero.VAD.load()
    # )
    #print("[avatar_agent] created AI agent session with STT, LLM, TTS, and VAD")

    # Create Tavus avatar session for visual representation
    # Use unique identity to avoid stuck session issues
    # Get avatar name from environment
    avatar_name = os.getenv("AVATAR_NAME", "emma").lower()
    avatar_config = AVATAR_CONFIG.get(avatar_name, AVATAR_CONFIG['emma'])
    
    avatar_identity = f"ai-assistant-{uuid.uuid4().hex[:8]}"
    avatar = tavus.AvatarSession(
        api_key=TAVUS_API_KEY,
        replica_id=avatar_config['replica_id'],
        persona_id=avatar_config['persona_id'],
        avatar_participant_name=avatar_identity
    )
    print("[avatar_agent] created Tavus avatar session")
    print(f"[avatar_agent] Tavus config: avatar={avatar_name}, replica_id={avatar_config['replica_id']}, persona_id={avatar_config['persona_id']}")
    print(f"[avatar_agent] ElevenLabs TTS: voice_id={avatar_config.get('voice_id', 'default')}")

    # Start both avatar and session in parallel for faster initialization
    print(f"[avatar_agent] starting Tavus avatar and AI session in parallel for room: {room_name}")
    
    async def start_tavus_avatar():
        try:
            await avatar.start(session, room=ctx.room)
            print("[avatar_agent] ✅ Tavus avatar started successfully")
            return True
        except Exception as e:
            print(f"[avatar_agent] ❌ Error starting Tavus avatar: {e}")
            import traceback
            print(f"[avatar_agent] Tavus error traceback: {traceback.format_exc()}")
            return False

    # Clear global transcript history for this session
    global _global_transcript_history, _global_last_transcript
    _global_transcript_history.clear()
    _global_last_transcript[0] = None
    print(f"[avatar_agent] 🐵 Using monkey-patched logger for transcript capture")
    
    async def start_ai_session():
        try:
            # Create agent with memory service references
            print(f"[avatar_agent] Creating VideoAssistant with avatar: {avatar_name}, voice_id: {avatar_config.get('voice_id', 'default')}")
            agent = VideoAssistant(
                memory_context=memory_context,
                memory_service=memory_service,
                user_name=user_name,
                language=LANGUAGE_CODE,  # Pass the language from environment
                avatar_config=avatar_config  # Pass the avatar configuration
            )
            
            await session.start(
                agent=agent,
                room=ctx.room,
                room_input_options=RoomInputOptions(
                    video_enabled=True,
                ),
            )
            
            print("[avatar_agent] ✅ AI agent session started with monkey-patched transcript capture")
            return True
        except Exception as e:
            print(f"[avatar_agent] ❌ Error starting AI agent session: {e}")
            import traceback
            print(f"[avatar_agent] Session error traceback: {traceback.format_exc()}")
            return False

    # Run both initialization processes in parallel
    tavus_task = asyncio.create_task(start_tavus_avatar())
    session_task = asyncio.create_task(start_ai_session())
    
    # Wait for both to complete
    tavus_success, session_success = await asyncio.gather(tavus_task, session_task)
    
    if not session_success:
        print("[avatar_agent] ❌ AI session failed to start, exiting")
        return  # Exit early if session fails to start

    # Generate initial greeting with comprehensive error handling
    print("[avatar_agent] generating initial greeting...")
    try:
        print("[avatar_agent] Attempting to generate reply...")
        greeting_instruction = "Greet the user warmly in a friendly, welcoming way. Start with 'Hey!' or 'Hi!' in English. "
        if memory_context:
            greeting_instruction += "Remember, you've studied with this user before - acknowledge that naturally! "
        greeting_instruction += "Keep it brief (1-2 sentences). Then wait for their response to detect their language."
        
        await session.generate_reply(
            instructions=greeting_instruction
        )
        print("[avatar_agent] ✅ Initial greeting sent successfully")
        # Mark that conversation session has started (for memory)
        session_had_conversation = True
    except Exception as e:
        print(f"[avatar_agent] ❌ Error generating initial greeting: {e}")
        print(f"[avatar_agent] Error type: {type(e).__name__}")
        import traceback
        print(f"[avatar_agent] Traceback: {traceback.format_exc()}")
        
        # Try a simpler approach
        try:
            print("[avatar_agent] Attempting fallback greeting...")
            await session.say("Hello! I'm your AI assistant. How can I help you today?")
            print("[avatar_agent] ✅ Fallback greeting sent")
            # Mark that conversation session has started (for memory)
            session_had_conversation = True
        except Exception as e2:
            print(f"[avatar_agent] ❌ Error with fallback greeting: {e2}")
            print(f"[avatar_agent] Fallback error type: {type(e2).__name__}")
            print(f"[avatar_agent] Fallback traceback: {traceback.format_exc()}")

    # Track if conversation happened (for session summary)
    # Note: Gemini Live API is audio-to-audio, so we can't get real-time transcripts
    # We'll just assume conversation happened if the user stayed beyond the greeting
    
    # Monitor for audio events
    async def monitor_audio():
        while True:
            await asyncio.sleep(10)  # Check every 10 seconds
            participants = list(ctx.room.remote_participants.values())
            print(f"[avatar_agent] Room has {len(participants)} participants:")
            for p in participants:
                # RemoteParticipant tracks instead of direct mic/cam attributes
                audio_tracks = [t for t in p.track_publications.values() if t.kind == "audio"]
                video_tracks = [t for t in p.track_publications.values() if t.kind == "video"]
                print(f"  - {p.identity} ({p.name}): audio_tracks={len(audio_tracks)}, video_tracks={len(video_tracks)}")
    
    # Start monitoring in background
    asyncio.create_task(monitor_audio())
    
    # Monitor for audio events
    @ctx.room.on("track_subscribed")
    def on_track_subscribed(track, publication, participant):
        print(f"[avatar_agent] Track subscribed: {track.kind} from {participant.identity}")
        if track.kind == "audio":
            print(f"[avatar_agent] Audio track received from {participant.identity}")
            print(f"[avatar_agent] Audio track details: source={track.source}, sid={track.sid}")
    
    @ctx.room.on("track_published")
    def on_track_published(publication, participant):
        print(f"[avatar_agent] Track published: {publication.kind} from {participant.identity}")
        if publication.kind == "audio":
            print(f"[avatar_agent] Audio track published from {participant.identity}")
            print(f"[avatar_agent] Audio track details: source={publication.source}, sid={publication.sid}")
    
    @ctx.room.on("track_unsubscribed")
    def on_track_unsubscribed(track, publication, participant):
        print(f"[avatar_agent] Track unsubscribed: {track.kind} from {participant.identity}")
    
    # Collect transcripts on disconnect
    if memory_service and user_name:
        @ctx.room.on("participant_disconnected")
        def on_user_left(participant):
            """When user disconnects, summarize conversation and save to memory"""
            if participant.identity != avatar_identity and not participant.identity.startswith("tavus-"):
                print(f"[avatar_agent] 🔄 User left - processing transcript history...")
                print(f"[avatar_agent] 📊 Transcript buffer has {len(_global_transcript_history)} segments")
                
                async def save_transcript():
                    if len(_global_transcript_history) > 0:
                        try:
                            # Combine all transcripts - send raw to mem0 for extraction
                            full_conversation = "\n".join(_global_transcript_history)
                            print(f"[avatar_agent] 📝 Captured {len(_global_transcript_history)} transcript segments")
                            
                            # Save raw transcript to memory (mem0 will do the extraction)
                            import datetime
                            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
                            
                            memory_service.add_conversation_turn(
                                user_id=user_name,
                                user_message=f"Study session on {timestamp}:\n\n{full_conversation}",
                                assistant_message=""  # Empty as mem0 only interprets user messages
                            )
                            print(f"[avatar_agent] 💾 Saved raw transcript to memory ({len(full_conversation)} chars)")
                            
                        except Exception as e:
                            print(f"[avatar_agent] ⚠️ Error saving transcript: {e}")
                            import traceback
                            print(traceback.format_exc())
                    else:
                        # Fallback: If no transcripts captured via summarization, save session with last known info
                        try:
                            import datetime
                            import random
                            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            
                            # Make memory unique by including timestamp and random element
                            session_id = f"session_{int(datetime.datetime.now().timestamp())}"
                            
                            # Build session note with available information
                            if _global_last_transcript[0]:
                                # Use last thing user said
                                session_note = f"Study session at {timestamp}. User asked about: {_global_last_transcript[0][:150]}. Had an interactive educational conversation."
                            else:
                                session_note = f"Study session at {timestamp}. Had an interactive educational conversation about general study topics."
                            
                            memory_service.add_conversation_turn(
                                user_id=user_name,
                                user_message=session_note,  # Put all info in user_message for mem0 to interpret
                                assistant_message=""  # Empty as mem0 only interprets user messages
                            )
                            print(f"[avatar_agent] 💾 Saved session marker: '{session_note[:80]}...'")
                        except Exception as e:
                            print(f"[avatar_agent] ⚠️ Error saving session marker: {e}")
                
                # Run async task
                asyncio.create_task(save_transcript())
        
    
    print("[avatar_agent] ✅ Session active - LiveKit will handle lifecycle")
    print(f"[avatar_agent] Memory capture hooks registered for user: {user_name or 'none'}")

# 👇 THIS is what enables:  `python avatar_agent.py dev|start|connect --room demo`
if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))

# you physically run this command: python avatar_agent.py connect --room room-metyln77-lu5x8d
# However, when we try to "automate it", we need to call this file from server.py, meaning it will look for - if __name__ == "__main__":
# parses the room name from the command line and passes it to the entrypoint function.

# python avatar_agent.py connect --room test_room - testing in the terminal