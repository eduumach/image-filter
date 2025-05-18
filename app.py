import os
from flask import Flask, render_template, request, url_for, send_file, jsonify
from PIL import Image
import filters
import base64
from io import BytesIO

app = Flask(__name__, static_url_path='/static', static_folder='static')
UPLOAD_FOLDER = 'static/uploads'
PROCESSED_FOLDER = 'static/processed'

# Ensure directories exist and are absolute paths
UPLOAD_FOLDER = os.path.abspath(UPLOAD_FOLDER)
PROCESSED_FOLDER = os.path.abspath(PROCESSED_FOLDER)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            try:
                # Save original image with safe filename
                filename = file.filename
                original_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(original_path)
                
                try:
                    # Open image and apply selected filter
                    img = Image.open(original_path)
                    img = img.convert('RGB')  # Ensure RGB mode
                except Exception as e:
                    return jsonify({'error': 'Failed to open image. Please ensure it is a valid image file.'}), 400
                
                filter_type = request.form.get('filter', 'negative')
                
                # Apply selected filter
                filters_map = {
                    'negative': filters.negative_filter,
                    'median': filters.median_filter,
                    'gaussian': filters.gaussian_filter,
                    'custom': filters.custom_filter,
                    'sobel': filters.sobel_filter,
                    'prewitt': filters.prewitt_filter,
                    'threshold': filters.threshold_filter
                }
                
                if filter_type not in filters_map:
                    return jsonify({'error': f'Unknown filter type: {filter_type}'}), 400
                
                try:
                    processed_img = filters_map[filter_type](img)
                except Exception as e:
                    return jsonify({'error': f'Error applying {filter_type} filter: {str(e)}'}), 500
                
                try:
                    # Save processed image
                    processed_filename = f'processed_{filename}'
                    processed_path = os.path.join(PROCESSED_FOLDER, processed_filename)
                    processed_img.save(processed_path, format='PNG')
                except Exception as e:
                    return jsonify({'error': 'Failed to save processed image'}), 500
                
                try:
                    # Generate histogram data
                    original_hist, bins = filters.generate_histogram(img)
                    processed_hist, _ = filters.generate_histogram(processed_img)
                except Exception as e:
                    return jsonify({'error': 'Failed to generate histograms'}), 500
                
                # Return JSON response with image paths and histogram data
                # Construct absolute URLs for images
                original_url = url_for('static', filename=f'uploads/{filename}', _external=True)
                processed_url = url_for('static', filename=f'processed/{processed_filename}', _external=True)
                
                return jsonify({
                    'original_image': original_url,
                    'processed_image': processed_url,
                    'original_histogram': original_hist,
                    'processed_histogram': processed_hist,
                    'bins': bins
                })
            except Exception as e:
                print(f"Unhandled error: {str(e)}")
                return jsonify({'error': 'An unexpected error occurred'}), 500
            
    return render_template('index.html')

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_file(os.path.join(PROCESSED_FOLDER, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
