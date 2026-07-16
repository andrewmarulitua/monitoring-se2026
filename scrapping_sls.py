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
    'f5avraaaaaaaaaaaaaaaa_session_': 'EDOJPPGFFNHJLHBPIGMCHPHOIDPHHIFIEOECFKBONJOOPINNKGHKGGPENJGPBMOKIHKDMIICJPKGKMHHKCBAGBNPKBCJFHMPMILCNELBBNCBMIFNEPOGANDKLLEHLEDE',
    '_ga': 'GA1.3.1765036020.1783921242',
    'cf_clearance': 'jNAO2DxRwIfpRCfBor16V.In2fth6zRc7zAs_vGs_Xc-1784113291-1.2.1.1-meVZV7.xwwjypN17tGkILzXiXB24ZNIwmYHnxVtjufSsQvEy88d3f2AlPSgFBeoUfz3FE4fxDnm8WXcZiBWSS1OzZTD_DgqpVqLoA9ZkdKexGYtLlA3lZwwOB1y1KClWJGMQslBAdEOXqCpqU4YxEYldnZYtm2e6a54n1Q1BoBczG1eIlf8T1F5WR7L1v7UewKf0Uf6Zi7Sx.Ity__bo6smCcpC80zUIKOGXTSDBQK52yM7YZIadn_AiM2RXBNdlk5j5.kxGwLXBc2fD2nWaQ_DjnUCldhqjpxDGpMAPHm9MGQswaUbtVEVIR1WYkyC68yMzTmS7.qs1gRCZwTPMug',
    '_ga_XXTTVXWHDB': 'GS2.3.s1784124600$o3$g0$t1784124600$j60$l0$h0',
    'f5avraaaaaaaaaaaaaaaa_session_': 'JJOCMHMFCHFHDEMFBNICKLJEAPOCNIIHGPBPJPGGINAOCPNNEGCLHOMMMAAIMDDNILCDMIGONPOJLCAMEBCAPHMPABHCKJOBBKFLJLBBICPKBMBICNDJMPGJAGBMKFLP',
    'TS00000000076': '0868f8be6fab2800cb2365707cbf542130ea21593b6dc63dc56d5ae5c969ad7987f6e2dbac182fad9a3954163b22db8508e261384409d00033a352f27581ba51ca2355fd3b3359ee61c81ceac69430e17ea1793cc27a1e668c31dd0dc222f9cff4affe1324b78a6ee63bae71c37c4d826d221e28c1d7330443d573f67718bd61cb03df2a175184956607fd84e1c9ee49ad4d75a6a1ec31b7c3e04897761cd9544a18589a287c1fc427d5bf2163eaacd881519840c9d4fe0b67d22fd9c473544a1614c8dc5757b1589818021817a7bcc4c54f30ba6394d28b78f56a8777dba5972774dd645b2f9ee191f6dc4011e9047d383910604dc844f721391e8a6e2900dfb8d83ec55d96fa84',
    'TSPD_101_DID': '0868f8be6fab2800cb2365707cbf542130ea21593b6dc63dc56d5ae5c969ad7987f6e2dbac182fad9a3954163b22db8508e2613844063800fd16b99ce156428e224efff81f520f78e814b4f4a93ca23da5194e3c4606ad88fdb5a3e8438a964be9e741b51a892badfb8cdc00bfa0639f',
    'db8ca2b43ed851cc93e71fd5fd72bff7': '7da4df40e36782a4b7d9902fb316b064',
    'TS011f2d1a': '01266d26d064180b21f00cb2146f44bcf48d820f7eda75138cf36e691dcfd926a62b41b628b8032fe5da52dd1bcd1791815c7feb77',
    'TSPD_101': '0868f8be6fab280039ca5ea2cb4e09d590e7fa336e3b6fea63f2cfc911eca646f701c163d775e0955c7e6cf93b97def008bc05075d05180005904505023f65995ca1732140a3428bba23ce13beb1c95e',
    'XSRF-TOKEN': 'fe10d05a-78d8-40db-83ad-3f9f249a139d',
    'SESSION': '65914d29-2821-4663-94b0-6035e6019dd9',
    'f5avr0793127497aaaaaaaaaaaaaaaa_cspm_': 'KGCPEJOOKJBAKJHJMIAMEMGDBLDHBCLOKPMJPPGMJKLKCBLOJCOOENNNEMEMLNCKMMACNKCJPFLCILHHDCKAJMIDAOBNGPPKJCNGGGAADLLONEDNPMJJONNLBAMCNDMB',
    'TS5220f739077': '0868f8be6fab2800e34ceed329ae9b67726c071075a7992dc7b76be8544d01c51d306427fb9932d3368be75e211061d20884864e09172000b866c6b3a5347494bd63aa4f6a9d96f6aab8a5b0db4ce7c82d501018f315829e',
    'TSf1edb2d2027': '0868f8be6fab20008fa3c43d51d5c4e17eb76f26024f8a323364a9f2272ba9533a7fb809d42a84ec08e99918651130004f293155feb5ca66eea2deedbdf94a49e11601fc250b15a87fe5a230481c97a645b6946d77cc0e2d841528c10fddb88c',
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
    'x-xsrf-token': 'fe10d05a-78d8-40db-83ad-3f9f249a139d',
    'cookie': 'f5avraaaaaaaaaaaaaaaa_session_=EDOJPPGFFNHJLHBPIGMCHPHOIDPHHIFIEOECFKBONJOOPINNKGHKGGPENJGPBMOKIHKDMIICJPKGKMHHKCBAGBNPKBCJFHMPMILCNELBBNCBMIFNEPOGANDKLLEHLEDE; _ga=GA1.3.1765036020.1783921242; cf_clearance=jNAO2DxRwIfpRCfBor16V.In2fth6zRc7zAs_vGs_Xc-1784113291-1.2.1.1-meVZV7.xwwjypN17tGkILzXiXB24ZNIwmYHnxVtjufSsQvEy88d3f2AlPSgFBeoUfz3FE4fxDnm8WXcZiBWSS1OzZTD_DgqpVqLoA9ZkdKexGYtLlA3lZwwOB1y1KClWJGMQslBAdEOXqCpqU4YxEYldnZYtm2e6a54n1Q1BoBczG1eIlf8T1F5WR7L1v7UewKf0Uf6Zi7Sx.Ity__bo6smCcpC80zUIKOGXTSDBQK52yM7YZIadn_AiM2RXBNdlk5j5.kxGwLXBc2fD2nWaQ_DjnUCldhqjpxDGpMAPHm9MGQswaUbtVEVIR1WYkyC68yMzTmS7.qs1gRCZwTPMug; _ga_XXTTVXWHDB=GS2.3.s1784124600$o3$g0$t1784124600$j60$l0$h0; f5avraaaaaaaaaaaaaaaa_session_=JJOCMHMFCHFHDEMFBNICKLJEAPOCNIIHGPBPJPGGINAOCPNNEGCLHOMMMAAIMDDNILCDMIGONPOJLCAMEBCAPHMPABHCKJOBBKFLJLBBICPKBMBICNDJMPGJAGBMKFLP; TS00000000076=0868f8be6fab2800cb2365707cbf542130ea21593b6dc63dc56d5ae5c969ad7987f6e2dbac182fad9a3954163b22db8508e261384409d00033a352f27581ba51ca2355fd3b3359ee61c81ceac69430e17ea1793cc27a1e668c31dd0dc222f9cff4affe1324b78a6ee63bae71c37c4d826d221e28c1d7330443d573f67718bd61cb03df2a175184956607fd84e1c9ee49ad4d75a6a1ec31b7c3e04897761cd9544a18589a287c1fc427d5bf2163eaacd881519840c9d4fe0b67d22fd9c473544a1614c8dc5757b1589818021817a7bcc4c54f30ba6394d28b78f56a8777dba5972774dd645b2f9ee191f6dc4011e9047d383910604dc844f721391e8a6e2900dfb8d83ec55d96fa84; TSPD_101_DID=0868f8be6fab2800cb2365707cbf542130ea21593b6dc63dc56d5ae5c969ad7987f6e2dbac182fad9a3954163b22db8508e2613844063800fd16b99ce156428e224efff81f520f78e814b4f4a93ca23da5194e3c4606ad88fdb5a3e8438a964be9e741b51a892badfb8cdc00bfa0639f; db8ca2b43ed851cc93e71fd5fd72bff7=7da4df40e36782a4b7d9902fb316b064; TS011f2d1a=01266d26d064180b21f00cb2146f44bcf48d820f7eda75138cf36e691dcfd926a62b41b628b8032fe5da52dd1bcd1791815c7feb77; TSPD_101=0868f8be6fab280039ca5ea2cb4e09d590e7fa336e3b6fea63f2cfc911eca646f701c163d775e0955c7e6cf93b97def008bc05075d05180005904505023f65995ca1732140a3428bba23ce13beb1c95e; XSRF-TOKEN=fe10d05a-78d8-40db-83ad-3f9f249a139d; SESSION=65914d29-2821-4663-94b0-6035e6019dd9; f5avr0793127497aaaaaaaaaaaaaaaa_cspm_=KGCPEJOOKJBAKJHJMIAMEMGDBLDHBCLOKPMJPPGMJKLKCBLOJCOOENNNEMEMLNCKMMACNKCJPFLCILHHDCKAJMIDAOBNGPPKJCNGGGAADLLONEDNPMJJONNLBAMCNDMB; TS5220f739077=0868f8be6fab2800e34ceed329ae9b67726c071075a7992dc7b76be8544d01c51d306427fb9932d3368be75e211061d20884864e09172000b866c6b3a5347494bd63aa4f6a9d96f6aab8a5b0db4ce7c82d501018f315829e; TSf1edb2d2027=0868f8be6fab20008fa3c43d51d5c4e17eb76f26024f8a323364a9f2272ba9533a7fb809d42a84ec08e99918651130004f293155feb5ca66eea2deedbdf94a49e11601fc250b15a87fe5a230481c97a645b6946d77cc0e2d841528c10fddb88c',
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