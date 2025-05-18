from PIL import Image, ImageFilter, ImageChops, ImageOps
import random
import numpy as np
import matplotlib.pyplot as plt

def sobel_filter(img):
    """Apply Sobel edge detection using custom kernels"""
    img_gray = img.convert('L')
    
    # Sobel kernels
    mask_x = [-1, 0, 1, -2, 0, 2, -1, 0, 1]
    mask_y = [-1, -2, -1, 0, 0, 0, 1, 2, 1]
    
    kernel_sobel_x = ImageFilter.Kernel((3, 3), mask_x, 1)
    kernel_sobel_y = ImageFilter.Kernel((3, 3), mask_y, 1)
    
    # Apply filters
    sobel_x = img_gray.filter(kernel_sobel_x)
    sobel_y = img_gray.filter(kernel_sobel_y)
    
    # Combine results
    return ImageChops.add(sobel_x, sobel_y)

def prewitt_filter(img):
    """Apply Prewitt edge detection using custom kernels"""
    img_gray = img.convert('L')
    
    # Prewitt kernels
    mask_x = [-1, 0, 1, -1, 0, 1, -1, 0, 1]
    mask_y = [-1, -1, -1, 0, 0, 0, 1, 1, 1]
    
    kernel_prewitt_x = ImageFilter.Kernel((3, 3), mask_x, 1)
    kernel_prewitt_y = ImageFilter.Kernel((3, 3), mask_y, 1)
    
    # Apply filters
    prewitt_x = img_gray.filter(kernel_prewitt_x)
    prewitt_y = img_gray.filter(kernel_prewitt_y)
    
    # Combine results
    return ImageChops.add(prewitt_x, prewitt_y)

def laplacian_filter(img):
    """Apply Laplacian edge detection using custom kernels"""
    img_gray = img.convert('L')
    
    # Two variants of Laplacian kernels
    mask_la1 = [0, 1, 0, 1, -4, 1, 0, 1, 0]
    mask_la2 = [1, 1, 1, 1, -8, 1, 1, 1, 1]
    
    # Apply both variants
    laplacian1 = img_gray.filter(ImageFilter.Kernel((3, 3), mask_la1, 1))
    laplacian2 = img_gray.filter(ImageFilter.Kernel((3, 3), mask_la2, 1))
    
    # Return the first variant
    return laplacian1

def blur_filter(img):
    """Apply blur filter using custom kernel"""
    # Create blur kernel (all values 1/9)
    mask = [1] * 9  # Creates [1,1,1,1,1,1,1,1,1]
    mask = [x/9 for x in mask]  # Divide each value by 9
    
    kernel = ImageFilter.Kernel((3, 3), mask, 1)
    return img.filter(kernel)

def sharpen_filter(img):
    """Apply sharpen filter using custom kernel"""
    mask = [0, -1, 0, -1, 5, -1, 0, -1, 0]
    kernel = ImageFilter.Kernel((3, 3), mask, 1)
    return img.filter(kernel)

def negative_filter(img):
    """Apply negative filter"""
    if img.mode == 'RGB':
        img_array = np.array(img)
        return Image.fromarray(255 - img_array)
    return ImageOps.invert(img)

def aplicar_ruido(img, prob=0.05):
    """Apply salt and pepper noise"""
    output = np.array(img)
    for i in range(output.shape[0]):
        for j in range(output.shape[1]):
            rnd = random.random()
            if rnd < prob:
                output[i][j] = 0  # black
            elif rnd > 1 - prob:
                output[i][j] = 255  # white
    return Image.fromarray(output)

def equalizar_histograma(img):
    """Apply histogram equalization"""
    img_array = np.array(img.convert('L'))
    histogram, bins = np.histogram(img_array.flatten(), bins=256, range=[0, 256])
    cdf = histogram.cumsum()
    cdf_normalized = cdf * (255 / cdf[-1])
    img_equalized = np.interp(img_array.flatten(), bins[:-1], cdf_normalized)
    return Image.fromarray(img_equalized.reshape(img_array.shape).astype('uint8'))

def generate_histogram(img):
    """Generate histogram data for the image"""
    img_array = np.array(img.convert('L'))
    hist, bins = np.histogram(img_array.flatten(), bins=256, range=[0, 256])
    return hist.tolist(), bins.tolist()

def ensure_rgb(func):
    """Decorator to ensure filter output is in RGB mode"""
    def wrapper(img, *args, **kwargs):
        result = func(img, *args, **kwargs)
        if result.mode != 'RGB':
            result = result.convert('RGB')
        return result
    return wrapper

# Apply decorator to filter functions
negative_filter = ensure_rgb(negative_filter)
sobel_filter = ensure_rgb(sobel_filter)
prewitt_filter = ensure_rgb(prewitt_filter)
laplacian_filter = ensure_rgb(laplacian_filter)
blur_filter = ensure_rgb(blur_filter)
sharpen_filter = ensure_rgb(sharpen_filter)
