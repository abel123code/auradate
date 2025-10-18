# AuraDate 💕

An intelligent AI dating companion with persistent memory, built with LiveKit real-time video, ElevenLabs voice synthesis, and mem0 Platform for advanced memory management.

## 🌟 Features

- **Real-time Video Calls with AI Avatar**: Voice and video conversations with charming AI dating companions powered by Tavus
- **Voice-Only Dating Facilitator**: AI-powered conversation facilitator for real users on voice dates
- **Persistent Memory**: Cross-session memory using mem0 Platform API with automatic extraction
- **Dating Companion**: Engaging, flirty conversations with AI avatars (Alex & Emma)
- **User Search & Memories**: Search for users and view their dating memories
- **Conversation Facilitation**: AI facilitator helps real users connect on voice dates
- **Emotional Support**: Caring companionship and romantic conversation

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                 FRONTEND (React Native + Expo)                      │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │
│   │  Date Tab    │  │  Search Tab  │  │ Profile Tab  │            │
│   │ - Avatar     │  │ - User List  │  │ - Display    │            │
│   │   Selection  │  │ - Memories   │  │   Name       │            │
│   │ - Video Call │  │ - Voice Date │  │ - Settings   │            │
│   └──────┬───────┘  └──────┬───────┘  └──────┬───────┘            │
│          │                  │                  │                     │
└──────────┼──────────────────┼──────────────────┼─────────────────────┘
           │ WebSocket/HTTP   │ REST API         │ AsyncStorage
           ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   BACKEND SERVER (FastAPI)                          │
│  ┌───────────────────────────────────────────────────────┐         │
│  │  API Endpoints                                        │         │
│  │  • POST /join-room → Generate tokens + spawn avatar  │         │
│  │  • GET /api/users → Fetch users from mem0           │         │
│  │  • POST /api/start-facilitated-conversation         │         │
│  │  • POST /api/launch-facilitator → Start AI agent    │         │
│  └───────────────────┬───────────────────────────────────┘         │
│                      │                                              │
│                      │ Spawns subprocess                            │
│                      ▼                                              │
│  ┌───────────────────────────────────────────────────────┐         │
│  │  Avatar Agent (LiveKit Agents Process)               │         │
│  │  ┌─────────────────────────────────────────────────┐ │         │
│  │  │  AI Components                                  │ │         │
│  │  │  • Gemini 2.0 Flash (LLM & Conversation)       │ │         │
│  │  │  • Deepgram (STT: nova-3)                       │ │         │
│  │  │  • ElevenLabs (TTS: Custom voice)               │ │         │
│  │  │  • Tavus (Visual Avatar with lip-sync)         │ │         │
│  │  └─────────────────────────────────────────────────┘ │         │
│  │  ┌─────────────────────────────────────────────────┐ │         │
│  │  │  Memory Capture                                 │ │         │
│  │  │  • Monkey-patched LiveKit logger                │ │         │
│  │  │  • Real-time transcript buffer                  │ │         │
│  │  │  • On disconnect: save raw transcript           │ │         │
│  │  └─────────────────────────────────────────────────┘ │         │
│  └───────────────────────────────────────────────────────┘         │
│                      │                                              │
│                      │ Memory Service (Python SDK)                  │
│                      ▼                                              │
└─────────────────────────────────────────────────────────────────────┘
                       │ REST API
                       ▼
