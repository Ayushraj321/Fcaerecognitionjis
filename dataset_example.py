#!/usr/bin/env python
"""
Example script to create a sample dataset structure for testing bulk registration
"""
import os
from pathlib import Path

def create_sample_dataset():
    """Create sample dataset structure"""
    
    dataset_dir = Path("sample_dataset")
    dataset_dir.mkdir(exist_ok=True)
    
    # Create sample person directories
    persons = ["john_doe", "jane_smith", "bob_johnson", "alice_brown", "charlie_wilson"]
    
    for person in persons:
        person_dir = dataset_dir / person
        person_dir.mkdir(exist_ok=True)
        
        # Create placeholder files (you would replace these with actual images)
        readme_file = person_dir / "README.txt"
        with open(readme_file, 'w') as f:
            f.write(f"Place {person}'s face images here.\n")
            f.write("Supported formats: .jpg, .jpeg, .png, .bmp\n")
            f.write("Example files:\n")
            f.write(f"- {person}_1.jpg\n")
            f.write(f"- {person}_2.png\n")
            f.write(f"- {person}_photo.jpeg\n")
    
    print(f"[SUCCESS] Sample dataset structure created in '{dataset_dir}'")
    print("\n[STRUCTURE] Directory structure:")
    for person in persons:
        print(f"-- {person}/")
        print(f"   -- README.txt")
    
    print(f"\n[INSTRUCTIONS]:")
    print(f"1. Replace README.txt files with actual face images")
    print(f"2. Create a ZIP file from the '{dataset_dir}' folder")
    print(f"3. Upload the ZIP file using the bulk registration feature")

if __name__ == "__main__":
    create_sample_dataset()