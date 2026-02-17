import os
from flask import Flask, request, jsonify, redirect, render_template
from flask_cors import CORS
from supabase import create_client
from dotenv import load_dotenv

# 1. Environment variables load karein
load_dotenv()

# 2. Flask Initialize (Vercel ke liye template folder ka path set kiya hai)
app = Flask(__name__, template_folder='../templates')
CORS(app, resources={r"/*": {"origins": "*"}})

# 3. Supabase Connection
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

# --- ROUTES ---

# A. Home Route (Ab ye seedha Tool dikhayega)
@app.route('/')
def home():
    try:
        return render_template('architect_tool.html')
    except Exception as e:
        return jsonify({"error": "Template not found", "details": str(e)}), 500

# B. Status Route (Dot Green karne ke liye)
@app.route('/status')
def status():
    return jsonify({
        "status": "Architect Engine Online",
        "project": "JarryLink",
        "message": "Connected to Supabase"
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

        # Smart Check: Try 'links' table (agar 'urls' table hai toh yahan badal dein)
        entry = {
            "short_code": short_code,
            "original_url": original_url,
            "clicks": 0
        }
        supabase.table('links').insert(entry).execute()
        
        return jsonify({"status": "success", "message": "Link saved!"}), 201

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

# D. Redirect Logic
@app.route('/<short_code>')
def redirect_to_url(short_code):
    if short_code in ["favicon.ico", "status", "tool"]: 
        return "", 204
        
    try:
        result = supabase.table('links').select("original_url").eq("short_code", short_code).execute()
        
        if result.data and len(result.data) > 0:
            target_url = result.data[0]['original_url']
            if not target_url.startswith(('http://', 'https://')):
                target_url = 'https://' + target_url
            return redirect(target_url)
        else:
            return f"<h1>Link Not Found!</h1><p>No link for '{short_code}' found on JarryLink.</p>", 404
            
    except Exception as e:
        return redirect("/")

# 4. Vercel ke liye 'app' export karna zaroori hai
app = app

if __name__ == '__main__':
    app.run(port=5000, debug=True)
