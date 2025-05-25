from PIL import Image, ImageFilter, ImageChops, ImageOps
import numpy as np

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

def negative_filter(img):
    """Apply negative filter"""
    if img.mode == 'RGB':
        img_array = np.array(img)
        return Image.fromarray(255 - img_array)
    return ImageOps.invert(img)

def generate_histogram(img):
    """Generate histogram data for the image"""
    img_array = np.array(img.convert('L'))
    hist, bins = np.histogram(img_array.flatten(), bins=256, range=[0, 256])
    return hist.tolist(), bins.tolist()

def gaussian_filter(img):
    """Apply Gaussian blur filter"""
    return img.filter(ImageFilter.GaussianBlur(radius=2))

def threshold_filter(img):
    """Apply threshold filter"""
    return img.convert('L').point(lambda x: 0 if x < 128 else 255, '1').convert('RGB')

def custom_filter(img):
    """Apply custom smoothing filter"""
    mask = [1/16, 2/16, 1/16,
            2/16, 4/16, 2/16,
            1/16, 2/16, 1/16]
    kernel = ImageFilter.Kernel((3, 3), mask, 1)
    return img.filter(kernel)

def median_filter(img):
    """Apply median filter for noise reduction"""
    return img.filter(ImageFilter.MedianFilter(size=3))

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
median_filter = ensure_rgb(median_filter)
gaussian_filter = ensure_rgb(gaussian_filter)
custom_filter = ensure_rgb(custom_filter)
sobel_filter = ensure_rgb(sobel_filter)
prewitt_filter = ensure_rgb(prewitt_filter)
threshold_filter = ensure_rgb(threshold_filter)
