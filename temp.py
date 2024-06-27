import os
import json
import numpy as np
from concurrent.futures import ProcessPoolExecutor
from pydub import AudioSegment
import re

def convert_numbers_to_korean(text):
    # 이 함수는 그대로 유지

def contains_english(text):
    return bool(re.search(r'[a-zA-Z]', text))

def clean_text(text):
    # 정규표현식을 사용하여 한 번에 처리
    text = re.sub(r'[!@#$%^&*(),.?":{}|<>]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def process_audio_file(audio_path, label_path):
    audio = AudioSegment.from_wav(audio_path)
    with open(label_path, 'r', encoding='utf-8') as f:
        label_data = json.load(f)
    reference_text = label_data['원하는키']['stt']
    if "SP" not in reference_text and not contains_english(reference_text):
        reference_text = clean_text(reference_text)
        reference_text = convert_numbers_to_korean(reference_text)
    return audio, reference_text

def extract_paths(audio_folder, label_folder):
    paths = []
    for root, _, files in os.walk(audio_folder):
        for file in files:
            if file.endswith(".wav"):
                audio_path = os.path.join(root, file)
                label_path = os.path.join(label_folder, os.path.relpath(audio_path, audio_folder)).replace(".wav", ".json")
                if os.path.exists(label_path):
                    paths.append((audio_path, label_path))
    return paths

def concatenate_audios_and_labels(paths):
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(process_audio_file, [p[0] for p in paths], [p[1] for p in paths]))
    
    combined_audio = AudioSegment.empty()
    combined_text = ""
    for audio, text in results:
        combined_audio += audio
        combined_text += text + " "
    
    return combined_audio, combined_text.strip()

def add_background_music(combined_audio, music_path, music_level=-10):
    music = AudioSegment.from_mp3(music_path)
    music = music - abs(music_level)  # Adjust music level
    return combined_audio.overlay(music, loop=True)

def add_noise(audio_segment, noise_level=0.5):
    noise = np.random.normal(0, noise_level, len(audio_segment.get_array_of_samples()))
    noise_audio = AudioSegment(
        noise.astype(np.int16).tobytes(),
        frame_rate=audio_segment.frame_rate,
        sample_width=2,
        channels=1
    )
    return audio_segment.overlay(noise_audio)

def main(audio_folder, label_folder, music_path, output_path):
    paths = extract_paths(audio_folder, label_folder)
    combined_audio, combined_text = concatenate_audios_and_labels(paths)
    combined_audio = add_background_music(combined_audio, music_path)
    combined_audio = add_noise(combined_audio)
    
    combined_audio.export(output_path, format="wav")
    with open(output_path.replace(".wav", ".txt"), "w", encoding="utf-8") as f:
        f.write(combined_text)

if __name__ == "__main__":
    audio_folder = "path/to/audio/folder"
    label_folder = "path/to/label/folder"
    music_path = "path/to/background/music.mp3"
    output_path = "path/to/output/combined_audio.wav"
    main(audio_folder, label_folder, music_path, output_path)
