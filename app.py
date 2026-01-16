import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# 1. Cấu hình API
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Chưa cấu hình API Key trong Secrets!")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

st.set_page_config(page_title="Vietnam Travel AI Image Gen", layout="wide")
st.title("📸 Vietnam Travel AI: Tạo Ảnh Trực Tiếp")

# Khởi tạo bộ nhớ lịch sử nếu chưa có
if "history" not in st.session_state:
    st.session_state.history = []

# Chọn Model Imagen khả dụng (Hãy kiểm tra lại trong Google AI Studio > List Models)
# Ví dụ: 'imagen-3.0-generate-001' hoặc 'imagen-2.0-generate-001'
IMAGEN_MODEL_NAME = 'imagen-3.0-generate-001' 

tab1, tab2 = st.tabs(["🚀 Thiết kế & Tạo Ảnh", "📜 Lịch sử hành trình"])

with tab1:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        location = st.selectbox("Điểm đến:", ["Đà Lạt", "Phú Quốc", "Huế", "Hội An", "Sapa", "Hạ Long"])
        ratio = st.radio("Tỉ lệ:", ["9:16 (TikTok)", "16:9 (YouTube)"], horizontal=True)
        uploaded_file = st.file_uploader("Tải ảnh lên...", type=["jpg", "png", "jpeg"])
        
    if uploaded_file and st.button("✨ Bắt đầu tạo ảnh"):
        img = Image.open(uploaded_file)
        
        with st.spinner("Đang kết nối AI và tạo hình ảnh..."):
            try:
                # Bước 1: Dùng Gemini để phân tích ảnh và viết Prompt
                gemini_model = genai.GenerativeModel('gemini-1.5-flash') 
                prompt_analysis = f"""
                Analyze the person in this image. Write a detailed English image prompt (max 150 words) to place them in {location}, Vietnam, with aspect ratio {ratio}. 
                Include details about their appearance, clothing, and the specific landscape elements of {location}.
                Style: Photorealistic, cinematic, professional travel photography.
                """
                response_gemini = gemini_model.generate_content([prompt_analysis, img])
                image_prompt_text = response_gemini.text
                
                # Bước 2: Dùng Imagen để tạo ảnh từ Prompt vừa tạo
                st.info(f"Đang dùng Imagen ({IMAGEN_MODEL_NAME}) để vẽ ảnh...")
                imagen_model = genai.GenerativeModel(IMAGEN_MODEL_NAME)
                response_imagen = imagen_model.generate_content(image_prompt_text)
                
                # Chuyển đổi dữ liệu ảnh trả về sang định dạng Streamlit có thể hiển thị
                # Lưu ý: Imagen API trả về dạng khác nhau tùy phiên bản và cách cấu hình
                # Thông thường là list of PIL Image hoặc byte data.
                if hasattr(response_imagen, 'images') and response_imagen.images:
                    generated_image = response_imagen.images[0]
                else: # Trường hợp API trả về thẳng data hoặc có method khác
                    # Đây là một giả định, bạn có thể cần chỉnh sửa tùy theo cách API Imagen trả về.
                    # Ví dụ: generated_image = Image.open(io.BytesIO(response_imagen.raw_data))
                    generated_image = None # Nếu không tìm thấy ảnh, đặt là None

                if generated_image:
                    with col2:
                        st.success("Tạo ảnh hoàn tất!")
                        st.image(generated_image, caption="Ảnh AI đã tạo", use_container_width=True)
                        st.download_button(
                            label="Tải ảnh về",
                            data=generated_image.save("generated_image.png"), # Lưu tạm vào file
                            file_name="vietnam_travel_ai.png",
                            mime="image/png"
                        )
                        st.info("Prompt đã dùng để tạo ảnh:")
                        st.code(image_prompt_text)
                else:
                    st.warning("Không thể hiển thị ảnh. Có thể do lỗi API Imagen hoặc định dạng trả về.")
                    st.info("Prompt đã tạo (dán vào công cụ khác):")
                    st.code(image_prompt_text)

                # Lưu vào lịch sử (cả prompt và ảnh nếu có)
                st.session_state.history.append({
                    "loc": location, 
                    "prompt": image_prompt_text, 
                    "image": generated_image 
                })
                
            except Exception as e:
                st.error(f"Lỗi khi tạo ảnh: {e}")
                st.info("Lỗi này thường do API Key chưa được cấp quyền cho Imagen hoặc tên Model không đúng.")
                st.warning("Chúng tôi sẽ hiển thị Prompt để bạn có thể dán vào công cụ khác.")
                # Nếu lỗi, vẫn cố gắng lấy prompt từ Gemini để người dùng sử dụng
                try:
                    gemini_model = genai.GenerativeModel('gemini-1.5-flash') 
                    prompt_analysis = f"""
                    Analyze the person in this image. Write a detailed English image prompt (max 150 words) to place them in {location}, Vietnam, with aspect ratio {ratio}. 
                    Include details about their appearance, clothing, and the specific landscape elements of {location}.
                    Style: Photorealistic, cinematic, professional travel photography.
                    """
                    response_gemini = gemini_model.generate_content([prompt_analysis, img])
                    st.code(response_gemini.text)
                except:
                    st.error("Không thể tạo cả Prompt. Vui lòng kiểm tra lại API Key.")

with tab2:
    if st.session_state.history:
        for i, item in enumerate(reversed(st.session_state.history)):
            st.subheader(f"Chuyến đi #{len(st.session_state.history) - i} đến {item['loc']}")
            st.code(item['prompt'])
            if item['image']:
                st.image(item['image'], caption="Ảnh đã tạo", use_container_width=True)
            st.markdown("---")
    else:
        st.write("Bạn chưa có chuyến đi nào trong lịch sử.")
