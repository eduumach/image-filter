# Image Processing Web Application

A web application for applying various image processing filters using Python, Flask, and PIL.

Repository: https://github.com/eduumach/image-filter

## Features

- Upload and process images (JPG, PNG)
- Multiple filter options:
  - Negative
  - Median
  - Gaussian Blur
  - Custom Edge Detection
  - Sobel Edge Detection
  - Prewitt Edge Detection
  - Threshold
- Real-time histogram visualization
- Download processed images
- Responsive design

## Requirements

- Python 3.7+
- Flask
- Pillow (PIL)
- NumPy
- Matplotlib

## Installation

1. Clone the repository:
```bash
git clone git@github.com:eduumach/image-filter.git
cd image-filter
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. Use the application:
   - Upload an image using the file input
   - Select a filter from the dropdown menu
   - Click "Process Image" to apply the filter
   - View the original and processed images side by side
   - Compare the histograms of both images
   - Download the processed image using the download button

## Project Structure

```
image-filter/
├── app.py              # Main Flask application
├── filters.py          # Image processing functions
├── requirements.txt    # Project dependencies
├── templates/
│   └── index.html     # HTML template
└── static/
    ├── css/
    │   └── style.css  # Custom styles
    ├── uploads/       # Uploaded images
    └── processed/     # Processed images
```

## Contributing

Feel free to submit issues and enhancement requests.

