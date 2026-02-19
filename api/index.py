import os
from flask import Flask, request, jsonify, make_response, redirect
from flask_cors import CORS
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

supabase = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY"))

@app.route('/<short_code>')
def redirect_logic(short_code):
    if short_code in ["favicon.ico", "status", "shorten", "static"]:
        return "", 204
    
    try:
        # STEP 1: Sirf URL fetch karein (Counter ko ignore karein speed ke liye)
        res = supabase.table('links').select("original_url").eq("short_code", short_code).execute()
        
        if res.data and len(res.data) > 0:
            target = res.data[0]['original_url']
            
            if not target.startswith(('http://', 'https://')): 
                target = 'https://' + target

            # STEP 2: Direct 301 Redirect (Bina headers ke delay ke)
            # 301 browser ko kehta hai "Ye site nahi hai, seedha agay jao"
            return redirect(target, code=301)
            
    except Exception:
        pass
        
    return redirect('https://jarrylink.site')

@app.route('/')
def home():
    # Direct text return karein taake render_template ka delay na aaye
    return "JarryLabs Engine Online", 200

@app.route('/shorten', methods=['POST', 'OPTIONS'])
def shorten():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
    try:
        data = request.get_json(silent=True) or request.form
        s_code = data.get('short_code', '').strip()
        l_url = data.get('original_url', '').strip()
        if s_code and l_url:
            supabase.table('links').insert({"short_code": s_code, "original_url": l_url, "clicks": 0}).execute()
            return jsonify({"status": "success"}), 201
    except:
        pass
    return jsonify({"status": "error"}), 400

# VERCEL REQUIREMENT: Ye line lazmi hai
app = app
