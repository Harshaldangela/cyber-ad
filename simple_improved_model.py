import pandas as pd
import numpy as np
import nltk
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, f1_score
import pickle
import string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Load and preprocess data
df = pd.read_csv('spam.csv', encoding='latin1')
df.drop(columns=['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], inplace=True)
df.rename(columns={'v1': 'target', 'v2': 'text'}, inplace=True)

# Map target labels
df['target'] = df['target'].map({'ham': 0, 'spam': 1})
df = df.drop_duplicates()

# Initialize stemmer
ps = PorterStemmer()

def advanced_text_preprocessing(text):
    """Advanced text preprocessing for better feature extraction"""
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    
    # Remove phone numbers
    text = re.sub(r'\d{3,}', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Tokenize
    tokens = word_tokenize(text)
    
    # Remove punctuation and non-alphabetic tokens
    tokens = [token for token in tokens if token.isalpha() and len(token) > 1]
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    
    # Stemming
    tokens = [ps.stem(token) for token in tokens]
    
    return " ".join(tokens)

# Apply advanced preprocessing
print("Preprocessing text data...")
df['transformed_text'] = df['text'].apply(advanced_text_preprocessing)

# Remove empty texts after preprocessing
df = df[df['transformed_text'].str.len() > 0]

# Prepare features and target
X = df['transformed_text']
y = df['target'].values

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Create TF-IDF vectorizer with better parameters
print("Creating TF-IDF vectorizer...")
tfidf = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2),  # Use both unigrams and bigrams
    min_df=2,
    max_df=0.95,
    stop_words='english'
)

# Transform the text data
X_train_tfidf = tfidf.fit_transform(X_train)
X_test_tfidf = tfidf.transform(X_test)

# Train Logistic Regression model (good balance of performance and speed)
print("Training Logistic Regression model...")
model = LogisticRegression(random_state=42, max_iter=1000, C=10)
model.fit(X_train_tfidf, y_train)

# Evaluate model
y_pred = model.predict(X_test_tfidf)
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print(f"\nModel Performance:")
print(f"  Accuracy: {accuracy:.4f}")
print(f"  Precision: {precision:.4f}")
print(f"  Recall: {recall:.4f}")
print(f"  F1-Score: {f1:.4f}")

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
print(f"\nConfusion Matrix:")
print(f"  TN: {cm[0,0]}, FP: {cm[0,1]}")
print(f"  FN: {cm[1,0]}, TP: {cm[1,1]}")

# Save the model and vectorizer
print("\nSaving the model and vectorizer...")
with open('improved_vectorizer.pkl', 'wb') as f:
    pickle.dump(tfidf, f)
with open('improved_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Model training completed successfully!")
print(f"Saved improved_model.pkl and improved_vectorizer.pkl")

# Test with some example messages
test_messages = [
    "Congratulations! You've won $1000. Click here to claim your prize now!",
    "Hey, are we still meeting for lunch tomorrow?",
    "URGENT: Your account will be suspended. Click here to verify immediately.",
    "Thanks for the meeting today. I'll send the report by Friday.",
    "FREE! Get your iPhone now! Limited time offer. Call 123-456-7890"
]

print("\nTesting with example messages:")
transformed_test = [advanced_text_preprocessing(msg) for msg in test_messages]
test_vectors = tfidf.transform(transformed_test)
predictions = model.predict(test_vectors)
probabilities = model.predict_proba(test_vectors)

for i, msg in enumerate(test_messages):
    spam_prob = probabilities[i][1]
    result = "SPAM" if predictions[i] == 1 else "NOT SPAM"
    print(f"'{msg}' -> {result} (Spam probability: {spam_prob:.4f})")