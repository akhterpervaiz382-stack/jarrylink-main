import os
from flask import Flask, request, jsonify, redirect, render_template_string
from flask_cors import CORS
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Database Connection
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")
supabase = create_client(supabase_url, supabase_key)

# --- JARRYLABS SEO OPTIMIZED INTERFACE ---
HTML_TOOL = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JarryLabs | Best Free URL Shortener & Custom Link Generator</title>
    <meta name="description" content="Use JarryLabs for free online link shortening with custom names. The best Bitly alternative for AI video and paragraph shorteners.">
    <style>
        body { font-family: 'Inter', sans-serif; background: #0f172a; color: white; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
        .container { background: #1e293b; padding: 2.5rem; border-radius: 20px; box-shadow: 0 20px 50px rgba(0,0,0,0.5); text-align: center; width: 100%; max-width: 450px; border: 1px solid #334155; }
        h1 { color: #38bdf8; font-size: 2.5rem; margin-bottom: 10px; }
        p { color: #94a3b8; margin-bottom: 2rem; }
        input { width: 100%; padding: 15px; border-radius: 10px; border: 1px solid #334155; background: #0f172a; color: white; margin-bottom: 1rem; box-sizing: border-box; font-size: 1rem; }
        button { width: 100%; padding: 15px; border-radius: 10px; border: none; background: linear-gradient(90deg, #38bdf8, #818cf8); color: white; font-weight: bold; cursor: pointer; transition: 0.3s; font-size: 1.1rem; }
        button:hover { transform: scale(1.02); opacity: 0.9; }
        .footer-text { margin-top: 2rem; font-size: 0.8rem; color: #475569; }
    </style>
</head>
<body>
    <div class="container">
        <h1>JarryLabs 🚀</h1>
        <p>Shorten, Track, and Grow your Traffic</p>
        <input type="text" id="longUrl" placeholder="Paste your long URL here..." required>
        <input type="text" id="customCode" placeholder="Custom name (optional)">
        <button onclick="shortenLink()">Shorten URL</button>
        <div id="result" style="margin-top: 20px; font-weight: bold; color: #38bdf8;"></div>
        <p class="footer-text">The best free custom url shortener for 2026</p>
    </div>
    <script>
        async function shortenLink() {
            const url = document.getElementById('longUrl').value;
            const code = document.getElementById('customCode').value || Math.random().toString(36).substring(7);
            const res = await fetch('/shorten', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({original_url: url, short_code: code})
            });
            if(res.ok) {
                document.getElementById('result').innerHTML = `Your link: jarrylabs.com/${code}`;
            } else {
                document.getElementById('result').innerHTML = "Error creating link.";
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TOOL)

@app.route('/<path:path>')
def handle_all_routes(path):
    if ".html" in path or path.startswith("p/") or path.startswith("20") or "/" in path:
        return redirect(f"https://www.jarrylabs.com/{path}", code=302)

    short_code = path 
    if short_code in ['shorten', 'favicon.ico']: return "", 204
    
    try:
        res = supabase.table('links').select("original_url").eq("short_code", short_code).execute()
        if res.data:
            url = res.data[0]['original_url']
            return redirect(url if url.startswith('http') else 'https://'+url, code=301)
    except Exception as e:
        print(f"Error: {e}")
    
    return redirect('/')

@app.route('/shorten', methods=['POST'])
def shorten():
    data = request.json
    try:
        supabase.table('links').insert({
            "short_code": data['short_code'], 
            "original_url": data['original_url']
        }).execute()
        return jsonify({"status": "success"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

# Vercel requirements
app = app
