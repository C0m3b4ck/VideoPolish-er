#!/usr/bin/env python3
"""
Create a test audio file with silence and stutters for testing
"""

import numpy as np
import soundfile as sf
import os

def create_test_audio():
    """Create a test audio file with silence and stutters."""
    print("Creating test audio file...")
    
    # Audio parameters
    sample_rate = 16000
    duration = 10  # seconds
    
    # Generate time array
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    
    # Create a simple sine wave (simulating speech)
    frequency = 440  # Hz
    audio = 0.3 * np.sin(2 * np.pi * frequency * t)
    
    # Add some noise
    audio += 0.01 * np.random.randn(len(audio))
    
    # Add silence periods (simulating pauses in speech)
    # First 2 seconds: speech
    # 2-4 seconds: silence
    # 4-6 seconds: speech
    # 6-8 seconds: silence
    # 8-10 seconds: speech
    silence_mask = np.zeros_like(audio)
    silence_mask[:int(2 * sample_rate)] = 1  # Speech
    silence_mask[int(2 * sample_rate):int(4 * sample_rate)] = 0  # Silence
    silence_mask[int(4 * sample_rate):int(6 * sample_rate)] = 1  # Speech
    silence_mask[int(6 * sample_rate):int(8 * sample_rate)] = 0  # Silence
    silence_mask[int(8 * sample_rate):] = 1  # Speech
    
    audio = audio * silence_mask
    
    # Normalize audio
    audio = audio / np.max(np.abs(audio))
    
    # Save audio file
    output_path = "test_audio.wav"
    sf.write(output_path, audio, sample_rate)
    
    print(f"✓ Test audio file created: {output_path}")
    print(f"  Duration: {duration}s")
    print(f"  Sample rate: {sample_rate} Hz")
    print(f"  Speech periods: 2-4s, 6-8s")
    print(f"  Silence periods: 0-2s, 4-6s, 8-10s")
    
    return output_path


if __name__ == "__main__":
    create_test_audio()