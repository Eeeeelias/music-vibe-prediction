import glob
import multiprocessing
import os
import pickle

import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import warnings

warnings.filterwarnings('ignore', category=DeprecationWarning)

# Load the audio file
audio_file = "P:\Music\Music\Bloodborne\『Bloodborne』 オリジナルサウンドトラック\\1. Omen.flac"

# Load the audio data and sample rate
y, sr = librosa.load(audio_file)


def dynamics(y, hop=128) -> list:
    # Calculate the RMS amplitude
    rms_amplitude = librosa.feature.rms(y=y, hop_length=hop)

    # Convert RMS to decibels (dB)
    rms_amplitude_db = librosa.amplitude_to_db(rms_amplitude)

    return rms_amplitude_db.tolist()[0]


def tempo(y, sr, hop=128):
    # Calculate the tempo of y
    tempo = librosa.feature.tempo(y=y, sr=sr, hop_length=hop, aggregate=None)

    return tempo



def pitch(y, sr, hop=128):
    # Calculate the pitch
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr, hop_length=hop)

    # Get the mean pitch per frame
    mean_pitch = pitches.mean(axis=0)

    # Convert the mean pitch per frame into Hz
    pitches_in_hz = librosa.hz_to_midi(mean_pitch)

    return pitches_in_hz

def chroma(y, sr, hop=128):
    chroma = librosa.feature.chroma_stft(y=y, sr=sr, hop_length=hop)

    chroma = chroma.flatten()
    return chroma


def set_all(file):
    # Load audio file with sample rate
    y, sr = librosa.load(file)

    hop_length = len(y) // 128

    features = dynamics(y, hop=hop_length)
    # Calculate several features
    try:
        features.extend(tempo(y, sr, hop=hop_length))
        features.extend(pitch(y, sr, hop=hop_length))
        features.extend(chroma(y, sr, hop=hop_length))
        features = np.array(features)
    except:
        features = 0
    return [file, features]



def mfcc(y, sr):
    # Extract the MFCCs
    mfccs = librosa.feature.mfcc(y=y, sr=sr)

    # Print the mean of the MFCCs
    mean_mfccs = mfccs.mean(axis=1)
    return mean_mfccs


def set_single_feature(file):
    # Load audio file with sample rate
    y, sr = librosa.load(file)

    # Get 100 mfccs at regular intervals
    hop_length = len(y) // 100
    mfccs = librosa.feature.chroma_stft(y=y, sr=sr, hop_length=hop_length)
    return [file, mfccs]

def worker(chunk):
    global chunks
    results = []
    for line in tqdm(chunk):
        result = set_all(line)
        if result is not None:
            results.append(result)
    return results


# implement multiprocessing to extract the features of all sound files given an input path
if __name__ == '__main__':
    path = "P:/Music/Music"
    extension_set = {'.mp3', '.flac', '.m4a', '.ogg', '.wav', '.wma', '.m4p', '.mp4', '.m4b', '.m4r', '.3gp', '.aac'}
    all_songs = []
    for artist in glob.glob(path.rstrip("/") + "/*"):
        if not os.path.isdir(artist):
            continue
        for song in glob.glob(artist + "/**/*", recursive=True):
            if not os.path.isfile(song):
                continue
            extension = os.path.splitext(song)[1]
            if extension not in extension_set:
                continue
            all_songs.append(song)
    print(f"Analyzing: {len(all_songs)} songs")


    # num_processes = multiprocessing.cpu_count() // 2
    num_processes = 6
    print(f"initializing {num_processes} cores")
    with multiprocessing.Pool(processes=num_processes) as pool:
        chunk_size = len(all_songs) // num_processes
        chunks = [all_songs[i:i + chunk_size] for i in range(0, len(all_songs), chunk_size)]

        results_list = pool.map(worker, chunks)

    # Combine results from all chunks
    combined_results = [result for sublist in results_list for result in sublist]
    pickle.dump(combined_results, open("features_all.pkl", "wb"))
