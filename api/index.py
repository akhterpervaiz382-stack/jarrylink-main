import os
from flask import Flask, request, jsonify, redirect, make_response
from flask_cors import CORS
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

supabase = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY"))

# --- FIVERR GREEN & BLACK PREMIUM INTERFACE (Clean Branding) ---
HTML_TOOL = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JarryLink | #1 Free URL Shortener & Branded Link Architect</title>
    
    <meta name="description" content="JarryLink is the ultimate bitly alternative and free url shortener with custom name. Create branded links easily.">
    <meta name="keywords" content="link shortener free online, url shortener free, custom url shortener, ai video shortener, bitly alternative, jarrylink, jarrylabs">
    
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;700;800&display=swap" rel="stylesheet">
    
    <style>
        :root { --fiverr-green: #1dbf73; --deep-black: #0a0a0a; --soft-black: #121212; --border-color: #2d2d2d; }
        body { background-color: var(--deep-black); font-family: 'Manrope', sans-serif; color: #ffffff; }
        .fiverr-bg { background-color: var(--fiverr-green); }
        .fiverr-text { color: var(--fiverr-green); }
        .nav-link:hover { color: var(--fiverr-green); }
        .glass-card { background: var(--soft-black); border: 1px solid var(--border-color); box-shadow: 0 20px 50px rgba(0,0,0,0.5); }
        input:focus { border-color: var(--fiverr-green) !important; }
        .btn-main { background-color: var(--fiverr-green); color: white; font-weight: 800; transition: all 0.3s ease; }
        .btn-main:hover { transform: scale(1.02); filter: brightness(1.1); }
        .animate-in { animation: fadeIn 0.5s ease-out forwards; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    </style>
</head>
<body class="flex flex-col min-h-screen">

    <header class="border-b border-white/5 sticky top-0 z-50 bg-black/80 backdrop-blur-md">
        <nav class="max-w-7xl mx-auto px-6 py-5 flex justify-between items-center">
            <div class="flex items-center">
                <span class="text-3xl font-extrabold tracking-tighter text-white">Jarry<span class="fiverr-text">Link.</span></span>
            </div>
            <div class="hidden md:flex space-x-10 text-[11px] font-bold uppercase tracking-[0.2em]">
                <a href="/" class="nav-link transition-all">Home</a>
                <a href="#" class="nav-link transition-all">Blog</a>
                <a href="#" class="nav-link transition-all">Best Tools</a>
                <a href="#" class="nav-link transition-all text-emerald-400">About Us</a>
                <a href="#" class="nav-link transition-all">Contact</a>
            </div>
            <div><button class="border border-white/20 px-6 py-2 rounded-full text-xs font-bold hover:bg-white hover:text-black transition-all font-black uppercase">Get Started</button></div>
        </nav>
    </header>

    <main class="flex-grow flex items-center justify-center py-20 px-4">
        <div class="max-w-5xl w-full text-center">
            <span class="fiverr-text font-bold text-xs uppercase tracking-[0.5em] mb-4 block">Professional Grade URL Architect</span>
            <h2 class="text-6xl md:text-8xl font-extrabold mb-8 tracking-tighter leading-[0.9]">
                Shorten. Brand. <br><span class="fiverr-text italic">Optimize.</span>
            </h2>
            
            <div class="glass-card p-4 rounded-[2.5rem] max-w-3xl mx-auto mt-12">
                <div class="bg-[#181818] rounded-[2.2rem] p-8 md:p-12">
                    <div class="space-y-8">
                        <div class="text-left">
                            <label class="text-[10px] uppercase tracking-widest font-bold text-gray-500 mb-3 block ml-2">Target URL</label>
                            <input type="text" id="longUrl" placeholder="https://example.com/very-long-link" 
                                class="w-full bg-black/40 border border-white/10 p-5 rounded-2xl focus:border-fiverr-green outline-none transition-all text-sm">
                        </div>
                        
                        <div class="text-left">
                            <label class="text-[10px] uppercase tracking-widest font-bold text-gray-500 mb-3 block ml-2">Custom Alias</label>
                            <div class="flex items-center bg-black/40 border border-white/10 rounded-2xl overflow-hidden">
                                <span class="pl-6 text-emerald-500 font-black italic text-sm">jarrylink/</span>
                                <input type="text" id="shortCode" placeholder="alias" 
                                    class="w-full bg-transparent p-5 outline-none text-white text-sm font-bold">
                            </div>
                        </div>

                        <button onclick="shortenLink()" id="btn" class="btn-main w-full py-5 rounded-2xl uppercase tracking-[0.2em] text-sm shadow-2xl shadow-emerald-500/10 active:scale-95">
                            Generate Link
                        </button>
                    </div>

                    <div id="result" class="hidden mt-10 p-8 border border-fiverr-green/30 bg-fiverr-green/5 rounded-3xl animate-in">
                        <p class="text-[10px] font-bold fiverr-text uppercase tracking-widest mb-3">Branded Link Ready</p>
                        <div class="text-4xl font-extrabold mb-8 tracking-tighter text-white italic" id="linkSpan">jarrylink/name</div>
                        <div class="flex gap-4">
                             <button onclick="copyLink()" id="copyBtn" class="flex-grow fiverr-bg text-white py-4 rounded-xl font-bold text-xs uppercase tracking-widest shadow-lg shadow-fiverr-green/20">Copy URL</button>
                             <button onclick="visitLink()" class="bg-white text-black px-8 rounded-xl font-bold text-xs uppercase hover:bg-fiverr-green hover:text-white transition-all">Visit</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </main>

    <footer class="bg-[#050505] border-t border-white/5 py-12 px-6">
        <div class="max-w-7xl mx-auto text-center md:text-left grid md:grid-cols-4 gap-10">
            <div class="col-span-2">
                <span class="text-2xl font-black italic text-white">JarryLink.</span>
                <p class="text-gray-500 mt-4 text-sm max-w-xs">Premium link management and SEO optimization by JarryLabs.</p>
            </div>
            <div>
                <h4 class="text-white font-bold text-xs uppercase tracking-widest mb-4">Legal</h4>
                <ul class="text-sm text-gray-500 space-y-2">
                    <li>Privacy Policy</li><li>Terms</li>
                </ul>
            </div>
            <div>
                <h4 class="text-white font-bold text-xs uppercase tracking-widest mb-4">Company</h4>
                <ul class="text-sm text-gray-500 space-y-2">
                    <li>About Us</li><li class="fiverr-text">JarryLabs.com</li>
                </ul>
            </div>
        </div>
    </footer>

    <script>
        let currentAlias = "";
        async function shortenLink() {
            const l_url = document.getElementById('longUrl').value;
            let s_code = document.getElementById('shortCode').value.trim();
            const btn = document.getElementById('btn');
            if(!l_url) return alert("Pehle URL dalo!");
            
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
                    document.getElementById('linkSpan').innerText = "jarrylink/" + currentAlias;
                    btn.innerText = "SUCCESS!";
                } else { alert("Alias Taken!"); btn.innerText = "TRY AGAIN"; }
            } catch (e) { alert("Error!"); }
            btn.disabled = false;
        }

        function copyLink() {
            const final = window.location.origin + "/" + currentAlias;
            navigator.clipboard.writeText(final).then(() => {
                document.getElementById('copyBtn').innerText = "COPIED!";
                setTimeout(() => { document.getElementById('copyBtn').innerText = "COPY URL"; }, 2000);
            });
        }
        
        function visitLink() {
            window.open(window.location.origin + "/" + currentAlias, '_blank');
        }
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
    except:
        pass
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
