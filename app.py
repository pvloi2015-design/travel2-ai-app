import streamlit as st
import google.generativeai as genai
from PIL import Image

# Kiểm tra Secrets
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Lỗi: Không tìm thấy API Key trong Secrets!")
    st.stop()

# Cấu hình API
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

st.set_page_config(page_title="Travel AI", page_icon="📸")
st.title("📸 Vietnam Travel AI Designer")

# Giao diện chọn
col_a, col_b = st.columns(2)
with col_a:
    location = st.selectbox("Điểm đến:", ["Đà Lạt", "Phú Quốc", "Huế", "Hội An", "Hà Giang"])
with col_b:
    ratio = st.radio("Tỉ lệ:", ["9:16 (TikTok)", "16:9 (YouTube)"], horizontal=True)

uploaded_file = st.file_uploader("Tải ảnh của bạn lên...", type=["jpg", "png", "jpeg"])

if uploaded_file and st.button("✨ Thiết kế ngay"):
    img = Image.open(uploaded_file)
    st.image(img, caption="Ảnh của bạn", width=300)
    
    with st.spinner("AI đang tìm đường đến " + location + "..."):
        try:
            # SỬA LỖI TẠI ĐÂY: Dùng tên model đầy đủ cho bản v1beta
            # Chúng ta thử gemini-1.5-flash-latest hoặc gemini-1.5-pro
            model = genai.GenerativeModel('models/gemini-1.5-flash-latest') 
            
            prompt = f"Analyze this person and write a high-quality English image prompt to place them in {location}, Vietnam. Aspect ratio {ratio}. Style: professional cinematic travel photography, ultra-realistic."
            
            # Gửi yêu cầu
            response = model.generate_content([prompt, img])
            
            st.success("🎉 Thành công! Dưới đây là Prompt của bạn:")
            st.code(response.text)
            st.info("Mẹo: Copy đoạn tiếng Anh trên dán vào các công cụ vẽ ảnh như Midjourney hoặc Leonardo.ai")
            
        except Exception as e:
            # Nếu vẫn lỗi, thử model gemini-1.5-pro
            try:
                model_pro = genai.GenerativeModel('models/gemini-1.5-pro-latest')
                response = model_pro.generate_content([prompt, img])
                st.success("🎉 Thành công (Dùng bản Pro):")
                st.code(response.text)
            except Exception as e2:
                st.error(f"Lỗi: {str(e2)}")
                st.warning("Gợi ý: Hãy thử vào Google AI Studio tạo lại một API Key mới hoàn toàn.")
