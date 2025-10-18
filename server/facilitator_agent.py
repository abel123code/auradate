import os
import asyncio
import logging
from dotenv import load_dotenv
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, AgentSession, Agent
from livekit.plugins import deepgram, elevenlabs, google
import json
import argparse

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

async def entrypoint(ctx: JobContext):
    """Main entrypoint for the facilitator agent"""
    logger.info("Starting conversation facilitator agent")
    
    # Parse command line arguments for memories
    import sys
    user1_memories = []
    user2_memories = []
    common_topics = []
    user1_name = "User 1"
    user2_name = "User 2"
    
    # Get user names and memories from environment variables
    user1_name = os.getenv('USER1_NAME', 'User 1')
    user2_name = os.getenv('USER2_NAME', 'User 2')
    
    # Try to get memories from environment variables
    try:
        user1_memories_json = os.getenv('USER1_MEMORIES', '[]')
        user2_memories_json = os.getenv('USER2_MEMORIES', '[]')
        user1_memories = json.loads(user1_memories_json) if user1_memories_json != '[]' else []
        user2_memories = json.loads(user2_memories_json) if user2_memories_json != '[]' else []
    except json.JSONDecodeError as e:
        logger.warning(f"Could not parse memories from environment: {e}")
        user1_memories = []
        user2_memories = []
    
    # Create system prompt for facilitator
    user1_summary = _summarize_memories(user1_memories)
    user2_summary = _summarize_memories(user2_memories)
    
    system_prompt = f"""
You are an AI conversation facilitator helping two people connect on a date. Your role is to:

## Your Role:
- **Facilitate conversation** between {user1_name} and {user2_name}
- **Break the ice** with engaging questions
- **Keep the conversation flowing** naturally
- **Help them discover common ground**

## Participant Information:
**{user1_name} interests/experiences:** {user1_summary}
**{user2_name} interests/experiences:** {user2_summary}
**Common topics:** {', '.join(common_topics) if common_topics else 'None identified'}

## Your Facilitation Style:
- **Warm and supportive** - Use encouraging, friendly tone
- **Brief interventions** - Keep prompts to 1-2 sentences max
- **Natural timing** - Only speak during pauses or silence
- **Memory-driven** - Reference their shared interests when relevant
- **Non-intrusive** - Let them lead the conversation

## Intervention Guidelines:
- Wait for natural pauses (3+ seconds of silence)
- Use phrases like: "That's interesting! {user1_name}, have you experienced...?"
- Suggest topics: "You both mentioned [interest], tell me more about that"
- Ask follow-ups: "What draws you to [topic]?"
- Build connections: "It sounds like you both value [value]"

## Example Interventions:
- "You both seem passionate about [topic]. {user1_name}, what got you interested in that?"
- "That's fascinating! {user2_name}, have you had similar experiences with [related topic]?"
- "I love how you both approach [subject]. What's something you'd love to explore more?"

## Important Rules:
- NEVER interrupt active conversation
- Keep responses under 15 seconds
- Use their actual names: {user1_name} and {user2_name}
- Reference their shared interests
- End with open-ended questions
- Stay positive and encouraging

Start by welcoming them warmly and suggesting a topic to get the conversation flowing.
"""
    
    # Create the agent with instructions
    agent = Agent(
        instructions=system_prompt
    )
    
    # Create agent session (voice-only)
    session = AgentSession(
        llm=google.LLM(model="gemini-2.0-flash-exp", temperature=0.3),
        stt=deepgram.STT(model="nova-3", language="en-US"),
        tts=elevenlabs.TTS(
            api_key=ELEVENLABS_API_KEY,
            voice_id="ODq5zmih8GrVes37Dizd",  # Professional narrator voice
            model="eleven_multilingual_v2"
        ),
    )
    
    # Start the session
    await session.start(agent=agent, room=ctx.room)
    logger.info("Facilitator agent started successfully")
    
    # Keep running until room ends
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        logger.info("Facilitator agent shutting down")
    except Exception as e:
        logger.error(f"Facilitator agent error: {e}")

def _summarize_memories(memories):
    """Summarize user memories into key interests"""
    if not memories:
        return "No specific interests identified"
    
    # Extract key themes from memories
    themes = []
    for memory in memories[:5]:  # Use top 5 memories
        memory_text = memory.get('memory', '')
        # Simple keyword extraction
        words = memory_text.lower().split()
        themes.extend([w for w in words if len(w) > 4])
    
    # Return most common themes
    from collections import Counter
    common_themes = Counter(themes).most_common(3)
    return ', '.join([theme for theme, count in common_themes])

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))