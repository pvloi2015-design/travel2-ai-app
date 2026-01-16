import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Cấu hình API
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Chưa cấu hình API Key trong Secrets!")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

st.set_page_config(page_title="Vietnam Travel AI Pro", layout="wide")
st.title("📸 Vietnam Travel AI Pro")

# Khởi tạo bộ nhớ lịch sử nếu chưa có
if "history" not in st.session_state:
    st.session_state.history = []

# Chia giao diện thành 2 Tab
tab1, tab2 = st.tabs(["🚀 Thiết kế mới", "📜 Lịch sử hành trình"])

with tab1:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        location = st.selectbox("Điểm đến:", ["Đà Lạt", "Phú Quốc", "Huế", "Hội An", "Sapa", "Hạ Long"])
        ratio = st.radio("Tỉ lệ:", ["9:16 (TikTok)", "16:9 (YouTube)"], horizontal=True)
        uploaded_file = st.file_uploader("Tải ảnh lên...", type=["jpg", "png", "jpeg"])
        
    if uploaded_file and st.button("✨ Bắt đầu thiết kế"):
        img = Image.open(uploaded_file)
        
        with st.spinner("Đang xử lý nghệ thuật..."):
            try:
                # Tìm model khả dụng
                available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                target_model = next((m for m in available_models if "gemini-1.5-flash" in m), available_models[0])
                model = genai.GenerativeModel(target_model)
                
                # Prompt yêu cầu AI viết cả tiếng Anh và tiếng Việt
                prompt = f"""
                Analyze the person in this image. 
                1. Write a high-quality English image prompt to place them in {location}, Vietnam with ratio {ratio}.
                2. After the English prompt, provide a Vietnamese translation for the user.
                Style: Cinematic, professional photography.
                """
                
                response = model.generate_content([prompt, img])
                result_text = response.text
                
                # Lưu vào lịch sử
                st.session_state.history.append({"loc": location, "res": result_text})
                
                with col2:
                    st.success("Thiết kế hoàn tất!")
                    st.markdown(result_text)
                    
            except Exception as e:
                st.error(f"Lỗi: {e}")

with tab2:
    if st.session_state.history:
        for item in reversed(st.session_state.history):
            with st.expander(f"Chuyến đi đến {item['loc']}"):
                st.write(item['res'])
    else:
        st.write("Bạn chưa có chuyến đi nào trong lịch sử.")
