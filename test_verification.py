#!/usr/bin/env python3
"""
Test script for verification feature
"""

import sys
import os
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_script_parsing():
    """Test script file parsing."""
    print("Testing script file parsing...")

    sys.argv = ["cli.py", "--input", "test.mp4"]
    from cli import parse_srt_file, parse_vtt_file, parse_ass_file, parse_txt_file

    # Create test SRT content
    srt_content = """1
00:00:00,000 --> 00:00:02,000
Hello world this is a test

2
00:00:02,000 --> 00:00:04,000
Another line of text
"""

    with tempfile.NamedTemporaryFile(mode='w', suffix='.srt', delete=False) as f:
        f.write(srt_content)
        srt_file = f.name

    text = parse_srt_file(srt_file)
    assert "Hello world this is a test" in text
    assert "Another line of text" in text
    os.unlink(srt_file)
    print("✓ SRT parsing works")

    # Create test VTT content
    vtt_content = """WEBVTT

1
00:00:00.000 --> 00:00:02.000
Hello world this is a test

2
00:00:02.000 --> 00:00:04.000
Another line of text
"""

    with tempfile.NamedTemporaryFile(mode='w', suffix='.vtt', delete=False) as f:
        f.write(vtt_content)
        vtt_file = f.name

    text = parse_vtt_file(vtt_file)
    assert "Hello world this is a test" in text
    assert "Another line of text" in text
    os.unlink(vtt_file)
    print("✓ VTT parsing works")

    # Create test ASS content
    ass_content = """[Script Info]
Title: Test

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,24,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,2,1, 2,20,20,30,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:02.00,Default,,0,0,0,,Hello world this is a test
Dialogue: 0,0:00:02.00,0:00:04.00,Default,,0,0,0,,Another line of text
"""

    with tempfile.NamedTemporaryFile(mode='w', suffix='.ass', delete=False) as f:
        f.write(ass_content)
        ass_file = f.name

    text = parse_ass_file(ass_file)
    assert "Hello world this is a test" in text
    assert "Another line of text" in text
    os.unlink(ass_file)
    print("✓ ASS parsing works")

    # Create test TXT content
    txt_content = "Hello world this is a test\nAnother line of text"

    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(txt_content)
        txt_file = f.name

    text = parse_txt_file(txt_file)
    assert "Hello world this is a test" in text
    assert "Another line of text" in text
    os.unlink(txt_file)
    print("✓ TXT parsing works")

    return True


def test_comparison():
    """Test text comparison."""
    print("\nTesting text comparison...")

    sys.argv = ["cli.py", "--input", "test.mp4"]
    from cli import calculate_similarity, find_missing_words, normalize_text

    # Test similar texts
    text1 = "Hello world this is a test"
    text2 = "Hello world this is a test"
    similarity = calculate_similarity(text1, text2)
    assert similarity == 100.0
    print("✓ Identical texts similarity = 100%")

    # Test slightly different texts
    text1 = "Hello world this is a test"
    text2 = "Hello world this is a test of the system"
    similarity = calculate_similarity(text1, text2)
    assert 50 < similarity < 100
    print(f"✓ Different texts similarity = {similarity:.1f}%")

    # Test missing words
    text1 = "Hello world this is a test"
    text2 = "Hello world this is"
    missing = find_missing_words(text1, text2)
    assert "a" in missing
    assert "test" in missing
    print(f"✓ Missing words detection works: {missing}")

    # Test normalization
    text1 = "Hello, World! This is a TEST."
    norm = normalize_text(text1)
    assert norm == "hello world this is a test"
    print("✓ Text normalization works")

    return True


def test_verification():
    """Test full verification."""
    print("\nTesting full verification...")

    sys.argv = ["cli.py", "--input", "test.mp4"]
    from cli import verify_transcription

    # Test passing verification
    original = "Hello world this is a test of the system"
    transcription = "Hello world this is a test of the system"
    is_valid, stats = verify_transcription(original, transcription, 80.0)
    assert is_valid == True
    assert stats["similarity"] == 100.0
    print("✓ Passing verification works")

    # Test failing verification
    original = "Hello world this is a test of the system"
    transcription = "Hello world"
    is_valid, stats = verify_transcription(original, transcription, 80.0)
    assert is_valid == False
    assert stats["similarity"] < 80.0
    print("✓ Failing verification works")

    # Test with missing words
    original = "Hello world this is a test"
    transcription = "Hello world this is"
    is_valid, stats = verify_transcription(original, transcription, 80.0)
    assert "a" in stats["missing_words"]
    assert "test" in stats["missing_words"]
    print(f"✓ Missing words detected: {stats['missing_words']}")

    return True


def main():
    """Run all tests."""
    print("=" * 60)
    print("VideoPolish-er Verification Feature Tests")
    print("=" * 60)

    tests = [
        test_script_parsing,
        test_comparison,
        test_verification
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
            import traceback
            traceback.print_exc()
            failed += 1

    print("\n" + "=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 60)

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())