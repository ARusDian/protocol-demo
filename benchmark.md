# Ringkasan Hasil Benchmark

Pada pengujian ini, dilakukan evaluasi terhadap latensi dari beberapa protokol komunikasi yang digunakan dalam sistem, yaitu **MQTT**, **HTTP**, dan **RPC**. Tujuan dari pengujian ini adalah untuk mengukur kecepatan respon dan efisiensi masing-masing protokol.

### 1. Latensi **MQTT**

- **Waktu Subscribe**: `0.00 ms`
- **Waktu Publish**: `557.56 ms`
- **Latensi Penerima**: `471.63 ms`
- **Total Latensi MQTT**: `1029.19 ms`

#### Penjelasan:
MQTT (Message Queuing Telemetry Transport) adalah protokol komunikasi ringan yang dioptimalkan untuk jaringan dengan bandwidth rendah dan latensi kecil. Protokol ini menggunakan model **publish/subscribe**, di mana pengirim (publisher) dan penerima (subscriber) berkomunikasi melalui **broker**.

#### Studi Kasus Umum:
- **Aplikasi IoT (Internet of Things)**: MQTT sering digunakan untuk mengirimkan data sensor dari perangkat IoT ke server atau antara perangkat satu dengan yang lain. Misalnya, perangkat rumah pintar (smart home), jaringan sensor lingkungan, dan sistem otomatisasi industri sering menggunakan MQTT karena kecepatan dan efisiensinya dalam menangani data real-time.
- **Sistem Kendali Jarak Jauh**: MQTT digunakan dalam sistem yang memerlukan komunikasi latensi rendah, seperti pengendalian kendaraan jarak jauh atau robotik.

**Kesimpulan**: Total latensi komunikasi MQTT adalah **1029.19 ms**, yang menunjukkan protokol ini sangat cocok untuk aplikasi yang memerlukan komunikasi data secara real-time dengan jaringan yang bandwidth-nya terbatas.

---

### 2. Latensi **HTTP**

- **Latensi Server**: `2029.19 ms`
- **Latensi Klien**: `1.07 ms`
- **Total Latensi HTTP**: `2030.25 ms`

#### Penjelasan:
HTTP (Hypertext Transfer Protocol) adalah protokol yang paling umum digunakan untuk pertukaran data di web. HTTP memerlukan overhead yang lebih besar karena setiap permintaan membutuhkan **koneksi**, **header data**, dan **proses respon**, yang membuatnya kurang efisien dibandingkan dengan protokol lain seperti MQTT dalam hal latensi.

#### Studi Kasus Umum:
- **Aplikasi Web**: HTTP adalah fondasi untuk komunikasi di web. Setiap kali kita mengunjungi situs web, browser mengirimkan permintaan HTTP ke server untuk mengambil data. HTTP juga digunakan untuk API komunikasi dalam aplikasi yang menampilkan dan memproses data yang diambil dari server.
- **Sistem REST API**: Banyak layanan yang menggunakan HTTP sebagai protokol dasar untuk komunikasi antara server dan klien menggunakan model REST (Representational State Transfer). Aplikasi seperti aplikasi mobile, layanan SaaS, dan portal online umumnya memanfaatkan HTTP.

**Kesimpulan**: Latensi total HTTP mencapai **2030.25 ms**, yang cukup tinggi dibandingkan protokol lain. HTTP lebih cocok untuk komunikasi yang membutuhkan keandalan dan pertukaran data dalam format yang kaya, seperti aplikasi web atau API, meskipun tidak optimal untuk skenario latensi rendah.

---

### 3. Latensi **RPC**

- **Latensi RPC**: `2020.60 ms`

#### Penjelasan:
RPC (Remote Procedure Call) adalah protokol yang memungkinkan klien untuk mengeksekusi fungsi di server remote seolah-olah fungsi tersebut dieksekusi secara lokal. RPC memungkinkan sistem terdistribusi untuk beroperasi dengan cara yang lebih mudah diprogram, tetapi latensinya bisa lebih besar karena overhead jaringan.

#### Studi Kasus Umum:
- **Layanan Terdistribusi**: RPC sering digunakan untuk komunikasi antara layanan yang berjalan di server yang berbeda dalam aplikasi skala besar, seperti di **sistem microservices**. Hal ini memudahkan satu layanan untuk memanggil fungsi di layanan lain tanpa harus khawatir tentang detail implementasi.
- **Sistem Perbankan Terdistribusi**: Di sistem yang memerlukan integrasi antar modul atau layanan yang berjalan di lokasi yang berbeda, seperti perbankan, RPC digunakan untuk memanggil proses-proses penting yang membutuhkan sinkronisasi.
- **Komputasi Terdistribusi**: RPC juga sering digunakan dalam sistem komputasi terdistribusi, di mana satu sistem klien bisa memanggil fungsi komputasi yang dilakukan di kluster server atau komputasi awan.

**Kesimpulan**: Total latensi untuk RPC adalah **2020.60 ms**, yang mirip dengan HTTP. Meskipun RPC menawarkan kemudahan dalam melakukan panggilan jarak jauh, protokol ini lebih cocok untuk aplikasi terdistribusi di mana komunikasi antar sistem harus dilakukan dengan abstraksi tinggi, dan latensi bukanlah faktor krusial.

---

### Kesimpulan Umum

Dari hasil pengujian, dapat disimpulkan bahwa:
1. **MQTT** menunjukkan performa terbaik dalam hal latensi dan sangat cocok untuk aplikasi yang memerlukan komunikasi real-time dan konsumsi bandwidth rendah.
2. **HTTP** adalah protokol yang lebih umum digunakan dalam komunikasi web dan REST API, namun memiliki latensi yang lebih tinggi dibandingkan dengan MQTT.
3. **RPC** menawarkan fleksibilitas untuk panggilan fungsi jarak jauh, terutama dalam sistem terdistribusi, tetapi memiliki latensi yang mirip dengan HTTP, sehingga tidak cocok untuk aplikasi dengan kebutuhan latensi rendah.

Penggunaan protokol harus disesuaikan dengan kebutuhan aplikasi. Jika aplikasi memerlukan pengiriman data real-time dengan latensi rendah, **MQTT** adalah pilihan terbaik. Jika aplikasi melibatkan interaksi pengguna melalui web atau API, **HTTP** lebih cocok. Sementara itu, untuk sistem yang terdistribusi dan memerlukan integrasi modul yang kompleks, **RPC** adalah opsi yang baik.
