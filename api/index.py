import os
from flask import Flask, request, jsonify, redirect, render_template
from flask_cors import CORS
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder='../templates')
CORS(app, resources={r"/*": {"origins": "*"}})

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

@app.route('/')
def home():
    try:
        return render_template('architect_tool.html')
    except Exception as e:
        return jsonify({"error": "Template not found"}), 500

@app.route('/status')
def status():
    return jsonify({
        "status": "Architect Engine Online",
        "project": "JarryLink"
    })

@app.route('/shorten', methods=['POST'])
def create_short_link():
    try:
        data = request.get_json()
        original_url = data.get('original_url')
        short_code = data.get('short_code')

        check = supabase.table('links').select("short_code").eq("short_code", short_code).execute()
        if check.data and len(check.data) > 0:
            return jsonify({"status": "error", "message": "Booked!"}), 400

        entry = {"short_code": short_code, "original_url": original_url, "clicks": 0}
        supabase.table('links').insert(entry).execute()
        return jsonify({"status": "success"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/<short_code>')
def redirect_to_url(short_code):
    if short_code in ["favicon.ico", "status"]: 
        return "", 204
    try:
        result = supabase.table('links').select("original_url").eq("short_code", short_code).execute()
        if result.data:
            url = result.data[0]['original_url']
            if not url.startswith(('http://', 'https://')): url = 'https://' + url
            return redirect(url)
        return "Link Not Found", 404
    except:
        return redirect("/")

app = app
