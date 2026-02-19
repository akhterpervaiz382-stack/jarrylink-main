import os
from flask import Flask, request, jsonify, make_response, render_template, redirect
from flask_cors import CORS
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder='../templates')
CORS(app)

# Supabase Connection
supabase = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY"))

@app.route('/')
def home():
    try:
        return render_template('architect_tool.html')
    except:
        return "JarryLink Engine Online & Ready", 200

@app.route('/<short_code>')
def redirect_logic(short_code):
    if short_code in ["favicon.ico", "status", "shorten", "static"]:
        return "", 204
    
    try:
        # Link fetch karna
        res = supabase.table('links').select("original_url").eq("short_code", short_code).execute()
        
        if res.data and len(res.data) > 0:
            target = res.data[0]['original_url']
            if not target.startswith(('http://', 'https://')):
                target = 'https://' + target
            
            # FAST 301 REDIRECT
            response = make_response(redirect(target, code=301))
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            return response
    except Exception as e:
        print(f"Error: {e}")
    
    return redirect('/')

@app.route('/shorten', methods=['POST', 'OPTIONS'])
def shorten():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
    try:
        data = request.get_json(silent=True)
        s_code = data.get('short_code', '').strip()
        l_url = data.get('original_url', '').strip()

        if s_code and l_url:
            supabase.table('links').insert({"short_code": s_code, "original_url": l_url, "clicks": 0}).execute()
            return jsonify({"status": "success"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"status": "failed"}), 400

app = app
