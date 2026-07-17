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
    'f5avraaaaaaaaaaaaaaaa_session_': 'GHEKJGHIDEPMPJBCDJGGKKPBMFLNNDBECAHAOOCDKAPENJGLEMCDFKBINMNNIGALJMCDPIHFOOHHPPOKALBAGEKBDIKCJGEGDLDBIFDKKHBDINODIFKHPBHDGNCDJHKJ',
    'f5avraaaaaaaaaaaaaaaa_session_': 'KDIJMKNFPEBKEEODNCLPFNBNKMMIMJBBFKNKLIMKLBFFNJKHNDIDFGEFDPANMCMAICEDLDENOBFNMEHADLNAFDAJAIAOKBFGIBBNIBPKHFCPPOADHGLAMDGABGPOAEPC',
    'f5_cspm': '1234',
    '_ga': 'GA1.3.1765036020.1783921242',
    'cf_clearance': 'jNAO2DxRwIfpRCfBor16V.In2fth6zRc7zAs_vGs_Xc-1784113291-1.2.1.1-meVZV7.xwwjypN17tGkILzXiXB24ZNIwmYHnxVtjufSsQvEy88d3f2AlPSgFBeoUfz3FE4fxDnm8WXcZiBWSS1OzZTD_DgqpVqLoA9ZkdKexGYtLlA3lZwwOB1y1KClWJGMQslBAdEOXqCpqU4YxEYldnZYtm2e6a54n1Q1BoBczG1eIlf8T1F5WR7L1v7UewKf0Uf6Zi7Sx.Ity__bo6smCcpC80zUIKOGXTSDBQK52yM7YZIadn_AiM2RXBNdlk5j5.kxGwLXBc2fD2nWaQ_DjnUCldhqjpxDGpMAPHm9MGQswaUbtVEVIR1WYkyC68yMzTmS7.qs1gRCZwTPMug',
    '_ga_XXTTVXWHDB': 'GS2.3.s1784124600$o3$g0$t1784124600$j60$l0$h0',
    'db8ca2b43ed851cc93e71fd5fd72bff7': '011af19a3d1e03881ca5c11517f5c28d',
    'XSRF-TOKEN': 'db76a989-0727-48f1-bc60-01405a9704d5',
    'SESSION': 'b3a3ab88-5229-4128-a4be-3e5f4d0fc9f7',
    'TS018af012': '0167a1c86124b3b81d779f2c88dcc0477e895708b2020f14d645add4305deb7b288ba72bc01de33b18ede67cedf12420501b1130890909ff8b4a87a97960a38ec3445ea431fe2f45f33e5d10b930d383dc0a1d7a5a',
    'TS00000000076': '0868f8be6fab28001584f9442190b9c4d406c99c04bcfd2886a0ae34014d42fc9b530b73d368d812b10d485869d9214408f9905f6609d0000ab3305ecd6b4d6e48058a1446d8330628a7e2142b4c36978848507a737f8ded4219c7e2b142b1c905340b268fcd9dfcdad4a8e4fb766b1159eb3f9de8f153e44d0b862388986289027fc5a5ac79ade948bb2ab8f712ad43d80484fa9f4d6bbf53e59f109856bfdcc3b84c7114dcf9b04f741bf7e7082759c0d0b90cad3bb0b8b4899b14a2b57189f2806724541bcdbd8536a524d3953db606eebaf03fd4ebfd0bf363627cfa545ab7b2ae3a6a69026a0c8942b2a7385dad361857b4145130368199f790f38574b5fffa511b32c348d9',
    'TSPD_101_DID': '0868f8be6fab28001584f9442190b9c4d406c99c04bcfd2886a0ae34014d42fc9b530b73d368d812b10d485869d9214408f9905f66063800198eef8d64ae7759f1e4ceda63f0254e2ed32549ec5ac635bb6e3ce95f78523db69b6dab62d2757bd43e7711c2e9b8d201e0851b28e12c08',
    'TS011f2d1a': '01266d26d012657364ea7b41f3005e129ffd73335fe5b0895127c82347a27b8e468b3d8f89c1d86a66b9f241904c7e7f1b336c2b85',
    'TSPD_101': '0868f8be6fab2800034c7b0f3979889033bb8e18852e2821f5b2a2021c03d85d4d42eecdb5e555d2e9d568e7a0eeca4d089ef43105051800b05df8779eb4efdf5ca1732140a3428bba23ce13beb1c95e',
    'f5avraaaaaaaaaaaaaaaa_session_': 'PDBHHOELFPOAJNAJGBJHGFFKPBOMCJCAOJJJCAAIIMENBGHBBOGJDBPNEPAAFMFBKLIDAHILKOCGGPBLHBEAEADIDIEMCELLHIMGBAMFKNIMDNLJEEMKJAOAOLAIACHP',
    'TS5220f739077': '0868f8be6fab280008987f3de5640856d4a5d346fb03ae4c8ab2bb20443fcf54fda1e2ab1e2792c01d58d6e6117f9741087abf9e9c1720005fb16d74e459abdeaf640bfffa657c8142a5e22ae1be98da48bc3208c9ca248c',
    'TS5220f739029': '0868f8be6fab2800f241b3f4c603eaff58609623608504b83a7c4160bdfdf98ad199a3860a636a97f7942a1402d4ccf3',
    'TSf1edb2d2027': '0868f8be6fab2000a154795338722f7b8ced55433a4d4a7528d78f2c7a02220605cf97fbea946d6408f21c60bc11300012e2b394fc5d2ccd407925eb034de502e80b73d3c2205747a495864f79fd53a12b48440c6345a10eb312be57b5ba5629',
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
    'x-xsrf-token': 'db76a989-0727-48f1-bc60-01405a9704d5',
    'cookie': 'f5avraaaaaaaaaaaaaaaa_session_=GHEKJGHIDEPMPJBCDJGGKKPBMFLNNDBECAHAOOCDKAPENJGLEMCDFKBINMNNIGALJMCDPIHFOOHHPPOKALBAGEKBDIKCJGEGDLDBIFDKKHBDINODIFKHPBHDGNCDJHKJ; f5avraaaaaaaaaaaaaaaa_session_=KDIJMKNFPEBKEEODNCLPFNBNKMMIMJBBFKNKLIMKLBFFNJKHNDIDFGEFDPANMCMAICEDLDENOBFNMEHADLNAFDAJAIAOKBFGIBBNIBPKHFCPPOADHGLAMDGABGPOAEPC; f5_cspm=1234; _ga=GA1.3.1765036020.1783921242; cf_clearance=jNAO2DxRwIfpRCfBor16V.In2fth6zRc7zAs_vGs_Xc-1784113291-1.2.1.1-meVZV7.xwwjypN17tGkILzXiXB24ZNIwmYHnxVtjufSsQvEy88d3f2AlPSgFBeoUfz3FE4fxDnm8WXcZiBWSS1OzZTD_DgqpVqLoA9ZkdKexGYtLlA3lZwwOB1y1KClWJGMQslBAdEOXqCpqU4YxEYldnZYtm2e6a54n1Q1BoBczG1eIlf8T1F5WR7L1v7UewKf0Uf6Zi7Sx.Ity__bo6smCcpC80zUIKOGXTSDBQK52yM7YZIadn_AiM2RXBNdlk5j5.kxGwLXBc2fD2nWaQ_DjnUCldhqjpxDGpMAPHm9MGQswaUbtVEVIR1WYkyC68yMzTmS7.qs1gRCZwTPMug; _ga_XXTTVXWHDB=GS2.3.s1784124600$o3$g0$t1784124600$j60$l0$h0; db8ca2b43ed851cc93e71fd5fd72bff7=011af19a3d1e03881ca5c11517f5c28d; XSRF-TOKEN=db76a989-0727-48f1-bc60-01405a9704d5; SESSION=b3a3ab88-5229-4128-a4be-3e5f4d0fc9f7; TS018af012=0167a1c86124b3b81d779f2c88dcc0477e895708b2020f14d645add4305deb7b288ba72bc01de33b18ede67cedf12420501b1130890909ff8b4a87a97960a38ec3445ea431fe2f45f33e5d10b930d383dc0a1d7a5a; TS00000000076=0868f8be6fab28001584f9442190b9c4d406c99c04bcfd2886a0ae34014d42fc9b530b73d368d812b10d485869d9214408f9905f6609d0000ab3305ecd6b4d6e48058a1446d8330628a7e2142b4c36978848507a737f8ded4219c7e2b142b1c905340b268fcd9dfcdad4a8e4fb766b1159eb3f9de8f153e44d0b862388986289027fc5a5ac79ade948bb2ab8f712ad43d80484fa9f4d6bbf53e59f109856bfdcc3b84c7114dcf9b04f741bf7e7082759c0d0b90cad3bb0b8b4899b14a2b57189f2806724541bcdbd8536a524d3953db606eebaf03fd4ebfd0bf363627cfa545ab7b2ae3a6a69026a0c8942b2a7385dad361857b4145130368199f790f38574b5fffa511b32c348d9; TSPD_101_DID=0868f8be6fab28001584f9442190b9c4d406c99c04bcfd2886a0ae34014d42fc9b530b73d368d812b10d485869d9214408f9905f66063800198eef8d64ae7759f1e4ceda63f0254e2ed32549ec5ac635bb6e3ce95f78523db69b6dab62d2757bd43e7711c2e9b8d201e0851b28e12c08; TS011f2d1a=01266d26d012657364ea7b41f3005e129ffd73335fe5b0895127c82347a27b8e468b3d8f89c1d86a66b9f241904c7e7f1b336c2b85; TSPD_101=0868f8be6fab2800034c7b0f3979889033bb8e18852e2821f5b2a2021c03d85d4d42eecdb5e555d2e9d568e7a0eeca4d089ef43105051800b05df8779eb4efdf5ca1732140a3428bba23ce13beb1c95e; f5avraaaaaaaaaaaaaaaa_session_=PDBHHOELFPOAJNAJGBJHGFFKPBOMCJCAOJJJCAAIIMENBGHBBOGJDBPNEPAAFMFBKLIDAHILKOCGGPBLHBEAEADIDIEMCELLHIMGBAMFKNIMDNLJEEMKJAOAOLAIACHP; TS5220f739077=0868f8be6fab280008987f3de5640856d4a5d346fb03ae4c8ab2bb20443fcf54fda1e2ab1e2792c01d58d6e6117f9741087abf9e9c1720005fb16d74e459abdeaf640bfffa657c8142a5e22ae1be98da48bc3208c9ca248c; TS5220f739029=0868f8be6fab2800f241b3f4c603eaff58609623608504b83a7c4160bdfdf98ad199a3860a636a97f7942a1402d4ccf3; TSf1edb2d2027=0868f8be6fab2000a154795338722f7b8ced55433a4d4a7528d78f2c7a02220605cf97fbea946d6408f21c60bc11300012e2b394fc5d2ccd407925eb034de502e80b73d3c2205747a495864f79fd53a12b48440c6345a10eb312be57b5ba5629',
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