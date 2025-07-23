# Panduan Setup dan Deployment Smart Contract OP_NET

Dokumen ini menyediakan panduan komprehensif untuk menyiapkan lingkungan pengembangan, mengkloning, membangun, dan melakukan deployment smart contract OP_NET. Proses ini dirancang untuk memfasilitasi pengujian di berbagai chain dan mempercepat pengembangan proyek.

## 1. Struktur Proyek

Struktur proyek yang diharapkan adalah sebagai berikut:

```
OP_NET/
├── OP_20/                # Direktori smart contract OP_20 asli (template)
│   ├── src/
│   │   └── contracts/
│   │       └── MyToken.ts
│   ├── ... (file konfigurasi lainnya)
├── clone_contracts.sh    # Script Bash untuk mengkloning dan membangun kontrak
├── deploy_contract.py    # Script Python untuk deployment otomatis melalui OP_WALLET
├── venv_opnet/           # Virtual environment Python (direkomendasikan)
└── README.md             # Dokumen panduan ini
```

Setelah menjalankan `clone_contracts.sh`, akan ada 20 direktori baru yang dibuat, seperti `OP_20_TKA`, `OP_20_TKB`, dst., masing-masing berisi smart contract yang telah dikloning dan dibangun.

## 2. Kloning dan Membangun Smart Contract (clone_contracts.sh)

Script `clone_contracts.sh` bertanggung jawab untuk mengkloning smart contract `OP_20` yang ada menjadi 20 kontrak terpisah. Setiap kontrak baru akan memiliki nama token, ticker, dan nama file yang unik. Script ini juga akan menginstal dependensi yang diperlukan dan membangun setiap kontrak, menghasilkan file `.wasm` yang siap untuk deployment.

### Cara Kerja Script Kloning:

1.  **Definisi Token:** Script ini memiliki array yang berisi pasangan nama token dan simbol (ticker) untuk 20 kontrak yang akan dibuat (misalnya, `TokenA:TKA`, `TokenB:TKB`, dst.).
2.  **Pembuatan Direktori:** Untuk setiap pasangan token, script akan membuat direktori baru (misalnya, `OP_20_TKA`) dan menyalin semua file dari template `OP_20` ke direktori baru tersebut.
3.  **Modifikasi Kontrak:** Script akan memodifikasi file `MyToken.ts` di setiap direktori baru untuk mengganti nama kontrak, nama token, dan simbol token sesuai dengan yang ditentukan dalam array. Ini juga akan memperbarui file `index.ts`, `asconfig.json`, dan `package.json` agar sesuai dengan nama kontrak dan token yang baru.
4.  **Instalasi Dependensi dan Build:** Setelah modifikasi, script akan masuk ke direktori kontrak yang baru, menjalankan `npm install` untuk menginstal dependensi Node.js, dan kemudian `npm run build` untuk mengkompilasi smart contract. Proses `npm run build` ini akan menghasilkan file `.wasm` (misalnya, `TokenA.wasm`) di dalam sub-direktori `build` di setiap folder kontrak yang dikloning (misalnya, `OP_20_TKA/build/TokenA.wasm`).

### Cara Menggunakan Script Kloning:

1.  Pastikan Anda memiliki Node.js dan npm terinstal di sistem Anda.
2.  Tempatkan file `clone_contracts.sh` di direktori yang sama dengan folder `OP_20` (template smart contract asli).
3.  Berikan izin eksekusi pada script:
    ```bash
    chmod +x clone_contracts.sh
    ```
4.  Jalankan script:
    ```bash
    ./clone_contracts.sh
    ```

Proses ini mungkin memakan waktu cukup lama karena melibatkan instalasi dependensi dan build untuk setiap dari 20 kontrak.

## 3. Deployment Smart Contract (deploy_contract.py)

Script `deploy_contract.py` menggunakan Playwright untuk mengotomatiskan proses deployment file `.wasm` smart contract melalui ekstensi browser OP_WALLET. Penting untuk dicatat bahwa OP_NET saat ini tidak menyediakan alat CLI khusus untuk deployment, sehingga otomatisasi browser adalah pendekatan yang diperlukan.

### Perilaku Otentikasi OP_WALLET:

Script ini dirancang untuk membuka ekstensi OP_WALLET di browser dan mensimulasikan interaksi pengguna. Ini **tidak** akan meminta Anda untuk mengimpor private key ke dalam script. Sebaliknya, script akan:

