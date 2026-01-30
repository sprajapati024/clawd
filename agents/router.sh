#!/bin/bash
# Agent Router - Routes requests to specialist agents

AGENT=$1
shift
TASK="$@"

case "$AGENT" in
  ledger|finance)
    echo "→ Routing to Ledger (Finance Agent)"
    echo "Task: $TASK"
    echo "Playbook: /root/clawd/agents/ledger/"
    ;;
  atlas|pm|project)
    echo "→ Routing to Atlas (PM Agent)"
    echo "Task: $TASK"
    echo "Playbook: /root/clawd/agents/atlas/"
    ;;
  forge|dev|developer)
    echo "→ Routing to Forge (Developer Agent)"
    echo "Task: $TASK"
    echo "Playbook: /root/clawd/agents/forge/"
    ;;
  *)
    echo "Unknown agent: $AGENT"
    echo "Available: ledger, atlas, forge"
    exit 1
    ;;
esac
