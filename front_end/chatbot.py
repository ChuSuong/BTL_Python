import streamlit as st
import os
import sys

# Thêm thư mục gốc vào sys.path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# Import các hàm từ src/main.py, load một lần
@st.cache_resource
def get_system_resources():
    from src.main import initialize_system, chat_with_ai
    return (*initialize_system(), chat_with_ai)
embedder, vector_search, chat_assistant, chat_with_ai = get_system_resources()

# Lưu trữ lịch sử trò chuyện
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

# Tiêu đề cho chatbot
st.title("ChatBot Data!")

# Tạo hộp thoại để nhập prompt
if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị lịch sử các câu hỏi và câu trả lời trước đó
if st.session_state.messages:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


# Nhập prompt từ người dùng
if prompt := st.chat_input("Hãy nhập yêu cầu?"):
    full_res = ""
    holder = st.empty()

    # Người dùng nhập vào
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )
    with st.chat_message("user"):
        st.markdown(prompt)

    # Sử dụng hàm chat_with_ai để xử lý câu hỏi
    result = chat_with_ai(embedder, vector_search, chat_assistant, prompt, st.session_state.conversation_history)

    if "error" in result:
        full_res = f"Lỗi: {result['error']}"
    else:
        full_res = result['response']

    # Hiển thị câu trả lời của chatbot
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": full_res
        }
    )
    with st.chat_message("assistant"):
        st.markdown(full_res)