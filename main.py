from dotenv import load_dotenv
import os
import streamlit as st
from PIL import Image
import google.generativeai as genai

genai.configure(api_key="AIzaSyBXRuSZwfdgMshapAtekdNmbVUn8OWpNzU")


model = genai.GenerativeModel(model_name="gemini-1.5-pro")

def get_gemini_response(input, image, prompt):
    res = model.generate_content([input, image[0], prompt])
    return res.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


st.set_page_config(page_title="Multi-Language Invoice Extractor", page_icon="🔮")

st.header("Multi-Language Invoice Extractor")
input = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

image = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

submit = st.button("Extract Info From Invoice")

input_prompt = """
You are an expert in extracting information from invoices. 
You will be given an invoice as an image and a prompt.
You will extract the required information from the invoice based on the prompt.
"""

if submit:
    image_data = input_image_details(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)
    st.subheader("Response:")
    st.write(response)



