from datetime import datetime
import os
import random
import schedule
import tempfile
import time
from config_se2026 import (
    BASE_PATH,
    LATEST_FILE,
    NAMA_KABUPATEN,
    archive_filename,
)
import pandas as pd
import requests

# ================= SETTINGS =================
URL_DATA = "https://fasih-sm.bps.go.id/app/api/analytic/api/v2/assignment/report-progress-by-responsibility"
base_path = BASE_PATH  # FOLDER UNTUK MENYIMPAN DATA HASIL SCRAPPING
# ==========================================================


# ===================== GANTI COOKIE DI SINI =====================
cookies = {
    'cf_clearance': 'HQwIeZ.AS7MaosOLHlONXmzkiqUal.b5qak.8P0X_Z0-1784535547-1.2.1.1-oPdlHNW4C0XrGVjAWY9djxZNUrmPrAVBwqz_o7cR73XAAT_UiwRfnQXD6n_EJQV.MNt8QCZ.nAba9BRJR.WCiuCCqpwUyKo0gV7yNsZ2re15VZlKnIwXsuiTQeIPDsqEsvVaOzF5YWtEAt2fVDu0qmpMNqdo8n__nu0dVZSniyYtXUppOglTQqYZ0nB8ZCZfNrYErNEsHrETnRrMRSxGylfEtdVEdRW7XkO7MfUZD2MhhF11b6XvSrm0YPGNPfNLlUuTtWlr72eJ0.LBhmgCM2QPO2EnlAGfS2YlDzEdJenVct0XJmsFQxac1IPEoklYR4tQUZzzPOC1ABiTVsDYNA',
    'TS018af012': '0167a1c8611f9bc7f94183445ced71dabcd223b3e7a2a292250bd81a273f628c85a18f42264b8fb5338c67d96e7ac7419e44f5edb566f6d0624851c6c471f29b935df9afbedf5add518187fdb88c0b5c425137ce90',
    'f5avraaaaaaaaaaaaaaaa_session_': 'MHDFICIFPAJCEMEHECIPADBKFGOENAGMGICMOOEBEBBAAMBIPCONEIJCEAGKJOOHAKODPBGOHMNPFIBLFOLAEJAKDKJKFPOJNPNMNCNBDOBDLCMHHGMMPGOEGEOPDMKJ',
    'TS00000000076': '0868f8be6fab28000307bd280dcb47f67c736c0758a53e745a4dccccf5976c244b72d9d2479889f2e3a7ead8a136937008c7a6fe7009d000e91b480472cc5e3827c1394c1d6041192e343e9350cd4b1976a7b3ea48c0323ed808ff9c1cac72884660009d54d24b6d243818e6cb7a5f3ede339dc20cc3888ab80c20824576004fac5eefc9d49d088035b178b6dc56e0ca3d728f96d77ae1668179a6a148358c28e8eaff9d9e26db09ee2d08af6c675186f1f4f0d08b3376fffa9e245d5fde3596e68c11a4c4e5b62cdba2e0cc483b49c22a223e0e2d902226e2882b898de0b309fa130047c118c4491bc33489a0713ab52d4d649cdc05aab164ef0e0993c52cdb63869d3de0c07297',
    'TSPD_101_DID': '0868f8be6fab28000307bd280dcb47f67c736c0758a53e745a4dccccf5976c244b72d9d2479889f2e3a7ead8a136937008c7a6fe70063800b893d3f98bc8eaf7c5c01f6ddab771fbee19ffdb8b97d5fd4d4a4f7f2860afa7039c65d331ed3a6dc519931148215a6d7771b9f329bec3c5',
    'db8ca2b43ed851cc93e71fd5fd72bff7': '2a501f1595b4730c02ec8ab8b8c9e9c6',
    'TS011f2d1a': '01266d26d04a0b06ad7a4cbd6b860f4e646462d0a7fc2a4b75a9bac589edb217fab4d404686554ba5a6a30a2ee6f8904eb1cd3e858',
    'TSPD_101': '0868f8be6fab280071c13e464bbbbc37d5a272fca2a799b13de61b474971ca194289279b38328a84ac23ae8c4e90adfc0877846ac50518005b77a1f221e61b9d5ca1732140a3428bba23ce13beb1c95e',
    'XSRF-TOKEN': 'bdc673ba-83b9-49b6-a237-7779854b5c81',
    'JSESSIONID': '96235E2AA1282B6F85B03FC7226A6A59',
    'SESSION': 'db84eddd-627c-445e-87b9-aae9dd35a82a',
    'TS5220f739077': '0868f8be6fab2800048ff5bbf4497145182fa23eee966072bc51ca0c577ce03e40cc761adc10e1296cf39b3bd369402408062a1677172000689635e3bd19fdee0bd26d96f36815638e5e40f55c79f7e88d19788317ac4975',
    'TS5220f739029': '0868f8be6fab2800565d2423dba09806c8c68458204d5d9356f5825f04c7f9db7f8aa94581727aaac3114afb42cadfd1',
    'TSf1edb2d2027': '0868f8be6fab200031af673654567c3d7da088801e08873c2ed0516c858136862a4704d3231025c80891f680bf11300015a83a8124ac1ec50e0e2d9f431e60a03ca74dfe95a594c6fdc1066691302cd77393af98e99a86f86772bb8beb76ba33',
}

