import os
from flask import Flask, request, jsonify, redirect, make_response
from flask_cors import CORS
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
# JarryLabs.com se requests allow karne ke liye CORS setup
CORS(app, resources={r"/*": {"origins": ["https://jarrylabs.com", "http://localhost:3000"]}})

supabase = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY"))

# --- JARRYLABS PREMIUM INTERFACE ---
HTML_TOOL = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JarryLabs | Professional URL Shortener & SEO Architect</title>
    
    <meta name="description" content="JarryLabs provides the best free custom url shortener. Create branded links, ai video shortener links, and optimize your SEO strategy with our advanced link architect.">
    <meta name="keywords" content="link shortener free online, url shortener free, custom url shortener, ai video shortener free online, sentence shortener, paragraph shortener, google url shortener free, bitly alternative, best free url shortener, url shortener with custom name, jarrylabs, link management">
    
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;700;800&display=swap" rel="stylesheet">
    
    <style>
        :root { --fiverr-green: #1dbf73; --deep-black: #0a0a0a; --soft-black: #121212; }
        body { background-color: var(--deep-black); font-family: 'Manrope', sans-serif; color: white; }
        .fiverr-text { color: var(--fiverr-green); }
        .fiverr-bg { background-color: var(--fiverr-green); }
        .glass-card { background: var(--soft-black); border: 1px solid #2d2d2d; box-shadow: 0 20px 50px rgba(0,0,0,0.5); }
        .btn-main { background-color: var(--fiverr-green); color: white; font-weight: 800; transition: all 0.3s ease; }
        .btn-main:hover { transform: scale(1.02); filter: brightness(1.1); }
    </style>
</head>
<body class="flex flex-col min-h-screen">

    <header class="border-b border-white/5 sticky top-0 z-50 bg-black/80 backdrop-blur-md">
        <nav class="max-w-7xl mx-auto px-6 py-5 flex justify-between items-center">
            <span class="text-3xl font-extrabold tracking-tighter">Jarry<span class="fiverr-text">Labs.</span></span>
            <div class="hidden md:flex space-x-10 text-[11px] font-bold uppercase tracking-[0.2em]">
                <a href="#" class="hover:text-[#1dbf73]">Tools</a>
                <a href="#" class="hover:text-[#1dbf73]">SEO Strategy</a>
                <a href="#" class="hover:text-[#1dbf73]">Fiverr Services</a>
            </div>
        </nav>
    </header>

    <main class="flex-grow flex items-center justify-center py-20 px-4">
        <div class="max-w-4xl w-full text-center">
            <h1 class="text-6xl md:text-8xl font-extrabold mb-8 tracking-tighter">
                Architect Your <br><span class="fiverr-text italic">Unstoppable</span> Link
            </h1>
            
            <div class="glass-card p-4 rounded-[2.5rem] max-w-3xl mx-auto">
                <div class="bg-[#181818] rounded-[2.2rem] p-8 md:p-12 space-y-8">
                    <div class="text-left space-y-6">
                        <div>
                            <label class="text-[10px] uppercase tracking-widest font-bold text-gray-500 ml-2">Destination URL</label>
                            <input type="text" id="longUrl" placeholder="https://..." class="w-full bg-black/40 border border-white/10 p-5 rounded-2xl focus:border-fiverr-green outline-none transition-all text-sm">
                        </div>
                        <div>
                            <label class="text-[10px] uppercase tracking-widest font-bold text-gray-500 ml-2">Branded Alias</label>
                            <div class="flex items-center bg-black/40 border border-white/10 rounded-2xl overflow-hidden focus-within:border-fiverr-green">
                                <span class="pl-6 fiverr-text font-black italic">jarrylabs/</span>
                                <input type="text" id="shortCode" placeholder="alias" class="w-full bg-transparent p-5 outline-none text-white font-bold">
                            </div>
                        </div>
                    </div>

                    <button onclick="shortenLink()" id="btn" class="btn-main w-full py-5 rounded-2xl uppercase tracking-widest text-sm shadow-xl shadow-emerald-500/10">
                        Generate Branded Link
                    </button>

                    <div id="result" class="hidden mt-10 p-8 border border-fiverr-green/30 bg-fiverr-green/5 rounded-3xl animate-pulse">
                        <p class="text-[10px] font-bold fiverr-text uppercase tracking-widest mb-3">Architected Successfully!</p>
                        <div class="text-4xl font-extrabold mb-8 italic" id="linkSpan">jarry/name</div>
                        <div class="flex gap-4">
                             <button onclick="copyLink()" id="copyBtn" class="flex-grow fiverr-bg text-white py-4 rounded-xl font-bold text-xs uppercase tracking-widest">Copy URL</button>
                             <button onclick="visitLink()" class="bg-white text-black px-8 rounded-xl font-bold text-xs uppercase">Visit</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </main>
    
    <script>
        let currentAlias = "";
        async function shortenLink() {
            const l_url = document.getElementById('longUrl').value;
            let s_code = document.getElementById('shortCode').value.trim();
            const btn = document.getElementById('btn');
            if(!l_url) return alert("Pehle URL dalo bhai!");
            
            btn.innerText = "ARCHITECTING..."; btn.disabled = true;
            currentAlias = s_code || Math.random().toString(36).substring(7);
            
            try {
                const res = await fetch('/shorten', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ original_url: l_url, short_code: currentAlias })
                });
                if(res.ok) {
                    document.getElementById('result').classList.remove('hidden');
                    document.getElementById('linkSpan').innerText = "jarrylabs/" + currentAlias;
                    btn.innerText = "SUCCESS!";
                } else { alert("Alias Taken!"); btn.innerText = "TRY AGAIN"; }
            } catch (e) { alert("Error!"); }
            btn.disabled = false;
        }

        function copyLink() {
            // Screen par jarrylabs dikhayega par copy asli domain (jarrylink.site) karega
            const final = window.location.origin + "/" + currentAlias;
            navigator.clipboard.writeText(final).then(() => {
                document.getElementById('copyBtn').innerText = "COPIED!";
                setTimeout(() => { document.getElementById('copyBtn').innerText = "COPY URL"; }, 2000);
            });
        }
        function visitLink() { window.open(window.location.origin + "/" + currentAlias, '_blank'); }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return HTML_TOOL

@app.route('/<short_code>')
def redirect_logic(short_code):
    if short_code in ["favicon.ico", "status", "shorten", "static"]:
        return "", 204
    try:
        res = supabase.table('links').select("original_url").eq("short_code", short_code).execute()
        if res.data and len(res.data) > 0:
            target = res.data[0]['original_url']
            if not target.startswith(('http://', 'https://')):
                target = 'https://' + target
            return redirect(target, code=301)
    except: pass
    return redirect('/')

@app.route('/shorten', methods=['POST', 'OPTIONS'])
def shorten():
    if request.method == 'OPTIONS': return jsonify({"status": "ok"}), 200
    try:
        data = request.get_json(silent=True)
        s_code = data.get('short_code', '').strip()
        l_url = data.get('original_url', '').strip()
        if s_code and l_url:
            supabase.table('links').insert({"short_code": s_code, "original_url": l_url, "clicks": 0}).execute()
            return jsonify({"status": "success"}), 201
    except: pass
    return jsonify({"status": "error"}), 400

app = app
