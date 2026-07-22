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
    '_ga': 'GA1.3.1765036020.1783921242',
    'cf_clearance': 'HQwIeZ.AS7MaosOLHlONXmzkiqUal.b5qak.8P0X_Z0-1784535547-1.2.1.1-oPdlHNW4C0XrGVjAWY9djxZNUrmPrAVBwqz_o7cR73XAAT_UiwRfnQXD6n_EJQV.MNt8QCZ.nAba9BRJR.WCiuCCqpwUyKo0gV7yNsZ2re15VZlKnIwXsuiTQeIPDsqEsvVaOzF5YWtEAt2fVDu0qmpMNqdo8n__nu0dVZSniyYtXUppOglTQqYZ0nB8ZCZfNrYErNEsHrETnRrMRSxGylfEtdVEdRW7XkO7MfUZD2MhhF11b6XvSrm0YPGNPfNLlUuTtWlr72eJ0.LBhmgCM2QPO2EnlAGfS2YlDzEdJenVct0XJmsFQxac1IPEoklYR4tQUZzzPOC1ABiTVsDYNA',
    '_ga_XXTTVXWHDB': 'GS2.3.s1784535547$o4$g1$t1784536228$j60$l0$h0',
    'TS00000000076': '0868f8be6fab28007d52fe9fb43fb2bb92e222ea627b57db9493dae46bd7dfcb04fd37f1f08ea1c713c6de17dc724c6a088fc02d4409d000a500d7cdb67f2f946c80b88724752d9e01db232880b2134456a99ca74a088f9f033faa1567c64a9612009f1bb3aefef6b0c54cba4cbdf5c969610bb8efa330365be0528d91f3cf4be74ec5c4db88cc008d17033b109a1c990e1e14f7ac5ccbdcb0c3664d68fad0197264f2ea6ed382c7e1cadcbddd93cdc3304a3b8e6f80f204d605656a75847ba083e6e965b22418a418186a529825ba3770564f5ebde249f75238d91cbdfedd8896809cb21c1641c04e523316f0dc2fc9eed93d55d80503578e0adeb0f4f3bd40388f45ec29692ea9',
    'TSPD_101_DID': '0868f8be6fab28007d52fe9fb43fb2bb92e222ea627b57db9493dae46bd7dfcb04fd37f1f08ea1c713c6de17dc724c6a088fc02d44063800efb5d98c8c33ab6a75bbca0f0e5a9b40a1c2e5f7c7f05af6323b8e8d78887c8e08c7002a98284abeb78353a4be005cbcee283244975087e3',
    'XSRF-TOKEN': '3b189cbb-3117-405a-a824-f48ca0529c76',
    'db8ca2b43ed851cc93e71fd5fd72bff7': 'f5a9d9c05b9b6dce00d74c156e302bc4',
    'TS011f2d1a': '01266d26d01c53901e04971070414fd78672c7774a93d4dfd9f0e71873c67c578d57bab0c2637799656ef76427fda79de02efdad25',
    'TSPD_101': '0868f8be6fab280097049d904c1928b36d1e1c228a3007c56ed325901aed9df021d54e64cf91900d87fa1f077ebc8530082f285aad051800eda92f83b15506c55ca1732140a3428bba23ce13beb1c95e',
    'JSESSIONID': '0FD39F6D7FFB379D5590D44300BB7CB5',
    'SESSION': 'c419c106-8285-4670-809c-7d9cd32dba86',
    'f5avraaaaaaaaaaaaaaaa_session_': 'FLCBFMFBABBNLEMPDCNIIMKGNFJCFFKGMADEOOFGOOAIDIDNBHIHIKJDEPJGPIGPIHGDDCAPLIBHHDAEKNDAMIDNDAPGJLOBFOBMLFFECBGMMCMLPCHFODGBEPLIELAL',
    'TS5220f739077': '0868f8be6fab2800b76de0747ebd5eb47865b28db63977b774d63c00ad5f06171d8d2d03d753a959059714f0de91f546085d61668b172000cc9ab4981a2cf3207642c13ca8acc91a038e8f1093f27f5700c9caaa2627f143',
    'TS5220f739029': '0868f8be6fab28007af4b6bfbd9689ee6a8ac000baaadb9468cc6046788df7673eb3172f051eab2f450dc4ce6803f7dd',
    'TSf1edb2d2027': '0868f8be6fab20009cafaca48005da2173ed70c2c814ce6ba95a339d029ffac794e6d5a84c6336fb0888ec5533113000bbcf69325c933ae10389c9de118dd8d441e427a75c8fe69f0e8774a0b942ea70e8875c336d32b63ddb31e579ce37fb45',
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
    'x-xsrf-token': '3b189cbb-3117-405a-a824-f48ca0529c76',
    'cookie': '_ga=GA1.3.1765036020.1783921242; cf_clearance=HQwIeZ.AS7MaosOLHlONXmzkiqUal.b5qak.8P0X_Z0-1784535547-1.2.1.1-oPdlHNW4C0XrGVjAWY9djxZNUrmPrAVBwqz_o7cR73XAAT_UiwRfnQXD6n_EJQV.MNt8QCZ.nAba9BRJR.WCiuCCqpwUyKo0gV7yNsZ2re15VZlKnIwXsuiTQeIPDsqEsvVaOzF5YWtEAt2fVDu0qmpMNqdo8n__nu0dVZSniyYtXUppOglTQqYZ0nB8ZCZfNrYErNEsHrETnRrMRSxGylfEtdVEdRW7XkO7MfUZD2MhhF11b6XvSrm0YPGNPfNLlUuTtWlr72eJ0.LBhmgCM2QPO2EnlAGfS2YlDzEdJenVct0XJmsFQxac1IPEoklYR4tQUZzzPOC1ABiTVsDYNA; _ga_XXTTVXWHDB=GS2.3.s1784535547$o4$g1$t1784536228$j60$l0$h0; TS00000000076=0868f8be6fab28007d52fe9fb43fb2bb92e222ea627b57db9493dae46bd7dfcb04fd37f1f08ea1c713c6de17dc724c6a088fc02d4409d000a500d7cdb67f2f946c80b88724752d9e01db232880b2134456a99ca74a088f9f033faa1567c64a9612009f1bb3aefef6b0c54cba4cbdf5c969610bb8efa330365be0528d91f3cf4be74ec5c4db88cc008d17033b109a1c990e1e14f7ac5ccbdcb0c3664d68fad0197264f2ea6ed382c7e1cadcbddd93cdc3304a3b8e6f80f204d605656a75847ba083e6e965b22418a418186a529825ba3770564f5ebde249f75238d91cbdfedd8896809cb21c1641c04e523316f0dc2fc9eed93d55d80503578e0adeb0f4f3bd40388f45ec29692ea9; TSPD_101_DID=0868f8be6fab28007d52fe9fb43fb2bb92e222ea627b57db9493dae46bd7dfcb04fd37f1f08ea1c713c6de17dc724c6a088fc02d44063800efb5d98c8c33ab6a75bbca0f0e5a9b40a1c2e5f7c7f05af6323b8e8d78887c8e08c7002a98284abeb78353a4be005cbcee283244975087e3; XSRF-TOKEN=3b189cbb-3117-405a-a824-f48ca0529c76; db8ca2b43ed851cc93e71fd5fd72bff7=f5a9d9c05b9b6dce00d74c156e302bc4; TS011f2d1a=01266d26d01c53901e04971070414fd78672c7774a93d4dfd9f0e71873c67c578d57bab0c2637799656ef76427fda79de02efdad25; TSPD_101=0868f8be6fab280097049d904c1928b36d1e1c228a3007c56ed325901aed9df021d54e64cf91900d87fa1f077ebc8530082f285aad051800eda92f83b15506c55ca1732140a3428bba23ce13beb1c95e; JSESSIONID=0FD39F6D7FFB379D5590D44300BB7CB5; SESSION=c419c106-8285-4670-809c-7d9cd32dba86; f5avraaaaaaaaaaaaaaaa_session_=FLCBFMFBABBNLEMPDCNIIMKGNFJCFFKGMADEOOFGOOAIDIDNBHIHIKJDEPJGPIGPIHGDDCAPLIBHHDAEKNDAMIDNDAPGJLOBFOBMLFFECBGMMCMLPCHFODGBEPLIELAL; TS5220f739077=0868f8be6fab2800b76de0747ebd5eb47865b28db63977b774d63c00ad5f06171d8d2d03d753a959059714f0de91f546085d61668b172000cc9ab4981a2cf3207642c13ca8acc91a038e8f1093f27f5700c9caaa2627f143; TS5220f739029=0868f8be6fab28007af4b6bfbd9689ee6a8ac000baaadb9468cc6046788df7673eb3172f051eab2f450dc4ce6803f7dd; TSf1edb2d2027=0868f8be6fab20009cafaca48005da2173ed70c2c814ce6ba95a339d029ffac794e6d5a84c6336fb0888ec5533113000bbcf69325c933ae10389c9de118dd8d441e427a75c8fe69f0e8774a0b942ea70e8875c336d32b63ddb31e579ce37fb45',
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