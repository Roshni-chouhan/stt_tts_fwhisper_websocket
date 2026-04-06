<<<<<<< HEAD
# AI Voice Assistant (STTS)

A modern, real-time Speech-to-Text (STT) and Text-to-Speech (TTS) assistant with a premium, responsive interface. This application uses OpenAI Whisper for high-accuracy local transcription and Edge-TTS for natural-sounding AI voice responses.

## ✨ Features

- **Premium UI Design**: Sleek dark-mode interface with glassmorphism effects, modern gradients, and smooth micro-animations.
- **Real-Time Transcription**: Spoken words appear in the UI as you speak (updated every 2 seconds).
- **Dual Controls**: Distinct **Start** and **Stop** buttons for more intuitive recording management.
- **Live Conversation Log**: A structured conversation history displaying user speech and AI responses.
- **Visual Feedback**: Real-time recording indicator and status badges for WebSocket connectivity.

## 🛠 Tech Stack

- **Backend**: Python 3.x
  - `websockets`: For real-time full-duplex communication.
  - `openai-whisper`: High-quality local speech-to-text conversion.
  - `edge-tts`: Microsoft Edge's high-performance text-to-speech engine.
- **Frontend**: 
  - **HTML5/CSS3**: Modern layouts using Flexbox, vanilla CSS gradients, and glassmorphism.
  - **JavaScript**: WebSocket client and MediaRecorder API for audio streaming.

## 🚀 Getting Started

### Prerequisites

Ensure you have Python 3 installed on your Mac. You will also need `ffmpeg` for audio processing:

```bash
brew install ffmpeg
```

### Installation

1. **Clone the repository**:
   ```bash
   git clone [your-repo-url]
   cd STTS_prashikshan-main
   ```

2. **Set up a virtual environment (optional but recommended)**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install websockets openai-whisper edge-tts numpy
   ```

### Usage

1. **Start the Backend Server**:
   ```bash
   python3 server.py
   ```
   *Note: Ensure port 8767 is available.*

2. **Open the Frontend**:
   - Locate `index.html` in the project folder and double-click to open it in your default browser.
   - Or, open it via a file URL: `file:///Users/archishanaik/Desktop/STTS_prashikshan-main/index.html`

## 💡 Troubleshooting

- **"Address already in use" Error**: If `server.py` fails to start because of port 8767, ensure any previous instances of the server are closed.
- **Microphone Access**: Ensure your browser has permission to access the microphone for `localhost` or local file access.
=======
# stt_tts_fwhisper_websocket

Your final content here
