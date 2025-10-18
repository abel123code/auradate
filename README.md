# AuraDate 💕

An intelligent AI dating companion with persistent memory, built with LiveKit real-time video, Tavus visual avatars, and mem0 Platform for advanced memory management.

## 🌟 Features

- **Real-time Video Calls with AI Avatar**: Voice and video conversations with charming AI dating companions powered by Tavus
- **English Language Support**: Full English support with natural conversation flow
- **Persistent Memory**: Cross-session memory using mem0 Platform API with automatic extraction
- **Dating Companion**: Engaging, flirty conversations with AI avatars (Alex & Emma)
- **Emotional Support**: Caring companionship and romantic conversation
- **Conversation Spark**: AI-generated conversation starters to facilitate meaningful connections

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                 FRONTEND (React Native + Expo)                      │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │
│   │  Call Tab    │  │  Spark Tab   │  │ Profile Tab  │            │
│   │ - Language   │  │ - User List  │  │ - Display    │            │
│   │   Selection  │  │ - AI-Gen     │  │   Name       │            │
│   │ - Video Call │  │   Questions  │  │ - Settings   │            │
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
│  │  • POST /api/conversation-starters → Generate Qs    │         │
│  └───────────────────┬───────────────────────────────────┘         │
│                      │                                              │
│                      │ Spawns subprocess                            │
│                      ▼                                              │
│  ┌───────────────────────────────────────────────────────┐         │
│  │  Avatar Agent (LiveKit Agents Process)               │         │
│  │  ┌─────────────────────────────────────────────────┐ │         │
│  │  │  AI Components                                  │ │         │
│  │  │  • Gemini 2.0 Flash (LLM & Conversation)       │ │         │
│  │  │  • Deepgram (STT: nova-3 / nova-2-general)     │ │         │
│  │  │  • OpenAI (TTS: "nova" voice - multilingual)   │ │         │
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
- **Deepgram** - Speech-to-Text (nova-3 for English, nova-2-general for Chinese)
- **OpenAI** - Text-to-Speech (nova voice, multilingual)
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
OPENAI_API_KEY=your_openai_api_key   # For TTS (nova voice)
DEEPGRAM_API_KEY=your_deepgram_api_key  # For STT
```

**Note**: Qdrant Cloud is no longer needed! mem0 Platform handles all storage.

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

### 3. (Optional) Add Test Users for Conversation Spark

```bash
cd server
python add_test_users.py
# Adds Henry (CS student) and Isaac (Physics student) to mem0 Platform
```

This takes ~30-60 seconds as it calls the mem0 API for each memory.

## 🎯 Key Features Explained

### 1. **Language-Specific AI**

- User selects language before call (English or Chinese)
- **STT Models**:
  - English: Deepgram `nova-3` with `en-US`
  - Chinese: Deepgram `nova-2-general` with `zh-CN`
- **LLM**: Gemini 2.0 Flash with language-specific prompts
- **TTS**: OpenAI `nova` voice (supports both languages naturally)

### 2. **Persistent Memory (mem0 Platform)**

**How It Works:**

1. **User Identification**: Display name stored locally via AsyncStorage
2. **Transcript Capture**: Real-time capture via monkey-patched LiveKit logger
3. **On Disconnect**: Raw transcript saved to mem0 Platform API
4. **Automatic Extraction**: mem0's LLM extracts key information:
   - Personal & academic profile
   - Goals & interests
   - Assignments & deadlines
   - Learning preferences
   - Challenges & support needs
   - Achievements & progress
5. **Context Loading**: Next session loads relevant memories automatically

**Example saved memory:**

```
Study session on 2025-01-12 14:30:

