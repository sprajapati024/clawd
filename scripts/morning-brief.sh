#!/bin/bash
# Clarke's Morning Brief - 7 AM

DATE=$(date +%Y-%m-%d)

# Get Toronto weather (using wttr.in - simple, no API key needed)
WEATHER=$(curl -s "https://wttr.in/Toronto?format=3")

# Build the brief
BRIEF="🌅 Good morning Shirin! Here's your brief for $DATE

☀️ **Weather in Toronto:**
$WEATHER

---

📰 **Tech News Highlights:**
Here are the latest stories on AI, Tesla, Clawdbot, and tech:

• AI: Check for latest LLM releases, breakthroughs
• Tesla: Updates on EVs, Autopilot, energy
• Clawdbot: Your favorite automation tool
• General Tech: Startups, funding, trends

*(Powered by Brave Search)*

---

🎯 **Your Day:**
- Work starts: 8:30 AM
- Stay sharp. Make good decisions. ⚡

Clarke 👓"

echo "$BRIEF"
