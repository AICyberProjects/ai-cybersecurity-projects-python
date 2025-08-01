import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report

# ----------------------------
# Load dataset
# ----------------------------
df = pd.read_csv("network_data.csv")

# Encode categorical columns
df['protocol'] = LabelEncoder().fit_transform(df['protocol'])
df['flag'] = LabelEncoder().fit_transform(df['flag'])
df['label'] = df['label'].map({'normal': 0, 'attack': 1})

# Features and labels
X = df.drop('label', axis=1)
y = df['label']

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ----------------------------
# Train model
# ----------------------------
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("Model Evaluation:\n")
print(classification_report(y_test, y_pred))

# Save model
joblib.dump(model, "model_nids.joblib")
print("Model saved as model_nids.joblib")

# ----------------------------
# Predict a new traffic sample
# ----------------------------
# Example input (make sure the feature order matches training data)
new_data = pd.DataFrame([{
    'duration': 0.5,
    'protocol': 1,    # Encoded protocol (e.g., TCP)
    'src_bytes': 100,
    'dst_bytes': 300,
    'flag': 2         # Encoded flag (e.g., SF)
}])

# Load and predict
model = joblib.load("model_nids.joblib")
prediction = model.predict(new_data)[0]
label = "ATTACK" if prediction == 1 else "NORMAL"
print(f"\n[RESULT] This traffic is classified as: {label}")