┌─────────────────────────────────────────────────────────────────────┐
│               mem0 PLATFORM (Managed Cloud Service)                 │
│  ┌───────────────────────────────────────────────────────┐         │
│  │  Automatic Memory Processing                          │         │
│  │  • Raw transcript ingestion                           │         │
│  │  • LLM-based information extraction                   │         │
│  │  • Embeddings generation (OpenAI)                     │         │
│  │  • Vector storage & semantic search                   │         │
│  │  • Entity tracking (users, agents, runs)              │         │
│  └───────────────────────────────────────────────────────┘         │
│                                                                      │
│  📊 Dashboard: https://app.mem0.ai                                  │
│  • View all memories                                                │
│  • Monitor user activity                                            │
│  • Manage memory data                                               │
└─────────────────────────────────────────────────────────────────────┘
```

## 🛠️ Tech Stack

### Frontend

- **React Native** with Expo
- **LiveKit React Native SDK** for video/audio
- **TailwindCSS (NativeWind)** for styling
- **AsyncStorage** for local persistence (display name)

### Backend

- **FastAPI** (Python) - REST API server
- **LiveKit Agents SDK** - Real-time AI agent framework
- **mem0 Platform API** - Managed memory service (Python SDK)

### AI Services

- **Gemini 2.0 Flash** - LLM for conversation & question generation
- **Deepgram** - Speech-to-Text (nova-3 for English)
- **ElevenLabs** - Text-to-Speech (Custom voice for facilitator)
- **Tavus** - Visual avatar with lip-sync
- **mem0 Platform** - Memory extraction, embeddings, and storage

### Infrastructure

- **LiveKit SFU** - Real-time video infrastructure
- **mem0 Cloud** - Managed memory database with vector search

## 📦 Setup

### Prerequisites

- Node.js 18+ and npm
- Python 3.11+
- Expo CLI (`npm install -g expo-cli`)
- **mem0 Platform Account** ([sign up at app.mem0.ai](https://app.mem0.ai))

### Get Your mem0 API Key

1. Go to [https://app.mem0.ai](https://app.mem0.ai)
2. Sign up for a free account
3. Navigate to **Settings → API Keys**
4. Create a new API key (starts with `m0-`)
5. Find your Organization ID and Project ID (from URL or Settings)

### Environment Variables

Create a `.env` file in `server/`:

**`server/.env`:**

```env
# mem0 Platform API (Required)
MEM0_API_KEY=m0-your-api-key-here
MEM0_ORG_ID=org_your-org-id-here          # Optional but recommended
MEM0_PROJECT_ID=proj_your-project-id-here  # Optional but recommended

# LiveKit (Required)
LIVEKIT_URL=wss://your-livekit-server.livekit.cloud
LIVEKIT_API_KEY=your_api_key
LIVEKIT_API_SECRET=your_api_secret

# Tavus Visual Avatar (Required)
TAVUS_API_KEY=your_tavus_api_key
TAVUS_REPLICA_ID=your_replica_id
TAVUS_PERSONA_ID=your_persona_id

# AI Services (Required)
GOOGLE_API_KEY=your_google_api_key   # For Gemini 2.0 Flash
ELEVENLABS_API_KEY=your_elevenlabs_api_key  # For TTS (Facilitator voice)
DEEPGRAM_API_KEY=your_deepgram_api_key  # For STT
```

### Installation

**Backend:**

```bash
cd server
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Frontend:**

```bash
cd rn-video-calling-app
npm install
```

## 🚀 Running the Application

### 1. Start Backend Server

```bash
cd server
source venv/bin/activate  # Windows: venv\Scripts\activate
python server.py
# Server runs on http://localhost:3001
```

You should see:

```
[MemoryService] ✅ Initialized with mem0 Platform API
[MemoryService] 🌐 Using managed cloud infrastructure
[MemoryService] 💾 Persistent cross-session memory enabled!
[MemoryService] 📊 Access dashboard at: https://app.mem0.ai
```

### 2. Start Frontend

```bash
cd rn-video-calling-app
npx expo start
# Scan QR code with Expo Go app (iOS/Android)
```

### 3. (Optional) Add Test Users for Dating

```bash
cd server
python add_test_users.py
# Adds Henry and Isaac with dating memories to mem0 Platform
```

## 🎯 Key Features Explained

### 1. **AI Dating Companions**

- **Alex & Emma**: Two charming AI avatars for romantic conversations
- **Persistent Memory**: Remembers past conversations and preferences
- **Emotional Support**: Caring, flirty, and supportive conversations
- **Visual Avatars**: Realistic video avatars with lip-sync via Tavus

### 2. **Voice Dating Facilitator**

**How It Works:**

1. User searches for another user in the Search tab
2. Views their memories and dating history
3. Clicks "Start Conversation" to begin a voice date
4. AI facilitator joins the LiveKit room with both users
5. Facilitator uses both users' memories to suggest conversation topics
6. Real-time voice conversation with AI guidance

**Features:**

- **Memory-Driven**: Uses both users' dating memories for personalized topics
- **ElevenLabs Voice**: Natural, expressive voice for the facilitator
- **Real-time Audio**: LiveKit-powered voice communication
- **Conversation Guidance**: AI suggests topics and keeps conversation flowing

### 3. **Persistent Memory (mem0 Platform)**

**How It Works:**

1. **User Identification**: Display name stored locally via AsyncStorage
2. **Transcript Capture**: Real-time capture via monkey-patched LiveKit logger
3. **On Disconnect**: Raw transcript saved to mem0 Platform API
4. **Automatic Extraction**: mem0's LLM extracts key information:
   - Personal preferences & interests
   - Dating history & experiences
   - Relationship goals & values
   - Conversation topics & style
   - Emotional patterns & support needs
