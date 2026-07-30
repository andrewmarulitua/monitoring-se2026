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
    'cf_clearance': 'HQwIeZ.AS7MaosOLHlONXmzkiqUal.b5qak.8P0X_Z0-1784535547-1.2.1.1-oPdlHNW4C0XrGVjAWY9djxZNUrmPrAVBwqz_o7cR73XAAT_UiwRfnQXD6n_EJQV.MNt8QCZ.nAba9BRJR.WCiuCCqpwUyKo0gV7yNsZ2re15VZlKnIwXsuiTQeIPDsqEsvVaOzF5YWtEAt2fVDu0qmpMNqdo8n__nu0dVZSniyYtXUppOglTQqYZ0nB8ZCZfNrYErNEsHrETnRrMRSxGylfEtdVEdRW7XkO7MfUZD2MhhF11b6XvSrm0YPGNPfNLlUuTtWlr72eJ0.LBhmgCM2QPO2EnlAGfS2YlDzEdJenVct0XJmsFQxac1IPEoklYR4tQUZzzPOC1ABiTVsDYNA',
    '_ga_XXTTVXWHDB': 'GS2.3.s1785131298$o7$g1$t1785132563$j60$l0$h0',
    '_ga': 'GA1.1.2055404639.1784774377',
    '_ga_QPPE1C18C5': 'GS2.1.s1785135144$o3$g1$t1785135282$j60$l0$h0',
    'TS0151fc2b': '0167a1c861160105ce471105f2fea8659474fd052e179e18e7dcdf969b7222406cbdbb413836b91ed4a4bc946f3977c75270b45e76',
    'TS00000000076': '0868f8be6fab2800fec71b11a56cf701c9e2b2c5e2316646ea2a01c2116900dcdec70945cf052edbf9f9da16238c9817083ffa844909d000e9f8cff614bbc236991882ff4d9d6b639d1a5fe0d20329aa18ffec059eaba00c85ed585971e9e04f1d785ebe2e1d52b17650a8d8ff65fba1e3e5d3eaaf7a87daa66a10caf63672b17ed415dec230f91cea35a42f2dec374147c48b9fc17960ee23775eb7c454a09f28f267efc914317fc8122a7f83f49a227b0859c788704d0c7dd64c8eac12de5057ff56cadd5df6d1457f1420c49e7fc2140d389b86063cce6642859e714c43f061feecf54256749078b540e0b6154ef44b55c2078b1f360aa052634c55443793ac06fe8a9ccb2621',
    'TSPD_101_DID': '0868f8be6fab2800fec71b11a56cf701c9e2b2c5e2316646ea2a01c2116900dcdec70945cf052edbf9f9da16238c9817083ffa84490638007bc8ef3a1c79321de7202a9399c277a45da111fa4d30e9bcf9f80eef667ec1bf61106380d77eeb5dade5e7fd27d81417c41de3be88903f62',
    'XSRF-TOKEN': '29cf260d-55f7-43d4-ab2f-5083a77334ad',
    'db8ca2b43ed851cc93e71fd5fd72bff7': 'de793f984ed2c9eb501928c09f67f37a',
    'TS011f2d1a': '01266d26d07219411b70c407de0b1351f338d5699336150befaa3f831574d3437eaa427dedce5b7049ae69f9b16c9fa13ee0a4198a',
    'TSPD_101': '0868f8be6fab280041ae9fa1c91bb9eddff3fcdeab48a9c4c08c6a552e4b5ed81e83255dfc700befdc024a2e794a2bc70801d5e7ce051800c857193aa54eb7185ca1732140a3428bba23ce13beb1c95e',
    'f5avraaaaaaaaaaaaaaaa_session_': 'MICCONNALIENFBMHGOFHIKHKMBPLHAMHCDCCBEGOBLIONDGBAKNHJDCENGEDABFACHGDEDMGAJDCEFMONFIAELMECMNIEBFMKODHBJILPPBKHELFEHOFJDFCGFIBGKBG',
    'JSESSIONID': 'B702280C5246F41D8288AC89CFD241B3',
    'SESSION': '4484c046-2867-4a36-87ae-d749f8f52249',
    'TS5220f739077': '0868f8be6fab28003cf6a9d43bfaff4f38fb543b6ac95938b8ff1a13569ce6e37d783c9888e212d17870c796d2e9c72c084b540908172000754e02c6802d33aed3e4dda2d750ac6d3319cb276183ee041180f15164739d3c',
    'TS5220f739029': '0868f8be6fab28001fabb1ef3d35b7ac62ff2b78e60aac4bc281df39224a70838d116a3f846a84f3584db32a0a30b054',
    'TSf1edb2d2027': '0868f8be6fab2000a6467878a744a2ed0e721bf6949ed704cc6f92d4e7dcf245181a7e3dcabf7c9e0822b7cb431130000dd7927bd485cd3b180edaad0c6da2dd02188874c2952ebe0bb40300b8648912d67b5f8f185fc9943dc50933bbb813e4',
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
    'x-xsrf-token': '29cf260d-55f7-43d4-ab2f-5083a77334ad',
    'cookie': 'cf_clearance=HQwIeZ.AS7MaosOLHlONXmzkiqUal.b5qak.8P0X_Z0-1784535547-1.2.1.1-oPdlHNW4C0XrGVjAWY9djxZNUrmPrAVBwqz_o7cR73XAAT_UiwRfnQXD6n_EJQV.MNt8QCZ.nAba9BRJR.WCiuCCqpwUyKo0gV7yNsZ2re15VZlKnIwXsuiTQeIPDsqEsvVaOzF5YWtEAt2fVDu0qmpMNqdo8n__nu0dVZSniyYtXUppOglTQqYZ0nB8ZCZfNrYErNEsHrETnRrMRSxGylfEtdVEdRW7XkO7MfUZD2MhhF11b6XvSrm0YPGNPfNLlUuTtWlr72eJ0.LBhmgCM2QPO2EnlAGfS2YlDzEdJenVct0XJmsFQxac1IPEoklYR4tQUZzzPOC1ABiTVsDYNA; _ga_XXTTVXWHDB=GS2.3.s1785131298$o7$g1$t1785132563$j60$l0$h0; _ga=GA1.1.2055404639.1784774377; _ga_QPPE1C18C5=GS2.1.s1785135144$o3$g1$t1785135282$j60$l0$h0; TS0151fc2b=0167a1c861160105ce471105f2fea8659474fd052e179e18e7dcdf969b7222406cbdbb413836b91ed4a4bc946f3977c75270b45e76; TS00000000076=0868f8be6fab2800fec71b11a56cf701c9e2b2c5e2316646ea2a01c2116900dcdec70945cf052edbf9f9da16238c9817083ffa844909d000e9f8cff614bbc236991882ff4d9d6b639d1a5fe0d20329aa18ffec059eaba00c85ed585971e9e04f1d785ebe2e1d52b17650a8d8ff65fba1e3e5d3eaaf7a87daa66a10caf63672b17ed415dec230f91cea35a42f2dec374147c48b9fc17960ee23775eb7c454a09f28f267efc914317fc8122a7f83f49a227b0859c788704d0c7dd64c8eac12de5057ff56cadd5df6d1457f1420c49e7fc2140d389b86063cce6642859e714c43f061feecf54256749078b540e0b6154ef44b55c2078b1f360aa052634c55443793ac06fe8a9ccb2621; TSPD_101_DID=0868f8be6fab2800fec71b11a56cf701c9e2b2c5e2316646ea2a01c2116900dcdec70945cf052edbf9f9da16238c9817083ffa84490638007bc8ef3a1c79321de7202a9399c277a45da111fa4d30e9bcf9f80eef667ec1bf61106380d77eeb5dade5e7fd27d81417c41de3be88903f62; XSRF-TOKEN=29cf260d-55f7-43d4-ab2f-5083a77334ad; db8ca2b43ed851cc93e71fd5fd72bff7=de793f984ed2c9eb501928c09f67f37a; TS011f2d1a=01266d26d07219411b70c407de0b1351f338d5699336150befaa3f831574d3437eaa427dedce5b7049ae69f9b16c9fa13ee0a4198a; TSPD_101=0868f8be6fab280041ae9fa1c91bb9eddff3fcdeab48a9c4c08c6a552e4b5ed81e83255dfc700befdc024a2e794a2bc70801d5e7ce051800c857193aa54eb7185ca1732140a3428bba23ce13beb1c95e; f5avraaaaaaaaaaaaaaaa_session_=MICCONNALIENFBMHGOFHIKHKMBPLHAMHCDCCBEGOBLIONDGBAKNHJDCENGEDABFACHGDEDMGAJDCEFMONFIAELMECMNIEBFMKODHBJILPPBKHELFEHOFJDFCGFIBGKBG; JSESSIONID=B702280C5246F41D8288AC89CFD241B3; SESSION=4484c046-2867-4a36-87ae-d749f8f52249; TS5220f739077=0868f8be6fab28003cf6a9d43bfaff4f38fb543b6ac95938b8ff1a13569ce6e37d783c9888e212d17870c796d2e9c72c084b540908172000754e02c6802d33aed3e4dda2d750ac6d3319cb276183ee041180f15164739d3c; TS5220f739029=0868f8be6fab28001fabb1ef3d35b7ac62ff2b78e60aac4bc281df39224a70838d116a3f846a84f3584db32a0a30b054; TSf1edb2d2027=0868f8be6fab2000a6467878a744a2ed0e721bf6949ed704cc6f92d4e7dcf245181a7e3dcabf7c9e0822b7cb431130000dd7927bd485cd3b180edaad0c6da2dd02188874c2952ebe0bb40300b8648912d67b5f8f185fc9943dc50933bbb813e4',
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