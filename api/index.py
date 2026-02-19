import os
from flask import Flask, request, jsonify, make_response, redirect
from flask_cors import CORS
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# CORS: Tameez se Blogger aur Custom Domain allow kiye hain
CORS(app, resources={r"/*": {
    "origins": ["https://jarrylink.blogspot.com", "https://jarrylink.site"],
    "methods": ["GET", "POST", "OPTIONS"],
    "allow_headers": ["Content-Type", "Accept"]
}})

supabase = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY"))

@app.route('/<short_code>')
def redirect_logic(short_code):
    if short_code in ["favicon.ico", "status", "shorten", "static"]:
        return "", 204
    
    try:
        res = supabase.table('links').select("original_url").eq("short_code", short_code).execute()
        
        if res.data and len(res.data) > 0:
            target = res.data[0]['original_url']
            if not target.startswith(('http://', 'https://')):
                target = 'https://' + target
            
            # FAST REDIRECT: 301 Use kiya hai taake domain hide ho jaye
            response = make_response(redirect(target, code=301))
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            return response
    except Exception as e:
        print(f"Error: {e}")
    
    return redirect('https://jarrylink.site')

@app.route('/shorten', methods=['POST', 'OPTIONS'])
def shorten():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
    try:
        data = request.get_json(silent=True)
        s_code = data.get('short_code', '').strip()
        l_url = data.get('original_url', '').strip()
        
        if not s_code or not l_url:
            return jsonify({"error": "Missing data"}), 400

        supabase.table('links').insert({"short_code": s_code, "original_url": l_url, "clicks": 0}).execute()
        return jsonify({"status": "success"}), 201
    except:
        return jsonify({"error": "Conflict or DB Error"}), 400
