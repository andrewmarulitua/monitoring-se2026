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
    'f5avraaaaaaaaaaaaaaaa_session_': 'HNBALAKMFJNIGEHDPPDJIFCPPDHDBJNKNNEOJDPKBBCKPGLNNLFGOBIPLCIAFIENNFGDADGKNAOEDBLOAFBAKOMJMFFPAPKEMOPHDGDEDCDKELDANDHMKEOHCCPOMBCM',
    'db8ca2b43ed851cc93e71fd5fd72bff7': '15faddc55339961e726413df06a9e1dc',
    'XSRF-TOKEN': 'ad37e770-b64f-4266-bd87-b9c4f1f4e35a',
    'SESSION': '5b511670-793a-48c6-9b08-7d77d36848db',
    'TS00000000076': '0868f8be6fab2800b062187c839ec54b92f5f02a40a523cdd0dc7d136f335a82364d7e74cc4621185937a37ac65f7f9008092eceb409d000a98f27bb28d0ea97138153cdfb6a78fec8a5198a2b4f3b82e5024b361522f3b897d823cabb9b833a8ff367fb83eb6d9f1db7e0932036ef49f4d5f7c67839cc639217f56abae8e2b011c791a26bf0d7b06bd1fe97ac4e46da96ae6727b0aeffdedacbb71796cb4793898263a2456b7d81f060a16a7af8ba307ee0e036dde05ae97341816cf3d324b243d95ec35ee268b6346c8530164189bb7152b52c7eedfdb306d05acd96377aae7b570cecd9c39b54d47bccde96023e68eda76733ae65dc6d0e2fa44822f361287aadbb4a84615dac',
    'TSPD_101_DID': '0868f8be6fab2800b062187c839ec54b92f5f02a40a523cdd0dc7d136f335a82364d7e74cc4621185937a37ac65f7f9008092eceb40638003926826612646aa26741adaf0bf1e3bc7105ca474ce92366c5f9c71490c3c46a9d3eb1956e51ee575b47e2404649b2c3f1121ece83ffc2de',
    'TS011f2d1a': '01266d26d08c1a57901f27f80c1106b04e39638974c42f804a398adbda728dd9b055e1673535368c012ae297dea0b4754f1d7ec838',
    'TSPD_101': '0868f8be6fab28002369be3285138eff2cf66f3b8dd265422132735757f77c3ab6f215f46d3c22735dd45ae0df8e68a30876ce17f10518000f11481afe7af4475ca1732140a3428bba23ce13beb1c95e',
    'TS5220f739077': '0868f8be6fab28001d5b87bc4f7f429d0d98713589c5d3dfe86b3c4eb1d71761e38c27ce394d217924814aa3a96bdf780829e53ed117200075dab3519e277707b8bd787bddb8aeec4798aab64816ba2b6c836136b953c8a8',
    'TS5220f739029': '0868f8be6fab28005da977c71eacdcfc2125909caeddd12f42b514fc546094295c176069fc411ec8252a6de7cab7ff79',
    'TSf1edb2d2027': '0868f8be6fab200046dd656f3ac01be3cd871990bef9b47b2fb68463b58864426dd3e9c57cf0e56d0860d3fe541130006565bcd28784d1edf3afb9b67346d1896c3a4d95a9a963989c598bfdd0bf3baca22a38f6a0fe9074cf33f470d0264535',
}

headers = {
    'accept': '*/*',
    'accept-language': 'id-ID,id;q=0.9',
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
    'x-xsrf-token': 'ad37e770-b64f-4266-bd87-b9c4f1f4e35a',
    'cookie': 'f5avraaaaaaaaaaaaaaaa_session_=HNBALAKMFJNIGEHDPPDJIFCPPDHDBJNKNNEOJDPKBBCKPGLNNLFGOBIPLCIAFIENNFGDADGKNAOEDBLOAFBAKOMJMFFPAPKEMOPHDGDEDCDKELDANDHMKEOHCCPOMBCM; db8ca2b43ed851cc93e71fd5fd72bff7=15faddc55339961e726413df06a9e1dc; XSRF-TOKEN=ad37e770-b64f-4266-bd87-b9c4f1f4e35a; SESSION=5b511670-793a-48c6-9b08-7d77d36848db; TS00000000076=0868f8be6fab2800b062187c839ec54b92f5f02a40a523cdd0dc7d136f335a82364d7e74cc4621185937a37ac65f7f9008092eceb409d000a98f27bb28d0ea97138153cdfb6a78fec8a5198a2b4f3b82e5024b361522f3b897d823cabb9b833a8ff367fb83eb6d9f1db7e0932036ef49f4d5f7c67839cc639217f56abae8e2b011c791a26bf0d7b06bd1fe97ac4e46da96ae6727b0aeffdedacbb71796cb4793898263a2456b7d81f060a16a7af8ba307ee0e036dde05ae97341816cf3d324b243d95ec35ee268b6346c8530164189bb7152b52c7eedfdb306d05acd96377aae7b570cecd9c39b54d47bccde96023e68eda76733ae65dc6d0e2fa44822f361287aadbb4a84615dac; TSPD_101_DID=0868f8be6fab2800b062187c839ec54b92f5f02a40a523cdd0dc7d136f335a82364d7e74cc4621185937a37ac65f7f9008092eceb40638003926826612646aa26741adaf0bf1e3bc7105ca474ce92366c5f9c71490c3c46a9d3eb1956e51ee575b47e2404649b2c3f1121ece83ffc2de; TS011f2d1a=01266d26d08c1a57901f27f80c1106b04e39638974c42f804a398adbda728dd9b055e1673535368c012ae297dea0b4754f1d7ec838; TSPD_101=0868f8be6fab28002369be3285138eff2cf66f3b8dd265422132735757f77c3ab6f215f46d3c22735dd45ae0df8e68a30876ce17f10518000f11481afe7af4475ca1732140a3428bba23ce13beb1c95e; TS5220f739077=0868f8be6fab28001d5b87bc4f7f429d0d98713589c5d3dfe86b3c4eb1d71761e38c27ce394d217924814aa3a96bdf780829e53ed117200075dab3519e277707b8bd787bddb8aeec4798aab64816ba2b6c836136b953c8a8; TS5220f739029=0868f8be6fab28005da977c71eacdcfc2125909caeddd12f42b514fc546094295c176069fc411ec8252a6de7cab7ff79; TSf1edb2d2027=0868f8be6fab200046dd656f3ac01be3cd871990bef9b47b2fb68463b58864426dd3e9c57cf0e56d0860d3fe541130006565bcd28784d1edf3afb9b67346d1896c3a4d95a9a963989c598bfdd0bf3baca22a38f6a0fe9074cf33f470d0264535',
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