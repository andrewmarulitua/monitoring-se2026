import pandas as pd
import requests
import os
import random
import tempfile
from datetime import datetime
import schedule
import time
from config_se2026 import NAMA_KABUPATEN, BASE_PATH, LATEST_FILE, archive_filename

# ================= SETTINGS =================
URL_DATA = 'https://fasih-sm.bps.go.id/app/api/analytic/api/v2/assignment/report-progress-by-responsibility' 
base_path = BASE_PATH                #FOLDER UNTUK MENYIMPAN DATA HASIL SCRAPPING
# ==========================================================


# ===================== GANTI COOKIE DI SINI =====================
cookies = {
    'f5avraaaaaaaaaaaaaaaa_session_': 'EAGNHLCHBGEKAAICNIIKNEMGCFLHKAJFIPGAGLGPGJADIFJEJNCGLAJEDMNECNICKBKDJKU65INNXNQYFK5WO5KI4UKDJV7XVVUJ36UCVRCQLGYW7ST7IFNM6ZWHASIM',
    'db8ca2b43ed851cc93e71fd5fd72bff7': '5be6cc123022eb8185a338c36f04c64c',
    'XSRF-TOKEN': 'ef22c573-6fec-48cc-afd4-be843044a656',
    'SESSION': '6658acf8-a026-470c-8501-5afeeeb46fce',
    'TS00000000076': '0868f8be6fab2800326ae3004626dcf0002d35cca868bfeee1647a69034a1babb1c08834e87de94f023332d881054e1a08ffff365809d0009645781cbfdc7e83773ef8429abfcf46ba4c02a487279cb09dc5e0f133e9b7cf301ba2ab54264404940680f7d237db4bea1cb230a49f82abf5c98789932cc544129036724eeffcb52f4552755b19c1d67f2efaafd4a8816cff0fb979bcb49e8a2755bd50682ef2f05d4dc808440a0f6a46238f037a58e217a07c70c272553313642457e5cfe00cab87e203de940e18ff3d7ea291e873cb6533889cd179889bb28cf42b1a2fcca81cb8ffb76e57af4c85e57018e7beb98551719db81eb8f3c51b3441f0e49fd1efc3ff5bc5d2d3f5dd2a',
    'TSPD_101_DID': '0868f8be6fab2800326ae3004626dcf0002d35cca868bfeee1647a69034a1babb1c08834e87de94f023332d881054e1a08ffff3658063800a13cca4b796d6181af674eb27eaa9c111a52495b5dbc9d88478d62f108fc91b292234c24cded4f6721dc51fbd1269edee9f006a047c36efa',
    'TS011f2d1a': '01266d26d017030d2448d09c828632c53dff5f0c7f602331370197c3d7129885e8e729e1e9477b6471f5390f1b1318425245245e98',
    'TSPD_101': '0868f8be6fab28003fd43d2d0091aa885e310010b40d8abfb1a06de47b507fec008cb738588cf7f8c9771b03a6e88b7808834d803c051800472caca9de57bfdf5ca1732140a3428bba23ce13beb1c95e',
    'TS5220f739077': '0868f8be6fab28000d00e740628b869fb7f76609416fc2a6b79c8d5b157b678cb981b9ef69e8380460c50999abb85122081355d235172000e41e0aa55df486302ba4DcJHrrHSgvFpsYxqb6g97uaQTd2kE31rPUeDZTeDsjVq',
    'TS5220f739029': '0868f8be6fab2800579d7a64d675d8a73bc4e07a2935a00a92e97535841fb19dd6f9e611e01b628f93b2c505d2c38047',
    'TSf1edb2d2027': '0868f8be6fab2000e4a6efab1f38dbd854d340f34f23e8dafd03b0a45ec3a512534d7b107aec746b08cc3e4e63113000f197d416fefbc7e8d34389abad079c5f3cbe48e00f5a84f2fba220f108a1c68a6f62afadc807587d682371c389ccb49c',
}

headers = {
    'accept': '*/*',
    'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7,ms;q=0.6',
    'content-type': 'application/json',
    'origin': 'https://fasih-sm.bps.go.id',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Not;A=Brand";v="8", "Chromium";v="150", "Google Chrome";v="150"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Linux; Android 15; Pixel 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Mobile Safari/537.36',
    'x-xsrf-token': 'ef22c573-6fec-48cc-afd4-be843044a656',
    'cookie': 'f5avraaaaaaaaaaaaaaaa_session_=EAGNHLCHBGEKAAICNIIKNEMGCFLHKAJFIPGAGLGPGJADIFJEJNCGLAJEDMNECNICKBKDJKU65INNXNQYFK5WO5KI4UKDJV7XVVUJ36UCVRCQLGYW7ST7IFNM6ZWHASIM; db8ca2b43ed851cc93e71fd5fd72bff7=5be6cc123022eb8185a338c36f04c64c; XSRF-TOKEN=ef22c573-6fec-48cc-afd4-be843044a656; SESSION=6658acf8-a026-470c-8501-5afeeeb46fce; TS00000000076=0868f8be6fab2800326ae3004626dcf0002d35cca868bfeee1647a69034a1babb1c08834e87de94f023332d881054e1a08ffff365809d0009645781cbfdc7e83773ef8429abfcf46ba4c02a487279cb09dc5e0f133e9b7cf301ba2ab54264404940680f7d237db4bea1cb230a49f82abf5c98789932cc544129036724eeffcb52f4552755b19c1d67f2efaafd4a8816cff0fb979bcb49e8a2755bd50682ef2f05d4dc808440a0f6a46238f037a58e217a07c70c272553313642457e5cfe00cab87e203de940e18ff3d7ea291e873cb6533889cd179889bb28cf42b1a2fcca81cb8ffb76e57af4c85e57018e7beb98551719db81eb8f3c51b3441f0e49fd1efc3ff5bc5d2d3f5dd2a; TSPD_101_DID=0868f8be6fab2800326ae3004626dcf0002d35cca868bfeee1647a69034a1babb1c08834e87de94f023332d881054e1a08ffff3658063800a13cca4b796d6181af674eb27eaa9c111a52495b5dbc9d88478d62f108fc91b292234c24cded4f6721dc51fbd1269edee9f006a047c36efa; TS011f2d1a=01266d26d017030d2448d09c828632c53dff5f0c7f602331370197c3d7129885e8e729e1e9477b6471f5390f1b1318425245245e98; TSPD_101=0868f8be6fab28003fd43d2d0091aa885e310010b40d8abfb1a06de47b507fec008cb738588cf7f8c9771b03a6e88b7808834d803c051800472caca9de57bfdf5ca1732140a3428bba23ce13beb1c95e; TS5220f739077=0868f8be6fab28000d00e740628b869fb7f76609416fc2a6b79c8d5b157b678cb981b9ef69e8380460c50999abb85122081355d235172000e41e0aa55df486302ba4DcJHrrHSgvFpsYxqb6g97uaQTd2kE31rPUeDZTeDsjVq; TS5220f739029=0868f8be6fab2800579d7a64d675d8a73bc4e07a2935a00a92e97535841fb19dd6f9e611e01b628f93b2c505d2c38047; TSf1edb2d2027=0868f8be6fab2000e4a6efab1f38dbd854d340f34f23e8dafd03b0a45ec3a512534d7b107aec746b08cc3e4e63113000f197d416fefbc7e8d34389abad079c5f3cbe48e00f5a84f2fba220f108a1c68a6f62afadc807587d682371c389ccb49c',
}

