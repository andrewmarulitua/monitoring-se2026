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
    'XSRF-TOKEN': 'e184bafb-7cfa-4485-8e7e-66c8af76a0a6',
    'db8ca2b43ed851cc93e71fd5fd72bff7': '8a46504d2a485aec98268ce2e16d88fd',
    'SESSION': '504f1c52-0487-4248-8974-f5d2ac0ca197',
    'f5avraaaaaaaaaaaaaaaa_session_': 'KFGFNPPNILGGEOBHNLBPBIDFGEPOPCBJCCFFDAIADDAFBALBKKDBAEDHOOCHONOKFKADJMBKANOAOAFDCMPAHNJFFJDFKIPMNOGNCLBIMLKLEOGKNNOKEFKJEBNGDJAK',
    'TS011f2d1a': '01266d26d05318128e827c1e3b3babb72e5011f03ce52a4758a959bcec49b1fee95816d1e04d15ed428aea3fdf3565cb2c0d8d3128',
    'TS00000000076': '0868f8be6fab280016def2036488872ebf776a4d0e26dc8d2c9aaa1f1ddc762940a3253490b0640eb0327706472603c008f977b97609d000f56756ea1c1d9773bb3a5c967a668f4fcdbed1465d8706e16115bb83ba3be74d63205ad5ba2dacc9040a8aeaa17059d1be9115ca3c142e19ab9bd00e31c23c2cc4961c7cbdd1fa719ee9fefd1d717f7a2e47f8214a1d0fbf82c4d0b58c2383fb8de2cbc0ccdb9b1de91f6830c595c29aaabe0be678b4c719afbb61bda1447a6847bd3a3cc8eaee7eff222331f4c01e09f219cce0d6c7ca99eb11253c9f3b4bd3cf549102c91228df4f5ae13319d4e7f84128b478631ff39f43977cb33aff48bf67839733036e6e4d9dbf216c28bfe1ae',
    'TSPD_101_DID': '0868f8be6fab280016def2036488872ebf776a4d0e26dc8d2c9aaa1f1ddc762940a3253490b0640eb0327706472603c008f977b97606380011ad98e9abba1f25b2fd6b6ee521e7cbdde8dcf3142bd3e62e1f797fc4c9505e6b01ce6768f74eadf23c5f7cddddca8c60d188eae82a91e5',
    'TSPD_101': '0868f8be6fab28007601887ecb1810a7e2714e1ed7b1c900ee10e3f2d6575874f6c2049d77ebbe45abf1bdaf9942b64508bd2a63620518009d65db537609a85c5ca1732140a3428bba23ce13beb1c95e',
    'TS5220f739077': '0868f8be6fab2800455c1adb9b84b52461bb2357b5d39f72516fb69b41371d71d1fd4eb83d671b4fa55c6550d0588f9408489fe33b172000a9252593459538aa75f64fb3352d772e77431938218eaeca2e6d6950270e56e7',
    'TS5220f739029': '0868f8be6fab28009d9fec0e6323ae4b306c66277a44273f67f84a9d22fffa4327538957f2c3d792ead46e17772005d4',
    'TSf1edb2d2027': '0868f8be6fab200017541889e3213b9bb98cbaf10880efd5543680a22c462c068d814674451c2ba308df6b0d76113000ca62236a2667b1e5991537749fd7e1ddda9fe8d4c704565382bea82f8129edbac46bc8610c527a0f3f682157f56ddb8c',
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
    'x-xsrf-token': 'e184bafb-7cfa-4485-8e7e-66c8af76a0a6',
    'cookie': 'XSRF-TOKEN=e184bafb-7cfa-4485-8e7e-66c8af76a0a6; db8ca2b43ed851cc93e71fd5fd72bff7=8a46504d2a485aec98268ce2e16d88fd; SESSION=504f1c52-0487-4248-8974-f5d2ac0ca197; f5avraaaaaaaaaaaaaaaa_session_=KFGFNPPNILGGEOBHNLBPBIDFGEPOPCBJCCFFDAIADDAFBALBKKDBAEDHOOCHONOKFKADJMBKANOAOAFDCMPAHNJFFJDFKIPMNOGNCLBIMLKLEOGKNNOKEFKJEBNGDJAK; TS011f2d1a=01266d26d05318128e827c1e3b3babb72e5011f03ce52a4758a959bcec49b1fee95816d1e04d15ed428aea3fdf3565cb2c0d8d3128; TS00000000076=0868f8be6fab280016def2036488872ebf776a4d0e26dc8d2c9aaa1f1ddc762940a3253490b0640eb0327706472603c008f977b97609d000f56756ea1c1d9773bb3a5c967a668f4fcdbed1465d8706e16115bb83ba3be74d63205ad5ba2dacc9040a8aeaa17059d1be9115ca3c142e19ab9bd00e31c23c2cc4961c7cbdd1fa719ee9fefd1d717f7a2e47f8214a1d0fbf82c4d0b58c2383fb8de2cbc0ccdb9b1de91f6830c595c29aaabe0be678b4c719afbb61bda1447a6847bd3a3cc8eaee7eff222331f4c01e09f219cce0d6c7ca99eb11253c9f3b4bd3cf549102c91228df4f5ae13319d4e7f84128b478631ff39f43977cb33aff48bf67839733036e6e4d9dbf216c28bfe1ae; TSPD_101_DID=0868f8be6fab280016def2036488872ebf776a4d0e26dc8d2c9aaa1f1ddc762940a3253490b0640eb0327706472603c008f977b97606380011ad98e9abba1f25b2fd6b6ee521e7cbdde8dcf3142bd3e62e1f797fc4c9505e6b01ce6768f74eadf23c5f7cddddca8c60d188eae82a91e5; TSPD_101=0868f8be6fab28007601887ecb1810a7e2714e1ed7b1c900ee10e3f2d6575874f6c2049d77ebbe45abf1bdaf9942b64508bd2a63620518009d65db537609a85c5ca1732140a3428bba23ce13beb1c95e; TS5220f739077=0868f8be6fab2800455c1adb9b84b52461bb2357b5d39f72516fb69b41371d71d1fd4eb83d671b4fa55c6550d0588f9408489fe33b172000a9252593459538aa75f64fb3352d772e77431938218eaeca2e6d6950270e56e7; TS5220f739029=0868f8be6fab28009d9fec0e6323ae4b306c66277a44273f67f84a9d22fffa4327538957f2c3d792ead46e17772005d4; TSf1edb2d2027=0868f8be6fab200017541889e3213b9bb98cbaf10880efd5543680a22c462c068d814674451c2ba308df6b0d76113000ca62236a2667b1e5991537749fd7e1ddda9fe8d4c704565382bea82f8129edbac46bc8610c527a0f3f682157f56ddb8c',
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