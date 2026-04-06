import asyncio
import websockets
import os
import tempfile
from faster_whisper import WhisperModel
import edge_tts

# -----------------------------
# Load Faster Whisper Model
# -----------------------------
print("Loading Faster-Whisper model...")
model = WhisperModel("base", compute_type="int8")  # faster + low RAM

# -----------------------------
# Dummy AI Logic (Replace later)
# -----------------------------
def call_langgraph(user_text):
    print("User:", user_text)
    return f"AI says: {user_text}"

# -----------------------------
# Speech → Text (Optimized)
# -----------------------------
def speech_to_text(audio_bytes):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp:
        temp.write(audio_bytes)
        temp_path = temp.name

    segments, _ = model.transcribe(temp_path)

    text = " ".join([seg.text for seg in segments])

    os.remove(temp_path)  # cleanup
    return text.strip()

# -----------------------------
# Text → Speech
# -----------------------------
async def text_to_speech(text):
    output_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
    communicate = edge_tts.Communicate(text, "en-US-AriaNeural")
    await communicate.save(output_file)
    return output_file

# -----------------------------
# WebSocket Handler
# -----------------------------
async def handler(websocket):
    print("Client connected ✅")
    audio_buffer = []

    try:
        while True:
            data = await websocket.recv()

            # -----------------------------
            # END signal
            # -----------------------------
            if isinstance(data, str) and data == "END":
                print("Processing audio...")

                audio_bytes = b"".join(audio_buffer)
                audio_buffer = []

                # STT
                text = speech_to_text(audio_bytes)
                await websocket.send(f"TRANSCRIPT:{text}")

                # AI Response
                response_text = call_langgraph(text)

                # TTS
                audio_file = await text_to_speech(response_text)

                # Send audio chunks
                with open(audio_file, "rb") as f:
                    while chunk := f.read(4096):
                        await websocket.send(chunk)

                await websocket.send("AUDIO_END")

                os.remove(audio_file)

            else:
                audio_buffer.append(data)

                # Partial transcription (faster logic)
                if len(audio_buffer) % 10 == 0:
                    try:
                        partial_text = speech_to_text(b"".join(audio_buffer))
                        await websocket.send(f"PARTIAL:{partial_text}")
                    except:
                        pass

    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected ❌")


# -----------------------------
# Start Server
# -----------------------------
async def main():
    print("Server running on ws://localhost:8767 🚀")
    async with websockets.serve(handler, "localhost", 8767):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())