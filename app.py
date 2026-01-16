import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Cấu hình API
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Chưa cấu hình API Key trong Secrets!")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

st.title("📸 App Du Lịch Ảo AI")

# 2. Giao diện
location = st.selectbox("Chọn nơi đến:", ["Đà Lạt", "Phú Quốc", "Huế", "Hội An", "Hà Giang"])
ratio = st.radio("Tỉ lệ:", ["9:16", "16:9"], horizontal=True)

uploaded_file = st.file_uploader("Tải ảnh chân dung...", type=["jpg", "png", "jpeg"])

if uploaded_file and st.button("✨ Thiết kế ngay"):
    img = Image.open(uploaded_file)
    st.image(img, width=300)
    
    with st.spinner("Đang kết nối với AI..."):
        # Cố gắng dùng Gemini 1.5 Flash (Bản nhanh nhất hiện nay)
        # Bỏ 'models/' vì một số môi trường v1beta tự thêm nó vào
        try:
            model = genai.GenerativeModel('gemini-1.5-flash') 
            prompt = f"Write an image prompt to place this person in {location}, Vietnam. Aspect ratio {ratio}."
            response = model.generate_content([prompt, img])
            st.success("Thành công!")
            st.code(response.text)
        except Exception as e:
            st.error(f"Vẫn gặp lỗi: {e}")
            st.info("Hãy thực hiện Bước 2 dưới đây để sửa lỗi hoàn toàn.")
