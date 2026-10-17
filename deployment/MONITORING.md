# Monitoring Model

Monitoring yang disertakan merupakan monitoring operasional sederhana.

## Yang dipantau
1. Total prediksi yang dilakukan pengguna.
2. Rata-rata biaya prediksi.
3. Prediksi tertinggi.
4. Tren nilai prediksi berdasarkan waktu.
5. Riwayat input dan output model yang dapat diunduh dalam format CSV.

## Batasan
Nilai prediksi saja tidak cukup untuk menghitung MAE, RMSE, atau R² setelah deployment. Untuk mengevaluasi performa model di produksi, tambahkan biaya aktual yang terverifikasi dan bandingkan dengan hasil prediksi. File log lokal juga dapat hilang atau tidak bertahan pada platform hosting tertentu.
