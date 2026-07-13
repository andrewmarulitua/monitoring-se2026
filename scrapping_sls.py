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
    'f5avraaaaaaaaaaaaaaaa_session_': 'NKAEAKEGDDLMJMHEGGHCENOIMOKBDJHGNLJAFCIBHJMEGNJJPCHNMCPICMBEECAIFGMDAJPCANBFHKOLBPAADBIEIHJDEBBEPCLBBOCLLLDMEHJHIHKKMBACMJCKJPPL',
    'cf_clearance': 'F_24x8yTfvl4LTgV2YD0dC65ZoTriIMdodHfnya1tXE-1783921239-1.2.1.1-U8_GjcPoQkuY5tsT2eC_evjxNhMUG1a65PQtWmUdT9ebR52DpxL_INWYoWn8e_o2sxs2MGu_tcqlhMgcV9j65yeWUSGAO0MCmAEq04.cgLkC6Hgl.Yq8Lq1HTh3.BSfmeIkhsr7sHL7Sweb75FMhSi25oPMLB.cN8IWFKkTH0wwlofV41w2nyzqkZNbVtv_t2Fk5WQCg9t1S5pQwfSzc5BSTs.O9iVHkoFTjOVpam_WJOu.elbnEwQOd833cBuiqxlsJEAUmRNCpnlmwqApBi1ngtwC.RuQgjsqXuQXTV1Dbm3yHffVai7FtZ4FbshncQhxZeqD1NMm7SlNtw79s_Q',
    '__cf_bm': 'zPxs5NY_qTtGbxvfAXgx1l5v0FbaT38xdV5kdZvEcLI-1783921239.2507615-1.0.1.1-8h_uX1M6O5KXhDlZC9g93fumkBsLMVIRaeA3kKByrJeToXpZwEySvW7TsQm9cH9kNpmF0G_o955Ht5AfuwP84OKcp5d6y6VX.yXLfqrP4ESqfUZsXZGUy_ZflBtfePSZ',
    '_ga': 'GA1.3.1765036020.1783921242',
    'f5avraaaaaaaaaaaaaaaa_session_': 'FDBEBIPLIAFCCCNKOCJKJAFHOCKMEFDDNBANLKKGNEFDPIOIFIOENKBPPGJHALPNKIGDMFMHKLEJABBNJMMAOLHECHGPKIFIFIDGOCIJDPJBGDPBCOBMJDGOHKOEDCEI',
    'db8ca2b43ed851cc93e71fd5fd72bff7': '6511da30cafb6308f40411f7dd2204a7',
    'XSRF-TOKEN': '46b95e07-a83e-475f-972a-6575d581280c',
    'SESSION': '3dfc7a86-2318-44d9-831c-f5f63b281c84',
    'TS011f2d1a': '01266d26d0122be1d96926918fe2902b417ab9abf4c1601d675d1212712378e5aee3164a9ff27dba21db937ffc1bec497a8335fc67',
    '_ga_XXTTVXWHDB': 'GS2.3.s1783921242$o1$g1$t1783922520$j60$l0$h0',
    'TS00000000076': '0868f8be6fab2800dbd78bc916aa8137f11c689c70bf171ef0af6d50e1a4d491a4a46eb27d4f1d743aa0e3facee277f508467f155809d000dca14197ed658b613055bbd1bb38941be412f175f52514680de10163b0d19c51381ddff52967edebd3200fe30b727fe1ebb978bfe39a0f2606b3525c056646e8f4ecc01a80dce00323594f09a1bd0207391903300feffac15a10485c1c647120b9ad8561c280bdf4c7c30beb5d0887b2ce6863cd18ba1697f28b994cc0f497440b0eeab25652ee60072905746b142965c0f3e3496bc68ed52ebcdc9fc4b79c62dd858c95bcbb6f76dfa1f1a1f392f25239faa2d221be1bc29ce7ba87bc6a18a17075c9d568ac0883217c80aecad99861',
    'TSPD_101_DID': '0868f8be6fab2800dbd78bc916aa8137f11c689c70bf171ef0af6d50e1a4d491a4a46eb27d4f1d743aa0e3facee277f508467f1558063800ee067d35675a3760ccaa5547880ca2979ae8051ce9f463461412c4520536d5da88ba0d50ff5427e4b7e74ac627313a6a0fb21fee969fb175',
    'TSPD_101': '0868f8be6fab2800d04026ebbc09dc17806f111686b23f7769fb56b5635312df5a477f9285d6876d2ce802d902eed5fe08d0a863c50518004c62d71c466a0fc65ca1732140a3428bba23ce13beb1c95e',
    'TS5220f739077': '0868f8be6fab280081ae7025b19c73b08275df316485f9139e402ccdf8e4173dcd02b04088e57666f22da001d833aed8080af69534172000b43c252d8c7ec5d4b3b80b901ddd21988aba443e40de704117892d720c719b6d',
    'TS5220f739029': '0868f8be6fab28004469feb69770dc6a106efdeedd6a17d1333c8f4f7c2a078943e7a6135cd8f50693cde8026132a8cb',
    'TSf1edb2d2027': '0868f8be6fab20006d755400292a6b2b788320fede926163ffe50119361672faa47cb6a515b2af9f088fcee02911300054e9c3125bdc51ff825b032f92d9cae62906daa7d5016c1c54e1d3c5bf3ea21a14e0f74544ada726eb4bbf2ca9ccca91',
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
    'x-xsrf-token': '46b95e07-a83e-475f-972a-6575d581280c',
    'cookie': 'f5avraaaaaaaaaaaaaaaa_session_=NKAEAKEGDDLMJMHEGGHCENOIMOKBDJHGNLJAFCIBHJMEGNJJPCHNMCPICMBEECAIFGMDAJPCANBFHKOLBPAADBIEIHJDEBBEPCLBBOCLLLDMEHJHIHKKMBACMJCKJPPL; cf_clearance=F_24x8yTfvl4LTgV2YD0dC65ZoTriIMdodHfnya1tXE-1783921239-1.2.1.1-U8_GjcPoQkuY5tsT2eC_evjxNhMUG1a65PQtWmUdT9ebR52DpxL_INWYoWn8e_o2sxs2MGu_tcqlhMgcV9j65yeWUSGAO0MCmAEq04.cgLkC6Hgl.Yq8Lq1HTh3.BSfmeIkhsr7sHL7Sweb75FMhSi25oPMLB.cN8IWFKkTH0wwlofV41w2nyzqkZNbVtv_t2Fk5WQCg9t1S5pQwfSzc5BSTs.O9iVHkoFTjOVpam_WJOu.elbnEwQOd833cBuiqxlsJEAUmRNCpnlmwqApBi1ngtwC.RuQgjsqXuQXTV1Dbm3yHffVai7FtZ4FbshncQhxZeqD1NMm7SlNtw79s_Q; __cf_bm=zPxs5NY_qTtGbxvfAXgx1l5v0FbaT38xdV5kdZvEcLI-1783921239.2507615-1.0.1.1-8h_uX1M6O5KXhDlZC9g93fumkBsLMVIRaeA3kKByrJeToXpZwEySvW7TsQm9cH9kNpmF0G_o955Ht5AfuwP84OKcp5d6y6VX.yXLfqrP4ESqfUZsXZGUy_ZflBtfePSZ; _ga=GA1.3.1765036020.1783921242; f5avraaaaaaaaaaaaaaaa_session_=FDBEBIPLIAFCCCNKOCJKJAFHOCKMEFDDNBANLKKGNEFDPIOIFIOENKBPPGJHALPNKIGDMFMHKLEJABBNJMMAOLHECHGPKIFIFIDGOCIJDPJBGDPBCOBMJDGOHKOEDCEI; db8ca2b43ed851cc93e71fd5fd72bff7=6511da30cafb6308f40411f7dd2204a7; XSRF-TOKEN=46b95e07-a83e-475f-972a-6575d581280c; SESSION=3dfc7a86-2318-44d9-831c-f5f63b281c84; TS011f2d1a=01266d26d0122be1d96926918fe2902b417ab9abf4c1601d675d1212712378e5aee3164a9ff27dba21db937ffc1bec497a8335fc67; _ga_XXTTVXWHDB=GS2.3.s1783921242$o1$g1$t1783922520$j60$l0$h0; TS00000000076=0868f8be6fab2800dbd78bc916aa8137f11c689c70bf171ef0af6d50e1a4d491a4a46eb27d4f1d743aa0e3facee277f508467f155809d000dca14197ed658b613055bbd1bb38941be412f175f52514680de10163b0d19c51381ddff52967edebd3200fe30b727fe1ebb978bfe39a0f2606b3525c056646e8f4ecc01a80dce00323594f09a1bd0207391903300feffac15a10485c1c647120b9ad8561c280bdf4c7c30beb5d0887b2ce6863cd18ba1697f28b994cc0f497440b0eeab25652ee60072905746b142965c0f3e3496bc68ed52ebcdc9fc4b79c62dd858c95bcbb6f76dfa1f1a1f392f25239faa2d221be1bc29ce7ba87bc6a18a17075c9d568ac0883217c80aecad99861; TSPD_101_DID=0868f8be6fab2800dbd78bc916aa8137f11c689c70bf171ef0af6d50e1a4d491a4a46eb27d4f1d743aa0e3facee277f508467f1558063800ee067d35675a3760ccaa5547880ca2979ae8051ce9f463461412c4520536d5da88ba0d50ff5427e4b7e74ac627313a6a0fb21fee969fb175; TSPD_101=0868f8be6fab2800d04026ebbc09dc17806f111686b23f7769fb56b5635312df5a477f9285d6876d2ce802d902eed5fe08d0a863c50518004c62d71c466a0fc65ca1732140a3428bba23ce13beb1c95e; TS5220f739077=0868f8be6fab280081ae7025b19c73b08275df316485f9139e402ccdf8e4173dcd02b04088e57666f22da001d833aed8080af69534172000b43c252d8c7ec5d4b3b80b901ddd21988aba443e40de704117892d720c719b6d; TS5220f739029=0868f8be6fab28004469feb69770dc6a106efdeedd6a17d1333c8f4f7c2a078943e7a6135cd8f50693cde8026132a8cb; TSf1edb2d2027=0868f8be6fab20006d755400292a6b2b788320fede926163ffe50119361672faa47cb6a515b2af9f088fcee02911300054e9c3125bdc51ff825b032f92d9cae62906daa7d5016c1c54e1d3c5bf3ea21a14e0f74544ada726eb4bbf2ca9ccca91',
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