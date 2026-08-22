#!/usr/bin/env bash
# Install the audit script as a git pre-commit hook for e36-wiring.
# Run once from anywhere inside the repo:
#   bash scripts/install-hooks.sh

set -euo pipefail

REPO_ROOT="$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"
HOOK="$REPO_ROOT/.git/hooks/pre-commit"

cat > "$HOOK" <<'EOF'
#!/usr/bin/env bash
# Auto-installed by scripts/install-hooks.sh — do not edit manually.
set -euo pipefail
REPO_ROOT="$(git rev-parse --show-toplevel)"
exec python3 "$REPO_ROOT/scripts/audit.py" --staged
EOF

chmod +x "$HOOK"
echo "✓ pre-commit hook installed at $HOOK"
echo "  Test it now: python3 scripts/audit.py"
