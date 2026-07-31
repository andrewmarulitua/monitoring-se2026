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
    'f5avraaaaaaaaaaaaaaaa_session_': 'MEAGAPIFEHFAHPDIJGILDHEICCHNNCGKDCMOAMIPMEDJDGINGJKEIHPNMJFIKEMHBKCDFAMAANLMADLFEBJAMDDNOCMBLPNGMDNFIFNLKADFONKKOJOOKIMJHEJHGIEB',
    'cf_clearance': 'HQwIeZ.AS7MaosOLHlONXmzkiqUal.b5qak.8P0X_Z0-1784535547-1.2.1.1-oPdlHNW4C0XrGVjAWY9djxZNUrmPrAVBwqz_o7cR73XAAT_UiwRfnQXD6n_EJQV.MNt8QCZ.nAba9BRJR.WCiuCCqpwUyKo0gV7yNsZ2re15VZlKnIwXsuiTQeIPDsqEsvVaOzF5YWtEAt2fVDu0qmpMNqdo8n__nu0dVZSniyYtXUppOglTQqYZ0nB8ZCZfNrYErNEsHrETnRrMRSxGylfEtdVEdRW7XkO7MfUZD2MhhF11b6XvSrm0YPGNPfNLlUuTtWlr72eJ0.LBhmgCM2QPO2EnlAGfS2YlDzEdJenVct0XJmsFQxac1IPEoklYR4tQUZzzPOC1ABiTVsDYNA',
    'TS00000000076': '0868f8be6fab2800342304038b6d195737070b20e87af92b23f6ef0f6d069f14786a4f5db26216f9d6c079330176e21e08819e410709d0002311ec91783ab9b4720cc031dfa5a8d13c9b8e6034226436d61aa19600789a41336210b4dab234351a8c0f1c34f5b971bd968f06259015365b5c8eae49446bb494f3715356c2646befa39df340815f6d3620c0e88174da830189840f35b642cc4d3fdfc109315b8e722df0c733386c2a936b55ba703691ddeb64d6f1dcd2364b799213d6955c48ffb2237871e97119e17d754935dac3c3e0e695b8e03e9ac11abf0cda7bc40d223e686afdf1428abe814d72a36bda1dad894e8c7b6e3ab75b1565d7c38c4c4399bb3743b0814b43f7b1',
    'TSPD_101_DID': '0868f8be6fab2800342304038b6d195737070b20e87af92b23f6ef0f6d069f14786a4f5db26216f9d6c079330176e21e08819e4107063800e2a4108b01e904f69a2633c6bcf873ba85b697b85ea6f33d2d0684a312cb17ac86fc3e9d178968e87dd00eb6fea01f0eaf79c7145cff73a4',
    'db8ca2b43ed851cc93e71fd5fd72bff7': '2a501f1595b4730c02ec8ab8b8c9e9c6',
    'TS011f2d1a': '01266d26d0dcff999f9ffd09a433664231dc31427de08a320e8e273d219afa15a917aa6d549fbcf3d0a3a8f11926f05f08abd154c9',
    'TSPD_101': '0868f8be6fab2800295e98efb0ea65544c15f8e4fd8638c8d70622017166a1656eab0e4d32ac49db40ba1b949360ed3408facba37705180042ca1da95c9ec9275ca1732140a3428bba23ce13beb1c95e',
    'XSRF-TOKEN': '9045e69a-865f-4a46-812d-531c112187dc',
    'JSESSIONID': '2F21D538337ABFFDDB89331B67C200DE',
    'SESSION': 'a87fc8f3-b6b6-4148-9cfb-7cb9bb9c4c9a',
    'f5avraaaaaaaaaaaaaaaa_session_': 'MIMJLKHBCHIFHPOBMCJIHCMAACIICFBINJBJBFKDFPGPFKJPGHJOPCMEOAOFLNEEBNKDLBGIHNDMOACGCPKAJEOFNCLEIIGFIPJPAILDPLKIPCJGGICLBKHKCHKHOAMH',
    'TS5220f739077': '0868f8be6fab2800e3e913f785c23ee39b56d7c790d3a05939bba5812aee58fd4560076db2ff7ff1e56c47a568cb53f308644b89aa172000e2e71c3dfad48a17ef79843c303a218494a163db42554b06544185b8d70cfb9b',
    'TS5220f739029': '0868f8be6fab2800e48947358103f28cb3fe44e1f0ecb579b96d073c56037aab2d824190a6ee84c7c406e29b8c0c658f',
    'TSf1edb2d2027': '0868f8be6fab20009dfa01c5f7e35dc1e5eab6be82206be8e07c6d03e9ce331fd2ff03154936716908284fd7cc113000e59353787cde0f388351473cefc3abfbfcd640274c34d5d560ff3bfe05cede1a2429cf81d2479bd00d26ef98f4eaa66f',
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
    'x-xsrf-token': '9045e69a-865f-4a46-812d-531c112187dc',
    'cookie': 'f5avraaaaaaaaaaaaaaaa_session_=MEAGAPIFEHFAHPDIJGILDHEICCHNNCGKDCMOAMIPMEDJDGINGJKEIHPNMJFIKEMHBKCDFAMAANLMADLFEBJAMDDNOCMBLPNGMDNFIFNLKADFONKKOJOOKIMJHEJHGIEB; cf_clearance=HQwIeZ.AS7MaosOLHlONXmzkiqUal.b5qak.8P0X_Z0-1784535547-1.2.1.1-oPdlHNW4C0XrGVjAWY9djxZNUrmPrAVBwqz_o7cR73XAAT_UiwRfnQXD6n_EJQV.MNt8QCZ.nAba9BRJR.WCiuCCqpwUyKo0gV7yNsZ2re15VZlKnIwXsuiTQeIPDsqEsvVaOzF5YWtEAt2fVDu0qmpMNqdo8n__nu0dVZSniyYtXUppOglTQqYZ0nB8ZCZfNrYErNEsHrETnRrMRSxGylfEtdVEdRW7XkO7MfUZD2MhhF11b6XvSrm0YPGNPfNLlUuTtWlr72eJ0.LBhmgCM2QPO2EnlAGfS2YlDzEdJenVct0XJmsFQxac1IPEoklYR4tQUZzzPOC1ABiTVsDYNA; TS00000000076=0868f8be6fab2800342304038b6d195737070b20e87af92b23f6ef0f6d069f14786a4f5db26216f9d6c079330176e21e08819e410709d0002311ec91783ab9b4720cc031dfa5a8d13c9b8e6034226436d61aa19600789a41336210b4dab234351a8c0f1c34f5b971bd968f06259015365b5c8eae49446bb494f3715356c2646befa39df340815f6d3620c0e88174da830189840f35b642cc4d3fdfc109315b8e722df0c733386c2a936b55ba703691ddeb64d6f1dcd2364b799213d6955c48ffb2237871e97119e17d754935dac3c3e0e695b8e03e9ac11abf0cda7bc40d223e686afdf1428abe814d72a36bda1dad894e8c7b6e3ab75b1565d7c38c4c4399bb3743b0814b43f7b1; TSPD_101_DID=0868f8be6fab2800342304038b6d195737070b20e87af92b23f6ef0f6d069f14786a4f5db26216f9d6c079330176e21e08819e4107063800e2a4108b01e904f69a2633c6bcf873ba85b697b85ea6f33d2d0684a312cb17ac86fc3e9d178968e87dd00eb6fea01f0eaf79c7145cff73a4; db8ca2b43ed851cc93e71fd5fd72bff7=2a501f1595b4730c02ec8ab8b8c9e9c6; TS011f2d1a=01266d26d0dcff999f9ffd09a433664231dc31427de08a320e8e273d219afa15a917aa6d549fbcf3d0a3a8f11926f05f08abd154c9; TSPD_101=0868f8be6fab2800295e98efb0ea65544c15f8e4fd8638c8d70622017166a1656eab0e4d32ac49db40ba1b949360ed3408facba37705180042ca1da95c9ec9275ca1732140a3428bba23ce13beb1c95e; XSRF-TOKEN=9045e69a-865f-4a46-812d-531c112187dc; JSESSIONID=2F21D538337ABFFDDB89331B67C200DE; SESSION=a87fc8f3-b6b6-4148-9cfb-7cb9bb9c4c9a; f5avraaaaaaaaaaaaaaaa_session_=MIMJLKHBCHIFHPOBMCJIHCMAACIICFBINJBJBFKDFPGPFKJPGHJOPCMEOAOFLNEEBNKDLBGIHNDMOACGCPKAJEOFNCLEIIGFIPJPAILDPLKIPCJGGICLBKHKCHKHOAMH; TS5220f739077=0868f8be6fab2800e3e913f785c23ee39b56d7c790d3a05939bba5812aee58fd4560076db2ff7ff1e56c47a568cb53f308644b89aa172000e2e71c3dfad48a17ef79843c303a218494a163db42554b06544185b8d70cfb9b; TS5220f739029=0868f8be6fab2800e48947358103f28cb3fe44e1f0ecb579b96d073c56037aab2d824190a6ee84c7c406e29b8c0c658f; TSf1edb2d2027=0868f8be6fab20009dfa01c5f7e35dc1e5eab6be82206be8e07c6d03e9ce331fd2ff03154936716908284fd7cc113000e59353787cde0f388351473cefc3abfbfcd640274c34d5d560ff3bfe05cede1a2429cf81d2479bd00d26ef98f4eaa66f',
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