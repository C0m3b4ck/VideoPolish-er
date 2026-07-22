# VideoPolish-er

A CLI tool for transcribing and cleaning up audio/video files with automatic noise removal and stutter detection.

Built on top of [Transcribix](https://github.com/C0m3b4ck/Transcribix) with additional audio cleanup features.

All models run 100% locally. No API keys, no tokens, no internet at runtime.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue?style=for-the-badge)](LICENSE)

## Features

- **11 local speech-to-text models** from Transcribix
- **Automatic silence removal** with configurable threshold and duration
- **Stutter detection and removal** (uhm, uh, um, er, ah, hmm, etc.)
- **Customizable stutter patterns** (add your own filler words)
- **Verification against original script** (SRT, VTT, ASS, TXT) to detect accidental content removal
- **Word-level timestamps** for caption generation
- **SRT, VTT, ASS, and JSON** output formats
- **Configurable words per caption chunk** (1-8 words)
- **No API keys required** — everything runs on your hardware
- **GPU and CPU support** with auto-detection
- **Multiple language support** (up to 99 languages)

## Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| Python | 3.10+ | 3.11 |
| RAM | 8 GB | 16 GB+ |
| GPU VRAM | 1 GB (Moonshine) | 6 GB+ (large-v3 models) |
| GPU | Any CUDA-capable | NVIDIA RTX 3060+ |
| Disk | 2 GB | 10 GB+ (models vary) |
| OS | Linux, macOS, Windows | Linux (best CUDA support) |

**Note:** CPU-only mode works but is 5-10x slower than GPU. Use Python 3.11 for best compatibility with PyTorch. All models auto-detect GPU/CPU availability.

## Quick Start

```bash
# Clone the repo
git clone https://github.com/sb3x/VideoPolish-er.git
cd VideoPolish-er

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Or use the Transcribix venv if available
# /home/sb3x/Code/Transcribix/venv/bin/pip install soundfile librosa pydub scipy
```

## Usage

### Basic Transcription

```bash
python cli.py --input video.mp4
```

### With Silence Removal

```bash
python cli.py --input video.mp4 --remove-silence
```

### With Stutter Removal

```bash
python cli.py --input video.mp4 --remove-stutters
```

### Full Pipeline

```bash
python cli.py --input video.mp4 --remove-silence --remove-stutters
```

### Custom Stutter Patterns

```bash
python cli.py --input video.mp4 --remove-stutters --stutter-patterns "uhm,uh,um,er,ah,hmm,mhm,erm,umm"
```

### Using the Wrapper Script

```bash
# Make the wrapper script executable
chmod +x run.sh

# Use the wrapper script
./run.sh --input video.mp4 --remove-silence --remove-stutters
```

### Verify Against Original Script

```bash
# Compare transcription against original script file
python cli.py --input video.mp4 --script original.srt

# With custom similarity threshold
python cli.py --input video.mp4 --script original.srt --similarity-threshold 85

# With all cleanup features
python cli.py --input video.mp4 --remove-silence --remove-stutters --script original.vtt
```

## CLI Example Output

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   VideoPolish-er                                            ║
║   Transcription & Audio Cleanup Tool                        ║
║   Based on Transcribix                                      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

=== Step 1: Removing Silence ===
Loading audio file...
Detecting silence (threshold: -40dB, min duration: 500ms)...
Removing silence...
✓ Silence removed: 12.5s (25.0%)

=== Step 2: Transcribing Audio ===
Transcribing with faster-whisper...
Language: en (prob=1.00)
Segment: 0.0s → 2.9s
Segment: 3.2s → 6.4s
Segment: 6.6s → 9.5s

=== Step 3: Removing Stutters ===
Found 3 stutters: uhm, uh, um
✓ Removed 3 stutters

=== Step 4: Generating Output Files ===
✓ SRT saved to ./output/video.srt (10 blocks)

=== Step 5: Verifying Against Original Script ===
Similarity: 95.2% (threshold: 80.0%)
✓ Verification PASSED - Transcription is consistent with original script
Original script words: 156
Transcription words: 148

============================================================
PROCESSING COMPLETE
============================================================
Input: video.mp4
Model: faster-whisper
Language: en
Silence removed: 12.5s (25.0%)
Stutters removed: 3
Verification: PASSED (95.2%)
Words detected: 28
Processing time: 9.5s

Output files:
✓   ./output/video.srt

