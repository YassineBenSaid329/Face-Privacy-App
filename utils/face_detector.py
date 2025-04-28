# utils/face_detector.py
import cv2 # type: ignore
import numpy as np # type: ignore
import os

def detect_and_blur_faces(input_path, output_path):
    """
    Detect faces in an image and apply Gaussian blur for privacy protection.
    
    Args:
        input_path (str): Path to the input image file
        output_path (str): Path where to save the processed image
        
    Returns:
        int: Number of faces detected and blurred
    """
    # Load the image
    image = cv2.imread(input_path)
    
    if image is None:
        raise ValueError(f"Could not load image from {input_path}")
    
    # Convert to grayscale for face detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Load the face detector
    face_cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    
    if not os.path.exists(face_cascade_path):
        raise FileNotFoundError(f"Face cascade file not found at {face_cascade_path}")
    
    face_cascade = cv2.CascadeClassifier(face_cascade_path)
    
    # Detect faces
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    
    # For each detected face, blur it and replace it in the original image
    for (x, y, w, h) in faces:
        # Extract the face region
        face_roi = image[y:y+h, x:x+w]
        
        # Apply Gaussian blur
        # The kernel size must be positive and odd
        # Larger kernel size and sigma values result in more blurring
        blurred_face = cv2.GaussianBlur(face_roi, (99, 99), 30)
        
        # Replace the face region with the blurred face
        image[y:y+h, x:x+w] = blurred_face
        
        # Optionally, draw a rectangle around the face
        # cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    # Save the result
    cv2.imwrite(output_path, image)
    
    return len(faces)  # Return the number of faces detected
