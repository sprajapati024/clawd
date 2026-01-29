#!/bin/bash
# Clarke's Finance Transaction Logger
# Usage: finance-log.sh <amount> <category> [description]

AMOUNT="$1"
CATEGORY="$2"
DESCRIPTION="${3:-No description}"

CURRENT_MONTH=$(date +%Y-%m)
TRANSACTIONS_FILE="/root/clawd/finance/transactions/${CURRENT_MONTH}.csv"

# Create transactions file if it doesn't exist
if [ ! -f "$TRANSACTIONS_FILE" ]; then
    echo "date,amount,category,description,logged_by" > "$TRANSACTIONS_FILE"
fi

# Validate inputs
if [ -z "$AMOUNT" ] || [ -z "$CATEGORY" ]; then
    echo "Usage: finance-log.sh <amount> <category> [description]"
    echo ""
    echo "Categories: grocery, eating_out, misc, gas, shopping, gifts, health, entertainment, home, auto, other"
    exit 1
fi

# Remove $ if present
AMOUNT=$(echo "$AMOUNT" | sed 's/\$//g')

# Log transaction
TIMESTAMP=$(date +%Y-%m-%d\ %H:%M:%S)
echo "$TIMESTAMP,$AMOUNT,$CATEGORY,\"$DESCRIPTION\",manual" >> "$TRANSACTIONS_FILE"

echo "✅ Logged: \$$AMOUNT → $CATEGORY ($DESCRIPTION)"
echo "   File: $TRANSACTIONS_FILE"
