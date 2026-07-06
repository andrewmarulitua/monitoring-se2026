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
    'f5avraaaaaaaaaaaaaaaa_session_': 'LDMKBBMANBLKBKACDHOHCBMOJBJPPCIFNHFFPOJNNGHFFENHIFGGBJFPPHOGIKKCLPKDOBOEKCONDLLGHBGAFEBAJEBOCKFMPFNHOHNLEFJCPDPCIBIFDLJBILLMKCNO',
    '_ga': 'GA1.3.417237891.1782976914',
    '_ga_XXTTVXWHDB': 'GS2.3.s1783060528$o2$g1$t1783067101$j60$l0$h0',
    'f5avraaaaaaaaaaaaaaaa_session_': 'LFOHHIAAMMAGJGPEONHNABHAKJELAAJNCHCJBFOJGEHLMAJILJCDGDAMKBPHIIICPFODCGJPCCOGGHLLDNPACNPMFEMBPGBJLDLMIJFOOMJKNCFPLHCBKDOEENMNFFGM',
    'TS00000000076': '0868f8be6fab2800747fefedd68e8f97520ba330f35649a6d87e690fa2af3f9c8ac095043b2f034a569379dc531f8caa08bbf826d309d0009f6c3cd988678a5d7ee6d785ce0236863e914a91c56df9d1f5c7a2d939803d23672497fa8006387956cf8843cd6fc7996a813376cd971dc4864add739f325b537b47bd38057005115047dd8d49fe01be0f2f41f83fd9fb70dfc9f265a41c5d34eeda67cbc207439fab187401fdeea64e2b2f389f500d5f64606b3c053e93af0af9cdca6e7b30c5f8fb3ef360e2e241df0b6a55b74e72fe34e3e051b0a6cf35b525b623969fa9dc053e8c2bfd93cef804408530a0b49225681e71e6515c6df7cfda5c741dfd880d822eb06a753b2c3e89',
    'TSPD_101_DID': '0868f8be6fab2800747fefedd68e8f97520ba330f35649a6d87e690fa2af3f9c8ac095043b2f034a569379dc531f8caa08bbf826d30638001f463d19ad4658dc031d97efc2e4d459c02f9ac902b5eac1ae623ba3830cd1834e6dbdc8b8655feb25bd6c2a682bb98d9d19e3540394752d',
    'db8ca2b43ed851cc93e71fd5fd72bff7': '622e65d34983a96bf46e8830a1b2b45a',
    'TS011f2d1a': '01266d26d0faf6dc7ef842a56d7a82599d9022c16720bd72602337de9cf8ef5a7fba6ebaa0023b65ea79c7d3c2c4339970df503cac',
    'TSPD_101': '0868f8be6fab280027d90313e3937244f91935c4c35038af0ea8f7f6f9513711ac164d09dffdf2cbffd6212f3c766b1f088e86abf9051800d95377e0e661a8e55ca1732140a3428bba23ce13beb1c95e',
    'XSRF-TOKEN': '1c5f735c-968e-4116-8b7c-427b8d435e5e',
    'SESSION': '21b216a6-ca60-43fd-8d89-9d61865195ab',
    'TS5220f739077': '0868f8be6fab28006f1ae671fee0e5e47812c245fadfb77fbd29aac66306559ca59e16a4b7a4782163961da90aefb7cf080f10eefb172000f60df60523989c99848fcea388d453480fc45691e24a6ea0b8a7ac6beff92c51',
    'TS5220f739029': '0868f8be6fab28003fe7cb2b6e26c279c95bd0e4ddbdba14e351574f65de05bafb27f359d2ed727023ef2bd6d70d57da',
    'TSf1edb2d2027': '0868f8be6fab2000affa8901e093fbca34ee7c6015a48b1f34a6ab7db032538f13ceefe3b292295d0822f5295d11300053579ea155a299df46b29506785f028465fec3f7abe8175b61d65a007f89a5ff090241472f6284b733045caaa6735c0d',
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
    'x-xsrf-token': '1c5f735c-968e-4116-8b7c-427b8d435e5e',
    'cookie': 'f5avraaaaaaaaaaaaaaaa_session_=LDMKBBMANBLKBKACDHOHCBMOJBJPPCIFNHFFPOJNNGHFFENHIFGGBJFPPHOGIKKCLPKDOBOEKCONDLLGHBGAFEBAJEBOCKFMPFNHOHNLEFJCPDPCIBIFDLJBILLMKCNO; _ga=GA1.3.417237891.1782976914; _ga_XXTTVXWHDB=GS2.3.s1783060528$o2$g1$t1783067101$j60$l0$h0; f5avraaaaaaaaaaaaaaaa_session_=LFOHHIAAMMAGJGPEONHNABHAKJELAAJNCHCJBFOJGEHLMAJILJCDGDAMKBPHIIICPFODCGJPCCOGGHLLDNPACNPMFEMBPGBJLDLMIJFOOMJKNCFPLHCBKDOEENMNFFGM; TS00000000076=0868f8be6fab2800747fefedd68e8f97520ba330f35649a6d87e690fa2af3f9c8ac095043b2f034a569379dc531f8caa08bbf826d309d0009f6c3cd988678a5d7ee6d785ce0236863e914a91c56df9d1f5c7a2d939803d23672497fa8006387956cf8843cd6fc7996a813376cd971dc4864add739f325b537b47bd38057005115047dd8d49fe01be0f2f41f83fd9fb70dfc9f265a41c5d34eeda67cbc207439fab187401fdeea64e2b2f389f500d5f64606b3c053e93af0af9cdca6e7b30c5f8fb3ef360e2e241df0b6a55b74e72fe34e3e051b0a6cf35b525b623969fa9dc053e8c2bfd93cef804408530a0b49225681e71e6515c6df7cfda5c741dfd880d822eb06a753b2c3e89; TSPD_101_DID=0868f8be6fab2800747fefedd68e8f97520ba330f35649a6d87e690fa2af3f9c8ac095043b2f034a569379dc531f8caa08bbf826d30638001f463d19ad4658dc031d97efc2e4d459c02f9ac902b5eac1ae623ba3830cd1834e6dbdc8b8655feb25bd6c2a682bb98d9d19e3540394752d; db8ca2b43ed851cc93e71fd5fd72bff7=622e65d34983a96bf46e8830a1b2b45a; TS011f2d1a=01266d26d0faf6dc7ef842a56d7a82599d9022c16720bd72602337de9cf8ef5a7fba6ebaa0023b65ea79c7d3c2c4339970df503cac; TSPD_101=0868f8be6fab280027d90313e3937244f91935c4c35038af0ea8f7f6f9513711ac164d09dffdf2cbffd6212f3c766b1f088e86abf9051800d95377e0e661a8e55ca1732140a3428bba23ce13beb1c95e; XSRF-TOKEN=1c5f735c-968e-4116-8b7c-427b8d435e5e; SESSION=21b216a6-ca60-43fd-8d89-9d61865195ab; TS5220f739077=0868f8be6fab28006f1ae671fee0e5e47812c245fadfb77fbd29aac66306559ca59e16a4b7a4782163961da90aefb7cf080f10eefb172000f60df60523989c99848fcea388d453480fc45691e24a6ea0b8a7ac6beff92c51; TS5220f739029=0868f8be6fab28003fe7cb2b6e26c279c95bd0e4ddbdba14e351574f65de05bafb27f359d2ed727023ef2bd6d70d57da; TSf1edb2d2027=0868f8be6fab2000affa8901e093fbca34ee7c6015a48b1f34a6ab7db032538f13ceefe3b292295d0822f5295d11300053579ea155a299df46b29506785f028465fec3f7abe8175b61d65a007f89a5ff090241472f6284b733045caaa6735c0d',
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