5. **Context Loading**: Next session loads relevant memories automatically

**Example saved memory:**

```
Dating conversation on 2025-01-12 14:30:

User: I love hiking and outdoor adventures
Assistant: That sounds amazing! Tell me about your favorite hiking spot...
User: I'm looking for someone who shares my passion for nature
Assistant: Nature lovers often make great partners...
```

mem0 extracts:

- "Passionate about hiking and outdoor adventures"
- "Values nature and outdoor activities"
- "Looking for partner who shares outdoor interests"

### 4. **User Search & Memory Viewing**

**Flow:**

1. User opens Search tab
2. Frontend calls `GET /api/users` → Retrieves users from mem0 Platform
3. User searches for someone (e.g., "Henry")
4. Views Henry's dating memories and history
5. Can start a voice date with AI facilitation

**Benefits:**

- Facilitates real connections between users
- Memory-based conversation topics
- Helps users find compatible matches
- AI guidance for meaningful conversations

## 📁 Project Structure

```
auradate/
├── rn-video-calling-app/          # React Native frontend
│   ├── app/
│   │   ├── (tabs)/
│   │   │   ├── index.tsx          # Date screen (avatar selection)
│   │   │   ├── spark.tsx          # Search users
│   │   │   └── profile.tsx        # Profile settings
│   │   ├── call.tsx               # LiveKit video call screen
│   │   ├── memories.tsx           # User memories view
│   │   └── voice-facilitator.tsx  # Voice dating facilitator
│   ├── hooks/
│   │   ├── useDisplayName.ts      # Persistent user identity
│   │   └── useLanguage.ts         # Language selection
│   ├── services/
│   │   └── pushNotifications.ts   # FCM push notifications
│   └── package.json
│
├── server/                         # Python backend
│   ├── server.py                  # FastAPI REST API server
│   ├── avatar_agent.py            # LiveKit AI agent (subprocess)
│   ├── facilitator_agent.py       # Voice dating facilitator
│   ├── memory_service.py          # mem0 Platform API wrapper
│   ├── add_test_users.py          # Populate test data
│   ├── requirements.txt
│   └── .env                       # Environment variables
│
└── README.md
```

## 🔧 Advanced Configuration

### Avatar Agent Process Management

- Each room spawns a separate avatar agent subprocess
- Automatic cleanup of terminated processes via background task
- Manual cleanup: `POST /cleanup-avatar/{room_name}`
- View active avatars: `GET /active-avatars`
- Logs appear in main server console

### Voice Facilitator Process Management

- Facilitator agent launched for each voice date
- Uses ElevenLabs TTS with custom voice ID
- Memory-driven conversation topics
- Automatic cleanup when date ends

### Memory Management with mem0 Platform

**Add Memory:**

```python
memory_service.add_conversation_turn(
    user_id="abel",
    user_message="Dating conversation content here",
    assistant_message=""  # Empty - mem0 only interprets user messages
)
```

**Retrieve Memories:**

```python
memories = memory_service.get_all_memories("abel")
```

**Get All Users:**

```python
users_data = memory_service.get_all_users()
# Returns: {"users": ["abel", "henry", "isaac"], "agents": [], "runs": []}
```

**View in Dashboard:**

