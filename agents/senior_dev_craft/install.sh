#!/usr/bin/env bash
# Install the craft skills into Claude Code (~/.claude/skills) as symlinks to this repo.
#   ./install.sh            install / refresh (idempotent)
#   ./install.sh --copy     copy instead of symlink (if your setup doesn't follow symlinks)
#   ./install.sh --remove   remove the craft skills this script installed
set -euo pipefail

SUITE="$(cd "$(dirname "$0")" && pwd)"
DEST="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
MODE="${1:-link}"
mkdir -p "$DEST"

for skill in "$SUITE"/skills/*/; do
  name="$(basename "$skill")"
  target="$DEST/$name"
  case "$MODE" in
    --remove)
      if [ -L "$target" ] || [ -f "$target/.craft-installed" ]; then rm -rf "$target"; echo "removed  $name"; fi
      continue ;;
  esac
  if [ -e "$target" ] && [ ! -L "$target" ] && [ ! -f "$target/.craft-installed" ]; then
    echo "skip     $name (exists and is not ours: $target)"; continue
  fi
  rm -rf "$target"
  if [ "$MODE" = "--copy" ]; then
    cp -R "$skill" "$target" && touch "$target/.craft-installed"; echo "copied   $name"
  else
    ln -s "${skill%/}" "$target"; echo "linked   $name -> ${skill%/}"
  fi
done
