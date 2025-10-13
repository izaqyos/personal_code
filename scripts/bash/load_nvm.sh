#!/bin/bash
# Script to manually load NVM into the current shell session

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"

# Optional: uncomment the line below to automatically use the default LTS version upon loading
# nvm use --lts >/dev/null 2>&1

echo "NVM has been loaded. Current version: $(nvm current)"
