import os
from flask import Flask, request, jsonify, redirect, render_template
from flask_cors import CORS
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder='../templates')
CORS(app)

# Supabase initialization
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

# 1. Sabse pehle redirect logic (Priority) - Is se redirection fast ho jati hai
@app.route('/<short_code>')
def redirect_logic(short_code):
    # In routes ko redirect nahi karna, ye system ke liye hain
    if short_code in ["favicon.ico", "status", "shorten", "static"]:
        return "", 204
    
    try:
        # Database se direct record uthayein
        res = supabase.table('links').select("original_url").eq("short_code", short_code).execute()
        
        if res.data and len(res.data) > 0:
            target = res.data[0]['original_url']
            if not target.startswith(('http://', 'https://')): 
                target = 'https://' + target
            
            # code=301 (Permanent Redirect) rb.gy ki tarah instant speed ke liye
            return redirect(target, code=301)
            
    except Exception:
        pass
        
    # Agar code nahi mila toh home page par bhej dein
    return redirect('/')

# 2. Home Route (Sirf tab khulega jab koi path nahi hoga)
@app.route('/')
def home():
    try:
        return render_template('architect_tool.html')
    except:
        return "Template folder error. Check your structure.", 500

@app.route('/status')
def status():
    return jsonify({"status": "online", "brand": "JarryLink"})

@app.route('/shorten', methods=['POST'])
def shorten():
    try:
        data = request.get_json()
        short_code = data.get('short_code').strip()
        original_url = data.get('original_url').strip()

        # Database Check
        check = supabase.table('links').select("*").eq("short_code", short_code).execute()
        if check.data:
            return jsonify({"status": "error", "message": "Booked!"}), 400

        # Insert
        supabase.table('links').insert({
            "short_code": short_code, 
            "original_url": original_url, 
            "clicks": 0
        }).execute()
        
        return jsonify({"status": "success"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

# Important for Vercel
app = app
