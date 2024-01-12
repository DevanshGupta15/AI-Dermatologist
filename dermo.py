from dotenv import load_dotenv
load_dotenv()  
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_response(input,image,prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,image[0],prompt])
    return response.text


def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
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
    
# Setting page config
st.set_page_config(page_title="Your Personal AI Dermatologist", page_icon="🌿")

# Setting header
st.title("👩‍⚕️ Your Personal AI Dermatologist")
st.subheader("Upload an image and get detailed dermatological insights")


input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit=st.button("HELP ME AI DOCTORR")

input_prompt="""
You are an expert AI dermatologist tasked with analyzing images of skin, nails, or hair to provide detailed insights into potential issues, their causes, and recommendations for management. Your goal is to identify and explain dermatological conditions in a user-friendly manner. The app should generate a report in the following format:
Condition - Description of the issue, including why it occurs.

Helpful advice - Advice on what can be done to reverse the disease.

Helpful medicine - Medicine that can help to resolve the issue.

Rarity - How rare the disease is - common, very often, rare, danger."
"""

## If submit button is clicked

if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_response(input_prompt,image_data,input)
    st.subheader("The Response is")
    st.write(response)

