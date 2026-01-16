import streamlit as st
import google.generativeai as genai
from PIL import Image

# Thiết lập API
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Bạn chưa cấu hình API Key trong mục Secrets!")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

st.title("📸 App Du Lịch Ảo AI")

# Menu chọn
location = st.selectbox("Chọn nơi muốn đến:", ["Đà Lạt", "Phú Quốc", "Huế", "Hà Giang"])
ratio = st.radio("Tỉ lệ khung hình:", ["9:16 (TikTok)", "16:9 (YouTube)"])

# Tải ảnh
uploaded_file = st.file_uploader("Tải ảnh chân dung của bạn", type=["jpg", "png", "jpeg"])

if uploaded_file and st.button("Tạo thiết kế"):
    img = Image.open(uploaded_file)
    st.image(img, caption="Ảnh gốc", width=300)
    
    with st.spinner("AI đang xử lý..."):
        try:
            # 1. Thử dùng model ổn định nhất
            model_name = 'gemini-1.5-flash' 
            model = genai.GenerativeModel(model_name)
            
            # 2. Câu lệnh gửi cho AI
            prompt = f"Analyze this person and write a high-quality image prompt to place them in {location}. Aspect ratio {ratio}. Style: cinematic travel photography."
            
            # 3. Gửi yêu cầu
            response = model.generate_content([prompt, img])
            
            st.success("Xong rồi! Hãy dùng Prompt này để tạo ảnh:")
            st.code(response.text)
            
        except Exception as e:
            # Nếu vẫn lỗi NotFound, AI sẽ thử model 'gemini-pro-vision' (bản cũ hơn nhưng ổn định)
            try:
                model = genai.GenerativeModel('gemini-1.0-pro-vision-latest')
                response = model.generate_content([prompt, img])
                st.success("Xong rồi! (Chạy bằng model dự phòng):")
                st.code(response.text)
            except:
                st.error(f"Lỗi kết nối API: {str(e)}")
                st.info("Mẹo: Hãy kiểm tra xem API Key của bạn đã được tạo trong mục 'Generative Language API' chưa.")
