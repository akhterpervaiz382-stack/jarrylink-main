import os
from flask import Flask, request, jsonify, redirect, render_template
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
    return render_template('architect_tool.html')

@app.route('/status')
def status():
    return jsonify({"status": "online"})

@app.route('/shorten', methods=['POST'])
def create():
    try:
        data = request.get_json()
        s_code = data.get('short_code').strip()
        l_url = data.get('original_url').strip()
        
        # Check if exists
        check = supabase.table('links').select("*").eq("short_code", s_code).execute()
        if check.data:
            return jsonify({"status": "error", "message": "Booked!"}), 400

        supabase.table('links').insert({"short_code": s_code, "original_url": l_url, "clicks": 0}).execute()
        return jsonify({"status": "success"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

# YE HAI GAME-CHANGER ROUTE
@app.route('/<path:short_code>')
def redirect_logic(short_code):
    # Ignore static files
    if short_code in ["favicon.ico", "status", "api"]: return "", 204
    
    try:
        res = supabase.table('links').select("original_url").eq("short_code", short_code).execute()
        if res.data:
            url = res.data[0]['original_url']
            if not url.startswith(('http://', 'https://')): url = 'https://' + url
            return redirect(url)
        return f"<h1>404 - Link Not Found</h1><p>'{short_code}' is not registered.</p>", 404
    except:
        return redirect('/')

app = app
