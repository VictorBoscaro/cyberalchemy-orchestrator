#!/usr/bin/env bash
# Renderiza um HTML -> PDF via headless Chrome (Windows).
# Uso: bash render.sh <input.html> <output.pdf>
# O controle de tamanho/margem/quebra de pagina fica NO CSS do HTML (@page).
set -euo pipefail
CHROME="/c/Program Files/Google/Chrome/Application/chrome.exe"
IN="$1"; OUT="$2"
# Chrome resolve caminhos relativos contra o proprio cwd -> resolver TUDO para absoluto (formato Windows).
IN_ABS="$(cd "$(dirname "$IN")" && pwd -W 2>/dev/null || cd "$(dirname "$IN")" && pwd)/$(basename "$IN")"
mkdir -p "$(dirname "$OUT")"
OUT_ABS="$(cd "$(dirname "$OUT")" && pwd -W 2>/dev/null || cd "$(dirname "$OUT")" && pwd)/$(basename "$OUT")"
# --user-data-dir isolado: evita colisao de instancia unica do Chrome em renders concorrentes.
PROFILE="$(mktemp -d)"
"$CHROME" --headless --disable-gpu --no-sandbox \
  --user-data-dir="$PROFILE" \
  --no-pdf-header-footer \
  --print-to-pdf="$OUT_ABS" \
  "file:///$IN_ABS" 2>/dev/null
rm -rf "$PROFILE"
echo "OK -> $OUT"
