import time, pdb, base64, requests, os
import streamlit as st

api_key = os.getenv('API_KEY')
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

st.title('나이 Bar 드립니다.')

uploaded_file = st.file_uploader("Choose a image file", accept_multiple_files=False)

if st.button('나이 추정하기'):
    time_log = time.time()
    st.write("filename:", uploaded_file.name)
    st.image(uploaded_file)
    base64_image = base64.b64encode(uploaded_file.read()).decode('utf-8')
    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "이 사람의 연령대를 대략적으로 추측해줘"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens" : 200
    }
    with st.spinner('나이 추측 중 ...'):
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        st.write(response.json()['choices'][0]["message"]["content"])
        st.write('추측까지 걸린 시간 : ', time.time() - time_log)
