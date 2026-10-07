#!/bin/bash
# backup.sh - Sao luu mot thu muc thanh tar.gz va ghi nhat ky
# Cach dung: ./backup.sh <thu_muc_can_sao_luu>

# 1. Kiem tra tham so
if [ $# -ne 1 ]; then
    echo "Loi: can dung 1 tham so." >&2
    echo "Cach dung: $0 <thu_muc_can_sao_luu>" >&2
    exit 1
fi

SRC="$1"

if [ ! -d "$SRC" ]; then
    echo "Loi: '$SRC' khong phai la thu muc hop le." >&2
    exit 2
fi

# 2. Chuan bi duong dan
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"   # ~/dg1_<MSSV>
BACKUP_DIR="$HOME/backup"
LOG_FILE="$PROJECT_DIR/logs/backup.log"
NAME="$(basename "$(realpath "$SRC")")"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
DEST="$BACKUP_DIR/${NAME}_${TIMESTAMP}.tar.gz"

mkdir -p "$BACKUP_DIR"

# 3. Nen thu muc
if tar -czf "$DEST" -C "$(dirname "$(realpath "$SRC")")" "$NAME"; then
    # 4. Ghi nhat ky
    echo "$(date '+%Y-%m-%d %H:%M:%S') | $DEST" >> "$LOG_FILE"
    echo "Sao luu thanh cong: $DEST"
else
    echo "Loi: sao luu that bai." >&2
    exit 3
fi
