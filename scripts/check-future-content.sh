#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

tmp_output="$(mktemp)"
cleanup() {
  rm -f "$tmp_output"
}
trap cleanup EXIT

HUGO_BIN="${HUGO_BIN:-$(command -v hugo || true)}"
if [[ -z "$HUGO_BIN" ]]; then
  printf 'Error: hugo was not found on PATH. Set HUGO_BIN to your Hugo executable when running locally.\n' >&2
  exit 127
fi

"$HUGO_BIN" list future "$@" >"$tmp_output"

future_paths=()
while IFS= read -r line; do
  [[ -n "$line" ]] || continue
  [[ "$line" == path,* ]] && continue

  path="${line%%,*}"
  [[ -n "$path" ]] || continue

  if [[ -f "$path" ]] && head -n 40 "$path" | grep -Eqi '^[[:space:]]*draft[[:space:]]*[:=][[:space:]]*true([[:space:]]|$)'; then
    continue
  fi

  future_paths+=("$path")
done <"$tmp_output"

if ((${#future_paths[@]})); then
  printf 'Error: Hugo found future-dated published content that would be omitted from deploy:\n' >&2
  for path in "${future_paths[@]}"; do
    printf '  - %s\n' "$path" >&2
  done
  printf '\n' >&2
  printf 'Static deploys do not automatically rebuild when midnight arrives.\n' >&2
  printf 'Use today'"'"'s site-local date, mark the content as draft, or publish it in a later deploy.\n' >&2
  exit 1
fi

printf 'No future-dated published content detected.\n'
