import os
from flask import Flask, request, jsonify, make_response, render_template, redirect
from flask_cors import CORS
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder='../templates')
CORS(app)

supabase = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY"))

# --- ULTRA-FAST SILENT REDIRECT ---
@app.route('/<short_code>')
def redirect_logic(short_code):
    # System files ignore karein
    if short_code in ["favicon.ico", "status", "shorten", "static"]:
        return "", 204
    
    try:
        res = supabase.table('links').select("original_url").eq("short_code", short_code).execute()
        if res.data and len(res.data) > 0:
            target = res.data[0]['original_url']
            if not target.startswith(('http://', 'https://')): 
                target = 'https://' + target
            
            # 301 ki jagah hum Headers wala direct redirect bhej rahe hain 
            # jo browser ke cache ko bypass karke seedha target marta hai
            response = make_response("", 302) # 302 is faster for non-cached jumps
            response.headers['Location'] = target
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response.headers['Pragma'] = 'no-cache'
            return response
            
    except Exception as e:
        print(f"Error: {e}")
        
    return redirect('/')

# --- HOME & SHORTEN LOGIC (Wohi rakha hai jo aapne diya tha) ---
@app.route('/')
def home():
    try:
        return render_template('architect_tool.html')
    except:
        return "Home Page Ready", 200

@app.route('/shorten', methods=['POST'])
def shorten():
    try:
        data = request.get_json(silent=True) or request.form
        s_code = data.get('short_code', '').strip()
        l_url = data.get('original_url', '').strip()

        if not s_code or not l_url:
            return jsonify({"status": "error"}), 400

        supabase.table('links').insert({
            "short_code": s_code, "original_url": l_url, "clicks": 0
        }).execute()
        
        return jsonify({"status": "success"}), 201
    except:
        return jsonify({"status": "error"}), 400

app = app