1.  Membuka ekstensi OP_WALLET.
2.  Memberikan waktu 10 detik bagi pengguna untuk **membuka kunci (unlock)** OP_WALLET secara manual jika terkunci. Ini berarti Anda perlu memastikan OP_WALLET Anda sudah terbuka dan siap digunakan sebelum script mencoba berinteraksi dengannya.
3.  Mencoba mengklik tombol atau elemen UI yang relevan untuk navigasi ke halaman deployment di OP_WALLET.
4.  Mengunggah file `.wasm` yang ditentukan.
5.  Mencoba mengklik tombol konfirmasi deployment.

**Konfirmasi Otentikasi Berulang:**

Ya, jika Anda berencana untuk melakukan deployment 20 kontrak secara berurutan menggunakan script ini, Anda **mungkin perlu melakukan konfirmasi otentikasi di OP_WALLET sebanyak 20 kali**, atau setidaknya setiap kali OP_WALLET meminta persetujuan transaksi. Ini adalah fitur keamanan standar dari dompet kripto untuk memastikan bahwa setiap transaksi (termasuk deployment kontrak) disetujui oleh pengguna. Script ini akan menginisiasi prosesnya, tetapi persetujuan akhir akan tetap memerlukan interaksi manual Anda di jendela ekstensi OP_WALLET.

### Cara Menggunakan Script Deployment:

1.  **Prasyarat:**
    *   Pastikan Anda telah menjalankan `clone_contracts.sh` dan memiliki file `.wasm` yang ingin di-deploy.
    *   Instal Python 3 dan `pip`.
    *   Instal Playwright dan browser yang diperlukan. Sangat disarankan untuk menggunakan virtual environment.

2.  **Setup Virtual Environment (Direkomendasikan):**
    ```bash
    python3 -m venv venv_opnet
    source venv_opnet/bin/activate  # Untuk Linux/macOS
    # venv_opnet\Scripts\activate.bat # Untuk Windows Command Prompt
    # .\venv_opnet\Scripts\Activate.ps1 # Untuk Windows PowerShell
    ```

3.  **Instal Dependensi Python:**
    ```bash
    pip install playwright
    playwright install
    ```

4.  **Sesuaikan Script `deploy_contract.py`:**
    Buka file `deploy_contract.py` dan ubah baris berikut untuk menunjuk ke file `.wasm` yang ingin Anda deploy:
    ```python
    wasm_to_deploy = "OP_20_TKA/build/TokenA.wasm" # Ganti dengan path file .wasm yang sesuai
    ```
    Anda perlu mengubah `wasm_to_deploy` setiap kali Anda ingin mendeploy kontrak yang berbeda, atau Anda bisa memodifikasi script untuk mengulang deployment untuk semua 20 kontrak (ini akan memerlukan logika tambahan dalam script).

5.  **Jalankan Script Deployment:**
    ```bash
    python3 deploy_contract.py
    ```

6.  **Interaksi Manual:** Setelah menjalankan script, perhatikan jendela ekstensi OP_WALLET Anda. Anda mungkin perlu membuka kunci dompet dan mengkonfirmasi setiap transaksi deployment secara manual.

## 4. Lokasi File

Pastikan struktur file Anda mengikuti panduan ini:

*   `clone_contracts.sh` dan `deploy_contract.py` harus berada di direktori yang sama dengan folder `OP_20` (template asli) dan folder-folder `OP_20_TKA`, `OP_20_TKB`, dst. (hasil kloning).
*   File `.wasm` yang akan di-deploy berada di dalam sub-direktori `build` di setiap folder kontrak yang dikloning (misalnya, `OP_20_TKA/build/TokenA.wasm`).

## 5. Catatan Penting

*   **Biaya Faucet:** Proses deployment akan memakan biaya faucet. Pastikan Anda memiliki cukup tBTC di OP_WALLET Anda.
*   **Otomatisasi Browser:** Script `deploy_contract.py` berjalan dalam mode headless di lingkungan sandbox. Anda tidak akan melihat browser terbuka secara visual. Interaksi akan disimulasikan di latar belakang.
*   **Perubahan UI OP_WALLET:** Jika antarmuka pengguna OP_WALLET berubah di masa mendatang, selektor elemen UI dalam `deploy_contract.py` mungkin perlu disesuaikan. Anda mungkin perlu menggunakan alat inspeksi browser untuk menemukan selektor yang benar.

---

