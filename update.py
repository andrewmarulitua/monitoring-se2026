import os
import pandas as pd

# 1. Definisikan Path dan Nama File
BASE_PATH = "data"
target_file_path = os.path.join(BASE_PATH, "SCRAPING_REKAP_SE2026_ENDE_LATEST.xlsx")
master_file_path = os.path.join(BASE_PATH, "master_data.xlsx")

# 2. Baca kedua file Excel
print("Membaca file data...")
df_target = pd.read_excel(target_file_path)
df_master = pd.read_excel(master_file_path)

# Kolom-kolom yang ingin disalin/dilengkapi (Tetap String karena berupa teks/nama)
columns_to_update = [
    "nmkab", "nmkec", "nmdesa", "nmsls", "nmsubsls", 
    "pengawas", "pencacah", "nama_pcl", "nama_pml"
]

# 3. Antisipasi inkonsistensi tipe data pada regionCode
# Tetap gunakan string untuk regionCode demi keamanan kode 16 digit BPS
df_target['regionCode'] = df_target['regionCode'].astype(str).str.strip()
df_master['regionCode'] = df_master['regionCode'].astype(str).str.strip()

# 4. Filter kolom master data agar hanya mengambil regionCode dan kolom yang dibutuhkan saja
available_master_cols = [col for col in columns_to_update if col in df_master.columns]
df_master_subset = df_master[['regionCode'] + available_master_cols]

# 5. Gabungkan data berdasarkan regionCode (Left Join)
df_merged = pd.merge(df_target, df_master_subset, on='regionCode', how='left', suffixes=('', '_master'))

# 6. Proses Pengisian Data yang Kosong
print("Mengisi data yang kosong...")
for col in available_master_cols:
    master_col_name = f"{col}_master"
    
    if col not in df_target.columns:
        df_merged[col] = df_merged[master_col_name]
    else:
        df_merged[col] = df_merged[col].fillna(df_merged[master_col_name])
    
    df_merged.drop(columns=[master_col_name], inplace=True)

# -------------------------------------------------------------
# TAMBAHAN: Konversi Kolom Hasil Rekapitulasi Menjadi Format "Number"
# -------------------------------------------------------------
print("Mengonversi kolom-kolom numerik ke format Number...")

# Daftarkan semua kolom yang seharusnya berisi angka/rekapan statistiknya
numeric_cols = [
    'total_data', 'APPROVED BY Pengawas', 'SUBMITTED BY Pencacah', 
    'OPEN', 'REJECTED BY Pengawas', 'DRAFT', 'EDITED BY Pengawas', 
    'REVOKED BY Pengawas', 'SUBMITTED RESPONDENT'
]

for col in numeric_cols:
    if col in df_merged.columns:
        # pd.to_numeric akan mengubah text angka menjadi format Number asli. 
        # errors='coerce' mengubah data teks yang rusak/tidak valid menjadi NaN (kosong)
        df_merged[col] = pd.to_numeric(df_merged[col], errors='coerce')
        
        # Opsional: Jika Anda ingin mengubah NaN (kosong) menjadi angka 0, aktifkan baris di bawah ini:
        # df_merged[col] = df_merged[col].fillna(0).astype(int)

# -------------------------------------------------------------

# 7. Simpan kembali hasil update ke file target asli
print("Menyimpan data kembali ke file target...")
df_merged.to_excel(target_file_path, index=False)

print("Selesai! Data berhasil diperbarui dan format angka telah disesuaikan.")