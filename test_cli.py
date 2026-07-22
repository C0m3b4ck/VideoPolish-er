#!/usr/bin/env python3
"""
Test script for VideoPolish-er CLI
"""

import sys
import os
import tempfile
import json
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_argument_parsing():
    """Test CLI argument parsing."""
    print("Testing argument parsing...")
    
    # Test with minimal arguments
    sys.argv = ["cli.py", "--input", "test.mp4"]
    from cli import parse_arguments
    
    args = parse_arguments()
    assert args.input == "test.mp4"
    assert args.output == "./output"
    assert args.model == "faster-whisper"
    assert args.language == "en"
    assert args.remove_silence == False
    assert args.remove_stutters == False
    
    print("✓ Minimal arguments parsing works")
    
    # Test with all arguments
    sys.argv = [
        "cli.py", "--input", "test.mp4",
        "--output", "./test_output",
        "--model", "whisperx",
        "--language", "es",
        "--remove-silence",
        "--silence-threshold", "-35",
        "--min-silence-duration", "300",
        "--remove-stutters",
        "--stutter-patterns", "uhm,uh,um",
        "--format", "vtt",
        "--words-per-chunk", "4",
        "--device", "cuda",
        "--verbose"
    ]
    
    args = parse_arguments()
    assert args.input == "test.mp4"
    assert args.output == "./test_output"
    assert args.model == "whisperx"
    assert args.language == "es"
    assert args.remove_silence == True
    assert args.silence_threshold == -35
    assert args.min_silence_duration == 300
    assert args.remove_stutters == True
    assert args.stutter_patterns == "uhm,uh,um"
    assert args.format == "vtt"
    assert args.words_per_chunk == 4
    assert args.device == "cuda"
    assert args.verbose == True
    
    print("✓ All arguments parsing works")
    
    return True


def test_file_validation():
    """Test file validation."""
    print("\nTesting file validation...")
    
    sys.argv = ["cli.py", "--input", "test.mp4"]
    from cli import validate_input_file
    
    # Test with non-existent file
    assert validate_input_file("nonexistent.mp4") == False
    print("✓ Non-existent file validation works")
    
    # Test with unsupported format
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
        temp_file = f.name
    assert validate_input_file(temp_file) == False
    os.unlink(temp_file)
    print("✓ Unsupported format validation works")
    
    # Test with valid file
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
        temp_file = f.name
    assert validate_input_file(temp_file) == True
    os.unlink(temp_file)
    print("✓ Valid file validation works")
    
    return True


def test_stutter_detection():
    """Test stutter detection and removal."""
    print("\nTesting stutter detection...")
    
    sys.argv = ["cli.py", "--input", "test.mp4"]
    from cli import detect_and_remove_stutters
    
    # Test with stutters
    words = [
        {"word": "Hello", "start": 0.0, "end": 0.5},
        {"word": "uhm", "start": 0.5, "end": 0.8},
        {"word": "world", "start": 0.8, "end": 1.2},
        {"word": "uh", "start": 1.2, "end": 1.4},
        {"word": "this", "start": 1.4, "end": 1.7},
        {"word": "is", "start": 1.7, "end": 1.9},
        {"word": "um", "start": 1.9, "end": 2.1},
        {"word": "great", "start": 2.1, "end": 2.5}
    ]
    
    stutter_patterns = ["uhm", "uh", "um", "er", "ah", "hmm", "mhm", "erm", "umm"]
    
    cleaned_words, stats = detect_and_remove_stutters(words, stutter_patterns)
    
    assert len(cleaned_words) == 5  # Should remove 3 stutters
    assert stats["stutters_found"] == 3
    assert stats["stutters_removed"] == 3
    assert "uhm" in stats["stutter_words"]
    assert "uh" in stats["stutter_words"]
    assert "um" in stats["stutter_words"]
    
    print("✓ Stutter detection works")
    
    # Test with no stutters
    words_no_stutters = [
        {"word": "Hello", "start": 0.0, "end": 0.5},
        {"word": "world", "start": 0.5, "end": 1.0}
    ]
    
    cleaned_words, stats = detect_and_remove_stutters(words_no_stutters, stutter_patterns)
    assert len(cleaned_words) == 2
    assert stats["stutters_found"] == 0
    
    print("✓ No stutter detection works")
    
    return True


def test_subtitle_generation():
    """Test subtitle generation."""
    print("\nTesting subtitle generation...")
    
    sys.argv = ["cli.py", "--input", "test.mp4"]
    from cli import words_to_srt, words_to_vtt, words_to_ass, words_to_json
    
    words = [
        {"word": "Hello", "start": 0.0, "end": 0.5},
        {"word": "world", "start": 0.5, "end": 1.0},
        {"word": "this", "start": 1.0, "end": 1.3},
        {"word": "is", "start": 1.3, "end": 1.5},
        {"word": "a", "start": 1.5, "end": 1.6},
        {"word": "test", "start": 1.6, "end": 2.0}
    ]
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test SRT
        srt_path = os.path.join(tmpdir, "test.srt")
        words_to_srt(words, srt_path, 3)
        assert os.path.exists(srt_path)
        with open(srt_path, 'r') as f:
            content = f.read()
            assert "Hello world this" in content
            assert "is a test" in content
        print("✓ SRT generation works")
        
        # Test VTT
        vtt_path = os.path.join(tmpdir, "test.vtt")
        words_to_vtt(words, vtt_path, 3)
        assert os.path.exists(vtt_path)
        with open(vtt_path, 'r') as f:
            content = f.read()
            assert "WEBVTT" in content
        print("✓ VTT generation works")
        
        # Test ASS
        ass_path = os.path.join(tmpdir, "test.ass")
        words_to_ass(words, ass_path, 3)
        assert os.path.exists(ass_path)
        with open(ass_path, 'r') as f:
            content = f.read()
            assert "[Script Info]" in content
            assert "Dialogue:" in content
        print("✓ ASS generation works")
        
        # Test JSON
        json_path = os.path.join(tmpdir, "test.json")
        words_to_json(words, json_path, 3)
        assert os.path.exists(json_path)
        with open(json_path, 'r') as f:
            data = json.load(f)
            assert "transcription" in data
            assert "groups" in data
            assert len(data["groups"]) == 2
        print("✓ JSON generation works")
    
    return True


def test_silence_removal():
    """Test silence removal (basic test without actual audio)."""
    print("\nTesting silence removal function signature...")
    
    sys.argv = ["cli.py", "--input", "test.mp4"]
    from cli import remove_silence_from_audio
    
    # Test that function exists and has correct signature
    import inspect
    sig = inspect.signature(remove_silence_from_audio)
    params = list(sig.parameters.keys())
    assert "audio_path" in params
    assert "output_path" in params
    assert "threshold_db" in params
    assert "min_silence_duration_ms" in params
    
    print("✓ Silence removal function signature is correct")
    
    return True


def main():
    """Run all tests."""
    print("=" * 60)
    print("VideoPolish-er CLI Tests")
    print("=" * 60)
    
    tests = [
        test_argument_parsing,
        test_file_validation,
        test_stutter_detection,
        test_subtitle_generation,
        test_silence_removal
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())