import os
from flask import Flask, request, jsonify, redirect, make_response
from flask_cors import CORS
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

supabase = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY"))

# --- MODERN FULL-PAGE TOOL INTERFACE ---
HTML_TOOL = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JarryLink | Professional URL Shortener & SEO Tool</title>
    
    <meta name="description" content="JarryLink is a professional, free custom URL shortener. Create branded links, track analytics, and optimize your SEO strategy with our advanced link architect.">
    <meta name="keywords" content="link shortener free online, url shortener free, custom url shortener, ai video shortener free online, sentence shortener, paragraph shortener, google url shortener free, bitly alternative, best free url shortener, url shortener with custom name, url shortener chrome extension, link shortener highest paying, free link shortener, link management, custom alias shortener, branded links, link cloaking, unstoppable links, jarrylink, url architect">
    
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap" rel="stylesheet">
    
    <style>
        :root {
            --dark-green: #064e3b;
            --mid-green: #065f46;
            --light-green: #10b981;
            --bg-dark: #020617;
        }
        body { 
            background-color: var(--bg-dark); 
            font-family: 'Plus Jakarta Sans', sans-serif;
            color: white;
            display: flex;
            flex-direction: column;
            min-height: screen;
        }
        .nav-link:hover { color: var(--light-green); }
        .footer-link:hover { color: var(--light-green); text-decoration: underline; }
        .glass-card { 
            background: rgba(255, 255, 255, 0.02); 
            backdrop-filter: blur(12px); 
            border: 1px solid rgba(255, 255, 255, 0.1); 
        }
        .btn-primary {
            background-color: white;
            color: black;
            transition: all 0.3s ease;
        }
        .btn-primary:hover {
            background-color: var(--light-green);
            transform: translateY(-2px);
        }
    </style>
