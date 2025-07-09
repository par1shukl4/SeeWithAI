print("Starting chatbot training...")
import json
import random
import numpy as np
import pickle
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sentence_transformers import SentenceTransformer

# Load intents
with open('intents.json', 'r') as f:
    data = json.load(f)

# Extract patterns and tags
all_patterns = []
all_tags = []

for intent in data['intents']:
    tag = intent['tag']
    for pattern in intent['patterns']:
        all_patterns.append(pattern)
        all_tags.append(tag)

# Encode labels
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(all_tags)

# Load BERT model
print("Loading sentence transformer...")
model = SentenceTransformer('all-MiniLM-L6-v2')

# Encode text to embeddings
print("Encoding patterns...")
X = model.encode(all_patterns)

# Train classifier
print("Training model...")
classifier = LogisticRegression()
classifier.fit(X, y)

# Save everything
with open('chatbot_model.pkl', 'wb') as f:
    pickle.dump(classifier, f)

with open('label_encoder.pkl', 'wb') as f:
    pickle.dump(label_encoder, f)

with open('intents.json', 'r') as f:
    intents_data = json.load(f)

print("Training complete.")
