import pandas as pd
import numpy as np
import nltk
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, f1_score
from sklearn.pipeline import Pipeline
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
    ngram_range=(1, 3),  # Use unigrams, bigrams, and trigrams
    min_df=2,
    max_df=0.95,
    stop_words='english'
)

# Transform the text data
X_train_tfidf = tfidf.fit_transform(X_train)
X_test_tfidf = tfidf.transform(X_test)

# Train ensemble of models
print("Training multiple models...")

# 1. Logistic Regression
print("Training Logistic Regression...")
lr_model = LogisticRegression(random_state=42, max_iter=1000, C=10)
lr_model.fit(X_train_tfidf, y_train)

# 2. Random Forest
print("Training Random Forest...")
rf_model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=20)
rf_model.fit(X_train_tfidf, y_train)

# Evaluate models
lr_pred = lr_model.predict(X_test_tfidf)
rf_pred = rf_model.predict(X_test_tfidf)

print("\nModel Evaluation Results:")
print("=" * 50)

# Logistic Regression Results
lr_accuracy = accuracy_score(y_test, lr_pred)
lr_precision = precision_score(y_test, lr_pred)
lr_recall = recall_score(y_test, lr_pred)
lr_f1 = f1_score(y_test, lr_pred)

print(f"\nLogistic Regression:")
print(f"  Accuracy: {lr_accuracy:.4f}")
print(f"  Precision: {lr_precision:.4f}")
print(f"  Recall: {lr_recall:.4f}")
print(f"  F1-Score: {lr_f1:.4f}")

# Random Forest Results
rf_accuracy = accuracy_score(y_test, rf_pred)
rf_precision = precision_score(y_test, rf_pred)
rf_recall = recall_score(y_test, rf_pred)
rf_f1 = f1_score(y_test, rf_pred)

print(f"\nRandom Forest:")
print(f"  Accuracy: {rf_accuracy:.4f}")
print(f"  Precision: {rf_precision:.4f}")
print(f"  Recall: {rf_recall:.4f}")
print(f"  F1-Score: {rf_f1:.4f}")

# Choose the best model based on F1-score
if lr_f1 >= rf_f1:
    best_model = lr_model
    best_name = "Logistic Regression"
    best_pred = lr_pred
    print(f"\nSelected Model: {best_name}")
else:
    best_model = rf_model
    best_name = "Random Forest"
    best_pred = rf_pred
    print(f"\nSelected Model: {best_name}")

# Create an ensemble model that combines both
class EnsembleModel:
    def __init__(self, model1, model2, threshold=0.5):
        self.model1 = model1
        self.model2 = model2
        self.threshold = threshold
    
    def predict(self, X):
        pred1 = self.model1.predict(X)
        pred2 = self.model2.predict(X)
        # Simple voting - if both agree, use that, otherwise use model1
        return np.where(pred1 == pred2, pred1, pred1)
    
    def predict_proba(self, X):
        prob1 = self.model1.predict_proba(X)
        prob2 = self.model2.predict_proba(X)
        # Average probabilities
        return (prob1 + prob2) / 2

# Create ensemble model
ensemble_model = EnsembleModel(lr_model, rf_model)
ensemble_pred = ensemble_model.predict(X_test_tfidf)
ensemble_accuracy = accuracy_score(y_test, ensemble_pred)
ensemble_precision = precision_score(y_test, ensemble_pred)
ensemble_recall = recall_score(y_test, ensemble_pred)
ensemble_f1 = f1_score(y_test, ensemble_pred)

print(f"\nEnsemble Model:")
print(f"  Accuracy: {ensemble_accuracy:.4f}")
print(f"  Precision: {ensemble_precision:.4f}")
print(f"  Recall: {ensemble_recall:.4f}")
print(f"  F1-Score: {ensemble_f1:.4f}")

# Use the best performing model
final_model = ensemble_model if ensemble_f1 > max(lr_f1, rf_f1) else best_model

# Save the final model and vectorizer
print("\nSaving the final model and vectorizer...")
with open('robust_vectorizer.pkl', 'wb') as f:
    pickle.dump(tfidf, f)
with open('robust_model.pkl', 'wb') as f:
    pickle.dump(final_model, f)

print("Model training completed successfully!")
print(f"Saved robust_model.pkl and robust_vectorizer.pkl")

# Test with the specific spam messages provided
test_messages = [
    "Congratulations! You've won a $1000 gift card! Click here to claim: http://bit.ly/claim-now Reply within 24 hours or prize expires.",
    "Your account has been suspended. Verify here: http://bank-verify.com Click now or account will be locked.",
    "Your package delivery failed. Reschedule here: http://delivery-reschedule.com Click to arrange pickup.",
    "Work from home opportunity! $2000/month guaranteed income. Apply now: http://job-apply.com No experience needed.",
    "Your computer has viruses. Call now: 1-800-555-0123 Immediate assistance required.",
    "Hi, I need you to buy gift cards urgently. Send codes ASAP. Will reimburse tomorrow.",
    "Hi! I think we know each other. Check my profile: http://profile-view.com Let's connect!",
    "Hi there! You seem interesting. I'm new to the area. Want to chat? Text me: 555-0123",
    "Make money fast! Double your investment in 24 hours. Click here: http://invest-now.com Limited time offer.",
    "Take this quick survey! Win $500 instantly. Click here: http://survey-win.com Only 2 minutes!",
    "Congratulations! You've won ₹10 lakh in the online lottery. To claim your prize, send your bank account details and pay a processing fee.",
    "Your mobile number has been selected for a ₹25 lakh international WhatsApp lottery. Contact this number to claim your prize.",
    "Lucky Winner! You've won ₹10,00,000. Click the link and enter your details to receive the amount.",
    "बधाई हो! आपने ₹10,00,000 जीते हैं। राशि पाने के लिए लिंक पर क्लिक करें और अपना विवरण दर्ज करें",
    "बधाई हो! आपने ₹10,00,000 जीते हैं। राशि पाने के लिए लिंक पर क्लिक करें और अपना विवरण दर्ज करें http://bank-verify.com"
]

print("\nTesting with specific spam messages:")
transformed_test = [advanced_text_preprocessing(msg) for msg in test_messages]
test_vectors = tfidf.transform(transformed_test)
predictions = final_model.predict(test_vectors)
probabilities = final_model.predict_proba(test_vectors)

for i, msg in enumerate(test_messages):
    spam_prob = probabilities[i][1]
    result = "SPAM" if predictions[i] == 1 else "NOT SPAM"
    print(f"'{msg[:50]}...' -> {result} (Spam probability: {spam_prob:.4f})")