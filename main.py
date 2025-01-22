import os
import openai
import requests
import json

# Initialize SambaNova client
client = openai.OpenAI(
    api_key=os.environ.get("SAMBANOVA_API_KEY"),
    base_url="https://api.sambanova.ai/v1",
)

def fetch_google_maps_data(location):
    """Fetch real-time traffic data from Google Maps API"""
    # Replace with your Google Maps API logic
    mock_data = {
        "location": location,
        "congestion_level": "high",
        "incidents": ["accident", "road_closure"],
        "speed": "20 km/h"
    }
    return mock_data

def analyze_traffic_with_sambanova(traffic_data):
    """Use SambaNova to analyze traffic data and generate insights"""
    prompt = f"""
    Analyze this traffic data and recommend optimal rerouting strategies:
    Location: {traffic_data['location']}
    Congestion: {traffic_data['congestion_level']}
    Incidents: {', '.join(traffic_data['incidents'])}
    Current Speed: {traffic_data['speed']}

    Consider these factors:
    - Proximity to hospitals/police stations
    - Weather conditions (assume clear)
    - Time of day (assume rush hour)
    
    Output format:
    [Incident Severity: Low/Medium/High]
    [Recommended Action: reroute/status_update/emergency_alert]
    [Alternative Routes: route1, route2]
    [Reasoning: 1-2 sentences]
    """
    
    response = client.chat.completions.create(
        model='Meta-Llama-3.1-8B-Instruct',
        messages=[
            {"role": "system", "content": "You are a traffic management AI specialized in UAE road networks"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
        top_p=0.1,
        max_tokens=300
    )
    
    return response.choices[0].message.content

def process_incident_response(response):
    """Parse SambaNova's response into actionable data"""
    parsed_response = {
        "severity": "Medium",
        "action": "reroute",
        "routes": [],
        "reasoning": ""
    }
    
    # Simple parsing logic (enhance with regex/ML for production)
    lines = response.split('\n')
    for line in lines:
        if "Incident Severity:" in line:
            parsed_response["severity"] = line.split(": ")[1].strip()
        elif "Recommended Action:" in line:
            parsed_response["action"] = line.split(": ")[1].strip()
        elif "Alternative Routes:" in line:
            parsed_response["routes"] = [r.strip() for r in line.split(": ")[1].split(",")]
        elif "Reasoning:" in line:
            parsed_response["reasoning"] = line.split(": ")[1].strip()
            
    return parsed_response

# Example workflow
if __name__ == "__main__":
    # 1. Get real-time data
    traffic_data = fetch_google_maps_data("Sheikh Zayed Road, Dubai")
    
    # 2. Analyze with SambaNova
    ai_response = analyze_traffic_with_sambanova(traffic_data)
    
    # 3. Process response
    action = process_incident_response(ai_response)
    
    # 4. Output results
    print("🚦 Traffic Management Decision 🚦")
    print(f"Severity: {action['severity']}")
    print(f"Action: {action['action'].upper()}")
    print(f"Suggested Routes: {', '.join(action['routes']) or 'Maintain current route'}")
    print(f"Reasoning: {action['reasoning']}")