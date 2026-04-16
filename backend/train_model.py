import pandas as pd
import pickle
import os
import gdown

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

dataset_path = os.path.join(BASE_DIR, "phishing_email.csv")

file_id = "1xkikel5OD2JUBYOPebErxmswwlxIWxOY"

# Download dataset
if not os.path.exists(dataset_path):
    print("Downloading dataset...")
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, dataset_path, quiet=False)

print("Loading dataset...")
df = pd.read_csv(dataset_path)

print("Dataset Columns:", df.columns)

X = df.iloc[:, 0]
y = df.iloc[:, -1]

print("Vectorizing...")
vectorizer = TfidfVectorizer(stop_words='english')
X_vector = vectorizer.fit_transform(X.astype(str))

print("Training model...")
X_train, X_test, y_train, y_test = train_test_split(
    X_vector, y, test_size=0.2, random_state=42
)

model = LogisticRegression(max_iter=1000, n_jobs=-1)
model.fit(X_train, y_train)

print("Saving model...")

pickle.dump(model, open(os.path.join(BASE_DIR, "scam_model.pkl"), "wb"))
pickle.dump(vectorizer, open(os.path.join(BASE_DIR, "vectorizer.pkl"), "wb"))

print("Model trained successfully")
