#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Process LFW dataset directly from the given path
"""
import os
import sys
import django
import tarfile
import json
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'imagerecognition.settings')
django.setup()

from recognition.models import KnownFace
from recognition.face_recognition_dl import DeepFaceRecognition
from django.core.files.base import ContentFile

def process_lfw_dataset():
    """Process LFW dataset from the specific path"""
    
    # Your LFW dataset path
    lfw_path = r"C:\Users\KIIT\AppData\Local\Temp\53907c5f-cbd6-4d69-9866-20df4ddd3470_lfw-funneled.tgz.zip.470\lfw-funneled.tgz"
    
    if not os.path.exists(lfw_path):
        print(f"[ERROR] File not found: {lfw_path}")
        return
    
    print(f"[INFO] Processing LFW dataset from: {lfw_path}")
    
    # Create temp extraction directory
    temp_dir = "temp_lfw_extraction"
    os.makedirs(temp_dir, exist_ok=True)
    
    try:
        # Extract TGZ file
        print("[INFO] Extracting TGZ file...")
        with tarfile.open(lfw_path, 'r:gz') as tar:
            tar.extractall(temp_dir)
        
        # Initialize face recognizer
        face_recognizer = DeepFaceRecognition()
        
        # Find the extracted directory (usually lfw-funneled or similar)
        extracted_dirs = [d for d in os.listdir(temp_dir) if os.path.isdir(os.path.join(temp_dir, d))]
        if not extracted_dirs:
            print("[ERROR] No directories found in extracted archive")
            return
        
        lfw_dir = os.path.join(temp_dir, extracted_dirs[0])
        print(f"[INFO] Found LFW directory: {lfw_dir}")
        
        # Process each person directory
        processed = 0
        errors = 0
        skipped = 0
        
        person_dirs = [d for d in os.listdir(lfw_dir) if os.path.isdir(os.path.join(lfw_dir, d))]
        total_persons = len(person_dirs)
        
        print(f"[INFO] Found {total_persons} persons in dataset")
        
        for i, person_name in enumerate(person_dirs):
            try:
                # Progress indicator
                if i % 100 == 0:
                    print(f"[PROGRESS] Processing {i}/{total_persons} persons...")
                
                # Skip if already registered
                if KnownFace.objects.filter(name=person_name).exists():
                    skipped += 1
                    continue
                
                person_dir = os.path.join(lfw_dir, person_name)
                
                # Get first image file
                image_files = [f for f in os.listdir(person_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
                if not image_files:
                    continue
                
                image_path = os.path.join(person_dir, image_files[0])
                
                # Detect faces
                face_regions = face_recognizer.detect_faces(image_path)
                
                if face_regions:
                    # Extract embedding
                    embedding = face_recognizer.extract_embedding(face_regions[0])
                    
                    if embedding is not None:
                        # Create KnownFace record
                        known_face = KnownFace(name=person_name)
                        
                        # Save image
                        with open(image_path, 'rb') as f:
                            known_face.image.save(
                                f'{person_name}_{image_files[0]}',
                                ContentFile(f.read()),
                                save=False
                            )
                        
                        known_face.encoding = json.dumps(embedding.tolist())
                        known_face.save()
                        processed += 1
                        
                        if processed % 50 == 0:
                            print(f"[SUCCESS] Registered {processed} faces so far...")
                
            except Exception as e:
                errors += 1
                if errors % 10 == 0:
                    print(f"[WARNING] {errors} errors encountered so far...")
        
        print(f"\n[COMPLETE] LFW Dataset Processing Results:")
        print(f"✅ Processed: {processed} faces")
        print(f"⏭️ Skipped: {skipped} (already registered)")
        print(f"❌ Errors: {errors}")
        print(f"📊 Total persons in dataset: {total_persons}")
        
    except Exception as e:
        print(f"[ERROR] Failed to process dataset: {e}")
    
    finally:
        # Cleanup
        import shutil
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)
            print("[CLEANUP] Temporary files removed")

if __name__ == "__main__":
    process_lfw_dataset()