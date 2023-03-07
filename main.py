import pyaudio
import numpy as np
import soundfile as sf
import io
from pydub import AudioSegment
from pydub.playback import play

try:
    import librosa
    use_librosa = True
except ImportError:
    use_librosa = False


FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
SILENCE_THRESHOLD = 500 / 32767.0

p = pyaudio.PyAudio()

mic = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK)

audio_chunks = []
chunk_duration = CHUNK / RATE
silence_duration = 0
sound_duration = 0
octaves = 0.5

print("Recording started")

# main loop
while True:
    # receive auido data
    data = mic.read(CHUNK)

    # calculate RMS amplitude of audio data
    audio_data = np.frombuffer(data, dtype=np.int16)
    audio_data = audio_data.astype(np.float32) / 32767.0
    rms = np.sqrt(np.mean(audio_data ** 2))

    # check if audio data is silent or not
    if rms < SILENCE_THRESHOLD:
        silence_duration += chunk_duration
    else:
        sound_duration += chunk_duration
        audio_chunks.append(data)
        silence_duration = 0

    # calculate duration of record
    audio_duration = len(audio_chunks) * 1024 / (2 * RATE * CHANNELS)
    print(f'\r{audio_duration}', end='')

    # if silence lasts for more than 0.3 seconds and
    # record duration lasts for more than 0.6 seconds,
    # pitch shift and play the recorded audio
    if silence_duration > 0.3 and sound_duration > 0.6:
        # combine audio frames into one continuous audio file
        audio_chunk = b"".join(audio_chunks)

        sound, sample_rate = sf.read(
            io.BytesIO(audio_chunk),
            format='raw',
            samplerate=RATE,
            channels=CHANNELS,
            subtype='PCM_16',
            endian='little')

        # if record is stereo
        if sound.ndim == 2:
            sound = sound[:, 0]

        # pitch shift audio data on the fly
        if use_librosa:  # not tested yet
            sound_pitched = librosa.effects.pitch_shift(
                sound,
                sample_rate,
                n_steps=octaves,
                bins_per_octave=12)
        else:
            new_sample_rate = int(RATE * (2.0 ** octaves))
            sound = AudioSegment(
                audio_chunk,
                sample_width=2,
                frame_rate=RATE,
                channels=CHANNELS)
            sound_pitched = sound._spawn(
                sound.raw_data,
                overrides={'frame_rate': new_sample_rate})
            sound_pitched = sound_pitched.set_frame_rate(RATE)

        print("\nPlaying...")
        # play the pitched audio data
        if use_librosa:
            sound_pitched = sound_pitched.astype(np.int16)
            play(AudioSegment(
                sound_pitched.tobytes(),
                sample_width=2,
                frame_rate=RATE,
                channels=CHANNELS))
        else:
            play(sound_pitched)

        print("Recording...")
        # reset state
        sound_duration = 0
        audio_chunks = []
