from pathlib import Path
import types
import sys

from pydub import AudioSegment

# Provide lightweight stubs for heavy dependencies imported by main.py
sys.modules.setdefault('whisper', types.ModuleType('whisper'))

_gtts_mod = types.ModuleType('gtts')
class _DummyGtts:
    def __init__(self, *args, **kwargs):
        pass
    def save(self, *args, **kwargs):
        pass
_gtts_mod.gTTS = _DummyGtts
sys.modules.setdefault('gtts', _gtts_mod)

_deep_mod = types.ModuleType('deep_translator')
class _DummyTranslator:
    def __init__(self, *args, **kwargs):
        pass
    def translate(self, text):
        return text
_deep_mod.GoogleTranslator = _DummyTranslator
sys.modules.setdefault('deep_translator', _deep_mod)

play_mod = types.ModuleType('pydub.playback')
play_mod.play = lambda *args, **kwargs: None
sys.modules.setdefault('pydub.playback', play_mod)


def load_split_audio():
    """Load split_audio function from main.py without running the example code."""
    module_path = Path(__file__).resolve().parents[1] / "audiodubbingpython" / "main.py"
    source_lines = module_path.read_text().splitlines()
    cutoff = len(source_lines)
    for i, line in enumerate(source_lines):
        if line.strip().startswith("english_mp3_to_spanish_mp3"):
            cutoff = i
            break
    trimmed_source = "\n".join(source_lines[:cutoff])
    module = types.ModuleType("main")
    exec(compile(trimmed_source, str(module_path), "exec"), module.__dict__)
    return module.split_audio

split_audio = load_split_audio()


def test_split_audio_splits_at_duration(tmp_path: Path):
    audio = AudioSegment.silent(duration=2500)
    audio_path = tmp_path / "audio.wav"
    audio.export(audio_path, format="wav")

    chunks = split_audio(str(audio_path), chunk_length_ms=1000)

    assert len(chunks) == 3
    assert len(chunks[0]) == 1000
    assert len(chunks[1]) == 1000
    assert len(chunks[2]) == 500

