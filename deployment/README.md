# Deployment dan Monitoring - Prediksi Biaya Asuransi

Aplikasi Streamlit untuk memprediksi biaya asuransi kesehatan menggunakan pipeline Random Forest, serta memantau riwayat prediksi.

## Fitur monitoring
- Jumlah prediksi yang tercatat.
- Rata-rata dan nilai prediksi tertinggi.
- Grafik tren nilai prediksi berdasarkan waktu.
- Tabel riwayat prediksi.
- Unduh riwayat sebagai CSV.

## Menjalankan secara lokal

1. Buka terminal pada folder `deployment`.
2. Install dependensi:
   ```bash
   pip install -r requirements.txt
   ```
3. Jalankan aplikasi:
   ```bash
   streamlit run app.py
   ```

Setiap kali prediksi dilakukan, input dan hasilnya disimpan ke `predictions_log.csv` di folder aplikasi. Untuk hosting cloud, penyimpanan file lokal bisa bersifat sementara atau tidak persisten bergantung pada platform; gunakan database atau penyimpanan persisten jika log harus bertahan setelah aplikasi dimulai ulang.

## Catatan
Monitoring ini mencatat aktivitas dan distribusi hasil prediksi. Ini belum mengukur akurasi prediksi secara langsung karena nilai biaya aktual tidak dimasukkan.
