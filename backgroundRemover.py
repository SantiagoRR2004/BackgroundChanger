from PIL import Image
import numpy as np

image = Image.open("input.png")

# Convert the image to RGBA
image = image.convert("RGBA")
data = np.array(image)

# Extract red, green, blue, and alpha channels
red, green, blue, alpha = data[:, :, 0], data[:, :, 1], data[:, :, 2], data[:, :, 3]

# Calculate the minimum of red, green, and blue for each pixel
avg = np.minimum.reduce([red, green, blue])

# If avg >= 128, set avg to 255
avg = np.where(avg >= 128, 255, avg)

# Update the alpha channel based on the calculated avg
data[:, :, 3] = np.minimum(alpha, 255 - avg)

transparentImage = Image.fromarray(data)
transparentImage.save("output.png")
