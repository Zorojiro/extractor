from dotenv import load_dotenv
import os
import streamlit as st
from PIL import Image
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Set API key from environment variable
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the model
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

# Set up Streamlit page configuration
st.set_page_config(page_title="Multi-Language Invoice Extractor", page_icon="🔮", layout="wide")

# Create columns for the layout with equal widths
col1, col2 = st.columns(2)  # Equal width columns

# Column 1: Chat Interface
with col1:
    st.header("Multi-Language Invoice Extractor")
    
    input_prompt = """
    You are an expert in extracting information from invoices. 
    You will be given an invoice as an image and a prompt.
    You will extract the required information from the invoice based on the prompt.
    """
    
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    
    input = st.text_input("Input Prompt: ", key="input", placeholder="Enter your prompt here")

    submit = st.button("Extract Info From Invoice")

    if submit:
        if uploaded_file is not None:
            image_data = input_image_details(uploaded_file)
            response = get_gemini_response(input_prompt, image_data, input)
            st.subheader("Response:")
            st.write(response)
        else:
            st.error("Please upload an image.")

# Column 2: Uploaded Image Display
with col2:
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
    else:
        st.text("No image uploaded yet.")
