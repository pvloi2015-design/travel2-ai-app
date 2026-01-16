import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Cấu hình API
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Chưa cấu hình API Key!")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

st.title("📸 Vietnam Travel AI Designer")

# 2. Giao diện
location = st.selectbox("Nơi muốn đến:", ["Đà Lạt", "Phú Quốc", "Huế", "Hội An"])
ratio = st.radio("Tỉ lệ:", ["9:16", "16:9"], horizontal=True)
uploaded_file = st.file_uploader("Tải ảnh chân dung...", type=["jpg", "png", "jpeg"])

if uploaded_file and st.button("✨ Thiết kế ngay"):
    img = Image.open(uploaded_file)
    
    with st.spinner("Đang tìm Model phù hợp trên server..."):
        try:
            # TỰ ĐỘNG DÒ TÌM MODEL KHẢ DỤNG
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            
            # Ưu tiên lấy bản Flash, nếu không có lấy bản bất kỳ hỗ trợ Vision
            target_model = ""
            for m in available_models:
                if "gemini-1.5-flash" in m:
                    target_model = m
                    break
            if not target_model:
                target_model = available_models[0] # Lấy đại 1 model nếu không thấy Flash

            st.info(f"Đang chạy bằng model: {target_model}")
            
            model = genai.GenerativeModel(target_model)
            prompt = f"Write a high-quality image prompt to place this person in {location}, Vietnam. Ratio {ratio}."
            
            response = model.generate_content([prompt, img])
            st.success("Thành công!")
            st.code(response.text)
            
        except Exception as e:
            st.error(f"Lỗi hệ thống: {e}")
            st.info("Vui lòng kiểm tra lại API Key đã tạo trong 'New Project' chưa.")
