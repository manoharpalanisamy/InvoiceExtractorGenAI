## Invoice Extractor

from dotenv import load_dotenv
load_dotenv() ## load all environment variables from .env

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

## configuring API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Fucntion to load Gemini Pro vision model and get response
def get_gemini_response(input, image, prompt):
    '''loading gemini model'''
    model=genai.GenerativeModel("gemini-pro-vision")
    response = model.generate_content([input, image[0], prompt])
    return response.text

def input_image_setup(uploaded_file):
    '''Input Image'''
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type, # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

## Initialize our streamlit APP
## Initialize our streamlit APP
st.set_page_config(page_title="Invoice Extractor")

st.header("Gemini Pro Vision: The Future of Invoice Data Extraction")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg","jpeg","png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

input=st.text_input("Input Prompt: ", key="input")
submit = st.button("Tell me about the Invoice")


input_prompt = """
You are an expert in understanding invoices. You will
receive input images as invoices and you will have to 
answer questions based on the input image.
"""

## If submit button is clicked

if submit:
    image_data = input_image_setup(uploaded_file)
    response= get_gemini_response(input_prompt, image_data, input)

    st.subheader("The Response is")
    st.write(response)