import streamlit as st
import pandas as pd
import joblib
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent
MODEL_PATH = ROOT / "model.pkl"
LOG_PATH = ROOT / "predictions_log.csv"

model = joblib.load(MODEL_PATH)

st.set_page_config(page_title="Prediksi & Monitoring Asuransi", page_icon="📊", layout="wide")
st.title("Prediksi Biaya Asuransi Kesehatan")
st.caption("Model Random Forest dengan pencatatan prediksi sederhana untuk monitoring.")

def read_logs():
    if LOG_PATH.exists():
        try:
            return pd.read_csv(LOG_PATH)
        except (pd.errors.EmptyDataError, pd.errors.ParserError):
            return pd.DataFrame()
    return pd.DataFrame()

tab_predict, tab_monitor = st.tabs(["🔮 Prediksi", "📊 Monitoring"])

with tab_predict:
    st.subheader("Masukkan Data")
    with st.form("form_prediksi"):
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Usia", min_value=18, max_value=100, value=30, step=1)
            sex = st.selectbox("Jenis kelamin", ["female", "male"])
            bmi = st.number_input("BMI", min_value=10.0, max_value=70.0, value=25.0, step=0.1)
        with col2:
            children = st.number_input("Jumlah anak", min_value=0, max_value=10, value=0, step=1)
            smoker = st.selectbox("Status merokok", ["no", "yes"])
            region = st.selectbox("Wilayah", ["northeast", "northwest", "southeast", "southwest"])
        submitted = st.form_submit_button("Prediksi Biaya")

    if submitted:
        input_data = pd.DataFrame([{
            "age": age, "sex": sex, "bmi": bmi,
            "children": children, "smoker": smoker, "region": region
        }])
        prediction = float(model.predict(input_data)[0])
        st.success(f"Perkiraan biaya asuransi: ${prediction:,.2f}")
        st.caption("Estimasi model, bukan penawaran biaya asuransi sebenarnya.")

        log_row = pd.DataFrame([{
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "age": age,
            "sex": sex,
            "bmi": bmi,
            "children": children,
            "smoker": smoker,
            "region": region,
            "predicted_charges": round(prediction, 2)
        }])
        if LOG_PATH.exists():
            old_logs = read_logs()
            updated_logs = pd.concat([old_logs, log_row], ignore_index=True)
        else:
            updated_logs = log_row
        updated_logs.to_csv(LOG_PATH, index=False)
        st.info("Prediksi dicatat pada log monitoring.")

with tab_monitor:
    st.subheader("Monitoring Aktivitas Prediksi")
    logs = read_logs()
    if logs.empty:
        st.info("Belum ada data prediksi. Jalankan prediksi pada tab Prediksi agar log monitoring terisi.")
    else:
        if "predicted_charges" in logs.columns:
            c1, c2, c3 = st.columns(3)
            c1.metric("Total prediksi", f"{len(logs):,}")
            c2.metric("Rata-rata prediksi", f"${logs['predicted_charges'].mean():,.2f}")
            c3.metric("Prediksi tertinggi", f"${logs['predicted_charges'].max():,.2f}")

            st.markdown("#### Tren nilai prediksi")
            if "timestamp" in logs.columns:
                chart_data = logs.copy()
                chart_data["timestamp"] = pd.to_datetime(chart_data["timestamp"], errors="coerce")
                chart_data = chart_data.dropna(subset=["timestamp"]).sort_values("timestamp")
                if not chart_data.empty:
                    st.line_chart(chart_data.set_index("timestamp")["predicted_charges"])
            st.markdown("#### Riwayat prediksi")
            st.dataframe(logs.tail(100), use_container_width=True)
            st.download_button(
                "Unduh log monitoring (CSV)",
                data=logs.to_csv(index=False).encode("utf-8"),
                file_name="predictions_log.csv",
                mime="text/csv"
            )
        else:
            st.warning("Format log tidak sesuai. Periksa file predictions_log.csv.")