Stats saved to ./output/video_stats.json
```

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--input, -i` | Input audio/video file path | Required |
| `--output, -o` | Output directory | `./output` |
| `--model, -m` | Transcription model | `faster-whisper` |
| `--language, -l` | Language code | `en` |
| `--model-size` | Model size | `large-v3` |
| `--remove-silence` | Enable silence removal | `false` |
| `--silence-threshold` | Silence threshold in dB | `-40` |
| `--min-silence-duration` | Minimum silence duration in ms | `500` |
| `--remove-stutters` | Enable stutter removal | `false` |
| `--stutter-patterns` | Comma-separated stutter patterns | `uhm,uh,um,er,ah,hmm,mhm,erm,umm` |
| `--format` | Output format (srt, vtt, ass, json) | `srt` |
| `--words-per-chunk` | Words per subtitle chunk | `3` |
| `--device` | Device to use (auto, cuda, cpu) | `auto` |
| `--verbose` | Enable verbose output | `false` |
| `--script, -s` | Original script file for verification | `None` |
| `--similarity-threshold` | Minimum similarity % for verification | `80.0` |

## Supported Models

| Model | VRAM | WER (English) | RTFx | Languages | Best For |
|-------|------|---------------|------|-----------|----------|
| **faster-whisper** | ~2.5 GB (int8) | ~7.4% | ~600x | 99 | General use |
| **WhisperX** | ~3-10 GB | ~7.4% | ~150x | 99 | Word timestamps |
| **stable-ts** | ~3-10 GB | ~7.4% | ~100x | 99 | Subtitles |
| **Parakeet** | ~2 GB | 6.32% | ~3,300x | 25 | English accuracy |
| **Canary** | ~6 GB | 5.63% | ~458x | English only | Top accuracy |
| **Distil-Whisper** | ~4 GB (fp16) | ~7.5% | ~3,600x | 99 | Speed |
| **Moonshine** | <1 GB | ~10% | ~80x | 8 | Edge/CPU |
| **SenseVoice** | ~1 GB | ~5.5% | ~50x | 50+ | Languages |
| **Vosk** | <500 MB | ~12% | ~100x | 20+ | Minimal resources |
| **Whisper original** | 1-10 GB | ~7.4% | ~1-10x | 99 | Most languages |
| **whisper.cpp** | 1-10 GB | ~7.4% | ~5-15x | 99 | CPU/anything |

## Supported Audio Formats

| Format | Status |
|--------|--------|
| MP4 | Supported |
| WAV | Supported |
| MP3 | Supported |
| M4A | Supported |
| FLAC | Supported |
| OGG | Supported |
| MKV | Supported |
| AVI | Supported |
| MOV | Supported |
| WebM | Supported |

## Project Structure

```
VideoPolish-er/
├── cli.py                  # Main CLI tool
├── run.sh                  # Wrapper script to use Transcribix venv
├── test_cli.py             # Unit tests
├── test_verification.py    # Verification feature tests
├── test_examples.sh        # Example usage tests
├── create_test_audio.py    # Create test audio files
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## Testing

```bash
# Run unit tests
python test_cli.py

# Run verification feature tests
python test_verification.py

# Run example tests
./test_examples.sh
```

## Credits

Started on July 2026.

### Based on

- [Transcribix](https://github.com/C0m3b4ck/Transcribix) — Local AI models for YouTube captioning (Apache License 2.0)

### Speech-to-Text Engines

- [faster-whisper](https://github.com/SYSTRAN/faster-whisper) — CTranslate2 Whisper (MIT License)
- [WhisperX](https://github.com/m-bain/whisperX) — Forced phoneme alignment (Apache 2.0)
- [stable-ts](https://github.com/jianfch/stable-ts) — Stabilized timestamps (MIT License)
- [NVIDIA NeMo](https://github.com/NVIDIA/NeMo) — Parakeet & Canary models (Apache 2.0)
- [Moonshine](https://github.com/usefulsensors/moonshine) — Ultra-lightweight ASR (MIT License)
- [FunASR](https://github.com/modelscope/FunASR) — SenseVoice (MIT License)
- [Vosk](https://github.com/alphacep/vosk-api) — Kaldi-based ASR (Apache 2.0)
- [OpenAI Whisper](https://github.com/openai/whisper) — Original implementation (MIT License)
- [whisper.cpp](https://github.com/ggerganov/whisper.cpp) — C++ port (MIT License)

### Audio Processing

- [pydub](https://github.com/jiaaro/pydub) — Audio manipulation (MIT License)
- [librosa](https://github.com/librosa/librosa) — Audio analysis (MIT License)
- [soundfile](https://github.com/soundfile/soundfile) — Audio file I/O (BSD License)

## License

Apache License 2.0