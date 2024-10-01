import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import fft2, ifft2, fftshift, ifftshift
from skimage import data, img_as_float
from skimage.color import rgb2gray

# Load an image
image = img_as_float(data.astronaut())  # Load an example image (astronaut)
gray_image = rgb2gray(image)  # Convert to grayscale

# Apply the 2D Fourier Transform
f_transform = fft2(gray_image)
f_transform_shifted = fftshift(f_transform)  # Shift the zero frequency component to the center

# Magnitude and phase spectrum
magnitude_spectrum = np.log(1 + np.abs(f_transform_shifted))
phase_spectrum = np.angle(f_transform_shifted)

# Visualize the original image, magnitude spectrum, and phase spectrum
plt.figure(figsize=(12, 8))

plt.subplot(131)
plt.imshow(gray_image, cmap='gray')
plt.title('Original Image')
plt.axis('off')

plt.subplot(132)
plt.imshow(magnitude_spectrum, cmap='gray')
plt.title('Magnitude Spectrum')
plt.axis('off')

plt.subplot(133)
plt.imshow(phase_spectrum, cmap='gray')
plt.title('Phase Spectrum')
plt.axis('off')

plt.show()

# Inverse Fourier Transform to reconstruct the image
f_ishift = ifftshift(f_transform_shifted)
reconstructed_image = ifft2(f_ishift)
reconstructed_image = np.abs(reconstructed_image)

# Display the reconstructed image
plt.figure(figsize=(6, 6))
plt.imshow(reconstructed_image, cmap='gray')
plt.title('Reconstructed Image')
plt.axis('off')
plt.show()

