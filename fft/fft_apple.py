import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from numpy.fft import fft2, ifft2, fftshift, ifftshift

# Load image and convert to grayscale
image = Image.open('apple.png').convert('L')  # Replace 'your_image.png' with the path to your image
image_array = np.array(image)

# Perform the 2D Fourier Transform
fourier_transform = fftshift(fft2(image_array))

# Magnitude Spectrum
magnitude_spectrum = np.log(np.abs(fourier_transform) + 1)

# Inverse Fourier Transform to reconstruct the image
inverse_transform = ifft2(ifftshift(fourier_transform))
reconstructed_image = np.abs(inverse_transform)

# Plot the original image, magnitude spectrum, and reconstructed image
plt.figure(figsize=(18, 6))

# Original Image
plt.subplot(1, 3, 1)
plt.imshow(image_array, cmap='gray')
plt.title('Original Image')
plt.axis('off')

# Fourier Magnitude Spectrum
plt.subplot(1, 3, 2)
plt.imshow(magnitude_spectrum, cmap='gray')
plt.title('Fourier Magnitude Spectrum')
plt.axis('off')

# Reconstructed Image
plt.subplot(1, 3, 3)
plt.imshow(reconstructed_image, cmap='gray')
plt.title('Reconstructed Image')
plt.axis('off')

plt.show()
