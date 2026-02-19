import os
from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
# JarryLabs.com aur jarrylink.site dono ke liye CORS setup
CORS(app, resources={r"/*": {"origins": ["https://jarrylabs.com", "https://jarrylink.site", "http://localhost:3000"]}})

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
    <title>Free Branded URL Shortener & Custom Link Generator | JarryLabs</title>
    <meta name="description" content="Create free branded short links with JarryLabs. The best URL shortener for custom, trackable links and AI video URLs. Fast, secure, and unstoppable.">
    <meta name="robots" content="index, follow, noarchive">
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; }
        .icon-wrapper svg { animation: float 3s ease-in-out infinite; }
        @keyframes float {
            0% { transform: translateY(0px) rotate(-5deg); }
            50% { transform: translateY(-10px) rotate(5deg); }
            100% { transform: translateY(0px) rotate(-5deg); }
        }
        .fiverr-green { color: #1dbf73; }
        .fiverr-bg { background-color: #1dbf73; }
    </style>
</head>
<body class="bg-gray-50 text-gray-800">

<div id="jarrylabs-tool-section" class="max-w-4xl mx-auto px-6 py-20">
    
    <div class="text-center mb-12">
        <div class="icon-wrapper flex justify-center mb-6">
            <svg width="70" height="70" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="filter: drop-shadow(0px 4px 10px rgba(29, 191, 115, 0.2));">
                <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71" stroke="#1dbf73" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71" stroke="#1dbf73" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </div>
        <h1 class="text-4xl md:text-5xl font-black text-gray-900 mb-4 tracking-tighter uppercase">
            FREE&nbsp; <span class="fiverr-green">BRANDED URL SHORTENER</span> &nbsp;& CUSTOM LINK GENERATOR
        </h1>
        <p class="text-lg text-gray-600 max-w-2xl mx-auto">The best <b>bitly alternative</b> for professional, trackable, and high-authority short links.</p>
    </div>

    <div class="bg-white shadow-2xl rounded-3xl p-8 md:p-12 border border-gray-100">
        <div class="space-y-6">
            <div>
                <label class="block text-[10px] font-black text-gray-400 uppercase tracking-[0.2em] mb-2">Paste Long URL</label>
                <input type="text" id="longUrl" placeholder="https://example.com/very-long-link..." class="w-full bg-gray-50 border border-gray-200 p-5 rounded-2xl outline-none focus:border-[#1dbf73] transition-all">
            </div>

            <div>
                <label class="block text-[10px] font-black text-gray-400 uppercase tracking-[0.2em] mb-2">Custom Branded Alias (Optional)</label>
                <div class="flex items-center bg-gray-50 border border-gray-200 rounded-2xl overflow-hidden focus-within:border-[#1dbf73]">
                    <span class="pl-5 text-gray-400 font-bold">jarrylink.site/</span>
                    <input type="text" id="shortCode" placeholder="my-brand" class="w-full bg-transparent p-5 outline-none font-bold text-gray-700">
                </div>
            </div>

            <button onclick="generateLink()" id="genBtn" class="w-full fiverr-bg text-white font-black py-5 rounded-2xl uppercase tracking-widest hover:brightness-110 transition-all shadow-lg shadow-emerald-500/20">
                Shorten Link Now
            </button>
        </div>

        <div id="resultSection" class="hidden mt-10 pt-10 border-t border-gray-100">
            <label class="block text-[10px] font-black text-gray-400 uppercase tracking-[0.2em] mb-2">Your Branded Link</label>
            <div class="flex flex-col md:flex-row gap-4">
                <input type="text" id="shortUrlDisplay" readonly class="flex-grow bg-emerald-50 text-[#1dbf73] font-black p-5 rounded-2xl outline-none border border-emerald-100">
                <button onclick="copyLink()" id="copyBtn" class="bg-gray-900 text-white px-10 py-5 rounded-2xl font-black uppercase text-xs tracking-widest hover:bg-black transition-all">Copy</button>
            </div>
        </div>
    </div>
</div>

<script>
    let lastGenerated = "";
    async function generateLink() {
        const url = document.getElementById('longUrl').value;
        let code = document.getElementById('shortCode').value.trim();
        const btn = document.getElementById('genBtn');
        if(!url) return alert("Please enter a URL!");
        
        btn.innerText = "Processing..."; btn.disabled = true;
        if(!code) code = Math.random().toString(36).substring(7);

        try {
            const res = await fetch('/shorten', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ original_url: url, short_code: code })
            });
            if(res.ok) {
                lastGenerated = window.location.origin + "/" + code;
                document.getElementById('shortUrlDisplay').value = lastGenerated;
                document.getElementById('resultSection').classList.remove('hidden');
                btn.innerText = "Success!";
            } else {
                alert("This Alias is already taken! Try another.");
                btn.innerText = "Shorten Link Now";
            }
        } catch (e) {
            alert("Connection failed! Backend is not responding.");
            btn.innerText = "Shorten Link Now";
        }
        btn.disabled = false;
    }

    function copyLink() {
        navigator.clipboard.writeText(lastGenerated);
        const cpBtn = document.getElementById('copyBtn');
        cpBtn.innerText = "Done!";
        setTimeout(() => { cpBtn.innerText = "Copy"; }, 2000);
    }
</script>
</body>
</html>
"""

# --- BACKEND ROUTES ---

@app.route('/')
def home():
    return HTML_TOOL

@app.route('/<short_code>')
def redirect_to_url(short_code):
    if short_code in ['shorten', 'favicon.ico']: return "", 204
    try:
        res = supabase.table('links').select("original_url").eq("short_code", short_code).execute()
        if res.data:
            url = res.data[0]['original_url']
            return redirect(url if url.startswith('http') else 'https://'+url, code=301)
    except: pass
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
    except:
        return jsonify({"status": "error", "message": "Alias exists"}), 400

app = app
