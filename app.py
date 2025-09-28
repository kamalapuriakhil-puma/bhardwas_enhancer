import os
from flask import Flask, request, render_template, send_file, url_for
from PIL import Image, ImageEnhance
from werkzeug.utils import secure_filename

# --- Configuration ---
app = Flask(__name__)
# Set a temporary directory for uploaded and processed images
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

# Create the directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# --- Helper Functions ---
def allowed_file(filename):
    """Checks if the file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def enhance_image(filepath):
    """
    Performs the core 'Bhardwas Enhancement'.
    This is a simple boost to contrast and brightness.
    """
    try:
        img = Image.open(filepath)
        
        # 1. Enhance Contrast (e.g., factor of 1.5)
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.5)
        
        # 2. Enhance Brightness (e.g., factor of 1.2)
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.2)
        
        # Generate a unique filename for the enhanced image
        basename = os.path.basename(filepath)
        processed_filename = f"enhanced_{basename}"
        save_path = os.path.join(app.config['PROCESSED_FOLDER'], processed_filename)
        
        # Save the enhanced image
        img.save(save_path)
        
        return processed_filename

    except Exception as e:
        print(f"Error during image processing: {e}")
        return None

# --- Routes ---

@app.route('/')
def index():
    """Serves the main website page."""
    return render_template('index.html')

@app.route('/enhance', methods=['POST'])
def upload_file():
    """Handles the file upload and enhancement process."""
    if 'file' not in request.files:
        return 'No file part', 400
        
    file = request.files['file']
    
    if file.filename == '':
        return 'No selected file', 400
        
    if file and allowed_file(file.filename):
        # Secure the filename to prevent security issues
        filename = secure_filename(file.filename)
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(upload_path)
        
        # Process the image
        processed_filename = enhance_image(upload_path)
        
        if processed_filename:
            # Pass the URL of the processed image back to the frontend
            return {'success': True, 
                    'download_url': url_for('download_file', name=processed_filename)}
        else:
            return {'success': False, 'message': 'Failed to process image.'}, 500
            
    return 'File type not allowed', 400

@app.route('/download/<name>')
def download_file(name):
    """Allows the user to download the processed file."""
    # Ensure the file is being served from the correct, secure folder
    return send_file(os.path.join(app.config['PROCESSED_FOLDER'], name), 
                     as_attachment=True, 
                     download_name=name)

# --- Run the App ---
# 0.0.0.0 is needed for external access (like from your EC2's public IP)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