headers = {
    'accept': '*/*',
    'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7,ms;q=0.6',
    'content-type': 'application/json',
    'origin': 'https://fasih-sm.bps.go.id',
    'priority': 'u=1, i',
    'referer': 'https://fasih-sm.bps.go.id/app/surveys/a0429e96-51a5-477b-a415-485f9c153004/fd68e454-ba45-4b85-8205-f3bf777ded24',
    'sec-ch-ua': '"Not;A=Brand";v="8", "Chromium";v="150", "Google Chrome";v="150"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Linux; Android 15; Pixel 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Mobile Safari/537.36',
    'x-xsrf-token': 'bdc673ba-83b9-49b6-a237-7779854b5c81',
    'cookie': 'cf_clearance=HQwIeZ.AS7MaosOLHlONXmzkiqUal.b5qak.8P0X_Z0-1784535547-1.2.1.1-oPdlHNW4C0XrGVjAWY9djxZNUrmPrAVBwqz_o7cR73XAAT_UiwRfnQXD6n_EJQV.MNt8QCZ.nAba9BRJR.WCiuCCqpwUyKo0gV7yNsZ2re15VZlKnIwXsuiTQeIPDsqEsvVaOzF5YWtEAt2fVDu0qmpMNqdo8n__nu0dVZSniyYtXUppOglTQqYZ0nB8ZCZfNrYErNEsHrETnRrMRSxGylfEtdVEdRW7XkO7MfUZD2MhhF11b6XvSrm0YPGNPfNLlUuTtWlr72eJ0.LBhmgCM2QPO2EnlAGfS2YlDzEdJenVct0XJmsFQxac1IPEoklYR4tQUZzzPOC1ABiTVsDYNA; TS018af012=0167a1c8611f9bc7f94183445ced71dabcd223b3e7a2a292250bd81a273f628c85a18f42264b8fb5338c67d96e7ac7419e44f5edb566f6d0624851c6c471f29b935df9afbedf5add518187fdb88c0b5c425137ce90; f5avraaaaaaaaaaaaaaaa_session_=MHDFICIFPAJCEMEHECIPADBKFGOENAGMGICMOOEBEBBAAMBIPCONEIJCEAGKJOOHAKODPBGOHMNPFIBLFOLAEJAKDKJKFPOJNPNMNCNBDOBDLCMHHGMMPGOEGEOPDMKJ; TS00000000076=0868f8be6fab28000307bd280dcb47f67c736c0758a53e745a4dccccf5976c244b72d9d2479889f2e3a7ead8a136937008c7a6fe7009d000e91b480472cc5e3827c1394c1d6041192e343e9350cd4b1976a7b3ea48c0323ed808ff9c1cac72884660009d54d24b6d243818e6cb7a5f3ede339dc20cc3888ab80c20824576004fac5eefc9d49d088035b178b6dc56e0ca3d728f96d77ae1668179a6a148358c28e8eaff9d9e26db09ee2d08af6c675186f1f4f0d08b3376fffa9e245d5fde3596e68c11a4c4e5b62cdba2e0cc483b49c22a223e0e2d902226e2882b898de0b309fa130047c118c4491bc33489a0713ab52d4d649cdc05aab164ef0e0993c52cdb63869d3de0c07297; TSPD_101_DID=0868f8be6fab28000307bd280dcb47f67c736c0758a53e745a4dccccf5976c244b72d9d2479889f2e3a7ead8a136937008c7a6fe70063800b893d3f98bc8eaf7c5c01f6ddab771fbee19ffdb8b97d5fd4d4a4f7f2860afa7039c65d331ed3a6dc519931148215a6d7771b9f329bec3c5; db8ca2b43ed851cc93e71fd5fd72bff7=2a501f1595b4730c02ec8ab8b8c9e9c6; TS011f2d1a=01266d26d04a0b06ad7a4cbd6b860f4e646462d0a7fc2a4b75a9bac589edb217fab4d404686554ba5a6a30a2ee6f8904eb1cd3e858; TSPD_101=0868f8be6fab280071c13e464bbbbc37d5a272fca2a799b13de61b474971ca194289279b38328a84ac23ae8c4e90adfc0877846ac50518005b77a1f221e61b9d5ca1732140a3428bba23ce13beb1c95e; XSRF-TOKEN=bdc673ba-83b9-49b6-a237-7779854b5c81; JSESSIONID=96235E2AA1282B6F85B03FC7226A6A59; SESSION=db84eddd-627c-445e-87b9-aae9dd35a82a; TS5220f739077=0868f8be6fab2800048ff5bbf4497145182fa23eee966072bc51ca0c577ce03e40cc761adc10e1296cf39b3bd369402408062a1677172000689635e3bd19fdee0bd26d96f36815638e5e40f55c79f7e88d19788317ac4975; TS5220f739029=0868f8be6fab2800565d2423dba09806c8c68458204d5d9356f5825f04c7f9db7f8aa94581727aaac3114afb42cadfd1; TSf1edb2d2027=0868f8be6fab200031af673654567c3d7da088801e08873c2ed0516c858136862a4704d3231025c80891f680bf11300015a83a8124ac1ec50e0e2d9f431e60a03ca74dfe95a594c6fdc1066691302cd77393af98e99a86f86772bb8beb76ba33',
}

