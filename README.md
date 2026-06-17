# 🚗 VoiceOps-AI — Voice AI Car Call Centre

VoiceOps-AI is a real-time voice assistant for an automotive service centre. A customer clicks **"Talk to an Agent!"**, speaks naturally, and an AI agent greets them, looks up their vehicle by **VIN**, creates a new profile if one doesn't exist, and answers their questions — all over live audio with a streaming transcript.

The agent is powered by **Google Gemini's realtime (speech-to-speech) model** running on the **LiveKit Agents** framework, with a **React + Vite** frontend and a lightweight **Flask** token server backed by **SQLite**.

---

## ✨ Features

- **Real-time voice conversation** — speech in, speech out, with no manual push-to-talk.
- **Live transcript** — agent and user turns render on screen as the conversation happens.
- **VIN lookup & profile creation** — the agent calls backend tools to find or create a vehicle record.
- **Function/tool calling** — `lookup_car`, `get_car_details`, and `create_car` are exposed to the model.
- **SQLite persistence** — vehicle profiles are stored locally.
- **Dynamic token issuing** — a Flask endpoint mints a fresh LiveKit token and a unique room per session.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Voice agent | LiveKit Agents (Python) `1.6.0` |
| LLM / Realtime | Google Gemini realtime audio model |
| Token server | Flask + flask-cors |
| Database | SQLite |
| Frontend | React + Vite |
| Realtime client | `@livekit/components-react`, `livekit-client` |

---

## 📂 Folder Structure

```
VoiceOps-AI/
│
├── Backend/
│   ├── agent.py            # LiveKit voice agent (Gemini realtime model + session)
│   ├── api.py              # AssistantFnc — agent with @function_tool methods
│   ├── db_driver.py        # SQLite driver (Car dataclass, lookup/create)
│   ├── prompts.py          # System instructions & welcome message
│   ├── server.py           # Flask token server (/getToken)
│   ├── requirements.txt    # Python dependencies
│   └── .env                # LiveKit + Google API credentials (not committed)
│
├── Frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── LivekitModal.jsx     # Connect modal + LiveKitRoom wrapper
│   │   │   ├── VoiceAssistant.jsx   # Visualizer, controls, live transcript
│   │   │   └── VoiceAssistant.css   # Voice assistant styles
│   │   ├── App.jsx          # Landing page + "Talk to an Agent!" button
│   │   ├── App.css          # Page styles
│   │   ├── index.css        # Base styles
│   │   └── main.jsx         # React entry point
│   ├── index.html
│   ├── vite.config.js       # Dev server + /api proxy to Flask
│   ├── package.json
│   └── .env                 # VITE_LIVEKIT_URL (not committed)
│
├── auto_db.sqlite           # Generated SQLite database
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Architecture & Flow

```
 Browser (React)                Flask Server              LiveKit Cloud              Agent Worker
      │                              │                          │                         │
      │  click "Talk to an Agent!"   │                          │                         │
      │ ───────── GET /getToken ───► │                          │                         │
      │ ◄──── signed JWT + room ──── │                          │                         │
      │                              │                          │                         │
      │ ───────── join room (token) ────────────────────────►  │                         │
      │                              │     room created ──────► dispatch job ───────────► │
      │ ◄═══════════ live audio + transcript ═══════════════════════════════════════════ │
```

1. The user opens the page and clicks **Talk to an Agent!**
2. The frontend requests a token from the Flask server, which returns a signed JWT for a fresh, unique room.
3. The browser joins that room. Because the room is created at that moment, LiveKit automatically dispatches the idle agent worker into it.
4. Gemini greets the user, and the conversation streams both ways in real time.

---

##  Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+ (LTS)
- A LiveKit Cloud project (URL, API key, API secret)
- A Google API key with access to the Gemini realtime model

### 1. Backend setup

```bash
cd Backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
```

Create `Backend/.env`:

```env
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your_api_key
LIVEKIT_API_SECRET=your_api_secret
GOOGLE_API_KEY=your_google_api_key
```

### 2. Frontend setup

```bash
cd Frontend
npm install
```

Create `Frontend/.env`:

```env
VITE_LIVEKIT_URL=wss://your-project.livekit.cloud
```

### 3. Run everything (three terminals)

```bash
# Terminal 1 — voice agent
python .\Backend\agent.py dev

# Terminal 2 — token server (port 5001)
python .\Backend\server.py

# Terminal 3 — frontend (port 5173)
cd Frontend
npm run dev
```

Open **http://localhost:5173**, click **Talk to an Agent!**, enter your name, allow microphone access, and start talking.

---

## 📸 Screenshots

![alt text](<example of result output  02.png>)

### 3. LiveKit Agent Connection

The LiveKit Agents Console confirming the session — room, region, participant count, and the agent configuration showing the Gemini realtime audio model in use, with conversation and state-change events streaming in the event log.

![alt text](<LiveKit-Agent connection - 01.png>)

---

## 🧩 Key Backend Components

- **`agent.py`** — Connects to the room, instantiates the Gemini realtime model (pinned to English), starts an `AgentSession`, and sends the welcome message.
- **`api.py`** — `AssistantFnc` subclasses `Agent` and exposes the `@function_tool` methods (`lookup_car`, `get_car_details`, `create_car`) so the model can act on the database.
- **`db_driver.py`** — Thin SQLite wrapper with a `cars` table keyed by VIN.
- **`server.py`** — Issues short-lived LiveKit access tokens and generates a unique room name per connection.

---

## 📝 License

This project is for educational and demonstration purposes. Add your preferred license here.
