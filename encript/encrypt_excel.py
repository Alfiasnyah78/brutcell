import msoffcrypto
import io
import os

def encrypt_excel(input_file, output_file, password):
    # Validasi file input
    if not os.path.exists(input_file):
        print(f"[!] File tidak ditemukan: {input_file}")
        return

    try:
        # Buka file asli
        with open(input_file, "rb") as f:
            original = f.read()

        # Buat objek Office baru dari file asli
        office_file = msoffcrypto.OfficeFile(io.BytesIO(original))

        # Enkripsi dengan password baru
        with open(output_file, "wb") as encrypted:
            office_file.encrypt(password=password, outfile=encrypted)

        print(f"[✓] File berhasil dienkripsi sebagai: {output_file}")

    except Exception as e:
        print(f"[!] Terjadi kesalahan: {e}")

def main():
    print("\n📦 Excel Encryptor - Enkripsi File XLSX dengan Password\n")
    input_path = input("📁 Masukkan path file Excel (xlsx): ").strip()
    password = input("🔒 Masukkan password untuk enkripsi: ").strip()
    output_path = input("💾 Nama file output (default: protected.xlsx): ").strip()
    if not output_path:
        output_path = "protected.xlsx"

    encrypt_excel(input_path, output_path, password)

if __name__ == "__main__":
    main()

