import os
from flask import Flask, request, jsonify, redirect, render_template
from flask_cors import CORS
from supabase import create_client
from dotenv import load_dotenv

# 1. Environment variables load karein
load_dotenv()

# 2. Flask Initialize
app = Flask(__name__)
# CORS setting for Vercel
CORS(app)

# 3. Supabase Connection
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

# --- ROUTES ---

# A. Home Route - Ab seedha Tool nazar aayega
@app.route('/')
def home():
    # Yeh aapke 'templates/architect_tool.html' ko load karega
    return render_template('architect_tool.html')

# B. System Status (Checking ke liye alag route)
@app.route('/status')
def status():
    return jsonify({
        "status": "Architect Engine Online",
        "project": "JarryLink",
        "message": "System is healthy"
    })

# C. Link Create Karne Ka Route
@app.route('/shorten', methods=['POST'])
def create_short_link():
    try:
        data = request.get_json()
        original_url = data.get('original_url')
        short_code = data.get('short_code')

        if not original_url or not short_code:
            return jsonify({"status": "error", "message": "Missing URL or Code"}), 400

        entry = {
            "short_code": short_code,
            "original_url": original_url,
            "clicks": 0
        }
        
        # NOTE: Agar table ka naam 'urls' hai toh niche 'links' ko 'urls' kar dein
        supabase.table('links').insert(entry).execute()
        
        return jsonify({"status": "success", "message": "Link saved!"}), 201

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

# D. Redirect Logic
@app.route('/<short_code>')
def redirect_to_url(short_code):
    if short_code in ["favicon.ico", "favicon.png", "robots.txt"]:
        return "", 204
        
    try:
        # Database se URL dhoondna
        result = supabase.table('links').select("original_url").eq("short_code", short_code).execute()
        
        if result.data and len(result.data) > 0:
            target_url = result.data[0]['original_url']
            # Protocol check (http/https)
            if not target_url.startswith(('http://', 'https://')):
                target_url = 'https://' + target_url
            return redirect(target_url)
        else:
            return "<h1>Link Not Found!</h1><p>Create it at jarrylink.site</p>", 404
            
    except Exception as e:
        return f"Error: {str(e)}", 500

# 4. Engine Start
if __name__ == '__main__':
    app.run(port=5000, debug=True)
