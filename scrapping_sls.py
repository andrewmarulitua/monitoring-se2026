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
    '_ga_XXTTVXWHDB': 'GS2.3.s1784708876$o6$g0$t1784708876$j60$l0$h0',
    '_ga': 'GA1.1.2055404639.1784774377',
    '_ga_QPPE1C18C5': 'GS2.1.s1784786369$o2$g0$t1784786369$j60$l0$h0',
    'TS00000000076': '0868f8be6fab280017b84a0bac856aa510bce9fe61b958e0781129a6c6eb7e6ca269b43cd42e316b43f37de9a83031e008f59df6d009d000e10383de2e87e892790e9135abdad3f3599d671ac9dc751808df5b1d7e165a9f415118117472ec28c09eb2ef98c9cfacf492e22b824f7c2b49bd7dd0a9f49151d8ea626e2fbaff42bd4ffd793e31d101c26cb4f40a8921e838691a0378cd5e290975623f04a570df515185555b45355774704e6e5fa240a8097c6a661f8737bfaa33208bac63d9ccc0b96ba01f8c96a07a60485cea63e00ca9aa78394f2bd7ba0a5ae16885a26b361aba3760a9825e9f064f9d66f3adb3a6191c192153912a9a2c5f67b0c0a11c8ce3fb3c2313ae92b3',
    'TSPD_101_DID': '0868f8be6fab280017b84a0bac856aa510bce9fe61b958e0781129a6c6eb7e6ca269b43cd42e316b43f37de9a83031e008f59df6d006380054085aeea08c01f9fe193e3b77946a66727786e0d0bc2f4970a32fdeb258bd8c1ec404aa3fcaff52a2ff63759a20cbf5ba7577a8abacef1d',
    'XSRF-TOKEN': '057d88db-c923-4df5-96e1-dbe0114674f6',
    'db8ca2b43ed851cc93e71fd5fd72bff7': '3649692ecd2a922e0639747ce2ceef1a',
    'TS011f2d1a': '01266d26d0c52d14d09eaf5dabd8e12fdcf01ce793052a3def2179dc02f1afa1a06d32db77c2f924be93afa9e6bce6f9be6463da30',
    'TSPD_101': '0868f8be6fab2800b419f84c4d30a2e1d6ba8d32f60f02ae20392b224c11dbf7bac318d8c1cdba4b503758e2fc2ff2f20894cef3e0051800457999ad8785f7a95ca1732140a3428bba23ce13beb1c95e',
    'f5avraaaaaaaaaaaaaaaa_session_': 'NKCOMEOGHJJBDCBPIGBGBAEOLKGAFPHOHGAEHIDPIAFFPCDECMJDPDDNGPHANMCABHODLNHCNHBAGNLDFKPAPAJLMLNGLJJHKJOCBBBJBGPAJCEGOIEOMIMCHDCFPFID',
    'JSESSIONID': 'F68BF574CD4B975E821E6435C574AFA4',
    'SESSION': '97b09ade-9066-4846-9416-88b20b8360a0',
    'TS5220f739077': '0868f8be6fab2800bf4c7c494a07e0eedebcfb6452229c1b205c494c62f790a249037f3e4a416ab9572e35d74ca0e8bc087cdbbe79172000c05273d9dd2a75bb04d5d0b458431beb933ae28af87f5ac2ba6db633e60f1e29',
    'TS5220f739029': '0868f8be6fab2800093c04a6b220bf10e35cbf617c5fc1259f8c6a30c2468ea59db90b5784a4958233d6f46383a0c9c4',
    'TSf1edb2d2027': '0868f8be6fab2000c63c95fe17f1c748415b480e4559587a51426e429ba42bc77da33b400fc0eb62083c1c1275113000043bdb7ee2a11f013de1204214bf59df7dd457c8d79e28aba79b41bdb41a8e05bcfbee1cc7fcc31c9b9259474daa9309',
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
    'x-xsrf-token': '057d88db-c923-4df5-96e1-dbe0114674f6',
    'cookie': 'cf_clearance=HQwIeZ.AS7MaosOLHlONXmzkiqUal.b5qak.8P0X_Z0-1784535547-1.2.1.1-oPdlHNW4C0XrGVjAWY9djxZNUrmPrAVBwqz_o7cR73XAAT_UiwRfnQXD6n_EJQV.MNt8QCZ.nAba9BRJR.WCiuCCqpwUyKo0gV7yNsZ2re15VZlKnIwXsuiTQeIPDsqEsvVaOzF5YWtEAt2fVDu0qmpMNqdo8n__nu0dVZSniyYtXUppOglTQqYZ0nB8ZCZfNrYErNEsHrETnRrMRSxGylfEtdVEdRW7XkO7MfUZD2MhhF11b6XvSrm0YPGNPfNLlUuTtWlr72eJ0.LBhmgCM2QPO2EnlAGfS2YlDzEdJenVct0XJmsFQxac1IPEoklYR4tQUZzzPOC1ABiTVsDYNA; _ga_XXTTVXWHDB=GS2.3.s1784708876$o6$g0$t1784708876$j60$l0$h0; _ga=GA1.1.2055404639.1784774377; _ga_QPPE1C18C5=GS2.1.s1784786369$o2$g0$t1784786369$j60$l0$h0; TS00000000076=0868f8be6fab280017b84a0bac856aa510bce9fe61b958e0781129a6c6eb7e6ca269b43cd42e316b43f37de9a83031e008f59df6d009d000e10383de2e87e892790e9135abdad3f3599d671ac9dc751808df5b1d7e165a9f415118117472ec28c09eb2ef98c9cfacf492e22b824f7c2b49bd7dd0a9f49151d8ea626e2fbaff42bd4ffd793e31d101c26cb4f40a8921e838691a0378cd5e290975623f04a570df515185555b45355774704e6e5fa240a8097c6a661f8737bfaa33208bac63d9ccc0b96ba01f8c96a07a60485cea63e00ca9aa78394f2bd7ba0a5ae16885a26b361aba3760a9825e9f064f9d66f3adb3a6191c192153912a9a2c5f67b0c0a11c8ce3fb3c2313ae92b3; TSPD_101_DID=0868f8be6fab280017b84a0bac856aa510bce9fe61b958e0781129a6c6eb7e6ca269b43cd42e316b43f37de9a83031e008f59df6d006380054085aeea08c01f9fe193e3b77946a66727786e0d0bc2f4970a32fdeb258bd8c1ec404aa3fcaff52a2ff63759a20cbf5ba7577a8abacef1d; XSRF-TOKEN=057d88db-c923-4df5-96e1-dbe0114674f6; db8ca2b43ed851cc93e71fd5fd72bff7=3649692ecd2a922e0639747ce2ceef1a; TS011f2d1a=01266d26d0c52d14d09eaf5dabd8e12fdcf01ce793052a3def2179dc02f1afa1a06d32db77c2f924be93afa9e6bce6f9be6463da30; TSPD_101=0868f8be6fab2800b419f84c4d30a2e1d6ba8d32f60f02ae20392b224c11dbf7bac318d8c1cdba4b503758e2fc2ff2f20894cef3e0051800457999ad8785f7a95ca1732140a3428bba23ce13beb1c95e; f5avraaaaaaaaaaaaaaaa_session_=NKCOMEOGHJJBDCBPIGBGBAEOLKGAFPHOHGAEHIDPIAFFPCDECMJDPDDNGPHANMCABHODLNHCNHBAGNLDFKPAPAJLMLNGLJJHKJOCBBBJBGPAJCEGOIEOMIMCHDCFPFID; JSESSIONID=F68BF574CD4B975E821E6435C574AFA4; SESSION=97b09ade-9066-4846-9416-88b20b8360a0; TS5220f739077=0868f8be6fab2800bf4c7c494a07e0eedebcfb6452229c1b205c494c62f790a249037f3e4a416ab9572e35d74ca0e8bc087cdbbe79172000c05273d9dd2a75bb04d5d0b458431beb933ae28af87f5ac2ba6db633e60f1e29; TS5220f739029=0868f8be6fab2800093c04a6b220bf10e35cbf617c5fc1259f8c6a30c2468ea59db90b5784a4958233d6f46383a0c9c4; TSf1edb2d2027=0868f8be6fab2000c63c95fe17f1c748415b480e4559587a51426e429ba42bc77da33b400fc0eb62083c1c1275113000043bdb7ee2a11f013de1204214bf59df7dd457c8d79e28aba79b41bdb41a8e05bcfbee1cc7fcc31c9b9259474daa9309',
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