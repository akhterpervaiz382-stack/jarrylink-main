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

# --- SITEMAP ROUTE (Added to fix Google Search Console Error) ---
@app.route('/sitemap.xml')
def sitemap():
    xml = """<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
      <url><loc>https://jarrylink.site/</loc><lastmod>2026-03-03</lastmod><priority>1.0</priority></url>
      <url><loc>https://jarrylink.site/privacy</loc><lastmod>2026-03-03</lastmod><priority>0.5</priority></url>
      <url><loc>https://jarrylink.site/terms</loc><lastmod>2026-03-03</lastmod><priority>0.5</priority></url>
    </urlset>"""
    return xml, 200, {'Content-Type': 'application/xml'}

# --- BASE HTML TEMPLATE ---
def base_template(content, title="JarryLink"):
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Best Free URL Shortener & Custom Branded Short Links</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
        body {{ font-family: 'Plus Jakarta Sans', sans-serif; background-color: #ffffff; color: #1e293b; }}
        .text-gradient {{ background: linear-gradient(90deg, #059669, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .prose {{ max-width: 65ch; color: #475569; }}
        .prose h1 {{ font-size: 2.25rem; font-weight: 800; color: #0f172a; margin-bottom: 1rem; }}
        .prose h2 {{ font-size: 1.5rem; font-weight: 700; color: #0f172a; margin-top: 2rem; margin-bottom: 1rem; }}
        .prose p {{ margin-bottom: 1rem; line-height: 1.75; }}
        .prose ul {{ list-style-type: disc; margin-left: 1.5rem; margin-bottom: 1rem; }}
        .prose li {{ margin-bottom: 0.5rem; }}
    </style>
</head>
<body class="bg-slate-50">
    <nav class="bg-white py-4 px-6 flex justify-between items-center border-b border-slate-100 sticky top-0 z-50">
        <a href="/" class="text-2xl font-extrabold tracking-tighter text-gradient">JarryLink 🚀</a>
        <a href="https://jarrylabs.com" class="text-xs font-bold bg-slate-900 text-white px-6 py-2.5 rounded-full hover:bg-emerald-600 transition">JARRYLABS</a>
    </nav>
    <main class="py-16 px-6">
        <div class="max-w-4xl mx-auto bg-white p-10 md:p-16 rounded-[2.5rem] border border-slate-100 shadow-sm">
            {content}
        </div>
    </main>
    <footer class="py-12 border-t border-slate-200 bg-white px-6 mt-10">
        <div class="max-w-6xl mx-auto flex flex-col md:flex-row justify-between items-center">
            <div class="mb-4 md:mb-0 text-left">
                <div class="text-xl font-extrabold text-gradient">JarryLink 🚀</div>
                <p class="text-xs text-slate-500 mt-2">© 2026 JarryLabs. All rights reserved.</p>
            </div>
            <div class="flex space-x-6 text-xs font-bold uppercase tracking-widest text-slate-400">
                <a href="https://jarrylabs.com" class="hover:text-emerald-600">Main Site</a>
                <a href="/privacy" class="hover:text-emerald-600">Privacy</a>
                <a href="/terms" class="hover:text-emerald-600">Terms</a>
            </div>
        </div>
    </footer>
</body>
</html>
    """

# --- PAGE CONTENTS ---
PRIVACY_CONTENT = """
<div class="prose">
    <h1>Privacy Policy</h1>
    <p>Last updated: March 3, 2026</p>
    <p>At JarryLink, one of our main priorities is the privacy of our visitors.</p>
    <h2>Information We Collect</h2>
    <p>When you use our URL shortener, we collect the original URL and the custom alias.</p>
</div>
"""

TERMS_CONTENT = """
<div class="prose">
    <h1>Terms of Service</h1>
    <p>Last updated: March 3, 2026</p>
    <p>By accessing this website, we assume you accept these terms of service.</p>
</div>
"""

# --- HOME PAGE HTML (Unaltered) ---
HTML_TOOL = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JarryLink | Best Free URL Shortener & Custom Branded Short Links</title>
    <meta name="description" content="JarryLink is the best free URL shortener with custom names.">
    <meta name="keywords" content="link shortener free online, url shortener free, custom url shortener, ai video shortener free online, sentence shortener, paragraph shortener, google url shortener free, bitly alternative, best free url shortener, url shortener with custom name, url shortener chrome extension, link shortener highest paying">
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
        body { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #ffffff; color: #1e293b; scroll-behavior: smooth; }
        .hero-gradient { background: radial-gradient(circle at 50% -20%, #f0fdf4 0%, #ffffff 50%); }
        .tool-card { background: #ffffff; border: 2px solid #e2e8f0; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.05); }
        .text-gradient { background: linear-gradient(90deg, #059669, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .btn-primary { background: linear-gradient(90deg, #10b981, #059669); color: white; transition: 0.3s; }
        .btn-primary:hover { transform: translateY(-2px); box-shadow: 0 10px 20px rgba(16, 185, 129, 0.2); }
    </style>
</head>
<body class="hero-gradient">
    <nav class="fixed top-0 w-full z-50 bg-white/90 backdrop-blur-sm py-4 px-6 flex justify-between items-center border-b border-slate-100">
        <div class="text-2xl font-extrabold tracking-tighter text-gradient">JarryLink 🚀</div>
        <a href="https://jarrylabs.com" class="text-xs font-bold bg-slate-900 text-white px-6 py-2.5 rounded-full hover:bg-emerald-600 transition">JARRYLABS</a>
    </nav>
    <header class="pt-40 pb-20 px-6 text-center">
        <h1 class="text-5xl md:text-7xl font-extrabold mb-6 tracking-tight text-slate-900 leading-tight">Shorten Links. <span class="text-gradient">Grow Authority.</span></h1>
    </header>
    <section id="tool" class="py-10 px-6">
        <div class="max-w-5xl mx-auto text-center">
            <div class="tool-card p-10 rounded-[2.5rem]">
                <input type="text" id="longUrl" placeholder="https://example.com" class="w-full p-4 mb-4 bg-slate-50 rounded-xl">
                <input type="text" id="shortCode" placeholder="custom-alias" class="w-full p-4 mb-4 bg-slate-50 rounded-xl">
                <button onclick="shortenLink()" id="btn" class="w-full py-4 btn-primary rounded-xl font-bold">Shorten</button>
                <div id="result" class="mt-8 hidden p-6 bg-emerald-50 rounded-2xl">
                    <div id="linkSpan" class="text-2xl font-bold mb-4"></div>
                    <button onclick="copyLink()" id="copyBtn" class="bg-black text-white px-8 py-2 rounded-lg">Copy</button>
                </div>
            </div>
        </div>
    </section>
    <script>
        async function shortenLink() {
            const url = document.getElementById('longUrl').value;
            let code = document.getElementById('shortCode').value.trim();
            if(!url) return alert("URL please!");
            const res = await fetch('/shorten', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({original_url: url, short_code: code})
            });
            if(res.ok) {
                document.getElementById('result').classList.remove('hidden');
                document.getElementById('linkSpan').innerText = `jarrylink/${code}`;
            }
        }
        function copyLink() {
            const code = document.getElementById('linkSpan').innerText.split('/')[1];
            navigator.clipboard.writeText("https://jarrylink.site/" + code);
        }
    </script>
</body>
</html>
"""

# --- ROUTES ---
@app.route('/')
def home():
    return render_template_string(HTML_TOOL)

@app.route('/privacy')
def privacy():
    return render_template_string(base_template(PRIVACY_CONTENT, title="Privacy Policy"))

@app.route('/terms')
def terms():
    return render_template_string(base_template(TERMS_CONTENT, title="Terms of Service"))

@app.route('/<path:path>')
def handle_all_routes(path):
    if ".html" in path or path.startswith("p/") or path.startswith("20") or "/" in path:
        return redirect(f"https://www.jarrylabs.com/{path}", code=302)
    
    short_code = path 
    if short_code in ['shorten', 'favicon.ico', 'sitemap.xml']: 
        if short_code == 'sitemap.xml': return sitemap()
        return "", 204
    
    try:
        res = supabase.table('links').select("original_url").eq("short_code", short_code).execute()
        if res.data:
            url = res.data[0]['original_url']
            target = url if url.startswith('http') else 'https://'+url
            return redirect(target, code=301)
    except: pass
    return redirect('/')

@app.route('/shorten', methods=['POST'])
def shorten():
    data = request.json
    try:
        supabase.table('links').insert({"short_code": data['short_code'], "original_url": data['original_url']}).execute()
        return jsonify({"status": "success"}), 201
    except:
        return jsonify({"status": "error"}), 400

if __name__ == "__main__":
    app.run(debug=True)
