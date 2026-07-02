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
    'f5avraaaaaaaaaaaaaaaa_session_': 'PHEMDKNLEPIPJKAGCJJMJOKKKKJFFDCNOABHBKCDIBDGGOKIAGHCIANLCMMLPGFELMMDBIMIFOOCHLMCEOOAAKCIHMKOEGBBIOPBFIBKKFJAACIEMPCOPAHPHLJNHAAE',
    '_ga': 'GA1.3.417237891.1782976914',
    '_ga_XXTTVXWHDB': 'GS2.3.s1782976913$o1$g1$t1782979791$j60$l0$h0',
    'db8ca2b43ed851cc93e71fd5fd72bff7': '5d1b416be39c99953e9281977e66b478',
    'XSRF-TOKEN': '60023f92-8830-4dc4-bf3a-52af89d5f0e9',
    'SESSION': '090b2196-b709-49e1-adc0-539c346b412c',
    'TS01433fd3': '01266d26d0cbe06cad9cade7b9bc4c4907fb10a076b09c65eb608442167eff028e298024cfd63d9fd1d64db2a2226194eb4aed42fe',
    'f5avraaaaaaaaaaaaaaaa_session_': 'POAAOACONBFLPBCNHILAIHDMBAOEIDJHBIOMCNELNOMOKDGPAJMEHCHLLBIABGIPDJCDCGFIOOPHPIJMAPIAGCLIMMKFBKJMAEIIBLAHPPHOAHCMALOMFMHGHNOBBKDB',
    'TS00000000076': '0868f8be6fab2800b9a6d93f3d22a8569493583bf0a4f59c68640e6a4396fbe5363128ffef90d7651c2596c22bce09a9083b61d6b809d000ac4eea2afa50820adc859fddf9287e5b6448065f9a936ef8016334d2afb08d81dd932bf8edbc4f7961b116fc7a3e942f78385470e5e5384166523362c2ce249cc031efbc9cb15d95ace39568527d8b4d79af36dd798b41d2fd7eaa2c18263676067b9ec31eaf29ffd6a4efd9bf622baf92acc2cbaf3fae2e2e07587d9b126f0c8e692d4d7ab454178fe1baf0a6be392de9990e1929d75946821ab1151f3796141d76093e419e77309d102a2c358081f3f7fc7295a4b5fd363f118fd691c9e635b9bf38a860f09eb8d1b6752e7b0ebdbd',
    'TSPD_101_DID': '0868f8be6fab2800b9a6d93f3d22a8569493583bf0a4f59c68640e6a4396fbe5363128ffef90d7651c2596c22bce09a9083b61d6b80638004c7d286ca0e2a50d54ee2429fce8ca93047959dd7120907da75ad08b6881a0d215c3225d8fd33159dc1e87b691aa42ad52f161825fad796f',
    'TS011f2d1a': '01266d26d0d4c2c6f3e4ba7293f0a7d675271fa4d4db97ad5b1cf946c942316bdd48bbcaf061931e40d3c84703d6bd2134801309b5',
    'TSPD_101': '0868f8be6fab2800efdd62c2c08dd7ea01fdbc107c7a3f57a8be7f0f21b6db0330bb3efd73cdf415ce304c4c2c99297b087d3343cc05180058efd421d25e3fe95ca1732140a3428bba23ce13beb1c95e',
    'TS5220f739077': '0868f8be6fab2800c0a6f47ddd574ad0c5c1b1b2001f78452e6c140c20e43d6a98f4b750796189a08df603fa778c0ec108107751071720007b0c7f0d0bc345d1dd2507c3b730840a281f6d72c471a66f4ab8e7d67ee186ca',
    'TS5220f739029': '0868f8be6fab28002da38c7e782940af12537bcb57892d6cd935d456857e93f07389c8e952a6225d693cd90ce2af6a34',
    'TSf1edb2d2027': '0868f8be6fab20005ff12a5c101f04b511386441d4445e77c98bdff4b27aaeae384ac800d3b3bd300895439850113000f747754c093cdbd4234e45620ce58e6f2f21c8b5e6d93bc3f38e16f98e9dd8059c00ef52a84108ef6ebb904f16da9f98',
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
    'x-xsrf-token': '60023f92-8830-4dc4-bf3a-52af89d5f0e9',
    'cookie': 'f5avraaaaaaaaaaaaaaaa_session_=PHEMDKNLEPIPJKAGCJJMJOKKKKJFFDCNOABHBKCDIBDGGOKIAGHCIANLCMMLPGFELMMDBIMIFOOCHLMCEOOAAKCIHMKOEGBBIOPBFIBKKFJAACIEMPCOPAHPHLJNHAAE; _ga=GA1.3.417237891.1782976914; _ga_XXTTVXWHDB=GS2.3.s1782976913$o1$g1$t1782979791$j60$l0$h0; db8ca2b43ed851cc93e71fd5fd72bff7=5d1b416be39c99953e9281977e66b478; XSRF-TOKEN=60023f92-8830-4dc4-bf3a-52af89d5f0e9; SESSION=090b2196-b709-49e1-adc0-539c346b412c; TS01433fd3=01266d26d0cbe06cad9cade7b9bc4c4907fb10a076b09c65eb608442167eff028e298024cfd63d9fd1d64db2a2226194eb4aed42fe; f5avraaaaaaaaaaaaaaaa_session_=POAAOACONBFLPBCNHILAIHDMBAOEIDJHBIOMCNELNOMOKDGPAJMEHCHLLBIABGIPDJCDCGFIOOPHPIJMAPIAGCLIMMKFBKJMAEIIBLAHPPHOAHCMALOMFMHGHNOBBKDB; TS00000000076=0868f8be6fab2800b9a6d93f3d22a8569493583bf0a4f59c68640e6a4396fbe5363128ffef90d7651c2596c22bce09a9083b61d6b809d000ac4eea2afa50820adc859fddf9287e5b6448065f9a936ef8016334d2afb08d81dd932bf8edbc4f7961b116fc7a3e942f78385470e5e5384166523362c2ce249cc031efbc9cb15d95ace39568527d8b4d79af36dd798b41d2fd7eaa2c18263676067b9ec31eaf29ffd6a4efd9bf622baf92acc2cbaf3fae2e2e07587d9b126f0c8e692d4d7ab454178fe1baf0a6be392de9990e1929d75946821ab1151f3796141d76093e419e77309d102a2c358081f3f7fc7295a4b5fd363f118fd691c9e635b9bf38a860f09eb8d1b6752e7b0ebdbd; TSPD_101_DID=0868f8be6fab2800b9a6d93f3d22a8569493583bf0a4f59c68640e6a4396fbe5363128ffef90d7651c2596c22bce09a9083b61d6b80638004c7d286ca0e2a50d54ee2429fce8ca93047959dd7120907da75ad08b6881a0d215c3225d8fd33159dc1e87b691aa42ad52f161825fad796f; TS011f2d1a=01266d26d0d4c2c6f3e4ba7293f0a7d675271fa4d4db97ad5b1cf946c942316bdd48bbcaf061931e40d3c84703d6bd2134801309b5; TSPD_101=0868f8be6fab2800efdd62c2c08dd7ea01fdbc107c7a3f57a8be7f0f21b6db0330bb3efd73cdf415ce304c4c2c99297b087d3343cc05180058efd421d25e3fe95ca1732140a3428bba23ce13beb1c95e; TS5220f739077=0868f8be6fab2800c0a6f47ddd574ad0c5c1b1b2001f78452e6c140c20e43d6a98f4b750796189a08df603fa778c0ec108107751071720007b0c7f0d0bc345d1dd2507c3b730840a281f6d72c471a66f4ab8e7d67ee186ca; TS5220f739029=0868f8be6fab28002da38c7e782940af12537bcb57892d6cd935d456857e93f07389c8e952a6225d693cd90ce2af6a34; TSf1edb2d2027=0868f8be6fab20005ff12a5c101f04b511386441d4445e77c98bdff4b27aaeae384ac800d3b3bd300895439850113000f747754c093cdbd4234e45620ce58e6f2f21c8b5e6d93bc3f38e16f98e9dd8059c00ef52a84108ef6ebb904f16da9f98',
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