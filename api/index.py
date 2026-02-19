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
    # Bekar files ko foran ignore karein
    if short_code in ["favicon.ico", "status", "shorten", "static"]:
        return "", 204
    
    try:
        # STEP 1: Sirf URL fetch karein (Clicks update yahan se hata diya taake delay na ho)
        res = supabase.table('links').select("original_url").eq("short_code", short_code).execute()
        
        if res.data and len(res.data) > 0:
            target = res.data[0]['original_url']
            
            if not target.startswith(('http://', 'https://')): 
                target = 'https://' + target
            
            # STEP 2: 301 Permanent Redirect (Sabse fastest tareeqa)
            # 301 browser ko kehta hai ke is domain ko bhool jao aur foran target par jao
            response = make_response(redirect(target, code=301))
            
            # Ye headers browser ko majboor karte hain ke domain ko hide kar de
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            return response
            
    except Exception:
        pass
        
    # Agar link na mile to jarrylink/ par wapsi
    return redirect('https://jarrylink.site', code=302)

@app.route('/shorten', methods=['POST', 'OPTIONS'])
def shorten():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
    try:
        data = request.get_json(silent=True)
        s_code = data.get('short_code', '').strip()
        l_url = data.get('original_url', '').strip()

        if s_code and l_url:
            supabase.table('links').insert({
                "short_code": s_code, "original_url": l_url, "clicks": 0
            }).execute()
            return jsonify({"status": "success"}), 201
    except:
        pass
    return jsonify({"status": "error"}), 400
