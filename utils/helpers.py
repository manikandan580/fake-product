import pandas as pd
import random
import os
from datetime import datetime

# Sample fake reviews (for auto-generation)
FAKE_REVIEWS = [
    "Amazing product! Best purchase ever! Highly recommended!",
    "Perfect! Exactly what I wanted. 5 stars!",
    "Great quality, fast shipping, awesome seller!",
    "Love it! Will buy again! Excellent service!",
    "Superb product! Very satisfied with the purchase!",
    "Excellent! Worth every penny!",
    "Fantastic! Couldn't be happier!",
    "Brilliant product! Very impressive!",
    "Outstanding! Top quality!",
    "Wonderful! Absolutely love it!",
    "Best product ever! Highly recommend to everyone!",
    "Perfect condition! Great value!",
    "Amazing quality! Very happy!",
    "Excellent product! Fast delivery!",
    "Great item! As described!",
    "Perfect transaction! Great seller!",
    "Awesome product! Highly satisfied!",
    "Fantastic value! Very pleased!",
    "Superb quality! Excellent purchase!",
    "Brilliant! Works perfectly!"
]

# Sample real reviews (for auto-generation)
REAL_REVIEWS = [
    "Good product but had some minor issues. Overall satisfied.",
    "Works as expected. Delivery was on time. Good value.",
    "Decent quality for the price. Would recommend.",
    "Average product. Nothing special but gets the job done.",
    "Good features but battery life could be better.",
    "Nice design but a bit expensive for what you get.",
    "Works fine but had to get used to it. Takes time.",
    "Good build quality. Satisfied with the purchase.",
    "Met my expectations. Good product overall.",
    "Pretty good. Some small improvements needed.",
    "Works well most of the time. Occasional glitches.",
    "Good value for money. Would buy again.",
    "Solid product. Does what it promises.",
    "Nice features but setup was complicated.",
    "Good performance. Satisfied customer.",
    "Works great after initial setup. Recommended.",
    "Good quality. Shipping was fast.",
    "Decent product. Good customer service.",
    "Works as advertised. Happy with purchase.",
    "Good product. Would recommend to friends."
]

def get_reviews_by_ratio(ratio_type):
    """
    Generate reviews based on the specified ratio of fake to real reviews
    
    Args:
        ratio_type (str): Type of ratio ('all_real', 'all_fake', '50_50', '70_30', '30_70')
    
    Returns:
        list: List of generated reviews
    """
    if ratio_type == 'all_real':
        return random.sample(REAL_REVIEWS, min(10, len(REAL_REVIEWS)))
    
    elif ratio_type == 'all_fake':
        return random.sample(FAKE_REVIEWS, min(10, len(FAKE_REVIEWS)))
    
    elif ratio_type == '50_50':
        num_reviews = 10
        num_real = num_reviews // 2
        num_fake = num_reviews - num_real
        
        reviews = []
        reviews.extend(random.sample(REAL_REVIEWS, min(num_real, len(REAL_REVIEWS))))
        reviews.extend(random.sample(FAKE_REVIEWS, min(num_fake, len(FAKE_REVIEWS))))
        random.shuffle(reviews)
        return reviews
    
    elif ratio_type == '70_30':
        num_reviews = 10
        num_real = int(num_reviews * 0.7)
        num_fake = num_reviews - num_real
        
        reviews = []
        reviews.extend(random.sample(REAL_REVIEWS, min(num_real, len(REAL_REVIEWS))))
        reviews.extend(random.sample(FAKE_REVIEWS, min(num_fake, len(FAKE_REVIEWS))))
        random.shuffle(reviews)
        return reviews
    
    elif ratio_type == '30_70':
        num_reviews = 10
        num_fake = int(num_reviews * 0.7)
        num_real = num_reviews - num_fake
        
        reviews = []
        reviews.extend(random.sample(REAL_REVIEWS, min(num_real, len(REAL_REVIEWS))))
        reviews.extend(random.sample(FAKE_REVIEWS, min(num_fake, len(FAKE_REVIEWS))))
        random.shuffle(reviews)
        return reviews
    
    else:
        # Default: return mixed reviews
        return get_reviews_by_ratio('50_50')

