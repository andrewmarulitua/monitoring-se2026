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
    'f5avraaaaaaaaaaaaaaaa_session_': 'PKEEGCPLJNBFIAOHCKHIFADBDONNEICIFHPDKCADCKFIPMEOJKBKIOKDCLJIGHDKOKODABEPEEJEKENDIFHAEAEGKOGDNKCEEMEPPPOHPOKPPFCBJPLKFJDFCGMODPIE',
    'cf_clearance': 'F_24x8yTfvl4LTgV2YD0dC65ZoTriIMdodHfnya1tXE-1783921239-1.2.1.1-U8_GjcPoQkuY5tsT2eC_evjxNhMUG1a65PQtWmUdT9ebR52DpxL_INWYoWn8e_o2sxs2MGu_tcqlhMgcV9j65yeWUSGAO0MCmAEq04.cgLkC6Hgl.Yq8Lq1HTh3.BSfmeIkhsr7sHL7Sweb75FMhSi25oPMLB.cN8IWFKkTH0wwlofV41w2nyzqkZNbVtv_t2Fk5WQCg9t1S5pQwfSzc5BSTs.O9iVHkoFTjOVpam_WJOu.elbnEwQOd833cBuiqxlsJEAUmRNCpnlmwqApBi1ngtwC.RuQgjsqXuQXTV1Dbm3yHffVai7FtZ4FbshncQhxZeqD1NMm7SlNtw79s_Q',
    '_ga': 'GA1.3.1765036020.1783921242',
    '_ga_XXTTVXWHDB': 'GS2.3.s1783921242$o1$g1$t1783922520$j60$l0$h0',
    'db8ca2b43ed851cc93e71fd5fd72bff7': '8ebdc6a32d7400509e0aaecff0b1d19b',
    'XSRF-TOKEN': 'c9a1919f-ebab-4b97-89a5-74b2f3643470',
    'SESSION': '5a12efe6-c4e1-4c55-9990-39ff79e52b12',
    'f5avraaaaaaaaaaaaaaaa_session_': 'LIJBJMFDFJFGIPMPGAMHFEGOFCHKKLHAAHOEIJGGJELBDCDAHNMALGFPJLONINPCHKEDDCJJHDLLGCPAEDNALAHAPOPMELEDEPNJAHAGJEPHCMFICOEAOGDMOIEIBKEI',
    'TS00000000076': '0868f8be6fab2800bda1a5f2ce95a204fddd7de6ef962eb753472c50f130af8b61583aa5c8b698c845baeee2be435bd908f0619f1209d00065fd51fbf54c52c0fca3398c23a01b452b5e67cb1cd9d495fbe4fb507d534887948c84b4a736b3b66a6d3c24d7482d3342808ea05c74d9d873658a9807ff73aab1c41548fcc93a1606a5c9eb298c88e8445b7d0136d6ab7038d5dabeab3875a4080729ed521c0e4a9438aeb912ba23773f521bcbdc7994cca76179ade002038634137f7ed80a680d1cdc70d3778096df623c6786129d7c4d7578bede414b0157a610b1f5982eca4784eeb915ec445afce14a6967b2d01e2fad751fee3ef128126935dc3fb9890d9cdbffb8f50becc723',
    'TSPD_101_DID': '0868f8be6fab2800bda1a5f2ce95a204fddd7de6ef962eb753472c50f130af8b61583aa5c8b698c845baeee2be435bd908f0619f120638004e836ca2a2e1df49a8a5097a9f940761cc289bde7d99a2fb7f684598da78f04736639e0aff6a4dd544f1df4b90f45309ef481f5eba5b9127',
    'TS011f2d1a': '01266d26d065580958784c397bc70fe64efef63efb20a617a0180bd4443d9813a8e157bad4509bc4d5bfa0cf5f86b887142766db7c',
    'TSPD_101': '0868f8be6fab28003340859fe760e0cf6b8b0bd9b47a4f2ef9dc477ede672e34d2bf23bcdf221a5fa58b80c005d2b94b08de460c590518008f5b365708fa507c5ca1732140a3428bba23ce13beb1c95e',
    'TS5220f739077': '0868f8be6fab28000fdf95f1e6b55c4a7eb168cbae2cc2f300626eaadb2b68fb57bb55271e170672454d048fef0b54a608729bf09e1720007f571959265335e055908aec309551c2b575881f929d9d16db75ee4300aef382',
    'TS5220f739029': '0868f8be6fab28005ba9c13f1de819fa5cf6da62531458108fcfcccdc2d7ab16f19f1b8c865d777aece9084079439dbc',
    'TSf1edb2d2027': '0868f8be6fab2000aec0a553e5a61b4237081e21ae18adf48045d10dbcb0cf9ef594ba6c75dc672d08071abe781130009ca5cf0218e2380baa8fbbc3f3065f1d4f75b35c339832b29ee7f0a2cddecc91fae379db5942db207935b58b4fe1d497',
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
    'x-xsrf-token': 'c9a1919f-ebab-4b97-89a5-74b2f3643470',
    'cookie': 'f5avraaaaaaaaaaaaaaaa_session_=PKEEGCPLJNBFIAOHCKHIFADBDONNEICIFHPDKCADCKFIPMEOJKBKIOKDCLJIGHDKOKODABEPEEJEKENDIFHAEAEGKOGDNKCEEMEPPPOHPOKPPFCBJPLKFJDFCGMODPIE; cf_clearance=F_24x8yTfvl4LTgV2YD0dC65ZoTriIMdodHfnya1tXE-1783921239-1.2.1.1-U8_GjcPoQkuY5tsT2eC_evjxNhMUG1a65PQtWmUdT9ebR52DpxL_INWYoWn8e_o2sxs2MGu_tcqlhMgcV9j65yeWUSGAO0MCmAEq04.cgLkC6Hgl.Yq8Lq1HTh3.BSfmeIkhsr7sHL7Sweb75FMhSi25oPMLB.cN8IWFKkTH0wwlofV41w2nyzqkZNbVtv_t2Fk5WQCg9t1S5pQwfSzc5BSTs.O9iVHkoFTjOVpam_WJOu.elbnEwQOd833cBuiqxlsJEAUmRNCpnlmwqApBi1ngtwC.RuQgjsqXuQXTV1Dbm3yHffVai7FtZ4FbshncQhxZeqD1NMm7SlNtw79s_Q; _ga=GA1.3.1765036020.1783921242; _ga_XXTTVXWHDB=GS2.3.s1783921242$o1$g1$t1783922520$j60$l0$h0; db8ca2b43ed851cc93e71fd5fd72bff7=8ebdc6a32d7400509e0aaecff0b1d19b; XSRF-TOKEN=c9a1919f-ebab-4b97-89a5-74b2f3643470; SESSION=5a12efe6-c4e1-4c55-9990-39ff79e52b12; f5avraaaaaaaaaaaaaaaa_session_=LIJBJMFDFJFGIPMPGAMHFEGOFCHKKLHAAHOEIJGGJELBDCDAHNMALGFPJLONINPCHKEDDCJJHDLLGCPAEDNALAHAPOPMELEDEPNJAHAGJEPHCMFICOEAOGDMOIEIBKEI; TS00000000076=0868f8be6fab2800bda1a5f2ce95a204fddd7de6ef962eb753472c50f130af8b61583aa5c8b698c845baeee2be435bd908f0619f1209d00065fd51fbf54c52c0fca3398c23a01b452b5e67cb1cd9d495fbe4fb507d534887948c84b4a736b3b66a6d3c24d7482d3342808ea05c74d9d873658a9807ff73aab1c41548fcc93a1606a5c9eb298c88e8445b7d0136d6ab7038d5dabeab3875a4080729ed521c0e4a9438aeb912ba23773f521bcbdc7994cca76179ade002038634137f7ed80a680d1cdc70d3778096df623c6786129d7c4d7578bede414b0157a610b1f5982eca4784eeb915ec445afce14a6967b2d01e2fad751fee3ef128126935dc3fb9890d9cdbffb8f50becc723; TSPD_101_DID=0868f8be6fab2800bda1a5f2ce95a204fddd7de6ef962eb753472c50f130af8b61583aa5c8b698c845baeee2be435bd908f0619f120638004e836ca2a2e1df49a8a5097a9f940761cc289bde7d99a2fb7f684598da78f04736639e0aff6a4dd544f1df4b90f45309ef481f5eba5b9127; TS011f2d1a=01266d26d065580958784c397bc70fe64efef63efb20a617a0180bd4443d9813a8e157bad4509bc4d5bfa0cf5f86b887142766db7c; TSPD_101=0868f8be6fab28003340859fe760e0cf6b8b0bd9b47a4f2ef9dc477ede672e34d2bf23bcdf221a5fa58b80c005d2b94b08de460c590518008f5b365708fa507c5ca1732140a3428bba23ce13beb1c95e; TS5220f739077=0868f8be6fab28000fdf95f1e6b55c4a7eb168cbae2cc2f300626eaadb2b68fb57bb55271e170672454d048fef0b54a608729bf09e1720007f571959265335e055908aec309551c2b575881f929d9d16db75ee4300aef382; TS5220f739029=0868f8be6fab28005ba9c13f1de819fa5cf6da62531458108fcfcccdc2d7ab16f19f1b8c865d777aece9084079439dbc; TSf1edb2d2027=0868f8be6fab2000aec0a553e5a61b4237081e21ae18adf48045d10dbcb0cf9ef594ba6c75dc672d08071abe781130009ca5cf0218e2380baa8fbbc3f3065f1d4f75b35c339832b29ee7f0a2cddecc91fae379db5942db207935b58b4fe1d497',
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