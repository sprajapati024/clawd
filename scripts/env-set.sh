#!/bin/bash
# Set environment variables securely
# Usage: env-set.sh KEY VALUE

KEY="$1"
VALUE="$2"

if [ -z "$KEY" ] || [ -z "$VALUE" ]; then
    echo "Usage: env-set.sh KEY VALUE"
    exit 1
fi

ENV_FILE="/root/.clawd-env"

# Remove existing key if present
sed -i "/^export $KEY=/d" "$ENV_FILE"
sed -i "/^$KEY=/d" "$ENV_FILE"

# Add new key
echo "export $KEY=\"$VALUE\"" >> "$ENV_FILE"

echo "✅ Set $KEY in $ENV_FILE"
echo "   Run 'source ~/.clawd-env' to load immediately"
