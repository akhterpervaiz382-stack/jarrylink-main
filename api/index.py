import os
from flask import Flask, request, jsonify, make_response, render_template
from flask_cors import CORS
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder='../templates')
CORS(app)

supabase = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY"))

@app.route('/<short_code>')
def redirect_logic(short_code):
    # System routes check
    if short_code in ["favicon.ico", "status", "shorten", "static"]:
        return "", 204
    
    try:
        res = supabase.table('links').select("original_url").eq("short_code", short_code).execute()
        
        if res.data and len(res.data) > 0:
            target = res.data[0]['original_url']
            if not target.startswith(('http://', 'https://')): 
                target = 'https://' + target
            
            # --- BULLETPROOF REDIRECT ---
            # Hum Flask ka default redirect use nahi kar rahe kyunke wo slow hai
            # Hum direct 'Location' header bhej rahe hain 301 status ke saath
            response = make_response("", 301)
            response.headers['Location'] = target
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            return response
            
    except Exception:
        pass
        
    # Agar link nahi milta toh seedha home par (Yahan bhi 302 use kiya taaki fast ho)
    response = make_response("", 302)
    response.headers['Location'] = '/'
    return response

@app.route('/')
def home():
    return render_template('architect_tool.html')

@app.route('/status')
def status():
    return jsonify({"status": "online"})

@app.route('/shorten', methods=['POST'])
def shorten():
    try:
        data = request.get_json()
        s_code, l_url = data.get('short_code').strip(), data.get('original_url').strip()
        supabase.table('links').insert({"short_code": s_code, "original_url": l_url, "clicks": 0}).execute()
        return jsonify({"status": "success"}), 201
    except:
        return jsonify({"status": "error"}), 400

app = app