def load_reviews():
    """
    Load reviews from CSV file with better error handling
    """
    dataset_folder = "dataset"
    review_csv = os.path.join(dataset_folder, "reviews.csv")
    
    if os.path.exists(review_csv):
        try:
            # Try reading with pandas
            df = pd.read_csv(review_csv, encoding='utf-8', on_bad_lines='skip')
            
            # Check if the required columns exist
            if 'product_link' not in df.columns or 'review_text' not in df.columns:
                print("CSV file missing required columns")
                return create_sample_reviews_data()
                
            # Check if the file is empty
            if df.empty:
                print("Reviews CSV is empty")
                return create_sample_reviews_data()
                
            return df
        except Exception as e:
            print(f"Error loading reviews: {e}")
            return create_sample_reviews_data()
    else:
        # Create sample reviews if file doesn't exist
        print("Reviews CSV not found, creating sample data")
        return create_sample_reviews_data()

def create_sample_reviews_data():
    """
    Create sample reviews data for testing
    """
    dataset_folder = "dataset"
    os.makedirs(dataset_folder, exist_ok=True)
    
    review_csv = os.path.join(dataset_folder, "reviews.csv")
    
    # Sample reviews for different products
    sample_reviews = [
        # Samsung Galaxy S24 reviews
        ("https://example.com/galaxy-s24", "Amazing phone! The camera quality is outstanding and battery life is great!", "unknown"),
        ("https://example.com/galaxy-s24", "Best Android phone I've ever used. Highly recommended!", "unknown"),
        ("https://example.com/galaxy-s24", "Great features but a bit expensive. Worth it though!", "unknown"),
        ("https://example.com/galaxy-s24", "The AI features are impressive. Love this phone!", "unknown"),
        ("https://example.com/galaxy-s24", "Not worth the price. Battery drains too fast.", "unknown"),
        
        # MacBook Pro reviews
        ("https://example.com/macbook", "Best laptop for developers! Fast and reliable.", "unknown"),
        ("https://example.com/macbook", "Expensive but worth every penny. Great performance!", "unknown"),
        ("https://example.com/macbook", "Battery life is amazing. Lasts all day!", "unknown"),
        
        # Sony Headphones reviews
        ("https://example.com/sony-headphones", "Noise cancellation is top-notch! Best headphones ever!", "unknown"),
        ("https://example.com/sony-headphones", "Great sound quality but a bit heavy.", "unknown"),
        
        # Apple Watch reviews
        ("https://example.com/apple-watch", "Perfect fitness tracker! Love the health features.", "unknown"),
        ("https://example.com/apple-watch", "Good watch but needs daily charging.", "unknown"),
        
        # iPad Pro reviews
        ("https://example.com/ipad-pro", "Perfect for artists and designers! Great display.", "unknown"),
        ("https://example.com/ipad-pro", "Powerful tablet but expensive accessories.", "unknown"),
    ]
    
    # Create DataFrame
    df = pd.DataFrame(sample_reviews, columns=['product_link', 'review_text', 'label'])
    
    # Save to CSV
    df.to_csv(review_csv, index=False, quoting=1, encoding='utf-8')
    print(f"Created sample reviews file with {len(df)} reviews")
    
    return df

def predict_reviews(review_text):
    """
    Simple rule-based prediction for fake vs real reviews
    
    Args:
        review_text (str): The review text to analyze
    
    Returns:
        tuple: (fake_score, real_score) - scores indicating likelihood
    """
    # Convert to lowercase for analysis
    review_lower = review_text.lower()
    
    # Fake review indicators (overly positive, short, using excessive punctuation)
    fake_indicators = [
        'amazing', 'perfect', 'best', 'love it', 'awesome', 'fantastic',
        'superb', 'brilliant', 'wonderful', 'outstanding', 'excellent',
        '!!!', 'best ever', 'highly recommend', 'couldn\'t be happier'
    ]
    
    # Real review indicators (more balanced, specific, critical)
    real_indicators = [
        'but', 'however', 'minor issues', 'works as expected', 'average',
        'decent', 'good but', 'could be better', 'takes time', 'gets the job done',
        'worth the price', 'met expectations', 'some improvements', 'bit expensive'
    ]
    
    fake_score = 0
    real_score = 0
    
    # Check for fake indicators
    for indicator in fake_indicators:
        if indicator in review_lower:
            fake_score += 1
    
    # Check for real indicators
    for indicator in real_indicators:
        if indicator in review_lower:
            real_score += 1
    
    # Length analysis (very short reviews are often fake)
    if len(review_text) < 20:
        fake_score += 1
    
    # All caps analysis (excessive caps might indicate fake)
    caps_ratio = sum(1 for c in review_text if c.isupper()) / max(len(review_text), 1)
    if caps_ratio > 0.3:
        fake_score += 0.5
    
    # Punctuation analysis (multiple exclamation marks)
    if review_text.count('!') > 2:
        fake_score += 1
    
    # Normalize scores to a range between 0 and 1
    total = max(fake_score + real_score, 1)
    fake_score_normalized = fake_score / total
    real_score_normalized = real_score / total
    
    return fake_score_normalized, real_score_normalized

