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
    '_ga': 'GA1.3.417237891.1782976914',
    '_ga_XXTTVXWHDB': 'GS2.3.s1783567220$o4$g0$t1783567220$j60$l0$h0',
    'TS0151fc2b': '0167a1c8616eba36414b311788ab1efae1f3122da3a3d81b96519f487b946080eb75997bcf719d0cc77047662a29c10bcc32cbc3c3',
    'db8ca2b43ed851cc93e71fd5fd72bff7': '13b6ee7a488307959e12f96ea563eca4',
    'XSRF-TOKEN': '0f2172a9-337b-48ea-b7cb-b51d08975f7f',
    'SESSION': '434d17dc-a834-4d82-9c3b-beb2ee1a4e02',
    'TS018af012': '0167a1c861f8184e66ed50992c904955b1982a4b783a350f37e4e1cd4b4b4bbefa34425827f1df0dbc7d817543f32e3c37117eb91989ae047090885e4ba087a8dc701d683d2176a31eeb92107c53dd3520e83a0358',
    'f5avraaaaaaaaaaaaaaaa_session_': 'INHDNCKOGDCGPEOLDDCAEFGEAODPJENBHFEEDINCCFEGPDOBDCKJAKENNHFLFCJNBFCDJMNPHDFEKAKBENJANGDNEEIIAPFIJOPMHMOJBCPAFOEONKHNFMKCEANKCHBL',
    'TS00000000076': '0868f8be6fab28009d48ea12d268b5d1b49d2d307ef1110c3f5b5ecb3e915cf9bec1e4dbb0972d0645f4b5a38accf9ce08c649de4a09d0005ec028d096f4880b5144fadd945b89e6bf10a31d43f325fbd974947a3515ce1a023c99528c77ae84e21b11c61cf647abe650ad9fc107430c7d30b2bda04f09854e5bcf75213991ebda54ba1fce8237af301af5833580effd3db8831afba7391a4a219ed6f2a5619bb3f3f3a4550f069a50ee1f8db1a1633b568ae30ffe8d57e9993530afe8689fc269d1e196088dcee42e5cfa2fe0fdcdfba80e8ca61f7598511696ebab49e72142cfda358c752411a4beb6c19afbd119c71dc3ba693fb96695013c995c59a975da1bf7eb7ffbca67e7',
    'TSPD_101_DID': '0868f8be6fab28009d48ea12d268b5d1b49d2d307ef1110c3f5b5ecb3e915cf9bec1e4dbb0972d0645f4b5a38accf9ce08c649de4a063800472a98aa1a97b4a79d0dcf2f2688db8c391e2911f9f8a1ed4b181247fe04f310a6a035fd96611c94d234594b87b510fb76e8270c90a79122',
    'TS011f2d1a': '01266d26d0d1756da51ce88520257d473df5f76109bd9d351dc923097200532f5a0990991adb4eda3679c164e483531d8ebe6e4501',
    'TSPD_101': '0868f8be6fab280042129d3148ebabff219fa0b14e0377749ebf8b2bffa95fb8c10ad0e0c0c21a36c1f55f7618e363ea08a08eb340051800c21ba130b7b9d4cf5ca1732140a3428bba23ce13beb1c95e',
    'TS5220f739077': '0868f8be6fab280059b56b329a8f1855fb53bc8890772aa83393a2704af35fac91908fe82eb565ecd58c72f2b74805520807a9c63d1720003edc34d94bc75e2ecd8329cb5862396b2aeae5b39526bf988dcbb16b17a9e8a6',
    'TS5220f739029': '0868f8be6fab2800fac6c0d81b437509400de1ee841cdb5834c7d7b6b42e236fcd3ff260a36c0a75c4105657b38d40ce',
    'TSf1edb2d2027': '0868f8be6fab2000ab0dd8b7e296e41c7a4699c79ae503ab270cef5d579582cc28406ff195294e0c085e4c65c91130007b6635b03b9bea051f9752e23ec251eacd44ea39d4b05e92239c244375fdb138c0390f9ffedd7e1afa9d65e94dca91b6',
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
    'x-xsrf-token': '0f2172a9-337b-48ea-b7cb-b51d08975f7f',
    'cookie': '_ga=GA1.3.417237891.1782976914; _ga_XXTTVXWHDB=GS2.3.s1783567220$o4$g0$t1783567220$j60$l0$h0; TS0151fc2b=0167a1c8616eba36414b311788ab1efae1f3122da3a3d81b96519f487b946080eb75997bcf719d0cc77047662a29c10bcc32cbc3c3; db8ca2b43ed851cc93e71fd5fd72bff7=13b6ee7a488307959e12f96ea563eca4; XSRF-TOKEN=0f2172a9-337b-48ea-b7cb-b51d08975f7f; SESSION=434d17dc-a834-4d82-9c3b-beb2ee1a4e02; TS018af012=0167a1c861f8184e66ed50992c904955b1982a4b783a350f37e4e1cd4b4b4bbefa34425827f1df0dbc7d817543f32e3c37117eb91989ae047090885e4ba087a8dc701d683d2176a31eeb92107c53dd3520e83a0358; f5avraaaaaaaaaaaaaaaa_session_=INHDNCKOGDCGPEOLDDCAEFGEAODPJENBHFEEDINCCFEGPDOBDCKJAKENNHFLFCJNBFCDJMNPHDFEKAKBENJANGDNEEIIAPFIJOPMHMOJBCPAFOEONKHNFMKCEANKCHBL; TS00000000076=0868f8be6fab28009d48ea12d268b5d1b49d2d307ef1110c3f5b5ecb3e915cf9bec1e4dbb0972d0645f4b5a38accf9ce08c649de4a09d0005ec028d096f4880b5144fadd945b89e6bf10a31d43f325fbd974947a3515ce1a023c99528c77ae84e21b11c61cf647abe650ad9fc107430c7d30b2bda04f09854e5bcf75213991ebda54ba1fce8237af301af5833580effd3db8831afba7391a4a219ed6f2a5619bb3f3f3a4550f069a50ee1f8db1a1633b568ae30ffe8d57e9993530afe8689fc269d1e196088dcee42e5cfa2fe0fdcdfba80e8ca61f7598511696ebab49e72142cfda358c752411a4beb6c19afbd119c71dc3ba693fb96695013c995c59a975da1bf7eb7ffbca67e7; TSPD_101_DID=0868f8be6fab28009d48ea12d268b5d1b49d2d307ef1110c3f5b5ecb3e915cf9bec1e4dbb0972d0645f4b5a38accf9ce08c649de4a063800472a98aa1a97b4a79d0dcf2f2688db8c391e2911f9f8a1ed4b181247fe04f310a6a035fd96611c94d234594b87b510fb76e8270c90a79122; TS011f2d1a=01266d26d0d1756da51ce88520257d473df5f76109bd9d351dc923097200532f5a0990991adb4eda3679c164e483531d8ebe6e4501; TSPD_101=0868f8be6fab280042129d3148ebabff219fa0b14e0377749ebf8b2bffa95fb8c10ad0e0c0c21a36c1f55f7618e363ea08a08eb340051800c21ba130b7b9d4cf5ca1732140a3428bba23ce13beb1c95e; TS5220f739077=0868f8be6fab280059b56b329a8f1855fb53bc8890772aa83393a2704af35fac91908fe82eb565ecd58c72f2b74805520807a9c63d1720003edc34d94bc75e2ecd8329cb5862396b2aeae5b39526bf988dcbb16b17a9e8a6; TS5220f739029=0868f8be6fab2800fac6c0d81b437509400de1ee841cdb5834c7d7b6b42e236fcd3ff260a36c0a75c4105657b38d40ce; TSf1edb2d2027=0868f8be6fab2000ab0dd8b7e296e41c7a4699c79ae503ab270cef5d579582cc28406ff195294e0c085e4c65c91130007b6635b03b9bea051f9752e23ec251eacd44ea39d4b05e92239c244375fdb138c0390f9ffedd7e1afa9d65e94dca91b6',
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