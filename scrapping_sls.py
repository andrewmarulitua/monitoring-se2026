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
    'f5avraaaaaaaaaaaaaaaa_session_': 'IANDMONHPEEKMDPHMKIHDDAIEDHEAIHJCBLINOHDOLMMDOAMOBBOFCFKIJLICFBBMEMDPEELLNHJIDMHFKLAHIAAFJLHIFBEDPIAFDDBDLEJNNKBGGEBNGAGHBKPFALG',
    'cf_clearance': 'HQwIeZ.AS7MaosOLHlONXmzkiqUal.b5qak.8P0X_Z0-1784535547-1.2.1.1-oPdlHNW4C0XrGVjAWY9djxZNUrmPrAVBwqz_o7cR73XAAT_UiwRfnQXD6n_EJQV.MNt8QCZ.nAba9BRJR.WCiuCCqpwUyKo0gV7yNsZ2re15VZlKnIwXsuiTQeIPDsqEsvVaOzF5YWtEAt2fVDu0qmpMNqdo8n__nu0dVZSniyYtXUppOglTQqYZ0nB8ZCZfNrYErNEsHrETnRrMRSxGylfEtdVEdRW7XkO7MfUZD2MhhF11b6XvSrm0YPGNPfNLlUuTtWlr72eJ0.LBhmgCM2QPO2EnlAGfS2YlDzEdJenVct0XJmsFQxac1IPEoklYR4tQUZzzPOC1ABiTVsDYNA',
    '_ga_XXTTVXWHDB': 'GS2.3.s1784708876$o6$g0$t1784708876$j60$l0$h0',
    '_ga': 'GA1.1.2055404639.1784774377',
    '_ga_QPPE1C18C5': 'GS2.1.s1784786369$o2$g0$t1784786369$j60$l0$h0',
    'XSRF-TOKEN': '64e6a693-f81f-4527-a580-79dfe36bdb5e',
    'db8ca2b43ed851cc93e71fd5fd72bff7': '83880ff33c67e214c4462679ca4ee144',
    'TS011f2d1a': '01266d26d0cf35e82868ad812d6569313a22d3fab6f2023453c753591524a35f992fbbc109df8f053e82c082dda78c7be69e7e7c02',
    'TS00000000076': '0868f8be6fab2800b397c93fa074e20e47de4165726575a19d86fe5da74d53f76f7c7f3310ddbe90e87d1bb859d43e56085b6918d209d000125d57c88cd29c56b8c71d148a2d6b0194531a3f5499f296a1db992ba66f731ba5183409340e67cbadbd8c091b7b49a91e895f617acb3f051516d774ad298fab63046c79546a80a48a9d6883a17d368cead80586337776662d0c9fd2d2de810cb16a0d32a9ab0ede705b5c067fb68b482522662a6fd4ee1e56dace3d3b88eae02adb2456cb4447122fd526a1887b37808d7a7189026b797724d868371eeb289ef91e68d6ab28f129974e17d9708abd9f840cd3657edd172fe3a9085a58edf15a24858f55dce5760ecb7e14d126f3624b',
    'TSPD_101_DID': '0868f8be6fab2800b397c93fa074e20e47de4165726575a19d86fe5da74d53f76f7c7f3310ddbe90e87d1bb859d43e56085b6918d206380092e1a3928ab838ed9c033180e0638f0a6e15c556898997a7b30d62e04de2199dc4db60424a531cc4f77f03fac9d1bae07b5a719b5e203cee',
    'TSPD_101': '0868f8be6fab2800e586217d609e3bdf05de6530002bd7be70fbf164848a8fd131e7dde7a656e0c0c8946041f8f8113e08cb74e7aa051800ac67fc624dd4e8835ca1732140a3428bba23ce13beb1c95e',
    'JSESSIONID': '4680EFD41CCFF76720BAF1B95889AF44',
    'SESSION': '545c1f42-d94e-4306-b282-7e7e7a7ac44a',
    'f5avraaaaaaaaaaaaaaaa_session_': 'BCPAPLNDFAKMBFIMCHGFHNFOHIBBNLCCBGCFNGHFDMMMEOMKPKIDGGOIDNNEBGGLMKMDGICAOMLLMKDKMGKABOJKNJFKJLGNLABCDNOANAFFNAJFMKOJPMIJLEKIJOJI',
    'TS5220f739077': '0868f8be6fab28003075a87ac2bdd7c04ce34b377088ebb679bfec596a474fcf9c95066573be0efa7633cb61df4d760c08ba13b153172000c28f8cfd4afe0935584daeac0b9fe9826e582850650c828163e580656f589e3a',
    'TS5220f739029': '0868f8be6fab280075353c54d2d313f2a0f5514f63e4242d5aa79e7e0d6d9510b472739758dd71a2cdf67430bc78d6ff',
    'TSf1edb2d2027': '0868f8be6fab20008ad4811696282079549fd9868dc5aea7f97e7fe61dbb11d380d874674fc7e4ea081764fe05113000c4f8971a5d66d756cddae8b75eb4ae5c80b2610d28b43d050ec182dfee42156f0ddd2384ecabe4047a8ae9a2318700db',
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
    'x-xsrf-token': '64e6a693-f81f-4527-a580-79dfe36bdb5e',
    # 'cookie': 'f5avraaaaaaaaaaaaaaaa_session_=IANDMONHPEEKMDPHMKIHDDAIEDHEAIHJCBLINOHDOLMMDOAMOBBOFCFKIJLICFBBMEMDPEELLNHJIDMHFKLAHIAAFJLHIFBEDPIAFDDBDLEJNNKBGGEBNGAGHBKPFALG; cf_clearance=HQwIeZ.AS7MaosOLHlONXmzkiqUal.b5qak.8P0X_Z0-1784535547-1.2.1.1-oPdlHNW4C0XrGVjAWY9djxZNUrmPrAVBwqz_o7cR73XAAT_UiwRfnQXD6n_EJQV.MNt8QCZ.nAba9BRJR.WCiuCCqpwUyKo0gV7yNsZ2re15VZlKnIwXsuiTQeIPDsqEsvVaOzF5YWtEAt2fVDu0qmpMNqdo8n__nu0dVZSniyYtXUppOglTQqYZ0nB8ZCZfNrYErNEsHrETnRrMRSxGylfEtdVEdRW7XkO7MfUZD2MhhF11b6XvSrm0YPGNPfNLlUuTtWlr72eJ0.LBhmgCM2QPO2EnlAGfS2YlDzEdJenVct0XJmsFQxac1IPEoklYR4tQUZzzPOC1ABiTVsDYNA; _ga_XXTTVXWHDB=GS2.3.s1784708876$o6$g0$t1784708876$j60$l0$h0; _ga=GA1.1.2055404639.1784774377; _ga_QPPE1C18C5=GS2.1.s1784786369$o2$g0$t1784786369$j60$l0$h0; XSRF-TOKEN=64e6a693-f81f-4527-a580-79dfe36bdb5e; db8ca2b43ed851cc93e71fd5fd72bff7=83880ff33c67e214c4462679ca4ee144; TS011f2d1a=01266d26d0cf35e82868ad812d6569313a22d3fab6f2023453c753591524a35f992fbbc109df8f053e82c082dda78c7be69e7e7c02; TS00000000076=0868f8be6fab2800b397c93fa074e20e47de4165726575a19d86fe5da74d53f76f7c7f3310ddbe90e87d1bb859d43e56085b6918d209d000125d57c88cd29c56b8c71d148a2d6b0194531a3f5499f296a1db992ba66f731ba5183409340e67cbadbd8c091b7b49a91e895f617acb3f051516d774ad298fab63046c79546a80a48a9d6883a17d368cead80586337776662d0c9fd2d2de810cb16a0d32a9ab0ede705b5c067fb68b482522662a6fd4ee1e56dace3d3b88eae02adb2456cb4447122fd526a1887b37808d7a7189026b797724d868371eeb289ef91e68d6ab28f129974e17d9708abd9f840cd3657edd172fe3a9085a58edf15a24858f55dce5760ecb7e14d126f3624b; TSPD_101_DID=0868f8be6fab2800b397c93fa074e20e47de4165726575a19d86fe5da74d53f76f7c7f3310ddbe90e87d1bb859d43e56085b6918d206380092e1a3928ab838ed9c033180e0638f0a6e15c556898997a7b30d62e04de2199dc4db60424a531cc4f77f03fac9d1bae07b5a719b5e203cee; TSPD_101=0868f8be6fab2800e586217d609e3bdf05de6530002bd7be70fbf164848a8fd131e7dde7a656e0c0c8946041f8f8113e08cb74e7aa051800ac67fc624dd4e8835ca1732140a3428bba23ce13beb1c95e; JSESSIONID=4680EFD41CCFF76720BAF1B95889AF44; SESSION=545c1f42-d94e-4306-b282-7e7e7a7ac44a; f5avraaaaaaaaaaaaaaaa_session_=BCPAPLNDFAKMBFIMCHGFHNFOHIBBNLCCBGCFNGHFDMMMEOMKPKIDGGOIDNNEBGGLMKMDGICAOMLLMKDKMGKABOJKNJFKJLGNLABCDNOANAFFNAJFMKOJPMIJLEKIJOJI; TS5220f739077=0868f8be6fab28003075a87ac2bdd7c04ce34b377088ebb679bfec596a474fcf9c95066573be0efa7633cb61df4d760c08ba13b153172000c28f8cfd4afe0935584daeac0b9fe9826e582850650c828163e580656f589e3a; TS5220f739029=0868f8be6fab280075353c54d2d313f2a0f5514f63e4242d5aa79e7e0d6d9510b472739758dd71a2cdf67430bc78d6ff; TSf1edb2d2027=0868f8be6fab20008ad4811696282079549fd9868dc5aea7f97e7fe61dbb11d380d874674fc7e4ea081764fe05113000c4f8971a5d66d756cddae8b75eb4ae5c80b2610d28b43d050ec182dfee42156f0ddd2384ecabe4047a8ae9a2318700db',
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