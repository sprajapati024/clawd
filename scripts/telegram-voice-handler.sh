#!/bin/bash
# Clarke's Telegram Voice Message Handler
# Auto-transcribes voice messages using OpenAI Whisper API

AUDIO_FILE="$1"
TRANSCRIPT_FILE="${AUDIO_FILE}.txt"

if [ -z "$AUDIO_FILE" ]; then
    echo "Usage: telegram-voice-handler.sh <audio_file>"
    exit 1
fi

# Use the OpenAI Whisper API skill
/usr/lib/node_modules/clawdbot/skills/openai-whisper-api/scripts/transcribe.sh "$AUDIO_FILE" --out "$TRANSCRIPT_FILE"

if [ $? -eq 0 ] && [ -f "$TRANSCRIPT_FILE" ]; then
    cat "$TRANSCRIPT_FILE"
else
    echo "❌ Transcription failed"
    exit 1
fi
