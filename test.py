from utils import process_profile_image
from PIL import Image

image_path = "me.jpg"
result = process_profile_image(image_path)
img = Image.open(result)

new_image = Image.new("RGB", img.size, "white")

# Paste the original image onto the new image, using the alpha channel (if present)
new_image.paste(img, (0, 0), img)

# Save the result
new_image.save("new.png")

new_image.show()
