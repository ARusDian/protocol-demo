
# Multi-Protocol Application

Aplikasi Multi-Protocol adalah aplikasi berbasis GUI yang memungkinkan pengguna untuk mengelola berbagai protokol komunikasi, termasuk HTTP, RPC, dan MQTT. Aplikasi ini juga menyediakan fungsionalitas untuk mengukur latensi dari protokol yang digunakan.

## Fitur

- **Pengelolaan Server HTTP**: Mulai dan hentikan server HTTP dengan antarmuka yang sederhana.
- **Pengelolaan Server RPC**: Mulai dan hentikan server RPC dengan mudah.
- **Klien MQTT**: Interaksi dengan broker MQTT untuk mengirim dan menerima pesan, termasuk diagram interaktif untuk visualisasi komunikasi.
- **Permintaan dan Respon**: Fasilitas untuk mengirim permintaan dan menerima respon melalui protokol tertentu, disertai diagram interaktif untuk memudahkan pemahaman.
- **Pengujian Latensi**: Mengukur latensi dari komunikasi antara server dan klien dengan diagram interaktif untuk analisis hasil.
  
### Demo

- **MQTT**: Aplikasi chat global yang menggunakan protokol MQTT untuk komunikasi antar pengguna.
- **Request-Response**: Pengujian request-response yang menunjukkan bagaimana permintaan dan respon diproses.
- **RPC**: Menjalankan perintah yang sangat berat pada perangkat lain untuk menguji efisiensi dan latensi protokol RPC.

## Instalasi

Untuk menjalankan aplikasi ini, Anda perlu menginstal beberapa dependensi. Gunakan perintah berikut untuk menginstalnya:

```bash
pip install -r requirements.txt
```

### Cara Instalasi

1. **Clone repositori**:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Instal dependensi**:
    Jalankan perintah berikut untuk menginstal semua dependensi yang diperlukan:
    ```bash
    pip install -r requirements.txt
    ```

## Cara Menjalankan Aplikasi

1. Jalankan aplikasi dengan menjalankan `main.py`:
    ```bash
    python main.py
    ```

2. Masukkan jalur Python yang benar pada input yang disediakan. Pastikan Anda memiliki Python terinstal di sistem Anda. Contoh:
   ```
   C:/Users/Dian/anaconda3/envs/py310/python.exe
   ```

3. Gunakan tombol di aplikasi untuk memulai atau menghentikan server HTTP dan RPC sesuai kebutuhan.

## Struktur Proyek

- `main.py`: Skrip utama untuk menjalankan aplikasi.
- `server/`: Direktori yang berisi skrip untuk server HTTP dan RPC.
- `mqtt_client.py`: Modul untuk klien MQTT.
- `request_response.py`: Modul untuk fungsionalitas permintaan dan respon.
- `rpc_client.py`: Modul untuk klien RPC.
- `benchmark.py`: Modul untuk pengujian latensi.

## Penjelasan Protokol

### 1. MQTT (Message Queuing Telemetry Transport)

MQTT adalah protokol messaging yang ringan dan dirancang untuk komunikasi machine-to-machine (M2M) dan Internet of Things (IoT). Protokol ini menggunakan model publish-subscribe, yang memungkinkan perangkat untuk berkomunikasi secara efisien dan menghemat bandwidth.

**Kelebihan:**
- **Ringan**: Memiliki overhead yang sangat rendah, cocok untuk perangkat dengan sumber daya terbatas.
- **Skalabilitas**: Mudah untuk menambahkan perangkat baru ke dalam sistem.
- **Dukungan untuk QoS (Quality of Service)**: Menyediakan pengaturan QoS yang berbeda untuk menjamin pengiriman pesan.

**Kekurangan:**
- **Keamanan**: Standar keamanan bawaannya tidak sekuat beberapa protokol lain, meskipun dapat ditingkatkan dengan implementasi tambahan.
- **Ketergantungan pada Broker**: Memerlukan broker untuk pengelolaan komunikasi, yang bisa menjadi titik tunggal kegagalan.

