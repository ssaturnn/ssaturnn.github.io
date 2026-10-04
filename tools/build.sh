#!/usr/bin/env bash
# Собирает QR и PDF-версии CV и визиток.
#   tools/build.sh
# Публичное:  Aleksandr-Turchaninov-CV.pdf (без телефона) — публикуется на сайте.
# Печатное:   print/ (с телефоном, визитки) — в .gitignore, не публикуется.
set -euo pipefail
cd "$(dirname "$0")/.."
CH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
pdf() { "$CH" --headless=new --disable-gpu --no-pdf-header-footer --virtual-time-budget=8000 \
        --run-all-compositor-stages-before-draw --print-to-pdf="$2" "$1" 2>/dev/null; }

.venv/bin/python tools/make_qr.py
pdf "file://$PWD/cv/index.html"            "Aleksandr-Turchaninov-CV.pdf"
# телефон хранится только локально в print/phone.txt и подставляется в печатную версию
PHONE="$(cat print/phone.txt 2>/dev/null || true)"
sed "s|<!--PHONE-->|${PHONE:+<span>$PHONE</span>}|" cv/index.html > print/cv-print.html
pdf "file://$PWD/print/cv-print.html" "print/Aleksandr-Turchaninov-CV-print.pdf"
[ -f print/cards.html ] && pdf "file://$PWD/print/cards.html" "print/cards.pdf"
[ -f print/cards-a4.html ] && pdf "file://$PWD/print/cards-a4.html" "print/cards-a4.pdf"
ls -la *.pdf print/*.pdf
