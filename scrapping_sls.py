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
    'db8ca2b43ed851cc93e71fd5fd72bff7': '7202bf84f2a9bbb038504de67c9e4b36',
    'TS011f2d1a': '01266d26d0f0b38b85b1b4613ac4fc14f9cfd919d9cb19a5bc5afbfcf2f50b36853aebb2eb81f45ab941233c9547d66986e3bd0ac0',
    'TS00000000076': '0868f8be6fab2800806bb1f355569456e09faeccf1d90bf792668ae45ab6982e97b8466f8c9c538d78a2e167826855970837e8fb9c09d00056a8ba8a845fc761097659547ad2538b79ab14205b483696b2d545f027294d230e5ba1d8ad225db816197f52004bb3d10ff7fa32cb1ad4cefe3e35f6b9f9f8752873cf0bcbdf494742f0f352c54f650905bebab0583ff0e90124a0c0873e2298531bc8859853e3762d8a1ac0c686e8ca5bb9a81ca2e79f788d0707ac312fe764183a7878899c5afd58d906077bb0387ceba19a20fafcba983003dcdb7f1b6699682c07dc6f7cd9fffc6a6dad9543169dff6b037de460ade73d5167bc24dcd4c6f3a4764deb747f8605b0e5195f21a35b',
    'TSPD_101_DID': '0868f8be6fab2800806bb1f355569456e09faeccf1d90bf792668ae45ab6982e97b8466f8c9c538d78a2e167826855970837e8fb9c063800e601aa197e9f4fccdd3fa2f2282cdc5ad53d0a8cf5dfd9c39f8de137ee022f022dc68bba980d7addbdd7d59b027b964ef9d57b9a1ddeb7b2',
    'XSRF-TOKEN': 'b4d9a1bb-e8b6-4fd6-9e72-3b5f6e9d8b4c',
    'TSPD_101': '0868f8be6fab2800c632054f0d78f821929205d8227ef4febb805799ef2e1b6649e58d770da9305a1752398ce374d3590823930fd3051800de709b4ce7a6dc7e5ca1732140a3428bba23ce13beb1c95e',
    'SESSION': '284c39f1-8a2e-420d-8f08-728d89297bfa',
    'f5avraaaaaaaaaaaaaaaa_session_': 'BGIKLIIDBLBFOEIIOMIKFFGIBDKMOGANDBLEKAEMIMPKHDHGEJDKLJJMJGACKLEGGKKDAKENPCJMGOAANDEAFLOIDOCDNDKPAEKLIIKHHGOJKOLCPNOKLHGFHDEBHHOP',
    'TS5220f739077': '0868f8be6fab2800924795f78db6c73d3cfa076091cbcc55b5dec6a0b193e7a2ae322703e1d50033ced80431cae364df0806e9439a172000463cf62cde70c34b85a975091005d708779501e62137c9d5cde1ef7863993b22',
    'TS5220f739029': '0868f8be6fab2800a93b175f5a8b20de701777c6362c239dbab208408258ff4de3ae240a37bdd9c9b1c4be5d7d1007d6',
    'TSf1edb2d2027': '0868f8be6fab20001eb92df23a6fb94318cf1d3ffc6c18abf3d4061d9c6d60c88f73b9268817923f0839bf6d81113000c51eafa8fde22d437a6f863b1de9825aaeeef53debe793f01dedc19d187a17af24f9a2dd9f80c2bd03ab7a7ec52ad2b6',
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
    'x-xsrf-token': 'b4d9a1bb-e8b6-4fd6-9e72-3b5f6e9d8b4c',
    'cookie': 'cf_clearance=HQwIeZ.AS7MaosOLHlONXmzkiqUal.b5qak.8P0X_Z0-1784535547-1.2.1.1-oPdlHNW4C0XrGVjAWY9djxZNUrmPrAVBwqz_o7cR73XAAT_UiwRfnQXD6n_EJQV.MNt8QCZ.nAba9BRJR.WCiuCCqpwUyKo0gV7yNsZ2re15VZlKnIwXsuiTQeIPDsqEsvVaOzF5YWtEAt2fVDu0qmpMNqdo8n__nu0dVZSniyYtXUppOglTQqYZ0nB8ZCZfNrYErNEsHrETnRrMRSxGylfEtdVEdRW7XkO7MfUZD2MhhF11b6XvSrm0YPGNPfNLlUuTtWlr72eJ0.LBhmgCM2QPO2EnlAGfS2YlDzEdJenVct0XJmsFQxac1IPEoklYR4tQUZzzPOC1ABiTVsDYNA; _ga_XXTTVXWHDB=GS2.3.s1785131298$o7$g1$t1785132563$j60$l0$h0; _ga=GA1.1.2055404639.1784774377; _ga_QPPE1C18C5=GS2.1.s1785135144$o3$g1$t1785135282$j60$l0$h0; db8ca2b43ed851cc93e71fd5fd72bff7=7202bf84f2a9bbb038504de67c9e4b36; TS011f2d1a=01266d26d0f0b38b85b1b4613ac4fc14f9cfd919d9cb19a5bc5afbfcf2f50b36853aebb2eb81f45ab941233c9547d66986e3bd0ac0; TS00000000076=0868f8be6fab2800806bb1f355569456e09faeccf1d90bf792668ae45ab6982e97b8466f8c9c538d78a2e167826855970837e8fb9c09d00056a8ba8a845fc761097659547ad2538b79ab14205b483696b2d545f027294d230e5ba1d8ad225db816197f52004bb3d10ff7fa32cb1ad4cefe3e35f6b9f9f8752873cf0bcbdf494742f0f352c54f650905bebab0583ff0e90124a0c0873e2298531bc8859853e3762d8a1ac0c686e8ca5bb9a81ca2e79f788d0707ac312fe764183a7878899c5afd58d906077bb0387ceba19a20fafcba983003dcdb7f1b6699682c07dc6f7cd9fffc6a6dad9543169dff6b037de460ade73d5167bc24dcd4c6f3a4764deb747f8605b0e5195f21a35b; TSPD_101_DID=0868f8be6fab2800806bb1f355569456e09faeccf1d90bf792668ae45ab6982e97b8466f8c9c538d78a2e167826855970837e8fb9c063800e601aa197e9f4fccdd3fa2f2282cdc5ad53d0a8cf5dfd9c39f8de137ee022f022dc68bba980d7addbdd7d59b027b964ef9d57b9a1ddeb7b2; XSRF-TOKEN=b4d9a1bb-e8b6-4fd6-9e72-3b5f6e9d8b4c; TSPD_101=0868f8be6fab2800c632054f0d78f821929205d8227ef4febb805799ef2e1b6649e58d770da9305a1752398ce374d3590823930fd3051800de709b4ce7a6dc7e5ca1732140a3428bba23ce13beb1c95e; SESSION=284c39f1-8a2e-420d-8f08-728d89297bfa; f5avraaaaaaaaaaaaaaaa_session_=BGIKLIIDBLBFOEIIOMIKFFGIBDKMOGANDBLEKAEMIMPKHDHGEJDKLJJMJGACKLEGGKKDAKENPCJMGOAANDEAFLOIDOCDNDKPAEKLIIKHHGOJKOLCPNOKLHGFHDEBHHOP; TS5220f739077=0868f8be6fab2800924795f78db6c73d3cfa076091cbcc55b5dec6a0b193e7a2ae322703e1d50033ced80431cae364df0806e9439a172000463cf62cde70c34b85a975091005d708779501e62137c9d5cde1ef7863993b22; TS5220f739029=0868f8be6fab2800a93b175f5a8b20de701777c6362c239dbab208408258ff4de3ae240a37bdd9c9b1c4be5d7d1007d6; TSf1edb2d2027=0868f8be6fab20001eb92df23a6fb94318cf1d3ffc6c18abf3d4061d9c6d60c88f73b9268817923f0839bf6d81113000c51eafa8fde22d437a6f863b1de9825aaeeef53debe793f01dedc19d187a17af24f9a2dd9f80c2bd03ab7a7ec52ad2b6',
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