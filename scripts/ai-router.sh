#!/bin/bash
# AI Router - Decide local (Mistral) vs Claude based on task complexity

TASK_TYPE="$1"
PROMPT="$2"

# Task complexity classification
case "$TASK_TYPE" in
    # LOCAL - Simple text processing, summaries, categorization
    "summarize"|"categorize"|"extract"|"simple")
        ENGINE="mistral"
        ;;
    
    # CLAUDE - Complex reasoning, code generation, architecture
    "code"|"debug"|"architecture"|"complex"|"conversation")
        ENGINE="claude"
        ;;
    
    *)
        echo "Unknown task type. Usage: ai-router.sh <summarize|categorize|extract|code|debug|architecture> <prompt>"
        exit 1
        ;;
esac

# Log the routing decision
echo "$(date +%Y-%m-%d\ %H:%M:%S) | $TASK_TYPE | $ENGINE" >> /var/log/clarke-monitor/ai-routing.log

if [ "$ENGINE" == "mistral" ]; then
    # Use local Mistral
    ollama run mistral:7b "$PROMPT"
else
    # Use Claude API (would need implementation)
    echo "ROUTE_TO_CLAUDE: $PROMPT"
fi