User: I'm studying biology, specifically the digestive system
Assistant: Great! Let's start with the stomach...
User: What about enzymes?
Assistant: Enzymes in the stomach include pepsin...
```

mem0 extracts:

- "Studying biology with focus on digestive system"
- "Interested in enzymatic processes"
- "Currently learning about stomach function"

### 3. **Conversation Spark**

**Flow:**

1. User opens Spark tab
2. Frontend calls `GET /api/users` → Retrieves users from mem0 Platform
3. User selects a study buddy (e.g., "Henry")
4. Frontend calls `POST /api/conversation-starters` with display name
5. Backend:
   - Fetches all of Henry's memories from mem0
   - Sends to Gemini with prompt to generate 5 personalized questions
6. Display questions like:
   - "How's your data structures project coming along?"
   - "Need help with those recursive algorithms?"
   - "Ready for your database exam next week?"

**Benefits:**

- Facilitates peer-to-peer study connections
- Questions based on actual study history
- Helps students find common interests

### 4. **Study Coaching Techniques**

The AI agent uses evidence-based methods:

- **Active Recall**: "Try saying the formula aloud before I show it."
- **Pomodoro**: "Let's do 20 minutes, then a 3-minute stretch."
- **Interleaving**: "This pattern also appears in energy equations — let's link them."
- **Acknowledgement**: "That sounds really frustrating. Anyone in your shoes would feel the same."
- **Cognitive Reframe**: "You're not failing — you're just in the middle of learning."

## 📁 Project Structure

```
Mission-Two/
├── rn-video-calling-app/          # React Native frontend
│   ├── app/
│   │   ├── (tabs)/
│   │   │   ├── index.tsx          # Call screen (language + video)
│   │   │   ├── spark.tsx          # Conversation Spark
│   │   │   └── profile.tsx        # Profile settings
│   │   └── call.tsx               # LiveKit video call screen
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

### Memory Management with mem0 Platform

**Add Memory:**

```python
memory_service.add_conversation_turn(
    user_id="abel",
    user_message="Study session content here",
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

### Conversation Spark

- `GET /api/users` - List all users with memories (from mem0 Platform)
- `POST /api/conversation-starters` - Generate personalized questions
  - Body: `{display_name}`
  - Returns: `{starters: [...], user_info, memory_count}`

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
│     • OpenAI TTS → audio → Tavus avatar                     │
│     • Transcripts captured in buffer (_global_transcript)   │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  3. CALL END (User Disconnects)                             │
│     • Combine all transcript segments                       │
│     • Save raw transcript to mem0 Platform                  │
│     • Format: "Study session on {timestamp}:\n\n{transcript}"│
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
│     • "Good to see you again! Last time we were working     │
│       on that biology assignment about enzymes..."          │
└─────────────────────────────────────────────────────────────┘
```

## 🎓 Memory Categories Tracked

The system automatically extracts and categorizes:

1. **Personal & Academic Profile**
   - Name, school, major, courses
2. **Academic Goals & Interests**
   - GPA targets, career aspirations, subject interests
3. **Assignments & Deadlines**
   - Upcoming projects, exams, due dates
4. **Learning Preferences**
   - Visual/auditory, solo/group, study environments
5. **Extracurricular Activities**
   - Clubs, sports, research projects
6. **Challenges & Support Needs**
   - Difficult subjects, motivation issues
7. **Achievements & Progress**
   - Awards, completed courses, new skills
8. **Feedback & Motivation**
   - What helps/hinders learning

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

This is a production-ready AI study companion. Key areas for enhancement:

- Additional language support (Spanish, French, etc.)
- Group study sessions (multi-user rooms)
- Study analytics dashboard
- Spaced repetition scheduling
- Integration with learning management systems (LMS)

## 📚 Documentation

- **mem0 Platform Setup**: See `server/MEM0_PLATFORM_SETUP.md`
- **Memory Migration Guide**: See `MEM0_PLATFORM_MIGRATION.md`
- **API Reference**: See inline documentation in `server.py`

## 🔗 Useful Links

- **mem0 Dashboard**: [https://app.mem0.ai](https://app.mem0.ai)
- **mem0 Docs**: [https://docs.mem0.ai](https://docs.mem0.ai)
- **LiveKit Docs**: [https://docs.livekit.io](https://docs.livekit.io)
- **Tavus Docs**: [https://docs.tavus.io](https://docs.tavus.io)

## 📄 License

MIT License - feel free to use this for your own educational projects!

---

**Built with ❤️ for students worldwide** 🌏

_Empowering learning through AI-powered conversations and persistent memory_
