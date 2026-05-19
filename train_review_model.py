import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import pickle

# Load reviews dataset
df = pd.read_csv("dataset/reviews.csv")

# Preprocessing function
def clean_text(text):
    import re
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

df['cleaned'] = df['review_text'].apply(clean_text)

# Encode target
df['label_num'] = df['label'].apply(lambda x: 1 if x=='real' else 0)

X = df['cleaned']
y = df['label_num']

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Pipeline: TF-IDF + Naive Bayes
model = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=500)),
    ('clf', MultinomialNB())
])

model.fit(X_train, y_train)

# Evaluate
score = model.score(X_test, y_test)
print(f"Review Model Accuracy: {score*100:.2f}%")

# Save model
with open("model/review_model.pkl", "wb") as f:
    pickle.dump(model, f)
print("Review model saved as review_model.pkl")