### 2. HTTP (Hypertext Transfer Protocol)

HTTP adalah protokol komunikasi yang digunakan untuk mentransfer data di web. Ini adalah protokol stateless yang digunakan oleh browser untuk berkomunikasi dengan server.

**Kelebihan:**
- **Umum dan Luas**: Digunakan secara luas di seluruh web, sehingga dukungan dan dokumentasi sangat banyak.
- **Mendukung Berbagai Format Data**: Mampu mentransfer berbagai jenis data, termasuk teks, gambar, dan video.
- **Dukungan untuk Protokol Keamanan (HTTPS)**: Dapat mengamankan komunikasi melalui enkripsi.

**Kekurangan:**
- **Overhead yang Tinggi**: Memiliki overhead yang lebih besar dibandingkan dengan protokol lain seperti MQTT.
- **Stateless**: Setiap permintaan baru dianggap sebagai permintaan baru, yang bisa mengakibatkan latensi lebih tinggi dalam sesi yang lebih kompleks.

### 3. RPC (Remote Procedure Call)

RPC adalah protokol yang memungkinkan program untuk menjalankan prosedur atau fungsi yang berada di server jarak jauh seolah-olah itu adalah fungsi lokal. Ini sangat berguna dalam arsitektur mikroservis.

**Kelebihan:**
- **Mudah Digunakan**: Memudahkan interaksi antara layanan yang berbeda dengan membuat panggilan seolah-olah itu adalah fungsi lokal.
- **Dukungan untuk Berbagai Bahasa Pemrograman**: Banyak implementasi RPC yang mendukung berbagai bahasa pemrograman.

**Kekurangan:**
- **Kompleksitas**: Implementasi dan pengelolaan RPC bisa menjadi rumit, terutama dalam skala besar.
- **Keterbatasan Kinerja**: Pada jaringan yang tidak stabil, panggilan RPC bisa mengalami latensi yang lebih tinggi dibandingkan komunikasi langsung.

## Studi Kasus Umum

### 1. MQTT (Message Queuing Telemetry Transport)

**Studi Kasus: Aplikasi Chat Global**
Aplikasi chat yang mengandalkan MQTT dapat memanfaatkan kemampuan publish-subscribe untuk mengirim dan menerima pesan secara real-time. Dengan menghubungkan berbagai klien ke broker MQTT, pengguna dapat berinteraksi dalam saluran chat tanpa harus langsung terhubung satu sama lain. Keuntungan penggunaan MQTT dalam aplikasi ini adalah latensi yang rendah dan efisiensi bandwidth, sehingga cocok untuk perangkat mobile dan IoT.

### 2. HTTP (Hypertext Transfer Protocol)

**Studi Kasus: Sistem Permintaan dan Respon**
Protokol HTTP dapat digunakan dalam sistem permintaan dan respon untuk mengirimkan data antara klien dan server. Misalnya, sebuah aplikasi web dapat mengirimkan permintaan HTTP ke server untuk mengambil data pengguna dan menerima respons dalam format JSON. Ini memungkinkan aplikasi web untuk memuat data secara dinamis, memberikan pengalaman pengguna yang lebih baik tanpa memuat ulang halaman.

### 3. RPC (Remote Procedure Call)

**Studi Kasus: Eksekusi Perintah Berat di Layanan Mikroservis**
RPC sangat cocok untuk aplikasi yang membutuhkan interaksi antar layanan mikroservis. Misalnya, dalam sistem manajemen data besar, satu layanan dapat menggunakan RPC untuk memanggil prosedur yang memerlukan pemrosesan data berat pada layanan lain. Ini memungkinkan sistem untuk memisahkan tanggung jawab dan meningkatkan skalabilitas serta efisiensi. Contohnya, aplikasi yang menghitung analitik secara real-time dapat memanggil prosedur di layanan lain yang khusus untuk pemrosesan data besar.

