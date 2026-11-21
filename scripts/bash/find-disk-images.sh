#!/bin/bash
set -euo pipefail

usage() {
  echo "Usage: $(basename "$0") [-d depth] [--no-spotlight] ROOT_PATH" >&2
  echo "  -d, --depth N        Limit search depth (optional)" >&2
  echo "      --no-spotlight  Skip Spotlight (mdfind) lookup" >&2
}

depth_arg=""
use_spotlight=1

args=("$@")
positional=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    -d|--depth)
      [[ $# -ge 2 ]] || { echo "Missing value for $1" >&2; usage; exit 2; }
      depth_arg="$2"; shift 2 ;;
    --no-spotlight)
      use_spotlight=0; shift ;;
    -h|--help)
      usage; exit 0 ;;
    --)
      shift; while [[ $# -gt 0 ]]; do positional+=("$1"); shift; done; break ;;
    -*)
      echo "Unknown option: $1" >&2; usage; exit 2 ;;
    *)
      positional+=("$1"); shift ;;
  esac
done

[[ ${#positional[@]} -ge 1 ]] || { usage; exit 2; }
root_path="${positional[0]}"

if [[ ! -d "$root_path" ]]; then
  echo "Root path not found or not a directory: $root_path" >&2
  exit 2
fi

# Build find command
find_cmd=(find "$root_path")
if [[ -n "${depth_arg}" ]]; then
  find_cmd+=(-maxdepth "$depth_arg")
fi
find_cmd+=(
  \( -path "$root_path/.Spotlight-V100" -o -path "$root_path/.fseventsd" -o -path "$root_path/.Trashes" -o -path "$root_path/Backups.backupdb" \) -prune -o
  \( -type d -iname "*.sparsebundle" -o -type f \( -iname "*.dmg" -o -iname "*.sparseimage" -o -iname "*.img" -o -iname "*.iso" -o -iname "*.cdr" -o -iname "*.qcow2" -o -iname "*.vdi" -o -iname "*.vmdk" \) \) -print
)

tmpfile_find=$(mktemp)
tmpfile_spot=$(mktemp)
trap 'rm -f "$tmpfile_find" "$tmpfile_spot"' EXIT

"${find_cmd[@]}" >"$tmpfile_find" || true

if [[ "$use_spotlight" -eq 1 ]] && command -v mdfind >/dev/null 2>&1; then
  # Spotlight search for disk images
  mdfind -onlyin "$root_path" 'kMDItemContentTypeTree == "com.apple.disk-image"c' >"$tmpfile_spot" || true
else
  : >"$tmpfile_spot"
fi

echo "Searching for disk images under: $root_path" >&2

results=$(cat "$tmpfile_find" "$tmpfile_spot" | sed '/^$/d' | sort -u)
if [[ -z "${results}" ]]; then
  echo "No disk images found."
  exit 1
fi

echo "$results"

exit 0


