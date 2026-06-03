import whisper


def transcribe_audio(audio_path):
    """Transcribes an audio file with Whisper."""

    model = whisper.load_model('turbo')
    result = model.transcribe(audio_path)
    return result.get("text", "").strip()