json_data = {
    'surveyPeriodId': 'fd68e454-ba45-4b85-8205-f3bf777ded24',
    'surveyRoleId': '6d7d919a-45e5-4779-bb87-2905b49fd31a',
    'size': 5,
    'page': 0,
    'search': '',
    'target': 'TARGET_ONLY',
    'region': {
        'region1Id': None,
        'region2Id': None,
        'region3Id': None,
        'region4Id': None,
        'region5Id': None,
        'region6Id': None,
        'region7Id': None,
        'region8Id': None,
        'region9Id': None,
        'region10Id': None,
    },
    'regionSummaryLevel': 6,
}

# ================================================================

if not os.path.exists(base_path):
    os.makedirs(base_path)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_file = archive_filename(timestamp)  # arsip histori, 1 file per kali scraping


def save_and_merge(new_data):
    """Simpan ke file arsip (histori, append) DAN ke file LATEST (overwrite, untuk dashboard)"""
    if not new_data:
        return

    df_new = pd.DataFrame(new_data)
    df_new["scraped_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    master = pd.read_excel("data/master_data.xlsx")

    master["pencacah"] = (
        master["pencacah"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    df_new["email"] = (
        df_new["email"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    master["regionCode"] = master["regionCode"].astype(str)
    df_new["regionCode"] = df_new["regionCode"].astype(str)

    df_new = df_new.merge(
        master[
            [
                "regionCode",
                "nmkab",
                "nmkec",
                "nmdesa",
                "nmsls",
                "nmsubsls",
                "pengawas",
                "pencacah",
                "nama_pcl",
                "nama_pml"
            ]
        ],
        left_on=["email", "regionCode"],
        right_on=["pencacah", "regionCode"],
        how="left"
    )

    # 1) Arsip histori - tetap ditambah (append), supaya bisa lihat tren dari waktu ke waktu
    if os.path.exists(backup_file):
        df_old = pd.read_excel(backup_file)
        df_archive = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df_archive = df_new
    df_archive.to_excel(backup_file, index=False)

    # 2) File LATEST - SELALU ditimpa dengan snapshot terbaru saja (dibaca dashboard)
    _atomic_write_excel(df_new, LATEST_FILE)
    print(f"💾 Snapshot terbaru disimpan ke: {LATEST_FILE}")


def _atomic_write_excel(df, path):
    """Tulis Excel dengan aman: tulis ke file sementara dulu, baru rename.
    Mencegah dashboard membaca file yang setengah jadi/korup saat scraping sedang menulis."""
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
        subprocess.run(
            ["git", "add", "data/"],
            check=True
        )

        status = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True
        )

        if not status.stdout.strip():
            print("📌 Tidak ada perubahan")
            return

        subprocess.run(
            ["git", "commit", "-m", "Update hasil scraping"],
            check=True
        )

        # sinkron dulu dengan GitHub
        subprocess.run(
            ["git", "pull", "--rebase", "origin", "main"],
            check=True
        )

        subprocess.run(
            ["git", "push", "origin", "main"],
            check=True
        )

        print("✅ Data berhasil dipush ke GitHub")

    except Exception as e:
        print(f"❌ Error push GitHub: {e}")
 
 
def fetch_data():
    all_rows = []
    page = 0
    size = 10

    while True:
        json_data['page'] = page
        json_data['size'] = size

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

        # 🔽 Flatten
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

    print("🎉 Semua data berhasil disimpan!")


def job():
    print(f"\n[+] Memulai proses scraping pada {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    fetch_data()
    auto_push_github()

if __name__ == "__main__":
    
    schedule.every(4).hours.do(job)

    print("⏱️  Script berjalan otomatis setiap 4 jam. Tekan Ctrl+C untuk menghentikan.")

    # Jalankan fungsi satu kali saat script pertama kali dibuka (opsional)
    job()

    # Loop agar script terus berjalan mengecek jadwal
    while True:
        schedule.run_pending()
        time.sleep(1)