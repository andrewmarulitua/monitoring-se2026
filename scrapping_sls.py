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
    'f5avraaaaaaaaaaaaaaaa_session_': 'IKEPJPALMHNNGPBBPAMMJECCHELPNLGNNMPIGNMOIHIPJCKCFNMFHLPMCBMFANCBMBGDLGMHECAJCCAMAKKALHHDMHHPMOCDCDOIAKHIBPIKBCPBHDKOPKLBMHHMFKNC',
    'db8ca2b43ed851cc93e71fd5fd72bff7': 'e8b047e6afd1e414b7c530096c901865',
    'XSRF-TOKEN': '5f5b63f5-7973-4cb6-9da8-f4c0cffc07c5',
    'f5avraaaaaaaaaaaaaaaa_session_': 'PHEJKKFEEICDPDINELBBMAPPGKDINIEHKEKIACBNKLLIFGEBCJAKDBGLHKAKANODBIGDHAFLFDKNGCAOHGFAMBICAHOPEIFAKOMKBOHLJCDPJHFIIBALDGHKBIFBFDKF',
    'JSESSIONID': 'FDBD00B21C7A94235ADC5C2242E3FE5C',
    'TS00000000076': '0868f8be6fab280082e241a8cb3d7f2464e5e0bdb96727f5d1e848b7d42863406382fd6654c137284ce47b79d56a928908faaba61f09d00089abad1fd15546a368d47e7de4401b649621fd6eefdb145a671eb614cace21eee539e5850552d8f0c1c9d451814bc5fc183da97a31a1450f0e2e61ec95b49a6c38bc2e2ab2014119cefc58aea72f0f2ff4a8654e7d741505aa1d309af17e77becabae54caeef8a5fa48120aac419f494a641249649c9fae4eda53d8465d85057ee3b75d18ce11ff394fc4da9b3387e14322dc6379ed320f8200d57d75012cf6dd0ef60dc5131a70cd717bed69d2b7eef7a037821b6c28e33068a38229eb27d5b330aae34af906ca682143f39c2bf4b97',
    'TSPD_101_DID': '0868f8be6fab280082e241a8cb3d7f2464e5e0bdb96727f5d1e848b7d42863406382fd6654c137284ce47b79d56a928908faaba61f063800a219d45658b4cecbed2420be1c3e20c2a47f2b6a52086441966725f34d02d50d356418de1d1b16c24cf5e3d9630b9c9863b2357102e4a956',
    'TS011f2d1a': '01266d26d0cdb19686c5dd89ae3fc0410f7e79f2e5e13c561d3f9b49cbb28cb41b63d937dc3206750f727b2a25474d6367edbe4163',
    'TSPD_101': '0868f8be6fab28007d9033747d4358b2c40366c680b7c784ca298aed99c6ed944d54b6f662ac12d03aac426f78cba1d00873b12b4f051800632038aefb659b885ca1732140a3428bba23ce13beb1c95e',
    'SESSION': 'f1cba717-708a-4115-876c-cd587a2717b8',
    'TS5220f739077': '0868f8be6fab28004f38464addee01ad30533cb0026a8c93aadb573b4f7a10780d8ee971bd76ab3fe8f97bb59778c38908c5c5ec20172000a18356ee08bf317b257c5f4620c2b7b4c581a5e6547bbcb60053aa008d5fbfba',
    'TS5220f739029': '0868f8be6fab28007bbccfa87bd497f568ba218aef2af94d000c9f5bd816ce59ff1e4891ca30412d0ca0d136db364e6d',
    'TSf1edb2d2027': '0868f8be6fab200029398ac152100d7ac3f7f1271f0ecd4786ba7aac34f39eba4c42e38bc314cb6e08a4b6fc6211300098ccd4413fa41b2129f1b767af20c8903fb555d2110fdd4be99530b60ccd98f71ecb58dc7f135aa07c071732fda28de0',
}

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://fasih-sm.bps.go.id',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
    'x-xsrf-token': '5f5b63f5-7973-4cb6-9da8-f4c0cffc07c5',
    'cookie': 'f5avraaaaaaaaaaaaaaaa_session_=IKEPJPALMHNNGPBBPAMMJECCHELPNLGNNMPIGNMOIHIPJCKCFNMFHLPMCBMFANCBMBGDLGMHECAJCCAMAKKALHHDMHHPMOCDCDOIAKHIBPIKBCPBHDKOPKLBMHHMFKNC; db8ca2b43ed851cc93e71fd5fd72bff7=e8b047e6afd1e414b7c530096c901865; XSRF-TOKEN=5f5b63f5-7973-4cb6-9da8-f4c0cffc07c5; f5avraaaaaaaaaaaaaaaa_session_=PHEJKKFEEICDPDINELBBMAPPGKDINIEHKEKIACBNKLLIFGEBCJAKDBGLHKAKANODBIGDHAFLFDKNGCAOHGFAMBICAHOPEIFAKOMKBOHLJCDPJHFIIBALDGHKBIFBFDKF; JSESSIONID=FDBD00B21C7A94235ADC5C2242E3FE5C; TS00000000076=0868f8be6fab280082e241a8cb3d7f2464e5e0bdb96727f5d1e848b7d42863406382fd6654c137284ce47b79d56a928908faaba61f09d00089abad1fd15546a368d47e7de4401b649621fd6eefdb145a671eb614cace21eee539e5850552d8f0c1c9d451814bc5fc183da97a31a1450f0e2e61ec95b49a6c38bc2e2ab2014119cefc58aea72f0f2ff4a8654e7d741505aa1d309af17e77becabae54caeef8a5fa48120aac419f494a641249649c9fae4eda53d8465d85057ee3b75d18ce11ff394fc4da9b3387e14322dc6379ed320f8200d57d75012cf6dd0ef60dc5131a70cd717bed69d2b7eef7a037821b6c28e33068a38229eb27d5b330aae34af906ca682143f39c2bf4b97; TSPD_101_DID=0868f8be6fab280082e241a8cb3d7f2464e5e0bdb96727f5d1e848b7d42863406382fd6654c137284ce47b79d56a928908faaba61f063800a219d45658b4cecbed2420be1c3e20c2a47f2b6a52086441966725f34d02d50d356418de1d1b16c24cf5e3d9630b9c9863b2357102e4a956; TS011f2d1a=01266d26d0cdb19686c5dd89ae3fc0410f7e79f2e5e13c561d3f9b49cbb28cb41b63d937dc3206750f727b2a25474d6367edbe4163; TSPD_101=0868f8be6fab28007d9033747d4358b2c40366c680b7c784ca298aed99c6ed944d54b6f662ac12d03aac426f78cba1d00873b12b4f051800632038aefb659b885ca1732140a3428bba23ce13beb1c95e; SESSION=f1cba717-708a-4115-876c-cd587a2717b8; TS5220f739077=0868f8be6fab28004f38464addee01ad30533cb0026a8c93aadb573b4f7a10780d8ee971bd76ab3fe8f97bb59778c38908c5c5ec20172000a18356ee08bf317b257c5f4620c2b7b4c581a5e6547bbcb60053aa008d5fbfba; TS5220f739029=0868f8be6fab28007bbccfa87bd497f568ba218aef2af94d000c9f5bd816ce59ff1e4891ca30412d0ca0d136db364e6d; TSf1edb2d2027=0868f8be6fab200029398ac152100d7ac3f7f1271f0ecd4786ba7aac34f39eba4c42e38bc314cb6e08a4b6fc6211300098ccd4413fa41b2129f1b767af20c8903fb555d2110fdd4be99530b60ccd98f71ecb58dc7f135aa07c071732fda28de0',
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