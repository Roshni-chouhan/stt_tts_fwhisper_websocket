import asyncio
import websockets
import pyaudio
import os
import platform

# -----------------------------
# Audio Config
# -----------------------------
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000  # Required for Whisper/faster-whisper

# -----------------------------
# Stream audio in real-time
# -----------------------------
async def stream_audio(websocket):
    p = pyaudio.PyAudio()

    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )

    print("🎤 Recording... Press Ctrl+C to stop")

    try:
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            await websocket.send(data)

    except KeyboardInterrupt:
        print("\n🛑 Stopping recording...")
        await websocket.send("END")

    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()


# -----------------------------
# Receive server response
# -----------------------------
async def receive_response(websocket):
    audio_chunks = []

    while True:
        data = await websocket.recv()

        # TEXT messages
        if isinstance(data, str):
            if data.startswith("PARTIAL:"):
                print("📝 Partial:", data[8:])

            elif data.startswith("TRANSCRIPT:"):
                print("✅ Final Transcript:", data[11:])

            elif data == "AUDIO_END":
                break

        # AUDIO chunks
        else:
            audio_chunks.append(data)

    return audio_chunks


# -----------------------------
# Save & Play audio
# -----------------------------
def play_audio(audio_chunks):
    file_name = "response.mp3"

    with open(file_name, "wb") as f:
        for chunk in audio_chunks:
            f.write(chunk)

    print(f"🔊 Saved: {file_name}")

    system = platform.system()

    if system == "Darwin":
        os.system(f"afplay {file_name}")
    elif system == "Windows":
        os.system(f"start {file_name}")
    else:
        os.system(f"aplay {file_name}")


# -----------------------------
# Main Client
# -----------------------------
async def client():
    uri = "ws://127.0.0.1:8767"  # more stable than localhost

    async with websockets.connect(uri) as websocket:
        print("✅ Connected to server")

        # Run send + receive together
        send_task = asyncio.create_task(stream_audio(websocket))
        receive_task = asyncio.create_task(receive_response(websocket))

        await send_task
        audio_chunks = await receive_task

        play_audio(audio_chunks)


# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    asyncio.run(client())