#!/bin/bash

# Nama environment virtual
VENV_DIR="venv"

# Cek apakah python3 sudah terinstall
if ! command -v python3 &> /dev/null; then
    echo "Python3 tidak ditemukan. Install dulu Python3."
    exit 1
fi

# Buat virtual environment kalau belum ada
if [ ! -d "$VENV_DIR" ]; then
    echo "Membuat virtual environment di ./$VENV_DIR ..."
    python3 -m venv "$VENV_DIR"
fi

# Aktifkan virtual environment
source "$VENV_DIR/bin/activate"

echo "Selesai! Virtual environment '$VENV_DIR' aktif dan dependencies sudah terinstall."
echo "Jalankan 'source $VENV_DIR/bin/activate' kalau belum aktif."
