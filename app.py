import os
from flask import Flask, request, jsonify, redirect, render_template
from flask_cors import CORS
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

# SMART FUNCTION: Try both 'links' and 'urls' tables
def get_table():
    tables_to_try = ['links', 'urls']
    for table in tables_to_try:
        try:
            # Sirf check karne ke liye ke table exist karti hai
            supabase.table(table).select("id").limit(1).execute()
            return table
        except:
            continue
    return 'links' # Default

@app.route('/')
def home():
    return render_template('architect_tool.html')

@app.route('/status')
def status():
    return jsonify({"status": "Architect Engine Online", "project": "JarryLink"})

@app.route('/shorten', methods=['POST'])
def create_short_link():
    try:
        data = request.get_json()
        original_url = data.get('original_url')
        short_code = data.get('short_code')
        
        target_table = get_table()
        entry = {"short_code": short_code, "original_url": original_url, "clicks": 0}
        
        supabase.table(target_table).insert(entry).execute()
        return jsonify({"status": "success", "message": f"Saved in {target_table}"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/<short_code>')
def redirect_to_url(short_code):
    if short_code in ["favicon.ico", "robots.txt", "status"]:
        return "", 204
    try:
        target_table = get_table()
        result = supabase.table(target_table).select("original_url").eq("short_code", short_code).execute()
        
        if result.data:
            url = result.data[0]['original_url']
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            return redirect(url)
        return "<h1>Link Not Found</h1>", 404
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
