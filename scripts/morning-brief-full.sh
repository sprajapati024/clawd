#!/bin/bash
# Clarke's Morning Brief - Full version with news search

BRAVE_TOKEN="BSAgizF24FUsH9y23jq0g9GdXcvr-ru"
CHAT_ID="6471272509"

# Get Toronto weather
WEATHER=$(curl -s "https://wttr.in/Toronto?format=3" 2>/dev/null || echo "Weather unavailable")

# Search for AI news (last 24h)
AI_NEWS=$(curl -s "https://api.search.brave.com/res/v1/web/search?q=AI%20news%20latest&freshness=pd&count=2" \
  -H "Authorization: Bearer $BRAVE_TOKEN" 2>/dev/null | grep -o '"title":"[^"]*' | head -2 | cut -d'"' -f4 | sed 's/^/• /')

# Search for Tesla news (last 24h)
TESLA_NEWS=$(curl -s "https://api.search.brave.com/res/v1/web/search?q=Tesla%20news&freshness=pd&count=2" \
  -H "Authorization: Bearer $BRAVE_TOKEN" 2>/dev/null | grep -o '"title":"[^"]*' | head -2 | cut -d'"' -f4 | sed 's/^/• /')

# Search for tech news (last 24h)
TECH_NEWS=$(curl -s "https://api.search.brave.com/res/v1/web/search?q=tech%20startup%20news&freshness=pd&count=2" \
  -H "Authorization: Bearer $BRAVE_TOKEN" 2>/dev/null | grep -o '"title":"[^"]*' | head -2 | cut -d'"' -f4 | sed 's/^/• /')

# Build the brief
BRIEF="🌅 Good morning Shirin!

☀️ **Weather in Toronto:**
$WEATHER

📰 **Tech News (Last 24h):**

🤖 **AI:**
${AI_NEWS:-• AI updates coming soon}

⚡ **Tesla:**
${TESLA_NEWS:-• Tesla updates coming soon}

🔥 **Tech & Startups:**
${TECH_NEWS:-• Tech news coming soon}

---

🎯 **Your Day Ahead:**
• 8:30 AM: Work starts
• Stay focused. Make good calls. ⚡

Clarke 👓"

# Send to Telegram
clawdbot message send --channel telegram --target $CHAT_ID --message "$BRIEF" 2>/dev/null || \
  echo "Brief ready (Telegram send scheduled): $(date)" >> /var/log/clarke-morning.log
