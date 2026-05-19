import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pickle

# Load products dataset
df = pd.read_csv("dataset/products.csv")

# Feature Engineering
# Use price, rating, description length as features
df['desc_len'] = df['description'].apply(lambda x: len(str(x)))
X = df[['price', 'rating', 'desc_len']]

# Encode target: Fake if price < 100 or rating > 4.8
df['target'] = df.apply(lambda row: 0 if (row['price'] < 100 or row['rating'] > 4.8) else 1, axis=1)
y = df['target']

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train RandomForest Classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Evaluate
score = clf.score(X_test, y_test)
print(f"Product Model Accuracy: {score*100:.2f}%")

# Save model
with open("model/product_model.pkl", "wb") as f:
    pickle.dump(clf, f)
print("Product model saved as product_model.pkl")