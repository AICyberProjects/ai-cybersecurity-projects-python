import pandas as pd
import joblib
import time
import os
from colorama import init, Fore

# ----------------------------
# Initialization
# ----------------------------
init()  # initialize colorama

MODEL_PATH = "model.joblib"
LOG_FILE = "log_stream.csv"
POLL_INTERVAL = 2  # seconds between checks

# ----------------------------
# Load model and log data
# ----------------------------
def load_model():
    return joblib.load(MODEL_PATH)

def load_log_data():
    return pd.read_csv(LOG_FILE)

# ----------------------------
# Check for new logs
# ----------------------------
def check_new_logs(model, last_seen):
    df = load_log_data()
    if len(df) <= last_seen:
        return last_seen  # No new logs

    new_entries = df.iloc[last_seen:]
    predictions = model.predict(new_entries)

    for i, pred in enumerate(predictions):
        if pred == -1:
            print(Fore.RED + f"[ALERT] Anomaly Detected in row {last_seen + i}!" + Fore.RESET)
            print(new_entries.iloc[i])
        else:
            print(Fore.GREEN + f"[OK] Normal log: {new_entries.iloc[i].to_dict()}" + Fore.RESET)

    return len(df)

# ----------------------------
# Monitor loop
# ----------------------------
def monitor():
    model = load_model()
    print("[*] Monitoring log stream...")
    last_seen = 0

    while True:
        try:
            last_seen = check_new_logs(model, last_seen)
            time.sleep(POLL_INTERVAL)
        except KeyboardInterrupt:
            print("Stopped by user.")
            break
        except Exception as e:
            print(Fore.YELLOW + f"[!] Error: {e}" + Fore.RESET)
            time.sleep(5)

# ----------------------------
# Run the monitor
# ----------------------------
if __name__ == "__main__":
    monitor()



 
