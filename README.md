# Face Privacy Protection Application

## Project Overview
A web application that automatically detects faces in images and applies a Gaussian blur filter to anonymize them, protecting the privacy of individuals in the photos.

## Features
- Upload images containing faces
- Automatic face detection using Haar Cascade classifiers
- Apply Gaussian blur filter to detected faces
- Preview anonymized images with blurred faces
- Download the processed images

## Technical Details

### Core Functionality
1. **Face Detection**: Uses OpenCV's Haar Cascade classifier to identify frontal faces in images
2. **Face Extraction**: Crops detected faces based on coordinates returned by the classifier
3. **Anonymization**: Applies a Gaussian blur filter to each detected face
4. **Image Reconstruction**: Merges the blurred faces back into the original image

### Limitations
- Only detects frontal-facing faces (not profile views)
- Detection accuracy may vary based on image quality, lighting, and face orientation

### Technologies Used
- Python for backend processing
- OpenCV for image processing and face detection
- Web framework for the application interface
- HTML/CSS/JavaScript for frontend

## How to Use
1. Launch the application
2. Upload an image containing faces
3. The application automatically detects and blurs faces
4. Preview the anonymized image
5. Download the processed image if desired

## Implementation Notes
The implementation follows techniques from the "Image Processing in Python" DataCamp course, specifically Chapter 4 on "Detecting Faces and Features," focusing on privacy protection through face anonymization.
