import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_prompt, image):
    model=genai.GenerativeModel('gemini-pro-vision')
    responce=model.generate_content([input_prompt, image[0]])
    return responce.text

def input_image(uploaded_file):
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    

st.set_page_config(page_title="AI Nutritionist")
# st.header("AI Nutritionist")
st.markdown(
        """<h1><span style="color:green">AI Nutritionist</span> </h1>
            <h5><span style="color:white">Don't worry I'll count calories for you..</span></h5>
        """,
        unsafe_allow_html=True,
    )
# st.subheader("Don't worry I'll count calories for you..")

input_prompt="""
You are an expert in nutritionist where you need to see the food items from the image
               and calculate the total calories, also provide the details of every food items with calories intake
               is below format

               1. Item 1 - no of calories
               2. Item 2 - no of calories

               In the end you need to mention is this a healthy meal or not. 
               Make the healthy meal/ not healty meal as BOLD and CAPITAL text.
               
               If the food is not healty also tell some good alternatives.
               ----
               ----


"""

uploaded_file = st.file_uploader("Choose your food image..", type=["jpe", "jpeg", "png"])
image=""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="🥗", use_column_width=True)

submit = st.button("tell me about my food..")

if submit:
    image_data = input_image(uploaded_file)
    response = get_gemini_response(input_prompt, image_data)
    st.subheader("according to our AI Nutritionist your food has..")
    st.write(response)