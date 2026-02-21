import os
from flask import Flask, request, jsonify, redirect
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
# (Aapka HTML_TOOL wala sara part waisa hi rahega)
HTML_TOOL = """
<!DOCTYPE html>
<html lang="en">
... (Aapka pura HTML yahan aayega) ...
</html>
"""

# --- BACKEND ROUTES ---

@app.route('/')
def home():
    return HTML_TOOL

# YEH HAI WOH "CATCH-ALL" ROUTE JO LINKS HANDLE KARTA HAI
@app.route('/<path:path>')
def handle_all_routes(path):
    # --- 🛡️ SMART GUARD FOR SEO PAGES & BLOGGER LINKS ---
    # Agar link mein .html hai, ya wo /p/ ya /202/ se shuru ho raha hai
    if ".html" in path or path.startswith("p/") or path.startswith("20") or "/" in path:
        # In links ko database mein mat dhoondo. 
        # Kyunke ye pages Google par live hain, hum inhein wapas unke original path par bhej rahe hain
        # Taake Blogger ya Vercel static files ise handle kar sakein bina loop ke.
        return redirect(f"https://www.jarrylabs.com/{path}", code=302)

    # --- 🔗 ORIGINAL SHORT LINK LOGIC ---
    # Agar upar wali conditions match nahi hoti, tab database check karo
    short_code = path 
    if short_code in ['shorten', 'favicon.ico']: return "", 204
    
    try:
        res = supabase.table('links').select("original_url").eq("short_code", short_code).execute()
        if res.data:
            url = res.data[0]['original_url']
            return redirect(url if url.startswith('http') else 'https://'+url, code=301)
    except Exception as e:
        print(f"Error: {e}")
    
    # Agar database mein bhi nahi mila, toh home page par bhej do
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

app = app
