import pandas as pd
import random
from datetime import datetime, timedelta
from sklearn.ensemble import IsolationForest

# ----------------------------
# Configuration Constants
# ----------------------------
NUM_LOGS = 500
NUM_ANOMALIES = 10
FILENAME_LOGS = 'synthetic_logs.csv'
FILENAME_ANOMALIES = 'anomalies_detected.csv'
SEED = 42
CONTAMINATION_RATE = 0.02
N_ESTIMATORS = 100

# Normal log value ranges
CPU_NORMAL = (0, 100)
MEMORY_NORMAL = (0, 100)
NET_NORMAL = (0, 1000)

# Anomaly value ranges
CPU_ANOMALY = (90, 100)
MEMORY_ANOMALY = (90, 100)
NET_ANOMALY = (2000, 3000)

# ----------------------------
# Log Generation Function
# ----------------------------
def generate_logs(filename=FILENAME_LOGS, num_logs=NUM_LOGS, num_anomalies=NUM_ANOMALIES, include_timestamps=True):
    random.seed(SEED)
    logs = []
    base_time = datetime.now()

    # Generate normal logs
    for i in range(num_logs):
        log = {
            'cpu_usage': round(random.uniform(*CPU_NORMAL), 2),
            'memory_usage': round(random.uniform(*MEMORY_NORMAL), 2),
            'network_in': round(random.uniform(*NET_NORMAL), 2),
            'network_out': round(random.uniform(*NET_NORMAL), 2)
        }
        if include_timestamps:
            log['timestamp'] = (base_time + timedelta(seconds=i)).isoformat()
        logs.append(log)

    # Inject anomalies
    for i in range(num_anomalies):
        log = {
            'cpu_usage': round(random.uniform(*CPU_ANOMALY), 2),
            'memory_usage': round(random.uniform(*MEMORY_ANOMALY), 2),
            'network_in': round(random.uniform(*NET_ANOMALY), 2),
            'network_out': round(random.uniform(*NET_ANOMALY), 2)
        }
        if include_timestamps:
            log['timestamp'] = (base_time + timedelta(seconds=num_logs + i)).isoformat()
        logs.append(log)

    # Save to CSV
    df = pd.DataFrame(logs)
    df.to_csv(filename, index=False)
    print(f"[✔] Saved {len(df)} synthetic logs to {filename}")

# ----------------------------
# Anomaly Detection Function
# ----------------------------
def detect_anomalies(filename_in=FILENAME_LOGS, filename_out=FILENAME_ANOMALIES):
    df = pd.read_csv(filename_in)

    # Drop non-numeric columns (e.g., timestamp)
    if 'timestamp' in df.columns:
        df_features = df.drop(columns=['timestamp'])
    else:
        df_features = df.copy()

    # Create and train the Isolation Forest model
    model = IsolationForest(
        n_estimators=N_ESTIMATORS,
        contamination=CONTAMINATION_RATE,
        random_state=SEED
    )
    model.fit(df_features)

    # Predict anomalies: -1 = anomaly, 1 = normal
    df['anomaly'] = model.predict(df_features)

    # Filter out anomalies
    anomalies = df[df['anomaly'] == -1]
    print("[!] Anomalies Detected:\n")
    print(anomalies)

    # Save anomalies to file
    anomalies.to_csv(filename_out, index=False)
    print(f"Anomalies saved to {filename_out}")

# ----------------------------
# Run Both Functions
# ----------------------------
if __name__ == "__main__":
    generate_logs()
    detect_anomalies()

