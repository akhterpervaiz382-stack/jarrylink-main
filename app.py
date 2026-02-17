import os
from flask import Flask, request, jsonify, redirect, render_template
from flask_cors import CORS
from supabase import create_client
from dotenv import load_dotenv

# 1. Environment variables load karein
load_dotenv()

# 2. Flask Initialize
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# 3. Supabase Connection
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

# --- ROUTES ---

# A. Home Route
@app.route('/')
def home():
    return jsonify({
        "status": "Architect Engine Online",
        "project": "JarryLink",
        "message": "System is healthy and connected to Mumbai Database"
    })

# B. Tool Route (Naya Page Open karne ke liye)
@app.route('/tool')
def open_tool():
    # Ensure karein architect_tool.html aapke 'templates' folder mein hai
    return render_template('architect_tool.html')

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
        supabase.table('links').insert(entry).execute()
        
        print(f"✅ New Link Created: {short_code} -> {original_url}")
        return jsonify({"status": "success", "message": "Link saved to Database!"}), 201

    except Exception as e:
        print(f"⚠️ Create Error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 400

# D. Redirect Logic
@app.route('/<short_code>')
def redirect_to_url(short_code):
    # Favicon request ko ignore karein taaki database error na aaye
    if short_code == "favicon.ico": 
        return "", 204
        
    try:
        print(f"🔍 Searching for: {short_code}")
        result = supabase.table('links').select("original_url").eq("short_code", short_code).execute()
        
        if result.data and len(result.data) > 0:
            url = result.data[0]['original_url']
            print(f"🚀 Redirecting to: {url}")
            return redirect(url)
        else:
            print("❌ Code not found.")
            return "<h1>Link Not Found!</h1><p>Check your URL at jarrylink.site</p>", 404
            
    except Exception as e:
        print(f"⚠️ Redirect Error: {str(e)}")
        return redirect("https://jarrylink.site")

# 4. Engine Start
if __name__ == '__main__':
    print("\n" + "="*30)
    print("🚀 JARRYLABS ARCHITECT IS LIVE!")
    print(f"📍 Tool URL: http://127.0.0.1:5000/tool")
    print("="*30 + "\n")
    app.run(port=5000, debug=True)