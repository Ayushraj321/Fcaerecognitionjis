#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Create a test dataset with generated face images for bulk registration testing
"""
import os
import cv2
import numpy as np
from pathlib import Path
import zipfile

def create_synthetic_face(width=200, height=200, person_id=0):
    """Create a synthetic face image with unique features"""
    # Create base face shape
    img = np.ones((height, width, 3), dtype=np.uint8) * 220
    
    # Face outline (oval)
    center = (width//2, height//2)
    axes = (width//3, height//2 - 20)
    cv2.ellipse(img, center, axes, 0, 0, 360, (200, 180, 160), -1)
    
    # Eyes
    eye_y = height//2 - 30
    left_eye = (width//2 - 40, eye_y)
    right_eye = (width//2 + 40, eye_y)
    
    # Eye variations based on person_id
    eye_color = [(50, 50, 50), (100, 50, 30), (30, 100, 50)][person_id % 3]
    cv2.circle(img, left_eye, 15, eye_color, -1)
    cv2.circle(img, right_eye, 15, eye_color, -1)
    
    # Pupils
    cv2.circle(img, left_eye, 8, (0, 0, 0), -1)
    cv2.circle(img, right_eye, 8, (0, 0, 0), -1)
    
    # Nose
    nose_pts = np.array([
        [width//2, height//2 - 10],
        [width//2 - 8, height//2 + 10],
        [width//2 + 8, height//2 + 10]
    ], np.int32)
    cv2.fillPoly(img, [nose_pts], (180, 150, 130))
    
    # Mouth
    mouth_center = (width//2, height//2 + 40)
    mouth_width = 30 + (person_id % 3) * 10
    cv2.ellipse(img, mouth_center, (mouth_width, 8), 0, 0, 180, (150, 100, 100), -1)
    
    # Hair (different styles based on person_id)
    hair_color = [(80, 60, 40), (40, 30, 20), (120, 100, 80)][person_id % 3]
    if person_id % 4 == 0:  # Short hair
        cv2.ellipse(img, (width//2, height//2 - 60), (width//3, 40), 0, 180, 360, hair_color, -1)
    elif person_id % 4 == 1:  # Long hair
        cv2.ellipse(img, (width//2, height//2 - 40), (width//3 + 20, 80), 0, 180, 360, hair_color, -1)
    
    # Add some noise for realism
    noise = np.random.randint(-20, 20, img.shape, dtype=np.int16)
    img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    
    return img

def create_test_dataset():
    """Create a complete test dataset with multiple persons and images"""
    
    dataset_dir = Path("test_dataset")
    dataset_dir.mkdir(exist_ok=True)
    
    # Person names for the dataset
    persons = [
        "john_doe", "jane_smith", "bob_johnson", "alice_brown", "charlie_wilson",
        "diana_prince", "peter_parker", "mary_jane", "bruce_wayne", "clark_kent"
    ]
    
    print("[INFO] Creating test dataset with synthetic faces...")
    
    for i, person in enumerate(persons):
        person_dir = dataset_dir / person
        person_dir.mkdir(exist_ok=True)
        
        # Create 3-5 images per person with variations
        num_images = np.random.randint(3, 6)
        
        for j in range(num_images):
            # Create face with slight variations
            face_img = create_synthetic_face(person_id=i)
            
            # Add variations for each image
            if j > 0:
                # Slight rotation
                angle = np.random.randint(-15, 15)
                center = (face_img.shape[1]//2, face_img.shape[0]//2)
                rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
                face_img = cv2.warpAffine(face_img, rotation_matrix, (face_img.shape[1], face_img.shape[0]))
                
                # Brightness variation
                brightness = np.random.randint(-30, 30)
                face_img = np.clip(face_img.astype(np.int16) + brightness, 0, 255).astype(np.uint8)
            
            # Save image
            image_path = person_dir / f"{person}_{j+1}.jpg"
            cv2.imwrite(str(image_path), face_img)
        
        print(f"[SUCCESS] Created {num_images} images for {person}")
    
    # Create ZIP file
    zip_path = "C:\Users\KIIT\AppData\Local\Temp\53907c5f-cbd6-4d69-9866-20df4ddd3470_lfw-funneled.tgz.zip.470\lfw-funneled.tgz\lfw_funneled"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(dataset_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, dataset_dir.parent)
                zipf.write(file_path, arcname)
    
    print(f"[SUCCESS] Created {zip_path} with {len(persons)} persons")
    print(f"[INFO] Total images: {sum([len(list(p.glob('*.jpg'))) for p in dataset_dir.iterdir() if p.is_dir()])}")
    
    return zip_path

if __name__ == "__main__":
    zip_file = create_test_dataset()
    print(f"\n[READY] Upload '{zip_file}' using the bulk registration feature!")
    print("[NOTE] These are synthetic faces for testing purposes.")