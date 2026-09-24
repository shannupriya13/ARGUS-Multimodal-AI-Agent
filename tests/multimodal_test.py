from ai.gemini_multimodal import analyze_image


image_path = "tests/test_image.jpg"

prompt = """
Analyze this image carefully.

Describe:
1. What is visible
2. Important objects or elements
3. Any useful information that can be understood from the image

Give a clear and concise response.
"""

result = analyze_image(image_path, prompt)

print("\n===== ARGUS IMAGE ANALYSIS =====\n")
print(result)