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
    '_ga_XXTTVXWHDB': 'GS2.3.s1784708876$o6$g0$t1784708876$j60$l0$h0',
    '_ga_QPPE1C18C5': 'GS2.1.s1784708877$o2$g0$t1784708877$j60$l0$h0',
    'db8ca2b43ed851cc93e71fd5fd72bff7': '51ba8c6b76b97407ee7740b537df4c15',
    'TS011f2d1a': '01266d26d07e6de5aef15515162c76d0816d07aa0732e2f8fc6a0e710645dc71ac852c0bab6bc304db4605b01306d7bbff25d72913',
    'TS00000000076': '0868f8be6fab280077a2f9ab1abe6ec83252c4859e555a1dea0f85846f6731afb75a1b42d348e454e613945c790111a3080b63221909d000bf8938f0c437652a46dd4773236aa4050352d18d8263553c857242e4bd5a4957d696c9d3637b7ee722499d3618d5fbfc743abd6d995a27fc54479c11b3046fadcdb937d07d4bfe2d5cf82727e787a694aa140231706081a3831cea22aaffde66eb97ab706611561d09300c8b160dc1caef174efdb56a4730ccc02218d4e4e95baba732745ba6c583de223512ad3479fca67cf3386acc34d04f835cd80f4caf1a8da2ec8b61ee2e05512246f98e2359f8fad7f135c16d20f225fa2824dc38adaccd1b6e4931b31d1238be24294cd138e7',
    'TSPD_101_DID': '0868f8be6fab280077a2f9ab1abe6ec83252c4859e555a1dea0f85846f6731afb75a1b42d348e454e613945c790111a3080b6322190638004a3bce2c07da034b3d6ee94e614d4a002d89255689b53703d447d8aa7a0bd0ea0b5b369c34369ed3e857ab246093fa49838141d6febf2156',
    'XSRF-TOKEN': 'fa9ef1ba-2950-4112-a024-aca3e0c228c7',
    'TSPD_101': '0868f8be6fab28006c8294eb9e1e1812e2f123c461c268af5508e599c9b948b3b263c73a39d7196cc89a1625b926217e0838f6266e051800fe1ac6a9d3b492905ca1732140a3428bba23ce13beb1c95e',
    'SESSION': 'ca090263-4f6a-4d85-9400-3d2e8e0faaa3',
    'f5avraaaaaaaaaaaaaaaa_session_': 'MEBIDAFICKFBNHPHPPJEJPNFHLAPBDGOLCNGGMJKLJJCHCPNKBKDHGENJPCLGFAFHAODFLMKPHGBHMPOMJFADODDDFIJIAFFBNDFBDFLHNEJPLOGMFCFDLJFGIOBIBIJ',
    'TS5220f739077': '0868f8be6fab28003fb734e7ea470516b53f909864789271e1799c9bfa8d94477a879f41baa817f1ab0d81b3480d5c380881c1ad9f17200060188fbe3616d4a46880499d651edae632060dda69b968689234e4c42873e424',
    'TS5220f739029': '0868f8be6fab280072371901fc236e94f2a18d19178409a8c0131651321bfe798a737814f7f685d6a8869cc8b9645f0b',
    'TSf1edb2d2027': '0868f8be6fab2000904009a5a3ba71a880275353e6d5e93a0ded3428bce03568c0891352224dae1508066ecd14113000d0898684d97fc5f1919822b63b552d10daac121e929c38c4270c5a80773d7c9f69c63254865fd446ce8e91f6af004bab',
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
    'x-xsrf-token': 'fa9ef1ba-2950-4112-a024-aca3e0c228c7',
    'cookie': 'cf_clearance=HQwIeZ.AS7MaosOLHlONXmzkiqUal.b5qak.8P0X_Z0-1784535547-1.2.1.1-oPdlHNW4C0XrGVjAWY9djxZNUrmPrAVBwqz_o7cR73XAAT_UiwRfnQXD6n_EJQV.MNt8QCZ.nAba9BRJR.WCiuCCqpwUyKo0gV7yNsZ2re15VZlKnIwXsuiTQeIPDsqEsvVaOzF5YWtEAt2fVDu0qmpMNqdo8n__nu0dVZSniyYtXUppOglTQqYZ0nB8ZCZfNrYErNEsHrETnRrMRSxGylfEtdVEdRW7XkO7MfUZD2MhhF11b6XvSrm0YPGNPfNLlUuTtWlr72eJ0.LBhmgCM2QPO2EnlAGfS2YlDzEdJenVct0XJmsFQxac1IPEoklYR4tQUZzzPOC1ABiTVsDYNA; _ga_XXTTVXWHDB=GS2.3.s1784708876$o6$g0$t1784708876$j60$l0$h0; _ga_QPPE1C18C5=GS2.1.s1784708877$o2$g0$t1784708877$j60$l0$h0; db8ca2b43ed851cc93e71fd5fd72bff7=51ba8c6b76b97407ee7740b537df4c15; TS011f2d1a=01266d26d07e6de5aef15515162c76d0816d07aa0732e2f8fc6a0e710645dc71ac852c0bab6bc304db4605b01306d7bbff25d72913; TS00000000076=0868f8be6fab280077a2f9ab1abe6ec83252c4859e555a1dea0f85846f6731afb75a1b42d348e454e613945c790111a3080b63221909d000bf8938f0c437652a46dd4773236aa4050352d18d8263553c857242e4bd5a4957d696c9d3637b7ee722499d3618d5fbfc743abd6d995a27fc54479c11b3046fadcdb937d07d4bfe2d5cf82727e787a694aa140231706081a3831cea22aaffde66eb97ab706611561d09300c8b160dc1caef174efdb56a4730ccc02218d4e4e95baba732745ba6c583de223512ad3479fca67cf3386acc34d04f835cd80f4caf1a8da2ec8b61ee2e05512246f98e2359f8fad7f135c16d20f225fa2824dc38adaccd1b6e4931b31d1238be24294cd138e7; TSPD_101_DID=0868f8be6fab280077a2f9ab1abe6ec83252c4859e555a1dea0f85846f6731afb75a1b42d348e454e613945c790111a3080b6322190638004a3bce2c07da034b3d6ee94e614d4a002d89255689b53703d447d8aa7a0bd0ea0b5b369c34369ed3e857ab246093fa49838141d6febf2156; XSRF-TOKEN=fa9ef1ba-2950-4112-a024-aca3e0c228c7; TSPD_101=0868f8be6fab28006c8294eb9e1e1812e2f123c461c268af5508e599c9b948b3b263c73a39d7196cc89a1625b926217e0838f6266e051800fe1ac6a9d3b492905ca1732140a3428bba23ce13beb1c95e; SESSION=ca090263-4f6a-4d85-9400-3d2e8e0faaa3; f5avraaaaaaaaaaaaaaaa_session_=MEBIDAFICKFBNHPHPPJEJPNFHLAPBDGOLCNGGMJKLJJCHCPNKBKDHGENJPCLGFAFHAODFLMKPHGBHMPOMJFADODDDFIJIAFFBNDFBDFLHNEJPLOGMFCFDLJFGIOBIBIJ; TS5220f739077=0868f8be6fab28003fb734e7ea470516b53f909864789271e1799c9bfa8d94477a879f41baa817f1ab0d81b3480d5c380881c1ad9f17200060188fbe3616d4a46880499d651edae632060dda69b968689234e4c42873e424; TS5220f739029=0868f8be6fab280072371901fc236e94f2a18d19178409a8c0131651321bfe798a737814f7f685d6a8869cc8b9645f0b; TSf1edb2d2027=0868f8be6fab2000904009a5a3ba71a880275353e6d5e93a0ded3428bce03568c0891352224dae1508066ecd14113000d0898684d97fc5f1919822b63b552d10daac121e929c38c4270c5a80773d7c9f69c63254865fd446ce8e91f6af004bab',
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