import os

import numpy as np
from scipy.io import wavfile

from audiomentations import (
    Compose,
    AddGaussianNoise,
    TimeStretch,
    PitchShift,
    Shift,
    Normalize,
    AddImpulseResponse,
    FrequencyMask,
    TimeMask,
    AddGaussianSNR,
)

SAMPLE_RATE = 16000
CHANNELS = 1


def load_wav_file(sound_file_path):
    sample_rate, sound_np = wavfile.read(sound_file_path)
    if sample_rate != SAMPLE_RATE:
        raise Exception(
            "Unexpected sample rate {} (expected {})".format(sample_rate, SAMPLE_RATE)
        )

    if sound_np.dtype != np.float32:
        assert sound_np.dtype == np.int16
        sound_np = sound_np / 32767  # ends up roughly between -1 and 1

    return sound_np


if __name__ == "__main__":
    current_dir = os.path.dirname(__file__)
    output_dir = os.path.join(current_dir, "output")
    os.makedirs(output_dir, exist_ok=True)

    samples = load_wav_file(os.path.join(current_dir, "acoustic_guitar_0.wav"))

    # AddImpulseResponse
    augmenter = Compose(
        [AddImpulseResponse(p=1.0, ir_path=os.path.join(current_dir, "ir"))]
    )
    output_file_path = os.path.join(
        output_dir, "AddImpulseResponse_{:03d}.wav".format(0)
    )
    augmented_samples = augmenter(samples=samples, sample_rate=SAMPLE_RATE)
    wavfile.write(output_file_path, rate=SAMPLE_RATE, data=augmented_samples)

    # FrequencyMask
    augmenter = Compose([FrequencyMask(p=1.0)])
    for i in range(5):
        output_file_path = os.path.join(
            output_dir, "FrequencyMask_{:03d}.wav".format(i)
        )
        augmented_samples = augmenter(samples=samples, sample_rate=SAMPLE_RATE)
        wavfile.write(output_file_path, rate=SAMPLE_RATE, data=augmented_samples)

    # TimeMask
    augmenter = Compose([TimeMask(p=1.0)])
    for i in range(5):
        output_file_path = os.path.join(output_dir, "TimeMask_{:03d}.wav".format(i))
        augmented_samples = augmenter(samples=samples, sample_rate=SAMPLE_RATE)
        wavfile.write(output_file_path, rate=SAMPLE_RATE, data=augmented_samples)

    # AddGaussianSNR
    augmenter = Compose([AddGaussianSNR(p=1.0)])
    for i in range(5):
        output_file_path = os.path.join(
            output_dir, "AddGaussianSNR_{:03d}.wav".format(i)
        )
        augmented_samples = augmenter(samples=samples, sample_rate=SAMPLE_RATE)
        wavfile.write(output_file_path, rate=SAMPLE_RATE, data=augmented_samples)

    # AddGaussianNoise
    augmenter = Compose(
        [AddGaussianNoise(min_amplitude=0.001, max_amplitude=0.015, p=1.0)]
    )
    for i in range(5):
        output_file_path = os.path.join(
            output_dir, "AddGaussianNoise_{:03d}.wav".format(i)
        )
        augmented_samples = augmenter(samples=samples, sample_rate=SAMPLE_RATE)
        wavfile.write(output_file_path, rate=SAMPLE_RATE, data=augmented_samples)

    # TimeStretch
    augmenter = Compose([TimeStretch(min_rate=0.8, max_rate=1.25, p=1.0)])
    for i in range(5):
        output_file_path = os.path.join(output_dir, "TimeStretch_{:03d}.wav".format(i))
        augmented_samples = augmenter(samples=samples, sample_rate=SAMPLE_RATE)
        wavfile.write(output_file_path, rate=SAMPLE_RATE, data=augmented_samples)

    # PitchShift
    augmenter = Compose([PitchShift(min_semitones=-4, max_semitones=4, p=1.0)])
    for i in range(5):
        output_file_path = os.path.join(output_dir, "PitchShift_{:03d}.wav".format(i))
        augmented_samples = augmenter(samples=samples, sample_rate=SAMPLE_RATE)
        wavfile.write(output_file_path, rate=SAMPLE_RATE, data=augmented_samples)

    # Shift
    augmenter = Compose([Shift(min_fraction=-0.5, max_fraction=0.5, p=1.0)])
    for i in range(5):
        output_file_path = os.path.join(output_dir, "Shift_{:03d}.wav".format(i))
        augmented_samples = augmenter(samples=samples, sample_rate=SAMPLE_RATE)
        wavfile.write(output_file_path, rate=SAMPLE_RATE, data=augmented_samples)

    # Normalize
    augmenter = Compose([Normalize(p=1.0)])
    output_file_path = os.path.join(output_dir, "Normalize_{:03d}.wav".format(0))
    augmented_samples = augmenter(samples=samples, sample_rate=SAMPLE_RATE)
    wavfile.write(output_file_path, rate=SAMPLE_RATE, data=augmented_samples)
