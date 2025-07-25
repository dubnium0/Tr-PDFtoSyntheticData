import streamlit as st
import requests
import json

st.set_page_config(page_title="Finansal PDF'ten Sentetik Veri Üretimi", layout="wide")
st.title("📄 Türkçe Finansal PDF'ten Sentetik İnstruction Data Üretimi")
st.write("PDF dosyanızı yükleyin, sistem otomatik olarak finansal sorular ve cevaplar üretsin!")

backend_url = "http://localhost:8000/process_pdf/"

q_prompt_input = st.text_area("Soru üretim promptu (opsiyonel)", value="", help="Boş bırakılırsa varsayılan prompt kullanılır.")
system_message_input = st.text_area("Cevap üretim promptu (opsiyonel)", value="", help="Boş bırakılırsa varsayılan prompt kullanılır.")

input_que = st.text_input("Kaç adet ve nasıl sorular üretilsin?", value="bana 50 tane mantıklı soru üret")

uploaded_file = st.file_uploader("PDF dosyanızı yükleyin", type=["pdf"])

if uploaded_file is not None:
    with st.spinner("PDF işleniyor, lütfen bekleyin..."):
        files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
        data = {
            "input_que": input_que,
            "q_prompt_input": q_prompt_input,
            "system_message_input": system_message_input
        }
        response = requests.post(backend_url, files=files, data=data)
        if response.status_code == 200:
            data = response.json()
            st.success("Soru-cevaplar başarıyla üretildi!")
            st.write("### Sonuçlar:")
            results = data["results"]
            progress_bar = st.progress(0)
            for i, item in enumerate(results):
                st.json(item)
                progress_bar.progress(int((i + 1) / len(results) * 100))
            st.download_button(
                label="JSON'u indir",
                data=json.dumps(results, ensure_ascii=False, indent=4),
                file_name="instruction_dataset.json",
                mime="application/json"
            )
        else:
            st.error("Bir hata oluştu. Lütfen tekrar deneyin.") 