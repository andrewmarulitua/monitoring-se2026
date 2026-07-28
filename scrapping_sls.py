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
    'TS00000000076': '0868f8be6fab2800d9c5c068bb077551c93b56ef33587fc6c70e330ed9d2eb4c99216949a6fe8aa20d1851f0516ad0b408cc15058409d0006e1dc396b94f3de8ebe75b8c679c71b00584034032ced9d786d4403f72403c9b1559774b75d4b6f521473601e15e095ede027d737b77f99ffa0f69428767ccd0e82c41f92388b929e406f2e8a6b61744641e5c2830d22ff7329abbc4cdb0835515eaab8bf72dee76c8c58d0a1f9bfc3789ea72c3b63d3fac2067d6e02bbeb0f1ac1ad0d9fe7af5a9352247d616f75949ee752cf1df0dc62cfb95aebbeec48eab7ebe27c893997f50e335dabcdf20ad191ba87a805b0b39a98a85fd898d93f83eabb5cd80445ebf8912eaa0d5f7226475',
    'TSPD_101_DID': '0868f8be6fab2800d9c5c068bb077551c93b56ef33587fc6c70e330ed9d2eb4c99216949a6fe8aa20d1851f0516ad0b408cc1505840638002a0e904edd41e26c5d0ebe818b94d96fff4cd86e60d3986f41000d5a4ad93369ff236d3f8fad12a152b69be79bb80e0d15e0d0db48f32f28',
    'XSRF-TOKEN': '7b1d1551-0e4f-4eb1-8cf0-729434d1c989',
    'db8ca2b43ed851cc93e71fd5fd72bff7': '8cae593523849c29d9b9b503b9b127e2',
    'TS011f2d1a': '01266d26d029eb286edc7523b290ceb9eab1b88bd8843a7556b32cfe7ac5b63f7731ee8e9014d9faf9b8e2bcc3075f04224f49e991',
    'TSPD_101': '0868f8be6fab2800bbbb5fb64a36f170c9ef2fa34bea080340ac7ea50c44e52900680a531984c8a35769532941ea6f180877b43ba6051800057ef445ab2c1c5b5ca1732140a3428bba23ce13beb1c95e',
    'f5avraaaaaaaaaaaaaaaa_session_': 'ODNAEDBBCLJPMODCAMJNJAODCAFMGHNEGHBJJMHEKHLPPOEFOOJDDAAIPPNPOMPNMBKDJCNOGOMFEENFEELACHJGFDHAKEHNKNNILMLMILKHDOHIBCINLIGCEOEENADJ',
    'JSESSIONID': '1C2C002883DE2CF4462552B46420D92A',
    'SESSION': 'c1f2a2cb-d15d-45a7-97a8-028fa81c6131',
    'TS5220f739077': '0868f8be6fab28003b9160e2ba17757e40d6743a4f04bb731f2b2bbd25bf7f0b8396d38a9eb49a0e6a036d0da9a91f9b081cf0f42b1720005229eb46bdcd320ae40881f6c4326107f2edf99940753b4be4e026578e5795ff',
    'TS5220f739029': '0868f8be6fab28001b517da3a99195dd181341ded5d831dceea909fe760bfa5cb9c8993ed9a6797c2791bb4c35820860',
    'TSf1edb2d2027': '0868f8be6fab200056f69d4ef0eb01ba1c5c37eb4a95c38be551a327f0c3d8b44660ffe3f60122ed08739d0b8a11300085e728df11a945e6f97a264c3eea8d64d9288e36d8bc3e00afa547099b24c6c188539759267e2d51bded6399af4cf3d0',
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
    'x-xsrf-token': '7b1d1551-0e4f-4eb1-8cf0-729434d1c989',
    'cookie': 'cf_clearance=HQwIeZ.AS7MaosOLHlONXmzkiqUal.b5qak.8P0X_Z0-1784535547-1.2.1.1-oPdlHNW4C0XrGVjAWY9djxZNUrmPrAVBwqz_o7cR73XAAT_UiwRfnQXD6n_EJQV.MNt8QCZ.nAba9BRJR.WCiuCCqpwUyKo0gV7yNsZ2re15VZlKnIwXsuiTQeIPDsqEsvVaOzF5YWtEAt2fVDu0qmpMNqdo8n__nu0dVZSniyYtXUppOglTQqYZ0nB8ZCZfNrYErNEsHrETnRrMRSxGylfEtdVEdRW7XkO7MfUZD2MhhF11b6XvSrm0YPGNPfNLlUuTtWlr72eJ0.LBhmgCM2QPO2EnlAGfS2YlDzEdJenVct0XJmsFQxac1IPEoklYR4tQUZzzPOC1ABiTVsDYNA; _ga_XXTTVXWHDB=GS2.3.s1785131298$o7$g1$t1785132563$j60$l0$h0; _ga=GA1.1.2055404639.1784774377; _ga_QPPE1C18C5=GS2.1.s1785135144$o3$g1$t1785135282$j60$l0$h0; TS00000000076=0868f8be6fab2800d9c5c068bb077551c93b56ef33587fc6c70e330ed9d2eb4c99216949a6fe8aa20d1851f0516ad0b408cc15058409d0006e1dc396b94f3de8ebe75b8c679c71b00584034032ced9d786d4403f72403c9b1559774b75d4b6f521473601e15e095ede027d737b77f99ffa0f69428767ccd0e82c41f92388b929e406f2e8a6b61744641e5c2830d22ff7329abbc4cdb0835515eaab8bf72dee76c8c58d0a1f9bfc3789ea72c3b63d3fac2067d6e02bbeb0f1ac1ad0d9fe7af5a9352247d616f75949ee752cf1df0dc62cfb95aebbeec48eab7ebe27c893997f50e335dabcdf20ad191ba87a805b0b39a98a85fd898d93f83eabb5cd80445ebf8912eaa0d5f7226475; TSPD_101_DID=0868f8be6fab2800d9c5c068bb077551c93b56ef33587fc6c70e330ed9d2eb4c99216949a6fe8aa20d1851f0516ad0b408cc1505840638002a0e904edd41e26c5d0ebe818b94d96fff4cd86e60d3986f41000d5a4ad93369ff236d3f8fad12a152b69be79bb80e0d15e0d0db48f32f28; XSRF-TOKEN=7b1d1551-0e4f-4eb1-8cf0-729434d1c989; db8ca2b43ed851cc93e71fd5fd72bff7=8cae593523849c29d9b9b503b9b127e2; TS011f2d1a=01266d26d029eb286edc7523b290ceb9eab1b88bd8843a7556b32cfe7ac5b63f7731ee8e9014d9faf9b8e2bcc3075f04224f49e991; TSPD_101=0868f8be6fab2800bbbb5fb64a36f170c9ef2fa34bea080340ac7ea50c44e52900680a531984c8a35769532941ea6f180877b43ba6051800057ef445ab2c1c5b5ca1732140a3428bba23ce13beb1c95e; f5avraaaaaaaaaaaaaaaa_session_=ODNAEDBBCLJPMODCAMJNJAODCAFMGHNEGHBJJMHEKHLPPOEFOOJDDAAIPPNPOMPNMBKDJCNOGOMFEENFEELACHJGFDHAKEHNKNNILMLMILKHDOHIBCINLIGCEOEENADJ; JSESSIONID=1C2C002883DE2CF4462552B46420D92A; SESSION=c1f2a2cb-d15d-45a7-97a8-028fa81c6131; TS5220f739077=0868f8be6fab28003b9160e2ba17757e40d6743a4f04bb731f2b2bbd25bf7f0b8396d38a9eb49a0e6a036d0da9a91f9b081cf0f42b1720005229eb46bdcd320ae40881f6c4326107f2edf99940753b4be4e026578e5795ff; TS5220f739029=0868f8be6fab28001b517da3a99195dd181341ded5d831dceea909fe760bfa5cb9c8993ed9a6797c2791bb4c35820860; TSf1edb2d2027=0868f8be6fab200056f69d4ef0eb01ba1c5c37eb4a95c38be551a327f0c3d8b44660ffe3f60122ed08739d0b8a11300085e728df11a945e6f97a264c3eea8d64d9288e36d8bc3e00afa547099b24c6c188539759267e2d51bded6399af4cf3d0',
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