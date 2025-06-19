import openpyxl
import msoffcrypto
import getpass
import os

def create_plain_xlsx(content, filename):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws['A1'] = content
    wb.save(filename)
    print(f"[✓] File Excel (xlsx) dibuat: {filename}")

def encrypt_xlsx_file(input_file, output_file, password):
    with open(input_file, 'rb') as f:
        office_file = msoffcrypto.OfficeFile(f)
        with open(output_file, 'wb') as encrypted:
            office_file.encrypt(password=password, outfile=encrypted)
    print(f"[✓] File Excel terenkripsi: {output_file}")

def main():
    print("\n📦 Excel Encryptor (XLSX format) - For Brute Test")

    content = input("📝 Masukkan isi sel A1: ")
    password = getpass.getpass("🔒 Masukkan password: ")
    filename = input("💾 Nama file output (tanpa ekstensi) [default: rahasia]: ").strip() or "rahasia"

    plain_file = f"{filename}_plain.xlsx"
    encrypted_file = f"{filename}.xlsx"

    create_plain_xlsx(content, plain_file)
    encrypt_xlsx_file(plain_file, encrypted_file, password)

    os.remove(plain_file)
    print("✅ Selesai! File terenkripsi siap untuk brute-force 🔓")

if __name__ == "__main__":
    main()