</head>
<body class="flex flex-col min-h-screen">

    <header class="bg-[#064e3b] border-b border-emerald-900/50 sticky top-0 z-50">
        <nav class="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
            <div class="flex items-center space-x-2">
                <span class="text-2xl font-extrabold tracking-tighter italic text-white">Jarry<span class="text-emerald-400">Link</span></span>
            </div>
            <div class="hidden md:flex space-x-8 text-sm font-semibold uppercase tracking-widest text-emerald-100">
                <a href="/" class="nav-link transition-all">Home</a>
                <a href="#" class="nav-link transition-all text-emerald-400">Blog</a>
                <a href="#" class="nav-link transition-all">Best Tools</a>
                <a href="#" class="nav-link transition-all">About Us</a>
                <a href="#" class="nav-link transition-all">Contact</a>
            </div>
            <div class="md:hidden text-emerald-400 text-2xl">☰</div>
        </nav>
    </header>

    <main class="flex-grow flex items-center justify-center py-20 px-4 relative overflow-hidden">
        <div class="absolute top-1/4 -left-20 w-96 h-96 bg-emerald-900/20 rounded-full blur-[120px]"></div>
        <div class="absolute bottom-1/4 -right-20 w-96 h-96 bg-blue-900/10 rounded-full blur-[120px]"></div>

        <div class="max-w-4xl w-full text-center z-10">
            <h2 class="text-5xl md:text-7xl font-extrabold mb-6 tracking-tight">
                Architect Your <span class="text-emerald-400 italic">Unstoppable</span> Link
            </h2>
            <p class="text-gray-400 max-w-2xl mx-auto mb-12 text-lg">
                The most advanced branded URL shortener for creators and marketers. Fast, secure, and permanent.
            </p>

            <div class="glass-card p-2 rounded-[2.5rem] shadow-2xl max-w-3xl mx-auto">
                <div class="bg-[#050505] rounded-[2.2rem] p-6 md:p-10 space-y-6">
                    <div class="grid md:grid-cols-2 gap-6 text-left">
                        <div class="space-y-2">
                            <label class="text-[10px] uppercase tracking-[0.2em] font-black text-emerald-500 ml-2">Destination URL</label>
                            <input type="text" id="longUrl" placeholder="Paste long link here..." 
                                class="w-full bg-white/5 border border-white/10 p-4 rounded-2xl focus:border-emerald-500 outline-none transition-all">
                        </div>
                        <div class="space-y-2">
                            <label class="text-[10px] uppercase tracking-[0.2em] font-black text-emerald-500 ml-2">Custom Alias</label>
                            <div class="flex items-center bg-white/5 border border-white/10 rounded-2xl overflow-hidden focus-within:border-emerald-500">
                                <span class="pl-4 text-gray-500 font-bold italic text-sm">jarrylink/</span>
                                <input type="text" id="shortCode" placeholder="brand-name" 
                                    class="w-full bg-transparent p-4 outline-none text-white">
                            </div>
                        </div>
                    </div>
                    <button onclick="shortenLink()" id="btn" class="btn-primary w-full py-5 rounded-2xl font-black uppercase tracking-widest text-sm shadow-lg shadow-emerald-900/20">
                        Create Branded Link
                    </button>

                    <div id="result" class="hidden mt-8 p-6 bg-emerald-900/20 border border-emerald-500/30 rounded-3xl animate-pulse">
                        <p class="text-[10px] font-bold text-emerald-400 uppercase tracking-widest mb-2">Architected Successfully!</p>
                        <div class="text-2xl font-bold mb-4" id="linkSpan">jarrylink/name</div>
                        <button onclick="copyLink()" id="copyBtn" class="bg-emerald-500 text-black px-8 py-3 rounded-xl font-bold text-xs uppercase hover:bg-white transition-all">
                            Copy Link
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </main>

    <footer class="bg-[#064e3b] text-emerald-100 py-12 px-6 border-t border-emerald-800">
        <div class="max-w-7xl mx-auto">
            <div class="grid md:grid-cols-4 gap-12 mb-12">
                <div class="col-span-2">
                    <span class="text-2xl font-black italic mb-4 block text-white">JarryLink</span>
                    <p class="text-emerald-200/60 max-w-sm text-sm leading-relaxed">
                        Leading the industry in link management and SEO optimization. JarryLink provides professional tools for digital growth.
                    </p>
                </div>
                <div>
                    <h4 class="font-bold uppercase tracking-widest text-xs text-white mb-6">Legal</h4>
                    <ul class="space-y-4 text-sm text-emerald-200/80 font-medium">
                        <li><a href="#" class="footer-link">Privacy Policy</a></li>
                        <li><a href="#" class="footer-link">Terms of Service</a></li>
                        <li><a href="#" class="footer-link">Disclaimer</a></li>
                    </ul>
                </div>
                <div>
                    <h4 class="font-bold uppercase tracking-widest text-xs text-white mb-6">Company</h4>
                    <ul class="space-y-4 text-sm text-emerald-200/80 font-medium">
                        <li><a href="#" class="footer-link">About Us</a></li>
                        <li><a href="#" class="footer-link">Contact</a></li>
                        <li><a href="#" class="footer-link">JarryLabs</a></li>
                    </ul>
                </div>
            </div>
            <div class="pt-8 border-t border-emerald-800/50 text-center text-xs text-emerald-400/50 font-bold uppercase tracking-[0.3em]">
                &copy; 2026 JarryLabs Architect Engine. All Rights Reserved.
            </div>
        </div>
    </footer>

    <script>
        async function shortenLink() {
            const l_url = document.getElementById('longUrl').value;
            let s_code = document.getElementById('shortCode').value.trim();
            const btn = document.getElementById('btn');
            if(!l_url) return alert("Pehle URL dalo bhai!");
            
            btn.innerText = "PROCESSING..."; btn.disabled = true;
            try {
                const res = await fetch('/shorten', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ original_url: l_url, short_code: s_code || Math.random().toString(36).substring(7) })
                });
                if(res.ok) {
                    document.getElementById('result').classList.remove('hidden');
                    document.getElementById('linkSpan').innerText = `jarrylink/${s_code || 'link'}`;
                    btn.innerText = "CREATE ANOTHER";
                } else { alert("Alias Taken!"); }
            } catch (e) { alert("Error!"); }
            btn.disabled = false;
        }

        function copyLink() {
            const code = document.getElementById('linkSpan').innerText.split('/')[1];
            const final = "https://jarrylink.site/" + code;
            navigator.clipboard.writeText(final).then(() => {
                document.getElementById('copyBtn').innerText = "COPIED!";
                setTimeout(() => { document.getElementById('copyBtn').innerText = "COPY LINK"; }, 2000);
            });
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
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
    try:
        data = request.get_json(silent=True)
        s_code = data.get('short_code', '').strip()
        l_url = data.get('original_url', '').strip()
        if s_code and l_url:
            supabase.table('links').insert({"short_code": s_code, "original_url": l_url, "clicks": 0}).execute()
            return jsonify({"status": "success"}), 201
    except:
        pass
    return jsonify({"status": "error"}), 400

app = app
