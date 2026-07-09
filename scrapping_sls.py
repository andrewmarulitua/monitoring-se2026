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
    '_ga_XXTTVXWHDB': 'GS2.3.s1783060528$o2$g1$t1783067101$j60$l0$h0',
    'db8ca2b43ed851cc93e71fd5fd72bff7': 'ac1248223b3e09af5f4465e476716078',
    'XSRF-TOKEN': '638e84bb-ce3f-4e5b-87fe-1b48dc18799e',
    'SESSION': 'a7e5fc8a-d8c5-4c7d-ab45-eacbdb5a4454',
    'TS00000000076': '0868f8be6fab2800bc1f71b5ac8e21cd4a8cadc9e6250831e2e5c81fa94e38fbbc8a887eda1b421b59994e627f46ce3e0855fd170209d000df6617f645728bdc4b0a5a394da1b20d4f91338bc2036bd405ed2e215312874480c892512bacf8fe6d7581383bae1fe007eca7fac417288803ffa39674f6659f85e879587f14ed6cdbbd5db2552e544378f2bc3c9933f693ae0263842228be3716f474c4dd611f4b53f73646c99e49fab19cf339ef4c0cb4ebcc8d2d803c28c3da7fda94a2c66e309f1948234e94d47701854c472aac0fbd9acf899c127e6d48c660ac6bbec025f0b7217ff9994a9c6884f573ce08f13343cca0b03c42b0e125791b046c548ee9ecedc89594e3659cc0',
    'TSPD_101_DID': '0868f8be6fab2800bc1f71b5ac8e21cd4a8cadc9e6250831e2e5c81fa94e38fbbc8a887eda1b421b59994e627f46ce3e0855fd1702063800ed7ca910432d0cb096c91b4987e1b1e4ef56ff9e09739466a6c6c82d50e6af6f3eee4f12fa5423c5cbb1fd3c466cd41734737cb3e1035867',
    'TS011f2d1a': '01266d26d0b198a8f81cb633c8d709adca9f79c96b4ec6a2e944b3a2601b0e1b993b2923ffc98d6958c36a5f3a29cca978ef6b2c3f',
    'TSPD_101': '0868f8be6fab28001070d8ef69e62b5fef5543ffcaeedafa94e1f4bbdd556ab41c622b904e1625d33c59f57b60a2e7b2086a5702ab0518000c951fc26ce1dff65ca1732140a3428bba23ce13beb1c95e',
    'f5avraaaaaaaaaaaaaaaa_session_': 'EIKELDKNGKLOMNKHCFNDMFCPIHMBAGHLNIBOOGJALHHLJACMMOFKFGCLKEBFPCJLNFGDOKEEFMCELOHOAFBALJNPIOFPLEKELOMCJGDMOADOFGENDNIEKJENBGCFCDHL',
    'TS5220f739077': '0868f8be6fab2800098ce6cc00894b064243620867ed29bb93d4cfe8bc994b1e1ccafc4857795ea718840a42d8579f49080397869017200014560e80160ba598aabab2e33667f87b1c754006072745092c1bee8e97844574',
    'TS5220f739029': '0868f8be6fab28007e76bc12e4849baf49fa7b9395f36d9776e6b3088d01d3d4f8a4e8f183fcaf047f7ad67ca7777458',
    'TSf1edb2d2027': '0868f8be6fab200072088abb27c2bb45fb9995e8f64b385225137a3fa4ceb36a4ac8ddd746a678cd08d771fee7113000c5b6105089a5cb83dc27deeba5c95188a0c3e0a179c9c28d8dabe5cce8b92e2040ac0698637c0af25ec4df44b33f09ea',
}

headers = {
    'accept': '*/*',
    'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7,ms;q=0.6',
    'content-type': 'application/json',
    'origin': 'https://fasih-sm.bps.go.id',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Linux; Android 15; Pixel 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Mobile Safari/537.36',
    'x-xsrf-token': '638e84bb-ce3f-4e5b-87fe-1b48dc18799e',
    'cookie': '_ga=GA1.3.417237891.1782976914; _ga_XXTTVXWHDB=GS2.3.s1783060528$o2$g1$t1783067101$j60$l0$h0; db8ca2b43ed851cc93e71fd5fd72bff7=ac1248223b3e09af5f4465e476716078; XSRF-TOKEN=638e84bb-ce3f-4e5b-87fe-1b48dc18799e; SESSION=a7e5fc8a-d8c5-4c7d-ab45-eacbdb5a4454; TS00000000076=0868f8be6fab2800bc1f71b5ac8e21cd4a8cadc9e6250831e2e5c81fa94e38fbbc8a887eda1b421b59994e627f46ce3e0855fd170209d000df6617f645728bdc4b0a5a394da1b20d4f91338bc2036bd405ed2e215312874480c892512bacf8fe6d7581383bae1fe007eca7fac417288803ffa39674f6659f85e879587f14ed6cdbbd5db2552e544378f2bc3c9933f693ae0263842228be3716f474c4dd611f4b53f73646c99e49fab19cf339ef4c0cb4ebcc8d2d803c28c3da7fda94a2c66e309f1948234e94d47701854c472aac0fbd9acf899c127e6d48c660ac6bbec025f0b7217ff9994a9c6884f573ce08f13343cca0b03c42b0e125791b046c548ee9ecedc89594e3659cc0; TSPD_101_DID=0868f8be6fab2800bc1f71b5ac8e21cd4a8cadc9e6250831e2e5c81fa94e38fbbc8a887eda1b421b59994e627f46ce3e0855fd1702063800ed7ca910432d0cb096c91b4987e1b1e4ef56ff9e09739466a6c6c82d50e6af6f3eee4f12fa5423c5cbb1fd3c466cd41734737cb3e1035867; TS011f2d1a=01266d26d0b198a8f81cb633c8d709adca9f79c96b4ec6a2e944b3a2601b0e1b993b2923ffc98d6958c36a5f3a29cca978ef6b2c3f; TSPD_101=0868f8be6fab28001070d8ef69e62b5fef5543ffcaeedafa94e1f4bbdd556ab41c622b904e1625d33c59f57b60a2e7b2086a5702ab0518000c951fc26ce1dff65ca1732140a3428bba23ce13beb1c95e; f5avraaaaaaaaaaaaaaaa_session_=EIKELDKNGKLOMNKHCFNDMFCPIHMBAGHLNIBOOGJALHHLJACMMOFKFGCLKEBFPCJLNFGDOKEEFMCELOHOAFBALJNPIOFPLEKELOMCJGDMOADOFGENDNIEKJENBGCFCDHL; TS5220f739077=0868f8be6fab2800098ce6cc00894b064243620867ed29bb93d4cfe8bc994b1e1ccafc4857795ea718840a42d8579f49080397869017200014560e80160ba598aabab2e33667f87b1c754006072745092c1bee8e97844574; TS5220f739029=0868f8be6fab28007e76bc12e4849baf49fa7b9395f36d9776e6b3088d01d3d4f8a4e8f183fcaf047f7ad67ca7777458; TSf1edb2d2027=0868f8be6fab200072088abb27c2bb45fb9995e8f64b385225137a3fa4ceb36a4ac8ddd746a678cd08d771fee7113000c5b6105089a5cb83dc27deeba5c95188a0c3e0a179c9c28d8dabe5cce8b92e2040ac0698637c0af25ec4df44b33f09ea',
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