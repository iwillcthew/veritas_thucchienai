from openai import OpenAI

# --- Cấu hình ---
# Thay <your_api_key> bằng API key của bạn
client = OpenAI(
  api_key="sk-ZUykbXHn_5WbchWWYfjn9Q",
  base_url="https://api.thucchien.ai"
)

# --- Thực thi ---
response = client.chat.completions.create(
  model="gemini-2.5-pro", # Chọn model bạn muốn
  messages=[
      {
          "role": "user",
          "content": "Viết promt tiếng "
      }
  ]
)

print(response.choices[0].message.content)
