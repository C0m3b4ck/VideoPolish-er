#!/bin/bash
# Test script for VideoPolish-er

echo "Testing VideoPolish-er CLI..."
echo ""

# Test 1: Basic transcription
echo "Test 1: Basic transcription"
./run.sh --input test_speech.wav --output ./test_output --format srt
echo ""

# Test 2: With silence removal
echo "Test 2: With silence removal"
./run.sh --input test_speech.wav --output ./test_output --remove-silence --format vtt
echo ""

# Test 3: With stutter removal
echo "Test 3: With stutter removal"
./run.sh --input test_speech.wav --output ./test_output --remove-stutters --format ass
echo ""

# Test 4: Full pipeline
echo "Test 4: Full pipeline (silence + stutter removal)"
./run.sh --input test_speech.wav --output ./test_output --remove-silence --remove-stutters --format json
echo ""

# Test 5: Custom stutter patterns
echo "Test 5: Custom stutter patterns"
./run.sh --input test_speech.wav --output ./test_output --remove-stutters --stutter-patterns "uhm,uh,um,er,ah,hmm" --format srt
echo ""

echo "All tests completed!"
echo ""
echo "Output files can be found in ./test_output/"