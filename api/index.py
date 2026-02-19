
import os
from flask import Flask, request, jsonify, make_response, render_template, redirect
from flask_cors import CORS
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder='../templates')

# CORS setting taake Blogger/Localhost se error na aaye
CORS(app)

supabase = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY"))

# --- ULTRA-FAST SILENT REDIRECT (With Click Counter) ---
@app.route('/<short_code>')
def redirect_logic(short_code):
    # System files ignore karein
    if short_code in ["favicon.ico", "status", "shorten", "static"]:
        return "", 204
    
    try:
        # 1. Database se link fetch karein
        res = supabase.table('links').select("original_url, clicks").eq("short_code", short_code).execute()
        
        if res.data and len(res.data) > 0:
            target = res.data[0]['original_url']
            current_clicks = res.data[0].get('clicks', 0)
            
            # 2. Click count update (Background mein)
            try:
                supabase.table('links').update({"clicks": current_clicks + 1}).eq("short_code", short_code).execute()
            except:
                pass 

            if not target.startswith(('http://', 'https://')): 
                target = 'https://' + target
            
            # 3. Direct 301 Redirect (Isse domain address bar mein show nahi hota, seedha target khulta hai)
            response = make_response(redirect(target, code=301)) 
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response.headers['Pragma'] = 'no-cache'
            return response
            
    except Exception as e:
        print(f"Error: {e}")
        
    return redirect('https://jarrylink/)

# --- HOME & SHORTEN LOGIC ---
@app.route('/')
def home():
    try:
        return render_template('architect_tool.html')
    except:
        return "JarryLabs Engine Online", 200

@app.route('/shorten', methods=['POST', 'OPTIONS'])
def shorten():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
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

# DO NOT ADD 'app = app' HERE.
