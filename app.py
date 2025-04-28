from flask import Flask, render_template, request, redirect, url_for, flash # type: ignore
import os
import cv2 # type: ignore
import numpy as np # type: ignore
from werkzeug.utils import secure_filename # type: ignore
from utils.face_detector import detect_and_blur_faces

app = Flask(__name__)
app.secret_key = "face_privacy_app_secret_key"  # Change this in production
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        print(f"Saved file to: {filepath}")  # Debug print
        
        # Process the image
        output_filename = 'blurred_' + filename
        output_filepath = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        
        try:
            print(f"Processing image: {filepath} -> {output_filepath}")  # Debug print
            num_faces = detect_and_blur_faces(filepath, output_filepath)
            print(f"Detected {num_faces} faces")  # Debug print
            
            if num_faces > 0:
                flash(f'Successfully detected and blurred {num_faces} face(s)')
            else:
                flash('No faces detected in the image')
            
            # Make sure both paths exist
            if not os.path.exists(filepath):
                flash(f"Original file not found: {filepath}")
                return redirect(url_for('index'))
                
            if not os.path.exists(output_filepath):
                flash(f"Processed file not found: {output_filepath}")
                return redirect(url_for('index'))
            
            print(f"Rendering result with original={filepath}, processed={output_filepath}")  # Debug print
            return render_template('result.html', 
                                  original_image=filepath, 
                                  processed_image=output_filepath)
        except Exception as e:
            import traceback
            print(f"Error: {str(e)}")
            print(traceback.format_exc())  # Print detailed error
            flash(f'Error processing image: {str(e)}')
            return redirect(url_for('index'))
    
    flash('Invalid file type. Please upload a JPG, JPEG, or PNG file.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)