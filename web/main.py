from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from datetime import datetime
import pandas as pd 
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GroupKFold, cross_val_score
from sklearn.preprocessing import LabelEncoder
import pickle

app = Flask(__name__)

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash')

with open('model/rf_model.pkl', 'rb') as f:
    rf = pickle.load(f)

with open('model/label_encoder.pkl', 'rb') as f:
    le = pickle.load(f)

# 2. Haversine helper
def haversine(lat1, lon1, lat2, lon2):
    """Compute distance (in meters) between two lat/lon points."""
    R = 6371000  # Earth radius in meters
    phi1, phi2 = np.radians(lat1), np.radians(lat2)
    dphi = phi2 - phi1
    dlambda = np.radians(lon2 - lon1)
    a = np.sin(dphi/2.0)**2 + np.cos(phi1)*np.cos(phi2)*np.sin(dlambda/2.0)**2
    return R * 2 * np.arcsin(np.sqrt(a))


# 9. Predict function for a new chunk (one user_wallet)
def predict_chunk(df_chunk):
    dfc = df_chunk.copy()
    dfc['timestamp'] = pd.to_datetime(dfc['timestamp'])
    dfc = dfc.sort_values('timestamp')

    features = [
    'location_lat','location_long',
    'hour','day','month','weekday',
    'distance_m','delta_s','speed_mps'
    ]
    
    # compute distance & delta
    dfc[['distance_m','delta_s']] = pd.DataFrame({
        'distance_m': haversine(
            dfc['location_lat'].shift(), dfc['location_long'].shift(),
            dfc['location_lat'],       dfc['location_long']
        ).fillna(0),
        'delta_s': (dfc['timestamp'] - dfc['timestamp'].shift()).dt.total_seconds().fillna(0),
    })
    dfc['speed_mps'] = (dfc['distance_m'] / dfc['delta_s'].replace(0, np.nan)).fillna(0)
    
    # time features
    dfc['hour']    = dfc['timestamp'].dt.hour
    dfc['day']     = dfc['timestamp'].dt.day
    dfc['month']   = dfc['timestamp'].dt.month
    dfc['weekday'] = dfc['timestamp'].dt.weekday
    
    Xc = dfc[features]
    preds = rf.predict(Xc)
    dfc['predicted_anomaly'] = le.inverse_transform(preds)
    return dfc

df = pd.read_csv('generated_dataset.csv', parse_dates=['timestamp'])
chunk = df[['timestamp','location_lat','location_long']]
result = predict_chunk(chunk)

userData = df.values.tolist()
for r in range(len(userData)):
    userData[r].append(result["predicted_anomaly"][r])


# print(type(userData), "\n", userData, "\n")

headers = list(df.columns)
headers.append("ML Result")


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        chat_history = data.get('history', [])
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Build conversation context for Gemini
        conversation_context = []
        
        # Add chat history to context
        for msg in chat_history:
            if msg['role'] == 'user':
                conversation_context.append(f"User: {msg['content']}")
            else:
                conversation_context.append(f"Assistant: {msg['content']}")
        
        # Add current user message
        conversation_context.append(f"User: {user_message}")

        
        
        prompt = f"""
                                    Developer prompt: The admin will send you a message and i will send you some data along with it. you have to use this info to answer the admin prompt. Be crisp and to the point, answer in 2-3 lines. respond exactly only what the admin asks. Style your responses with nice html and css.
                                    Admin prompt: f{user_message}
                                    Data headers:  {headers}
                                    Data:""" + str(userData)
        
        # Create prompt with context
        if conversation_context:
            prompt = "\n".join(conversation_context[:-1]) + f"\n\n{prompt}\n\nAssistant:"
        else:
            prompt = f"User: {user_message}\n\nAssistant:"
        
        # Generate response from Gemini
        response = model.generate_content(prompt)
        bot_response = response.text

        if "```html" in bot_response:
            bot_response = bot_response.split("```html")[1].split("```")[0]
        
        return jsonify({
            'response': bot_response,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            'error': 'Sorry, I encountered an error. Please try again.',
            'timestamp': datetime.now().isoformat()
        }), 500

if __name__ == '__main__':
    # Check if API key is set
    if not os.getenv('GEMINI_API_KEY'):
        print("Warning: GEMINI_API_KEY environment variable not set")
        print("Please set it with: export GEMINI_API_KEY='your_api_key_here'")
    
    app.run(debug=True, host='0.0.0.0', port=5000)