json_data = {
    "surveyPeriodId": "fd68e454-ba45-4b85-8205-f3bf777ded24",
    "surveyRoleId": "6d7d919a-45e5-4779-bb87-2905b49fd31a",
    "size": 5,
    "page": 0,
    "search": "",
    "target": "TARGET_ONLY",
    "region": {
        "region1Id": None,
        "region2Id": None,
        "region3Id": None,
        "region4Id": None,
        "region5Id": None,
        "region6Id": None,
        "region7Id": None,
        "region8Id": None,
        "region9Id": None,
        "region10Id": None,
    },
    "regionSummaryLevel": 6,
}

# ================================================================

if not os.path.exists(base_path):
    os.makedirs(base_path)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_file = archive_filename(
    timestamp
)  # arsip histori, 1 file per kali scraping


def save_and_merge(new_data):
    """Menerima data hasil scraping, memperbarui & memperkaya datanya dengan master_data,

    lalu menyimpan snapshot ke LATEST_FILE dan merekamnya ke arsip histori.
    """
    if not new_data:
        return

    print("\n-------------------------------------------------------------")
    print("🔄 Memproses dan menyelaraskan data hasil scraping...")

    df_target = pd.DataFrame(new_data)
    df_target["scraped_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Baca file master jika tersedia
    master_file_path = os.path.join(base_path, "master_data.xlsx")
    if os.path.exists(master_file_path):
        df_master = pd.read_excel(master_file_path)

        columns_to_update = [
            "nmkab",
            "nmkec",
            "nmdesa",
            "nmsls",
            "nmsubsls",
            "pengawas",
            "pencacah",
            "nama_pcl",
            "nama_pml",
        ]

        # 1. Antisipasi inkonsistensi tipe data pada regionCode
        df_target["regionCode"] = (
            df_target["regionCode"].astype(str).str.strip()
        )
        df_master["regionCode"] = (
            df_master["regionCode"].astype(str).str.strip()
        )

        # 2. Filter kolom master data agar hanya mengambil regionCode dan kolom yang dibutuhkan
        available_master_cols = [
            col for col in columns_to_update if col in df_master.columns
        ]
        df_master_subset = df_master[
            ["regionCode"] + available_master_cols
        ].drop_duplicates(subset=["regionCode"])

        # 3. Gabungkan data berdasarkan regionCode (Left Join)
        df_merged = pd.merge(
            df_target,
            df_master_subset,
            on="regionCode",
            how="left",
            suffixes=("", "_master"),
        )

        # 4. Pembaruan dan Penyelarasan 'pengawas' & 'nama_pml' serta Wilayah
        strict_overwrite_cols = ["pengawas", "nama_pml"]

        for col in available_master_cols:
            master_col_name = f"{col}_master"

            if master_col_name in df_merged.columns:
                if col not in df_merged.columns:
                    # Jika kolom belum ada di target, langsung pakai dari master
                    df_merged[col] = df_merged[master_col_name]
                else:
                    if col in strict_overwrite_cols:
                        # Gunakan master_data sebagai acuan utama
                        df_merged[col] = df_merged[master_col_name].fillna(
                            df_merged[col]
                        )
                    else:
                        # Untuk kolom wilayah/lainnya, cukup lengkapi jika kosong (fillna)
                        df_merged[col] = df_merged[col].fillna(
                            df_merged[master_col_name]
                        )

                # Hapus kolom bantuan '_master'
                df_merged.drop(columns=[master_col_name], inplace=True)

        # 5. Penyelarasan Kolom Username, Pencacah, dan Nama PCL
        if "username" in df_merged.columns and "pencacah" in df_merged.columns:
            mask_mismatch = (
                df_merged["username"].astype(str).str.strip()
                != df_merged["pencacah"].astype(str).str.strip()
            )
            df_merged.loc[mask_mismatch, "pencacah"] = df_merged.loc[
                mask_mismatch, "username"
            ]

        if "pencacah" in df_master.columns and "nama_pcl" in df_master.columns:
            df_master_clean = df_master.dropna(
                subset=["pencacah", "nama_pcl"]
            ).drop_duplicates(subset=["pencacah"])
            pcl_map = dict(
                zip(
                    df_master_clean["pencacah"].astype(str).str.strip(),
                    df_master_clean["nama_pcl"],
                )
            )

            if "pencacah" in df_merged.columns:
                existing_nama_pcl = df_merged.get(
                    "nama_pcl", pd.Series([None] * len(df_merged))
                )
                df_merged["nama_pcl"] = (
                    df_merged["pencacah"]
                    .astype(str)
                    .str.strip()
                    .map(pcl_map)
                    .fillna(existing_nama_pcl)
                )

        df_final = df_merged
    else:
        print(
            f"⚠️ Warning: File '{master_file_path}' tidak ditemukan."
            " Menggunakan data tanpa enrichment master."
        )
        df_final = df_target

    # 6. Konversi Kolom Hasil Rekapitulasi Menjadi Format Number
    numeric_cols = [
        "total_data",
        "APPROVED BY Pengawas",
        "SUBMITTED BY Pencacah",
        "OPEN",
        "REJECTED BY Pengawas",
        "DRAFT",
        "EDITED BY Pengawas",
        "REVOKED BY Pengawas",
        "SUBMITTED RESPONDENT",
    ]

    for col in numeric_cols:
        if col in df_final.columns:
            df_final[col] = pd.to_numeric(df_final[col], errors="coerce")

    # 7. Simpan Arsip histori (append)
    if os.path.exists(backup_file):
        try:
            df_old = pd.read_excel(backup_file)
            df_archive = pd.concat([df_old, df_final], ignore_index=True)
        except Exception:
            df_archive = df_final
    else:
        df_archive = df_final

    df_archive.to_excel(backup_file, index=False)

    # 8. Simpan File LATEST dengan aman (Atomic Write)
    _atomic_write_excel(df_final, LATEST_FILE)
    print(f"💾 Snapshot terbaru dan terolah berhasil disimpan ke: {LATEST_FILE}")
    print("-------------------------------------------------------------\n")


def _atomic_write_excel(df, path):
    """Tulis Excel dengan aman: tulis ke file sementara dulu, baru rename.

    Mencegah dashboard membaca file yang setengah jadi/korup saat scraping
    sedang menulis.
    """
    folder = os.path.dirname(path) or "."
    fd, tmp_path = tempfile.mkstemp(suffix=".xlsx", dir=folder)
    os.close(fd)
    try:
        df.to_excel(tmp_path, index=False)
        os.replace(tmp_path, path)  # atomic di OS yang sama (Windows/Linux)
    except Exception:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise


def auto_push_github():
    import subprocess

    try:
        # 1. Add semua perubahan di folder data/
        subprocess.run(["git", "add", "data/"], check=True)

        # 2. Cek apakah ada perubahan
        status = subprocess.run(
            ["git", "status", "--porcelain"], capture_output=True, text=True
        )

        if not status.stdout.strip():
            print("📌 Tidak ada perubahan untuk dipush ke GitHub.")
            return

        # 3. Commit dengan pesan "update" saja
        subprocess.run(
            ["git", "commit", "-m", "update"],  # <-- Diubah di sini
            check=True,
        )

        # 4. Sinkronisasi (pull) terlebih dahulu
        subprocess.run(
            ["git", "pull", "--rebase", "origin", "main"], check=True
        )

        # 5. Push ke GitHub
        subprocess.run(["git", "push", "origin", "main"], check=True)

        print("✅ Data berhasil dipush ke GitHub dengan pesan commit 'update'")

    except Exception as e:
        print(f"❌ Error push GitHub: {e}")


def fetch_data():
    all_rows = []
    page = 0
    size = 10

    while True:
        json_data["page"] = page
        json_data["size"] = size

        response = requests.post(
            URL_DATA,
            cookies=cookies,
            headers=headers,
            json=json_data,
        )

        if response.status_code != 200:
            print(f"❌ Error di page {page}")
            print(f"Status Code: {response.status_code}")
            print(response.text[:1000])
            break

        json_res = response.json()
        data_block = json_res.get("data", {})
        data = data_block.get("content", [])
        is_last = data_block.get("last", True)

        print(f"📄 Page {page} | jumlah data: {len(data)} | last: {is_last}")

        # 🔽 Flattening Data JSON
        for user in data:
            for region in user.get("regionSummary", []):
                row = {
                    "userId": user.get("userId"),
                    "username": user.get("username"),
                    "email": user.get("email"),
                    "role": user.get("roleName"),
                    "regionCode": region.get("regionCode"),
                    "total_data": region.get("total"),
                }

                for status in region.get("statusBreakdown", []):
                    row[status.get("status")] = status.get("count")

                all_rows.append(row)

        if is_last:
            print("✅ Sudah sampai halaman terakhir")
            break

        page += 1
        time.sleep(random.uniform(1, 3))  # delay acak 1-3 detik antar request

    if all_rows:
        save_and_merge(all_rows)

    print("🎉 Semua data berhasil diproses dan disimpan!")


def job():
    print(
        f"\n[+] Memulai proses scraping pada"
        f" {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    fetch_data()
    auto_push_github()


if __name__ == "__main__":
    schedule.every(4).hours.do(job)

    print(
        "⏱️  Script berjalan otomatis setiap 4 jam. Tekan Ctrl+C untuk"
        " menghentikan."
    )

    # Jalankan fungsi satu kali saat script pertama kali dibuka
    job()

    # Loop agar script terus berjalan mengecek jadwal
    while True:
        schedule.run_pending()
        time.sleep(1)