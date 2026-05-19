import re
from sklearn.feature_extraction.text import TfidfVectorizer

# -----------------------------
# Text Preprocessing
# -----------------------------
def clean_text(text):
    """
    Lowercase, remove special chars, extra spaces
    """
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def preprocess_reviews(reviews_list):
    """
    Return TF-IDF vector for ML model
    """
    cleaned = [clean_text(r) for r in reviews_list]
    vectorizer = TfidfVectorizer(max_features=500)
    X = vectorizer.fit_transform(cleaned)
    return X

# -----------------------------
# Image Preprocessing (Optional)
# -----------------------------
from PIL import Image
import numpy as np

def preprocess_image(image_path, size=(224,224)):
    """
    Resize and normalize image for ML model
    """
    img = Image.open(image_path).convert("RGB")
    img = img.resize(size)
    img_array = np.array(img) / 255.0
    return img_array