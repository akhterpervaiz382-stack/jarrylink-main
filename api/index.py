import os
from flask import Flask, request, jsonify, make_response, render_template, redirect
from flask_cors import CORS
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder='../templates')
CORS(app)

supabase = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY"))

@app.route('/shorten', methods=['POST'])
def shorten():
    try:
        # JSON aur Form dono ko handle karne ke liye logic
        data = request.get_json(silent=True) or request.form
        
        if not data:
            return jsonify({"status": "error", "message": "No data received"}), 400

        s_code = data.get('short_code', '').strip()
        l_url = data.get('original_url', '').strip()

        if not s_code or not l_url:
            return jsonify({"status": "error", "message": "Missing fields"}), 400

        # Database insertion
        supabase.table('links').insert({
            "short_code": s_code, 
            "original_url": l_url, 
            "clicks": 0
        }).execute()
        
        return jsonify({"status": "success"}), 201
    except Exception as e:
        # Asli error janne ke liye (Logs mein nazar ayega)
        print(f"Supabase Error: {str(e)}")
        return jsonify({"status": "error", "reason": str(e)}), 400
