from openai import OpenAI
import base64
from PIL import Image
from io import BytesIO


# --- Cấu hình ---
AI_API_BASE = "https://api.thucchien.ai/v1"
AI_API_KEY = "sk-ZUykbXHn_5WbchWWYfjn9Q" # Thay bằng API key của bạn
IMAGE_SAVE_PATH = "res5.png"


# --- Khởi tạo client ---
client = OpenAI(
  api_key=AI_API_KEY,
  base_url=AI_API_BASE,
)


# --- Đọc và encode ảnh thành base64 ---
image_path = "bia.png"
image = Image.open(image_path)


# Chuyển đổi ảnh sang base64
buffered = BytesIO()
image.save(buffered, format="PNG")
img_bytes = buffered.getvalue()
img_base64 = base64.b64encode(img_bytes).decode('utf-8')
img_data_url = f"data:image/png;base64,{img_base64}"


# --- Bước 1: Gọi API để tạo hình ảnh ---
try:
  response = client.chat.completions.create(
      model="gemini-2.5-flash-image-preview",
      messages=[
          {
              "role": "user",
              "content": [
                  {
                      "type": "text",
                      "text":
                          """
A detailed design for the back panel of a tri-fold A4 public awareness flyer, presented as a single tall, vertical image. The purpose of this panel is to provide crucial contact information and a message of hope. The overall artistic style is heavily inspired by classic Vietnamese propaganda and public information posters (tranh cổ động), featuring bold lines, strong symbolic imagery, and a limited but impactful color palette (e.g., revolutionary red, sunburst yellow, deep blue, off-white). Crucially, this design must maintain the exact same artistic style as a previously established cover image for visual consistency.

Crucial Instruction: The entire image must contain NO text, letters, or numbers. All areas intended for text are to be rendered as clear, blank placeholders (such as empty white rectangles, banners, or negative space integrated into the design).

Back Panel Design (Top to Bottom Layout):

Header & Main Message:

The top third of the panel is dominated by a powerful and supportive central image: two hands firmly clasping each other in a gesture of help and solidarity. One hand is reaching down to pull the other one up, symbolizing rescue and support.
Immediately below this image, there is a prominent, blank, ribbon-style banner stretching across the width of the panel. This is the placeholder for the main title: "BẠN KHÔNG CÔ ĐƠN! HÃY TÌM KIẾM SỰ GIÚP ĐỠ!".
Contact Information Section:

This middle section is cleanly organized into three distinct rows, each containing a symbolic icon on the left and a blank rectangular placeholder for contact information on the right.
Row 1 (National Addiction Hotline): A stylized icon of a classic telephone handset with a plus sign (+) or a heart symbol superimposed on it. Next to it is a clean, blank rectangular placeholder for the phone number.
Row 2 (Mental Health Center): A symbolic icon of a human head in profile, with a simple, growing plant or a shining lightbulb inside, representing healing and mental clarity. Next to it is a slightly larger blank rectangular placeholder for a phone number and website address.
Row 3 (Drug Crime Prevention Hotline): A strong icon of a shield with a stylized telephone symbol inside, representing protection and official help. Next to it is a clean, blank rectangular placeholder for the phone number.
Final Hopeful Image & Message:

The bottom third of the panel features an inspiring and optimistic scene. A silhouette of a single strong figure (or a small family) stands on a hilltop, looking towards a large, radiant rising sun in the background. At the figure's feet are broken chains or shackles, symbolizing breaking free from addiction. The overall feeling is one of a new dawn and a bright future.
At the very bottom, integrated into the design, is a final, simple, blank rectangular placeholder for the closing message: "Một cuộc sống khỏe mạnh và hạnh phúc hoàn toàn nằm trong tầm tay bạn."
Overall Composition Keywords: flyer back panel, Vietnamese propaganda art, public health campaign, social awareness, anti-drug poster, hope, support, contact information, symbolic icons, helping hand, rising sun, breaking free, no text, text placeholders, retro illustration, strong message, bold graphic design.

--ar 10:21
                          """
                  },
                  {
                      "type": "image_url",
                      "image_url": {
                          "url": img_data_url
                      }
                  }
              ]
          }
      ],
      modalities=["image"]  # Chỉ định trả về dữ liệu ảnh
  )


  # Trích xuất dữ liệu ảnh base64
  base64_string = response.choices[0].message.images[0].get('image_url').get("url")
  print("Image data received successfully.")


  # --- Bước 2: Giải mã và lưu hình ảnh ---
  if ',' in base64_string:
      header, encoded = base64_string.split(',', 1)
  else:
      encoded = base64_string


  image_data = base64.b64decode(encoded)


  with open(IMAGE_SAVE_PATH, 'wb') as f:
      f.write(image_data)
     
  print(f"Image saved to {IMAGE_SAVE_PATH}")


except Exception as e:
  print(f"An error occurred: {e}")
