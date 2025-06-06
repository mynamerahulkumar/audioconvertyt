import whisper
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
from deep_translator import GoogleTranslator
import os

# --- Step 1: Split audio into smaller chunks ---
def split_audio(audio_path, chunk_length_ms=60000):
    audio = AudioSegment.from_file(audio_path)
    chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
    return chunks

# --- Step 2: Transcribe English audio ---
# --- Step 2: Transcribe English audio ---
def transcribe_audio_to_text(audio_chunk_path):
    # Load the audio chunk as an AudioSegment
    audio_chunk = AudioSegment.from_file(audio_chunk_path)
    
    # Export the audio chunk to a temporary WAV file
    temp_wav_path = "temp_chunk.wav"
    audio_chunk.export(temp_wav_path, format="wav")
    
    # Load the Whisper model and transcribe the audio
    model = whisper.load_model("base")  # or "small", "medium", "large"
    result = model.transcribe(temp_wav_path)
    
    # Clean up the temporary WAV file
    os.remove(temp_wav_path)
    
    return result["text"]
# --- Step 3: Translate English text to Spanish ---
def translate_text(text, target_lang="es"):
    translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
    return translated

# --- Step 4: Convert Spanish text to speech (MP3) ---
def text_to_speech(text, output_mp3):
    tts = gTTS(text=text, lang='es')
    tts.save(output_mp3)

# --- Step 5: Combine audio chunks ---
def combine_audio(chunks, output_path):
    combined = AudioSegment.empty()
    for chunk in chunks:
        combined += AudioSegment.from_file(chunk)
    combined.export(output_path, format="mp3")

# --- Main pipeline ---
def english_mp3_to_spanish_mp3(input_mp3, output_mp3, chunk_length_ms=60000):
    print("Splitting audio into smaller chunks...")
    chunks = split_audio(input_mp3, chunk_length_ms)
    
    spanish_audio_chunks = []
    for i, chunk in enumerate(chunks):
        print(f"Processing chunk {i + 1}/{len(chunks)}...")
        
        # Export chunk to a temporary file
        chunk_path = f"temp_chunk_{i}.wav"
        chunk.export(chunk_path, format="wav")
        
        # Transcribe English audio
        english_text = transcribe_audio_to_text(chunk_path)
        print(f"English Text (Chunk {i + 1}):", english_text)
        
        # Translate to Spanish
        spanish_text = translate_text(english_text)
        print(f"Spanish Text (Chunk {i + 1}):", spanish_text)
        
        # Convert Spanish text to speech
        spanish_chunk_path = f"spanish_chunk_{i}.mp3"
        text_to_speech(spanish_text, spanish_chunk_path)
        spanish_audio_chunks.append(spanish_chunk_path)
        
        # Clean up temporary chunk file
        os.remove(chunk_path)
    
    print("Combining Spanish audio chunks...")
    combine_audio(spanish_audio_chunks, output_mp3)
    
    # Clean up temporary Spanish audio files
    for chunk_path in spanish_audio_chunks:
        os.remove(chunk_path)
    
    print(f"Spanish audio saved to {output_mp3}")

# Example usage:
if __name__ == "__main__":
    input_mp3_file = "english_long_audio.mp3"
    output_mp3_file = "spanish_long_audio.mp3"
    english_mp3_to_spanish_mp3(input_mp3_file, output_mp3_file)
