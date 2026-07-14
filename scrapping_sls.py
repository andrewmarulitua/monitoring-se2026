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
    'cf_clearance': 'F_24x8yTfvl4LTgV2YD0dC65ZoTriIMdodHfnya1tXE-1783921239-1.2.1.1-U8_GjcPoQkuY5tsT2eC_evjxNhMUG1a65PQtWmUdT9ebR52DpxL_INWYoWn8e_o2sxs2MGu_tcqlhMgcV9j65yeWUSGAO0MCmAEq04.cgLkC6Hgl.Yq8Lq1HTh3.BSfmeIkhsr7sHL7Sweb75FMhSi25oPMLB.cN8IWFKkTH0wwlofV41w2nyzqkZNbVtv_t2Fk5WQCg9t1S5pQwfSzc5BSTs.O9iVHkoFTjOVpam_WJOu.elbnEwQOd833cBuiqxlsJEAUmRNCpnlmwqApBi1ngtwC.RuQgjsqXuQXTV1Dbm3yHffVai7FtZ4FbshncQhxZeqD1NMm7SlNtw79s_Q',
    '_ga': 'GA1.3.1765036020.1783921242',
    '_ga_XXTTVXWHDB': 'GS2.3.s1783921242$o1$g1$t1783922520$j60$l0$h0',
    'f5avraaaaaaaaaaaaaaaa_session_': 'CCOOLOEECKECJPOMPPBGLOGNDMOGBNCLEOKIDEMNNOOPMLIMLBMGADFAFGIGJNEAPCADKBU65INNXNQYFK5WO5KI4UKDJV7XVVUJ36UCVRCQLGYW7ST7IFNM6ZWHASIM',
    'TS00000000076': '0868f8be6fab28003885c1dcab7ca435f9b7a831cce1b90d0ead73276a6fb812785527fd285eb990e124774bdfdd1bfe088a1e3aca09d000c973d09470ab37e6569ae671a62fdbaa9f15b3d2b435dcd5cea8420a183c1b4874514d4d8d65f2c0d2e4b5f766b0568b9d5f15b1a1b1d8e6e4bec0cfcf59eea433f80af48e8e8966c67cdfa91a8b2486a13e80bbd307629a1213e6c7dd1333f9377673efc1537430ebbea01127a1b149eb5f5685c29e468664bca278c7ae7a548e51e815711a17a3ea43cfe3a385af59c02995e6e3d0cedcb4260eaa444bdaa4cce8e1c2be6127661adc2a998fc6caac55acdb455744fe0fe25cab1a0DcJHrrHSgvFpsYxqb6g97uaQTd2kE31rPUeDZTeDsjVq',
    'TSPD_101_DID': '0868f8be6fab28003885c1dcab7ca435f9b7a831cce1b90d0ead73276a6fb812785527fd285eb990e124774bdfdd1bfe088a1e3aca063800ee4c0c2c3284ea3cc95bebc0e704afe241a8ab716a7eb34b0b0df5dc6b4de1dc0187b80009b32c6c4621569319c88d7045b322c78bc6ef3a',
    'db8ca2b43ed851cc93e71fd5fd72bff7': 'a51d57045a670f057f2b728e7eafbdc8',
    'TS011f2d1a': '01266d26d093c34c538164b0139533912914e528ac402490867dcaccb3e0f8f752da6c3186ddac1605d1e3c4b7e3f803c49762103f',
    'TSPD_101': '0868f8be6fab28009470fad36fd60b542d1bc82592d1b3b78fa07e78c4e928ea86e28731b54159f309f48df5556a0850083c43868e05180038de9186632226035ca1732140a3428bba23ce13beb1c95e',
    'XSRF-TOKEN': '7dd8e47d-147d-4cf1-93db-59ab7d55e623',
    'SESSION': '983a3647-f446-4254-ba5c-5c87f1d30a07',
    'TS5220f739077': '0868f8be6fab28003092f17c3acf9a41b9f3602c13f533f3a74290afedb6cd6dccdcb8a94f910f7c0a4c9ddd087006b208b2fd1fdb172000ba0107cc1cec5d7621983f7930f11ac145f3314f2003ec7f8b56f0333cc3e935',
    'TS5220f739029': '0868f8be6fab280031d2e2bca046e81aad5b794a5d82b458f23b2e7e4f1407b82c460e334890cc0d8e42a1978c6b1f31',
    'TSf1edb2d2027': '0868f8be6fab20006da31f87e1f72dd4b4dceaf192cf205489bd817150a32a7759ab5b4da3c7a264083fef689211300052f32870c3bee35f5208efdff0081d0aba26e4019b6d7315c1a73a223f70d947580057faa5482777ccccec4f1df6ed50',
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
    'x-xsrf-token': '7dd8e47d-147d-4cf1-93db-59ab7d55e623',
    'cookie': 'cf_clearance=F_24x8yTfvl4LTgV2YD0dC65ZoTriIMdodHfnya1tXE-1783921239-1.2.1.1-U8_GjcPoQkuY5tsT2eC_evjxNhMUG1a65PQtWmUdT9ebR52DpxL_INWYoWn8e_o2sxs2MGu_tcqlhMgcV9j65yeWUSGAO0MCmAEq04.cgLkC6Hgl.Yq8Lq1HTh3.BSfmeIkhsr7sHL7Sweb75FMhSi25oPMLB.cN8IWFKkTH0wwlofV41w2nyzqkZNbVtv_t2Fk5WQCg9t1S5pQwfSzc5BSTs.O9iVHkoFTjOVpam_WJOu.elbnEwQOd833cBuiqxlsJEAUmRNCpnlmwqApBi1ngtwC.RuQgjsqXuQXTV1Dbm3yHffVai7FtZ4FbshncQhxZeqD1NMm7SlNtw79s_Q; _ga=GA1.3.1765036020.1783921242; _ga_XXTTVXWHDB=GS2.3.s1783921242$o1$g1$t1783922520$j60$l0$h0; f5avraaaaaaaaaaaaaaaa_session_=CCOOLOEECKECJPOMPPBGLOGNDMOGBNCLEOKIDEMNNOOPMLIMLBMGADFAFGIGJNEAPCADKBU65INNXNQYFK5WO5KI4UKDJV7XVVUJ36UCVRCQLGYW7ST7IFNM6ZWHASIM; TS00000000076=0868f8be6fab28003885c1dcab7ca435f9b7a831cce1b90d0ead73276a6fb812785527fd285eb990e124774bdfdd1bfe088a1e3aca09d000c973d09470ab37e6569ae671a62fdbaa9f15b3d2b435dcd5cea8420a183c1b4874514d4d8d65f2c0d2e4b5f766b0568b9d5f15b1a1b1d8e6e4bec0cfcf59eea433f80af48e8e8966c67cdfa91a8b2486a13e80bbd307629a1213e6c7dd1333f9377673efc1537430ebbea01127a1b149eb5f5685c29e468664bca278c7ae7a548e51e815711a17a3ea43cfe3a385af59c02995e6e3d0cedcb4260eaa444bdaa4cce8e1c2be6127661adc2a998fc6caac55acdb455744fe0fe25cab1a0DcJHrrHSgvFpsYxqb6g97uaQTd2kE31rPUeDZTeDsjVq; TSPD_101_DID=0868f8be6fab28003885c1dcab7ca435f9b7a831cce1b90d0ead73276a6fb812785527fd285eb990e124774bdfdd1bfe088a1e3aca063800ee4c0c2c3284ea3cc95bebc0e704afe241a8ab716a7eb34b0b0df5dc6b4de1dc0187b80009b32c6c4621569319c88d7045b322c78bc6ef3a; db8ca2b43ed851cc93e71fd5fd72bff7=a51d57045a670f057f2b728e7eafbdc8; TS011f2d1a=01266d26d093c34c538164b0139533912914e528ac402490867dcaccb3e0f8f752da6c3186ddac1605d1e3c4b7e3f803c49762103f; TSPD_101=0868f8be6fab28009470fad36fd60b542d1bc82592d1b3b78fa07e78c4e928ea86e28731b54159f309f48df5556a0850083c43868e05180038de9186632226035ca1732140a3428bba23ce13beb1c95e; XSRF-TOKEN=7dd8e47d-147d-4cf1-93db-59ab7d55e623; SESSION=983a3647-f446-4254-ba5c-5c87f1d30a07; TS5220f739077=0868f8be6fab28003092f17c3acf9a41b9f3602c13f533f3a74290afedb6cd6dccdcb8a94f910f7c0a4c9ddd087006b208b2fd1fdb172000ba0107cc1cec5d7621983f7930f11ac145f3314f2003ec7f8b56f0333cc3e935; TS5220f739029=0868f8be6fab280031d2e2bca046e81aad5b794a5d82b458f23b2e7e4f1407b82c460e334890cc0d8e42a1978c6b1f31; TSf1edb2d2027=0868f8be6fab20006da31f87e1f72dd4b4dceaf192cf205489bd817150a32a7759ab5b4da3c7a264083fef689211300052f32870c3bee35f5208efdff0081d0aba26e4019b6d7315c1a73a223f70d947580057faa5482777ccccec4f1df6ed50',
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