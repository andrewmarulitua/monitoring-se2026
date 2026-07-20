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
    'f5avraaaaaaaaaaaaaaaa_session_': 'FLMKLAPKHAHJGEKGDKHJINGCIDOFLBJDOKNJHFKGJPNIMJGCPIIJIKEHGHCJKDBGDPGDDKHIKEGDAMFLDALACECOJLFJMKNKFJEMEGHEILMGLNAPDBJPALMBEIPBDLDD',
    '_ga': 'GA1.3.1765036020.1783921242',
    'cf_clearance': 'HQwIeZ.AS7MaosOLHlONXmzkiqUal.b5qak.8P0X_Z0-1784535547-1.2.1.1-oPdlHNW4C0XrGVjAWY9djxZNUrmPrAVBwqz_o7cR73XAAT_UiwRfnQXD6n_EJQV.MNt8QCZ.nAba9BRJR.WCiuCCqpwUyKo0gV7yNsZ2re15VZlKnIwXsuiTQeIPDsqEsvVaOzF5YWtEAt2fVDu0qmpMNqdo8n__nu0dVZSniyYtXUppOglTQqYZ0nB8ZCZfNrYErNEsHrETnRrMRSxGylfEtdVEdRW7XkO7MfUZD2MhhF11b6XvSrm0YPGNPfNLlUuTtWlr72eJ0.LBhmgCM2QPO2EnlAGfS2YlDzEdJenVct0XJmsFQxac1IPEoklYR4tQUZzzPOC1ABiTVsDYNA',
    '_ga_XXTTVXWHDB': 'GS2.3.s1784535547$o4$g1$t1784536228$j60$l0$h0',
    'TS00000000076': '0868f8be6fab2800ff6c7f842bff6368f9bd0d73f729c49d5f183ddf3b655b9df5fad5f77a59ba575652169f8d5d6c830886dc71cc09d0000c83d89a55374acdf43a6efc20565dba35115c8771d9a379fc3f4653f50f4b099a4833106b5e2fcfb6571f42f72a25510dc2ed3c9da62bae38c4922b7e4df402bd267aee9be9f738e16b05995292737799212f46dddcefa4f2acb17875f1c5948f1304cd41b21fea7835918763edf186154e6dac4b22a858cc6a06400191357037c87ea6bdd53b5dc9ac678c83e193ebf21cd7d09b4dcc4b84dbe954b3bb67013766fd97443a7ec78481657cc568c17d30e4e362a5dd4de3f44d461f26d58376459eda73905e3349671987788d211f37',
    'TSPD_101_DID': '0868f8be6fab2800ff6c7f842bff6368f9bd0d73f729c49d5f183ddf3b655b9df5fad5f77a59ba575652169f8d5d6c830886dc71cc063800640541f8b1d62c5ab3e48326fc94b91f83446fb024e06776c6c470cbf7a01b64e4ea4bc2974a542c80b518f250aa646b95ac30e9f75541ac',
    'XSRF-TOKEN': '1ab93c11-0c1a-454a-8afc-4c96a48609f0',
    'db8ca2b43ed851cc93e71fd5fd72bff7': 'acd85465bb10aacd7f2bfc117385302f',
    'TS011f2d1a': '01266d26d03b2e62310b8886d6a751cbfcdd5c8459f864dbaa73178991bfe46486560f9c6e2dc6f455b9c89d3b2c02a5b34055e7bc',
    'TSPD_101': '0868f8be6fab280038eb7c48795b9b85fed2f9ac888a724fabe25c85c2c84e17ca2a23395639717654035895972f423108ad504bbd0518008aecae7728779d285ca1732140a3428bba23ce13beb1c95e',
    'f5avraaaaaaaaaaaaaaaa_session_': 'BDFMNJNFDKGCEJKPJDGGHOKBCPNEFMLDIPNMCMMAOCMAHMJHMIOGELGIPPEKCABOBMEDKECLFEOINFOLGLKAGLDPFLHONJOPLNFKBNIGIFGDJIAABEGIDOLFDGLFKGBA',
    'JSESSIONID': '02AD319502226BE2BD55C8FEF16D6252',
    'SESSION': '3c5619c8-e3ca-4357-9007-2b2974102ead',
    'TS5220f739077': '0868f8be6fab2800c6f0cf75968a7087f93b4d49eadfa9dff570bd9659345664d3c5f2311d690427d4d5b3dd98b03e0e08222d91f617200037e272551df2e49ed9935e394fb7026824567e589dec68197dcacea8a73cbb55',
    'TS5220f739029': '0868f8be6fab28004b15ac4f1343eefcf760d799c01e8318ca968a3016581b5b53e7466f428e4545db2d6e9d446038ed',
    'TSf1edb2d2027': '0868f8be6fab20003bc03e7c94ec80df9b5c340f8874cdbf298d9b6c82dcdbf09b8375570796349308b0fad1b7113000c488f9953175d2671e7c97e101e9326d59cfd15b4dad9fdab6e3cc3121226846eb274a750ffb382890118dd2136c62d4',
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
    'x-xsrf-token': '1ab93c11-0c1a-454a-8afc-4c96a48609f0',
    'cookie': 'f5avraaaaaaaaaaaaaaaa_session_=FLMKLAPKHAHJGEKGDKHJINGCIDOFLBJDOKNJHFKGJPNIMJGCPIIJIKEHGHCJKDBGDPGDDKHIKEGDAMFLDALACECOJLFJMKNKFJEMEGHEILMGLNAPDBJPALMBEIPBDLDD; _ga=GA1.3.1765036020.1783921242; cf_clearance=HQwIeZ.AS7MaosOLHlONXmzkiqUal.b5qak.8P0X_Z0-1784535547-1.2.1.1-oPdlHNW4C0XrGVjAWY9djxZNUrmPrAVBwqz_o7cR73XAAT_UiwRfnQXD6n_EJQV.MNt8QCZ.nAba9BRJR.WCiuCCqpwUyKo0gV7yNsZ2re15VZlKnIwXsuiTQeIPDsqEsvVaOzF5YWtEAt2fVDu0qmpMNqdo8n__nu0dVZSniyYtXUppOglTQqYZ0nB8ZCZfNrYErNEsHrETnRrMRSxGylfEtdVEdRW7XkO7MfUZD2MhhF11b6XvSrm0YPGNPfNLlUuTtWlr72eJ0.LBhmgCM2QPO2EnlAGfS2YlDzEdJenVct0XJmsFQxac1IPEoklYR4tQUZzzPOC1ABiTVsDYNA; _ga_XXTTVXWHDB=GS2.3.s1784535547$o4$g1$t1784536228$j60$l0$h0; TS00000000076=0868f8be6fab2800ff6c7f842bff6368f9bd0d73f729c49d5f183ddf3b655b9df5fad5f77a59ba575652169f8d5d6c830886dc71cc09d0000c83d89a55374acdf43a6efc20565dba35115c8771d9a379fc3f4653f50f4b099a4833106b5e2fcfb6571f42f72a25510dc2ed3c9da62bae38c4922b7e4df402bd267aee9be9f738e16b05995292737799212f46dddcefa4f2acb17875f1c5948f1304cd41b21fea7835918763edf186154e6dac4b22a858cc6a06400191357037c87ea6bdd53b5dc9ac678c83e193ebf21cd7d09b4dcc4b84dbe954b3bb67013766fd97443a7ec78481657cc568c17d30e4e362a5dd4de3f44d461f26d58376459eda73905e3349671987788d211f37; TSPD_101_DID=0868f8be6fab2800ff6c7f842bff6368f9bd0d73f729c49d5f183ddf3b655b9df5fad5f77a59ba575652169f8d5d6c830886dc71cc063800640541f8b1d62c5ab3e48326fc94b91f83446fb024e06776c6c470cbf7a01b64e4ea4bc2974a542c80b518f250aa646b95ac30e9f75541ac; XSRF-TOKEN=1ab93c11-0c1a-454a-8afc-4c96a48609f0; db8ca2b43ed851cc93e71fd5fd72bff7=acd85465bb10aacd7f2bfc117385302f; TS011f2d1a=01266d26d03b2e62310b8886d6a751cbfcdd5c8459f864dbaa73178991bfe46486560f9c6e2dc6f455b9c89d3b2c02a5b34055e7bc; TSPD_101=0868f8be6fab280038eb7c48795b9b85fed2f9ac888a724fabe25c85c2c84e17ca2a23395639717654035895972f423108ad504bbd0518008aecae7728779d285ca1732140a3428bba23ce13beb1c95e; f5avraaaaaaaaaaaaaaaa_session_=BDFMNJNFDKGCEJKPJDGGHOKBCPNEFMLDIPNMCMMAOCMAHMJHMIOGELGIPPEKCABOBMEDKECLFEOINFOLGLKAGLDPFLHONJOPLNFKBNIGIFGDJIAABEGIDOLFDGLFKGBA; JSESSIONID=02AD319502226BE2BD55C8FEF16D6252; SESSION=3c5619c8-e3ca-4357-9007-2b2974102ead; TS5220f739077=0868f8be6fab2800c6f0cf75968a7087f93b4d49eadfa9dff570bd9659345664d3c5f2311d690427d4d5b3dd98b03e0e08222d91f617200037e272551df2e49ed9935e394fb7026824567e589dec68197dcacea8a73cbb55; TS5220f739029=0868f8be6fab28004b15ac4f1343eefcf760d799c01e8318ca968a3016581b5b53e7466f428e4545db2d6e9d446038ed; TSf1edb2d2027=0868f8be6fab20003bc03e7c94ec80df9b5c340f8874cdbf298d9b6c82dcdbf09b8375570796349308b0fad1b7113000c488f9953175d2671e7c97e101e9326d59cfd15b4dad9fdab6e3cc3121226846eb274a750ffb382890118dd2136c62d4',
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