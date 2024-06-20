import os
import streamlit as st
from dotenv import load_dotenv
import io
from io import BytesIO
from PIL import Image
from openai import OpenAI
import base64

def encode_image(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

def generate_gpt_response(image):
    try:
        load_dotenv()
        base64_image = encode_image(image)
        openai_api = os.getenv('OPENAI_API')
        openai_client = OpenAI(api_key=openai_api)
        MODEL = 'gpt-4o'

        response = openai_client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": '''You are a professional in pharmaceuticals, with expertise in drug names, dosages, and administration schedules. I will provide an image of a drug, and you will confirm its intended use, optimal administration time and conditions, and precautions regarding sensitivities. Additionally, provide information on potential side effects and necessary cautions.

When considering taking a drug, consider:

1. Medical History: Pre-existing conditions and past reactions.
2. Allergies: Known drug allergies.
3. Current Medications: Avoid harmful interactions.
4. Pregnancy/Breastfeeding: Effects on the baby.
5. Age: Pediatric or geriatric considerations.
6. Dosage: Correct amount based on individual factors.
7. Administration: Proper technique and route.
8. Timing: Optimal times and frequency.
9. Dietary Restrictions: Foods and supplements to avoid.
10. Lifestyle Factors: Impact of alcohol and tobacco.
11. Storage: Proper storage conditions.
12. Monitoring: Follow-up tests or monitoring.
13. Side Effects: Common and serious side effects.
14. Missed Dose: Instructions for missed doses.
15. Emergency: Signs of overdose or severe reactions.'''},
                {"role": "user", "content": [
                    {"type": "text", "text": '''If this image in pharmaceuticals, please analyze it. Additionally, offer recommendations based on your analysis, Answer ONLY in Arabic.
                else (The given Text not related to any pharmaceuticals) then reponse "لا يمكنني المساعدة بذلك'''},
                    {"type": "image_url", "image_url": {
                        "url": f"data:image/png;base64,{base64_image}"}
                    }
                ]}
            ],
    temperature=0.0,
)
        return response.choices[0].message.content
    except Exception as e:
        st.error("Failed to generate GPT response: {}".format(e))
        return None

def main():
    st.title("prescription")
    st.markdown("##### Verify Before You Take: Quick AI Drug Check")
    
    img_file_buffer = st.file_uploader("Upload an image (jpg, png, jpeg):", type=["jpg", "png", "jpeg"])
    img = None
    if img_file_buffer is not None:
        img = Image.open(io.BytesIO(img_file_buffer.getvalue()))

    if st.button("Analysis"):
        if img:
            res = generate_gpt_response(img)
            st.markdown("### Result")
            st.markdown(f"<div style='direction: rtl; text-align: right;'> {res}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
