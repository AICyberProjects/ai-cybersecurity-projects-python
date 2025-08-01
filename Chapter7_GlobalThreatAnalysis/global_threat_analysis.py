import os
import folium
import openai
import pandas as pd

# ----------------------------
# Config
# ----------------------------
openai.api_key = "your-api-key"  # Replace with your real key

# Example DataFrame (replace this with actual data loading)
country_scores = pd.DataFrame([
    {"country": "USA", "avg_threat": 0.92, "risk_label": "HIGH", "severity_score": 0.95, "description": "Major DDoS attack on finance systems."},
    {"country": "China", "avg_threat": 0.68, "risk_label": "MEDIUM", "severity_score": 0.65, "description": "Increased phishing activity targeting industrial networks."},
    {"country": "Germany", "avg_threat": 0.34, "risk_label": "LOW", "severity_score": 0.3, "description": "Brute force attempts detected on minor endpoints."},
    {"country": "Russia", "avg_threat": 0.88, "risk_label": "HIGH", "severity_score": 0.91, "description": "Suspected APT group activity on infrastructure."}
])

coords = {
    "USA": [37.7749, -122.4194],
    "China": [39.9042, 116.4074],
    "Germany": [52.52, 13.4050],
    "Russia": [55.7558, 37.6173],
}

# ----------------------------
# Step 1: Generate World Threat Map
# ----------------------------
world_map = folium.Map(location=[20, 0], zoom_start=2)

for _, row in country_scores.iterrows():
    country = row["country"]
    risk = row["risk_label"]
    threat = row["avg_threat"]

    if country in coords:
        folium.CircleMarker(
            location=coords[country],
            radius=10,
            popup=f"{country}: {risk} ({threat:.2f})",
            color="red" if risk == "HIGH" else "orange" if risk == "MEDIUM" else "green",
            fill=True,
            fill_opacity=0.6
        ).add_to(world_map)

world_map.save("world_map.html")
print("[✔] Threat map saved as world_map.html")

# ----------------------------
# Step 2: Filter and Summarize Severe Threats with OpenAI
# ----------------------------
summary_input = "\n".join(
    country_scores[country_scores["severity_score"] > 0.75]["description"].tolist()
)

if summary_input:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a cybersecurity analyst. Analyze the following security incidents."},
            {"role": "user", "content": f"Summarize these incidents:\n{summary_input}"}
        ]
    )

    print("\n[AI SUMMARY]")
    print(response["choices"][0]["message"]["content"])
else:
    print("No high-severity incidents to summarize.")



