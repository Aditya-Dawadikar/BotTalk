from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import os

import dotenv
dotenv.load_dotenv()

# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
client = genai.Client()

def generate_image_prompt_from_description(description: str) -> str:
    return f"""Create a vibrant, eye-catching podcast thumbnail image based on the following episode description:

\"\"\"{description}\"\"\"

The image should be:
- Modern and minimal
- 3D or stylized vector-style preferred
- Use bright, futuristic colors
- Avoid text in the image

Return a creative, detailed visual prompt.
"""

def create_thumbnail_from_description(description: str, output_path="outputs/thumbnail.png"):
    # Step 1: Get image prompt
    image_prompt_response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=generate_image_prompt_from_description(description)
    )
    image_prompt = image_prompt_response.text.strip()

    print(f"🧠 Gemini image prompt:\n{image_prompt}\n")

    # Step 2: Generate image from visual prompt
    response = client.models.generate_content(
        model="gemini-2.0-flash-preview-image-generation",
        contents=image_prompt,
        config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE']
        )
    )

    for part in response.candidates[0].content.parts:
        if part.inline_data:
            image = Image.open(BytesIO(part.inline_data.data))
            image.save(output_path)
            print(f"🖼️ Thumbnail saved to: {output_path}")
            return

    raise RuntimeError("No image returned from Gemini.")
