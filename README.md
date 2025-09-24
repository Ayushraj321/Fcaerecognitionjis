# Django Deep Learning Face Identification System

A sophisticated Django-based face identification system using deep learning algorithms for accurate face recognition.

## Features
- **Deep Learning Recognition**: Uses FaceNet neural network for 512-dimensional face embeddings
- **High Accuracy**: Cosine similarity matching with confidence scores
- **Face Registration**: Register known faces with AI-powered feature extraction
- **Real-time Identification**: Identify multiple faces in uploaded images
- **Confidence Scoring**: Shows similarity scores for identified faces
- **Responsive UI**: Bootstrap-styled modern interface

## Deep Learning Architecture
- **FaceNet Model**: Pre-trained on millions of faces for robust embeddings
- **MTCNN**: Multi-task CNN for accurate face detection
- **Cosine Similarity**: Advanced matching algorithm
- **512-D Embeddings**: High-dimensional feature vectors for precise identification

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Run migrations: `python manage.py migrate`
3. Start server: `python manage.py runserver`
4. Visit: http://127.0.0.1:8000

## Usage
1. **Register Known Faces**: Upload photos to create AI embeddings
2. **Bulk Registration**: Upload ZIP files with multiple faces organized by person
3. **Identify Faces**: Upload images for deep learning analysis
4. **View Results**: See identified faces with confidence scores

## Bulk Registration
For large datasets, use the bulk registration feature:

### Dataset Structure
```
dataset.zip
├── person1/
│   ├── image1.jpg
│   └── image2.jpg
├── person2/
│   ├── photo1.png
│   └── photo2.png
└── person3/
    └── face.jpg
```

### Command Line Usage
```bash
# Bulk register from directory
python manage.py bulk_register /path/to/dataset --batch-size 10

# Create sample dataset structure
python dataset_example.py
```

### Web Interface
1. Go to "Bulk Register" page
2. Upload ZIP file with organized face images
3. System processes all faces automatically
4. View registration results and statistics

## Technology Stack
- Django 5.2.6
- TensorFlow 2.20.0 for deep learning
- MTCNN for face detection
- VGG16 for feature extraction
- OpenCV for image processing
- Scikit-learn for similarity calculations
- Bootstrap for modern UI

## Performance Features
- **Batch Processing**: Handle large datasets efficiently
- **Duplicate Detection**: Skip already registered faces
- **Error Handling**: Robust processing with detailed feedback
- **Memory Optimization**: Process images in configurable batches
- **Progress Tracking**: Real-time feedback during bulk operations