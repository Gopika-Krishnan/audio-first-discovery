import tempfile

import numpy as np
import scipy.io.wavfile as wavfile
import sounddevice as sd
import whisper
from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer


class WhisperListener:
    def __init__(self, model_name="base"):
        print(f"🎙️ Loading Whisper model: {model_name}")
        self.model = whisper.load_model(model_name)

    def listen(self, duration=5, sample_rate=16000) -> str:
        """
        Record audio from microphone and transcribe it
        """
        print("🎧 Listening...")
        audio = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype=np.float32
        )
        sd.wait()

        # Save to temp WAV
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as f:
            wavfile.write(f.name, sample_rate, audio)
            result = self.model.transcribe(f.name, fp16=False)

        text = result["text"].strip()
        print(f"🗣️ You said: {text}")
        return text


async def read_text(text: str) -> None:
    openai = AsyncOpenAI()
    async with openai.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="coral",
        input=text,
        instructions="Speak in a neutral, pleasant voice.",
        response_format="pcm",
    ) as response:
        await LocalAudioPlayer().play(response)
