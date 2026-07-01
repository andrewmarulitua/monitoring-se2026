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
    '_ga_XXTTVXWHDB': 'GS2.3.s1781684707$o4$g0$t1781684707$j60$l0$h0',
    '_ga': 'GA1.1.1082300738.1781504126',
    '_ga_FMZTHHQN2K': 'GS2.1.s1782446723$o1$g1$t1782447263$j53$l0$h0',
    '_ga_QPPE1C18C5': 'GS2.1.s1782459355$o1$g1$t1782461722$j60$l0$h0',
    'f5avraaaaaaaaaaaaaaaa_session_': 'FENPPPJNBHJIHKEEPOACNIILFJOIOBALKNGPJJLPOJHFLMALGIKLBDBEOEAPPGADFCMDMBCNBJCKNBAFINFAKAMPOPMOJHHEHLOAEKDKJFFNAGDFBNODBAIJHLDHAGAF',
    'XSRF-TOKEN': '2673c323-5fe5-499e-8b82-278c31e8cdc6',
    'db8ca2b43ed851cc93e71fd5fd72bff7': '3c2b07cffe2c94e5a32c216eb4c6aea7',
    'SESSION': '6963fbb2-77ef-4a80-b002-e2145782076c',
    'TS00000000076': '0868f8be6fab2800e028b5e4932260be6c1fb4d3ea4660d812c0af1e0c8747466a250ee8938384bd8eff3de3b5b77d2508f18b5b9609d000ce8f26da85cb1d3605834f34052a3d1b2093433f8536f6946fda7dde65c69038527b1709011488249e2cc4d27ca5aaa305ff477271e0e438b6954e0c8908ef4aa5b2cfa439ff384f12ddde294caa55899d2607eb048684f30af023ce97d2444dbdb7e2ff24a16e86e9840add38771d31e6337e2ead9c2fc8dbf5cde76e80404ad0431ed252342275b240b9813e3823440781b8f8ed9b171e02f8e77d2ffb9b73af84cc6ea49b6e86ad51f6c2f1e7a036bbd67de522e3e9b71e3e1cdae2934a3fe8ddacee23d478d2feac8e5097e11f14',
    'TSPD_101_DID': '0868f8be6fab2800e028b5e4932260be6c1fb4d3ea4660d812c0af1e0c8747466a250ee8938384bd8eff3de3b5b77d2508f18b5b9606380050a64534dcd8d23cf695ba7e0f752f7378313462511b960e2f188dbbe55b1ab7f1fcd98d102b434aad31f23be4ba7eccbdcb89242c19ee97',
    'TS011f2d1a': '01266d26d023c23ccbe820ba2c5e787960659d0855668dc2b3e07c5aa531d1710ac40865cf8d72f2e05a9dcde79788bfd44dfaace1',
    'TSPD_101': '0868f8be6fab2800d9df65497c1e5aa7f1e34e980a5131e8750a58ebcfdafc4283998eaf34fde26adf625b13318e0d6408757e30ea051800d05653a698d835c65ca1732140a3428bba23ce13beb1c95e',
    'TS5220f739077': '0868f8be6fab2800533501397670fa3fef46b1484e29ff51ab041f4a49ef81a63a6805b83d3bd8dd3415d840cf55bf42087c4526df172000069cdad2342afa9946800eddf5f86a481c7804ebd144619813aefce804169bab',
    'TS5220f739029': '0868f8be6fab28008426935a9c5645c652e08b707567c7166ee995c83ae16f026dbb103d3ad12c0a1f50dedf64ab4c89',
    'TSf1edb2d2027': '0868f8be6fab20009666e9f2fa259fe2ee0d290ad898f49788fba84872920f4e980a34039c21b1b508e95d9b011130002e5c455a5411c6822e4545912e2c6658b689954326c59da7f7f32937723a6fe46eabe0d9105c513b4b22a7de67a91602',
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
    'x-xsrf-token': '2673c323-5fe5-499e-8b82-278c31e8cdc6',
    'cookie': '_ga_XXTTVXWHDB=GS2.3.s1781684707$o4$g0$t1781684707$j60$l0$h0; _ga=GA1.1.1082300738.1781504126; _ga_FMZTHHQN2K=GS2.1.s1782446723$o1$g1$t1782447263$j53$l0$h0; _ga_QPPE1C18C5=GS2.1.s1782459355$o1$g1$t1782461722$j60$l0$h0; f5avraaaaaaaaaaaaaaaa_session_=FENPPPJNBHJIHKEEPOACNIILFJOIOBALKNGPJJLPOJHFLMALGIKLBDBEOEAPPGADFCMDMBCNBJCKNBAFINFAKAMPOPMOJHHEHLOAEKDKJFFNAGDFBNODBAIJHLDHAGAF; XSRF-TOKEN=2673c323-5fe5-499e-8b82-278c31e8cdc6; db8ca2b43ed851cc93e71fd5fd72bff7=3c2b07cffe2c94e5a32c216eb4c6aea7; SESSION=6963fbb2-77ef-4a80-b002-e2145782076c; TS00000000076=0868f8be6fab2800e028b5e4932260be6c1fb4d3ea4660d812c0af1e0c8747466a250ee8938384bd8eff3de3b5b77d2508f18b5b9609d000ce8f26da85cb1d3605834f34052a3d1b2093433f8536f6946fda7dde65c69038527b1709011488249e2cc4d27ca5aaa305ff477271e0e438b6954e0c8908ef4aa5b2cfa439ff384f12ddde294caa55899d2607eb048684f30af023ce97d2444dbdb7e2ff24a16e86e9840add38771d31e6337e2ead9c2fc8dbf5cde76e80404ad0431ed252342275b240b9813e3823440781b8f8ed9b171e02f8e77d2ffb9b73af84cc6ea49b6e86ad51f6c2f1e7a036bbd67de522e3e9b71e3e1cdae2934a3fe8ddacee23d478d2feac8e5097e11f14; TSPD_101_DID=0868f8be6fab2800e028b5e4932260be6c1fb4d3ea4660d812c0af1e0c8747466a250ee8938384bd8eff3de3b5b77d2508f18b5b9606380050a64534dcd8d23cf695ba7e0f752f7378313462511b960e2f188dbbe55b1ab7f1fcd98d102b434aad31f23be4ba7eccbdcb89242c19ee97; TS011f2d1a=01266d26d023c23ccbe820ba2c5e787960659d0855668dc2b3e07c5aa531d1710ac40865cf8d72f2e05a9dcde79788bfd44dfaace1; TSPD_101=0868f8be6fab2800d9df65497c1e5aa7f1e34e980a5131e8750a58ebcfdafc4283998eaf34fde26adf625b13318e0d6408757e30ea051800d05653a698d835c65ca1732140a3428bba23ce13beb1c95e; TS5220f739077=0868f8be6fab2800533501397670fa3fef46b1484e29ff51ab041f4a49ef81a63a6805b83d3bd8dd3415d840cf55bf42087c4526df172000069cdad2342afa9946800eddf5f86a481c7804ebd144619813aefce804169bab; TS5220f739029=0868f8be6fab28008426935a9c5645c652e08b707567c7166ee995c83ae16f026dbb103d3ad12c0a1f50dedf64ab4c89; TSf1edb2d2027=0868f8be6fab20009666e9f2fa259fe2ee0d290ad898f49788fba84872920f4e980a34039c21b1b508e95d9b011130002e5c455a5411c6822e4545912e2c6658b689954326c59da7f7f32937723a6fe46eabe0d9105c513b4b22a7de67a91602',
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