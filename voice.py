from pathlib import Path
import requests

from config import (
    GROQ_API_KEY,
    GROQ_STT_MODEL,
    GROQ_TTS_MODEL,
    GROQ_TTS_VOICE,
    require_groq_key,
)

_STT_URL = "https://api.groq.com/openai/v1/audio/transcriptions"
_TTS_URL = "https://api.groq.com/openai/v1/audio/speech"


def speech_to_text(audio_path: str) -> str:
    require_groq_key()

    with open(audio_path, "rb") as f:
        response = requests.post(
            _STT_URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
            },
            files={
                "file": (
                    Path(audio_path).name,
                    f,
                    "audio/wav",
                )
            },
            data={
                "model": GROQ_STT_MODEL,
            },
            timeout=60,
        )

    if not response.ok:
        raise RuntimeError(
            f"Groq STT Error {response.status_code}: {response.text}"
        )

    return response.json()["text"]


def text_to_speech(text: str, out_path: str = "reply.wav") -> str:
    require_groq_key()

    if not text or not text.strip():
        raise ValueError("TTS text cannot be empty.")

    text = text.strip()

    if len(text) > 200:
        text = text[:200]

    response = requests.post(
        _TTS_URL,
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": GROQ_TTS_MODEL,
            "input": text,
            "voice": GROQ_TTS_VOICE,
            "response_format": "wav",
        },
        timeout=60,
    )

    if not response.ok:
        raise RuntimeError(
            f"Groq TTS Error {response.status_code}: {response.text}"
        )

    with open(out_path, "wb") as f:
        f.write(response.content)

    return out_path


def record_audio(
    path: str = "input.wav",
    seconds: float = 4,
    rate: int = 16000,
) -> str:

    import sounddevice as sd
    import soundfile as sf

    print(f"Listening... ({seconds:.0f}s)")

    audio = sd.rec(
        int(seconds * rate),
        samplerate=rate,
        channels=1,
    )

    sd.wait()

    sf.write(
        path,
        audio,
        rate,
    )

    return path


def play_audio(path: str) -> None:

    import sounddevice as sd
    import soundfile as sf

    data, rate = sf.read(path)

    sd.play(data, rate)
    sd.wait()


if __name__ == "__main__":

    require_groq_key()

    print("Testing JARVIS TTS...")

    path = text_to_speech(
        "Hello, sir. JARVIS voice systems are online."
    )

    print(f"Audio created: {path}")

    print("Playing audio...")

    play_audio(path)

    print("Voice test completed successfully.")
