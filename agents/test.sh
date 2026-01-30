#!/bin/bash
# Test multi-agent system

echo "🧪 Testing Multi-Agent System"
echo "=============================="
echo

# Test 1: File structure
echo "✓ Checking file structure..."
for agent in ledger atlas forge; do
  if [ -d "/root/clawd/agents/$agent" ]; then
    echo "  ✓ $agent directory exists"
    for file in ROLE.md KNOWLEDGE.md EXAMPLES.md config.json; do
      if [ -f "/root/clawd/agents/$agent/$file" ]; then
        echo "    ✓ $file"
      else
        echo "    ✗ $file MISSING"
      fi
    done
  else
    echo "  ✗ $agent directory MISSING"
  fi
done
echo

# Test 2: Todoist integration
echo "✓ Checking Todoist CLI..."
if command -v todoist &> /dev/null; then
  echo "  ✓ todoist CLI installed"
  if todoist today &> /dev/null; then
    echo "  ✓ todoist authenticated"
    echo "    $(todoist today | wc -l) tasks today"
  else
    echo "  ✗ todoist not authenticated"
  fi
else
  echo "  ✗ todoist CLI not found"
fi
echo

# Test 3: Router
echo "✓ Checking router..."
if [ -x "/root/clawd/agents/router.sh" ]; then
  echo "  ✓ router.sh executable"
else
  echo "  ✗ router.sh not executable"
fi
echo

echo "=============================="
echo "✅ System Check Complete"
