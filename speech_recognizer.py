from transformers import WhisperProcessor, WhisperForConditionalGeneration
import torchaudio

# Load model and processor
processor = WhisperProcessor.from_pretrained("openai/whisper-tiny.en")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-tiny.en")
# processor = WhisperProcessor.from_pretrained("openai/whisper-medium")
# model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-medium")

def transcribe_audio(audio_file_path, chunk_length_s=30):
    # Load the audio file
    audio, sampling_rate = torchaudio.load(audio_file_path)
    
    # If the audio file has multiple channels, convert it to mono
    if audio.shape[0] > 1:
        audio = audio.mean(dim=0).unsqueeze(0)
    
    # Resample the audio to 16kHz
    resampler = torchaudio.transforms.Resample(orig_freq=sampling_rate, new_freq=16000)
    audio = resampler(audio).squeeze()
    
    # Calculate the number of samples in each chunk
    chunk_length_samples = chunk_length_s * 16000  # 16kHz sampling rate
    
    # Split the audio into chunks
    audio_chunks = audio.split(chunk_length_samples)
    
    # Process each chunk
    full_transcription = ""
    for i, chunk in enumerate(audio_chunks):
        print(f"Processing chunk {i + 1}/{len(audio_chunks)}")
        
        # Convert chunk to the required format
        input_features = processor(chunk, sampling_rate=16000, return_tensors="pt").input_features

        # Generate token ids
        predicted_ids = model.generate(input_features)

        # Decode token ids to text
        transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)

        # Append the transcription
        full_transcription += transcription[0] + " "

    return full_transcription.strip()

# Test the function
def Speech_recognizer(path):
    audio_file_path = path
    transcript = transcribe_audio(audio_file_path)
    print(transcript)
    return transcript