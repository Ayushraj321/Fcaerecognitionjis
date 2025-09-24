#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Create a real face dataset using webcam or by organizing existing images
"""
import cv2
import os
from pathlib import Path
import zipfile
import time

def capture_faces_webcam():
    """Capture faces using webcam for dataset creation"""
    
    dataset_dir = Path("webcam_dataset")
    dataset_dir.mkdir(exist_ok=True)
    
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERROR] Could not open webcam")
        return None
    
    # Load face detector
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    print("[INFO] Webcam face capture started")
    print("[INSTRUCTIONS]:")
    print("- Press 'n' to start capturing for a new person")
    print("- Press 'c' to capture image for current person")
    print("- Press 'q' to quit")
    
    current_person = None
    person_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Detect faces
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        # Draw rectangles around faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(frame, f"Face detected", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
        
        # Display instructions
        cv2.putText(frame, f"Person: {current_person or 'None'}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, "Press 'n' for new person, 'c' to capture, 'q' to quit", (10, frame.shape[0]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        cv2.imshow('Face Capture', frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('n'):
            # New person
            person_name = input("\\nEnter person name: ").strip().replace(" ", "_")
            if person_name:
                current_person = person_name
                person_dir = dataset_dir / current_person
                person_dir.mkdir(exist_ok=True)
                person_count += 1
                print(f"[INFO] Started capturing for {current_person}")
        
        elif key == ord('c') and current_person:
            # Capture image
            if len(faces) > 0:
                person_dir = dataset_dir / current_person
                existing_images = len(list(person_dir.glob("*.jpg")))
                image_path = person_dir / f"{current_person}_{existing_images + 1}.jpg"
                cv2.imwrite(str(image_path), frame)
                print(f"[SUCCESS] Captured image {existing_images + 1} for {current_person}")
            else:
                print("[WARNING] No face detected, image not saved")
        
        elif key == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    if person_count > 0:
        # Create ZIP file
        zip_path = "webcam_dataset.zip"
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(dataset_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, dataset_dir.parent)
                    zipf.write(file_path, arcname)
        
        print(f"\\n[SUCCESS] Created {zip_path} with {person_count} persons")
        return zip_path
    
    return None

def organize_existing_images():
    """Help organize existing images into dataset structure"""
    
    print("[INFO] Image organization helper")
    print("[INSTRUCTIONS]:")
    print("1. Create a folder named 'my_dataset'")
    print("2. Inside 'my_dataset', create folders for each person")
    print("3. Put face images of each person in their respective folders")
    print("4. Run this function to create a ZIP file")
    
    dataset_dir = Path("my_dataset")
    
    if not dataset_dir.exists():
        dataset_dir.mkdir()
        print(f"[CREATED] {dataset_dir} folder")
        print("[TODO] Add person folders and images, then run this script again")
        return None
    
    # Check for person folders
    person_folders = [d for d in dataset_dir.iterdir() if d.is_dir()]
    
    if not person_folders:
        print("[WARNING] No person folders found in my_dataset/")
        print("[TODO] Create folders named after each person and add their images")
        return None
    
    # Count images
    total_images = 0
    for person_folder in person_folders:
        images = list(person_folder.glob("*.jpg")) + list(person_folder.glob("*.png")) + list(person_folder.glob("*.jpeg"))
        total_images += len(images)
        print(f"[FOUND] {person_folder.name}: {len(images)} images")
    
    if total_images == 0:
        print("[WARNING] No images found in person folders")
        return None
    
    # Create ZIP file
    zip_path = "my_dataset.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(dataset_dir):
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, dataset_dir.parent)
                    zipf.write(file_path, arcname)
    
    print(f"[SUCCESS] Created {zip_path} with {len(person_folders)} persons and {total_images} images")
    return zip_path

def main():
    print("=== Face Dataset Creator ===")
    print("1. Capture faces using webcam")
    print("2. Organize existing images")
    print("3. Exit")
    
    choice = input("Choose option (1-3): ").strip()
    
    if choice == "1":
        zip_file = capture_faces_webcam()
        if zip_file:
            print(f"\\n[READY] Upload '{zip_file}' using the bulk registration feature!")
    
    elif choice == "2":
        zip_file = organize_existing_images()
        if zip_file:
            print(f"\\n[READY] Upload '{zip_file}' using the bulk registration feature!")
    
    elif choice == "3":
        print("[EXIT] Goodbye!")
    
    else:
        print("[ERROR] Invalid choice")

if __name__ == "__main__":
    main()