- Visit [https://app.mem0.ai](https://app.mem0.ai)
- Navigate to **Memories** section
- See all users and their extracted memories

## 🐛 Debugging

### View Backend Logs

```bash
cd server
python server.py
# Avatar agent logs appear in same console
```

### Check Memory Service

```bash
# Look for this in logs:
[MemoryService] ✅ Initialized with mem0 Platform API
[MemoryService] 🏢 Using organization: org_xxx
[MemoryService] 📁 Using project: proj_xxx
```

### Verify Transcript Capture

When a user disconnects, you should see:

```
[avatar_agent] 📝 Captured 5 transcript segments
[avatar_agent] 💾 Saved raw transcript to memory (532 chars)
```

### Check Active Avatar Processes

```bash
curl http://localhost:3001/active-avatars
```

### Test Tavus Credentials

```bash
curl http://localhost:3001/test-tavus
```

## 📝 API Endpoints

### Room Management

- `POST /join-room` - Generate LiveKit token & spawn avatar
  - Body: `{room_name, participant_name, language, invite_avatar}`
- `GET /room-info/{room_name}` - Get room status
- `POST /cleanup-avatar/{room_name}` - Terminate avatar process

### User Search & Memories

- `GET /api/users` - List all users with memories (from mem0 Platform)
- `GET /api/user-memories/{username}` - Get specific user's memories
- `POST /api/start-facilitated-conversation` - Start voice date with AI facilitator
- `POST /api/launch-facilitator` - Launch AI facilitator agent

### Debug & Monitoring

- `GET /active-avatars` - List active avatar processes
- `GET /test-tavus` - Verify Tavus credentials
- `GET /registered-tokens` - View push notification tokens

## 🌍 Language Support

| Language | STT Model       | STT Code | LLM              | TTS        |
| -------- | --------------- | -------- | ---------------- | ---------- |
| English  | Deepgram nova-3 | `en-US`  | Gemini 2.0 Flash | ElevenLabs |

**Note**:

- Gemini provides English-only instructions for dating conversations
- ElevenLabs provides natural, expressive voices for romantic conversations
- Facilitator uses custom ElevenLabs voice for guidance

## 📊 Memory System Flow

```
┌─────────────────────────────────────────────────────────────┐
│  1. CALL START                                              │
│     • Load user's recent memories from mem0                 │
│     • Inject context into Gemini's system prompt            │
│     • Avatar greets with memory awareness                   │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  2. DURING CONVERSATION                                     │
│     • User speaks → Deepgram STT → text                     │
│     • Gemini generates response                             │
│     • ElevenLabs TTS → audio → Tavus avatar                │
│     • Transcripts captured in buffer (_global_transcript)   │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  3. CALL END (User Disconnects)                             │
│     • Combine all transcript segments                       │
│     • Save raw transcript to mem0 Platform                  │
│     • Format: "Dating conversation on {timestamp}:\n\n{transcript}"│
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  4. mem0 AUTOMATIC PROCESSING                               │
│     • Extract key information using LLM                     │
│     • Create structured memories                            │
│     • Generate embeddings                                   │
│     • Store in vector database                              │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  5. NEXT SESSION                                            │
│     • Retrieve relevant memories via semantic search        │
│     • Avatar continues conversation with context            │
│     • "Good to see you again! Last time we were talking     │
│       about your love for hiking and outdoor adventures..." │
└─────────────────────────────────────────────────────────────┘
```

## 🎓 Memory Categories Tracked

The system automatically extracts and categorizes:

1. **Personal & Dating Profile**
   - Name, age, location, relationship status
2. **Dating Goals & Interests**
   - Relationship goals, partner preferences, interests
3. **Dating History & Experiences**
   - Past relationships, dating stories, lessons learned
4. **Values & Preferences**
   - Core values, deal-breakers, must-haves
5. **Lifestyle & Activities**
   - Hobbies, interests, social activities
6. **Emotional Patterns & Support Needs**
   - Communication style, emotional needs
7. **Achievements & Growth**
   - Personal growth, accomplishments, goals
8. **Feedback & Relationship Insights**
   - What works/doesn't work in relationships

## 🚀 Deployment

### Backend (Render.com)

- Python 3.11 runtime
- Add all environment variables in Render dashboard
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn server:app --host 0.0.0.0 --port $PORT`

### Frontend (EAS Build)

```bash
cd rn-video-calling-app
eas build --platform android --profile preview
# or
eas build --platform ios --profile preview
```

## 🤝 Contributing

This is a production-ready AI dating companion. Key areas for enhancement:

- Additional language support (Spanish, French, etc.)
- Group dating events (multi-user rooms)
- Dating analytics dashboard
- Compatibility matching algorithms
- Integration with dating platforms

## 📚 Documentation

- **mem0 Platform Setup**: See `server/MEM0_PLATFORM_SETUP.md`
- **Memory Migration Guide**: See `MEM0_PLATFORM_MIGRATION.md`
- **API Reference**: See inline documentation in `server.py`

## 🔗 Useful Links

- **mem0 Dashboard**: [https://app.mem0.ai](https://app.mem0.ai)
- **mem0 Docs**: [https://docs.mem0.ai](https://docs.mem0.ai)
- **LiveKit Docs**: [https://docs.livekit.io](https://docs.livekit.io)
- **Tavus Docs**: [https://docs.tavus.io](https://docs.tavus.io)
- **ElevenLabs Docs**: [https://docs.elevenlabs.io](https://docs.elevenlabs.io)

## 📄 License

MIT License - feel free to use this for your own dating projects!

---

**Built with ❤️ for love and connection** 💕

_Empowering relationships through AI-powered conversations and persistent memory_