def extract_features_from_review(review_text):
    """
    Extract features from review text for machine learning
    
    Args:
        review_text (str): The review text
    
    Returns:
        dict: Dictionary of extracted features
    """
    review_lower = review_text.lower()
    
    features = {
        'length': len(review_text),
        'word_count': len(review_text.split()),
        'exclamation_count': review_text.count('!'),
        'question_count': review_text.count('?'),
        'caps_ratio': sum(1 for c in review_text if c.isupper()) / max(len(review_text), 1),
        'has_positive_words': any(word in review_lower for word in ['good', 'great', 'excellent', 'amazing', 'perfect']),
        'has_negative_words': any(word in review_lower for word in ['bad', 'poor', 'terrible', 'awful', 'disappointing']),
        'has_specific_details': any(word in review_lower for word in ['battery', 'screen', 'price', 'shipping', 'quality'])
    }
    
    return features

def analyze_review_batch(reviews_list):
    """
    Analyze a batch of reviews and return statistics
    
    Args:
        reviews_list (list): List of review texts
    
    Returns:
        dict: Statistics about the reviews
    """
    fake_count = 0
    real_count = 0
    
    for review in reviews_list:
        fake_score, real_score = predict_reviews(review)
        if fake_score > real_score:
            fake_count += 1
        else:
            real_count += 1
    
    total = len(reviews_list)
    fake_percentage = (fake_count / total) * 100 if total > 0 else 0
    real_percentage = (real_count / total) * 100 if total > 0 else 0
    
    return {
        'total_reviews': total,
        'fake_count': fake_count,
        'real_count': real_count,
        'fake_percentage': fake_percentage,
        'real_percentage': real_percentage
    }

def save_review_analysis(product_link, reviews_analysis):
    """
    Save review analysis results to a file
    
    Args:
        product_link (str): The product link
        reviews_analysis (dict): Analysis results
    """
    analysis_file = os.path.join("dataset", "review_analysis.csv")
    file_exists = os.path.exists(analysis_file)
    
    df = pd.DataFrame([{
        'product_link': product_link,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'total_reviews': reviews_analysis['total_reviews'],
        'fake_count': reviews_analysis['fake_count'],
        'real_count': reviews_analysis['real_count'],
        'fake_percentage': reviews_analysis['fake_percentage'],
        'real_percentage': reviews_analysis['real_percentage']
    }])
    
    if file_exists:
        df.to_csv(analysis_file, mode='a', header=False, index=False)
    else:
        df.to_csv(analysis_file, index=False)

def get_product_statistics(product_link):
    """
    Get statistics for a specific product
    
    Args:
        product_link (str): The product link
    
    Returns:
        dict: Statistics about the product's reviews
    """
    df = load_reviews()
    product_reviews = df[df['product_link'] == product_link]
    
    if product_reviews.empty:
        return None
    
    reviews_list = product_reviews['review_text'].tolist()
    return analyze_review_batch(reviews_list)

def generate_sample_reviews(product_link, num_reviews=10, fake_percentage=50):
    """
    Generate sample reviews for a product
    
    Args:
        product_link (str): The product link
        num_reviews (int): Number of reviews to generate
        fake_percentage (int): Percentage of fake reviews (0-100)
    
    Returns:
        list: List of generated reviews
    """
    num_fake = int((fake_percentage / 100) * num_reviews)
    num_real = num_reviews - num_fake
    
    reviews = []
    
    # Generate fake reviews
    for _ in range(num_fake):
        review = random.choice(FAKE_REVIEWS)
        reviews.append(review)
    
    # Generate real reviews
    for _ in range(num_real):
        review = random.choice(REAL_REVIEWS)
        reviews.append(review)
    
    # Shuffle the reviews
    random.shuffle(reviews)
    
    return reviews

# Export functions for use in the main app
__all__ = [
    'get_reviews_by_ratio',
    'load_reviews',
    'predict_reviews',
    'extract_features_from_review',
    'analyze_review_batch',
    'save_review_analysis',
    'get_product_statistics',
    'generate_sample_reviews'
]