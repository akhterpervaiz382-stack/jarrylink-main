import os
from flask import Flask, request, jsonify, redirect, render_template_string
from flask_cors import CORS
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Database Connection (Logic intact)
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")
supabase = create_client(supabase_url, supabase_key)

# --- JARRYLABS CLEAN PROFESSIONAL INTERFACE ---
HTML_TOOL = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JarryLink | Best Free URL Shortener & Custom Branded Short Links</title>
    <meta name="description" content="JarryLink is the best free URL shortener to create branded short links & analytics. A powerful Bitly and Google URL shortener alternative for 2026.">
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
        body { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #ffffff; color: #1e293b; scroll-behavior: smooth; }
        .hero-gradient { background: radial-gradient(circle at 50% 0%, #f0fdf4 0%, #ffffff 70%); }
        .tool-card { background: #ffffff; border: 2px solid #e2e8f0; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.05); transition: 0.4s; }
        .tool-card:hover { border-color: #10b981; }
        .text-gradient { background: linear-gradient(90deg, #059669, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .btn-primary { background: linear-gradient(90deg, #10b981, #059669); color: white; transition: 0.3s; }
        .btn-primary:hover { transform: translateY(-2px); box-shadow: 0 10px 20px rgba(16, 185, 129, 0.2); }
        .faq-box { background: #f8fafc; border-left: 4px solid #10b981; padding: 1.5rem; border-radius: 0.75rem; transition: 0.3s; }
        .faq-box:hover { background: #f1f5f9; }
        input { border: 1.5px solid #e2e8f0 !important; }
        input:focus { border-color: #10b981 !important; outline: none; box-shadow: 0 0 0 4px rgba(16, 185, 129, 0.1); }
    </style>
</head>
<body class="hero-gradient">

    <nav class="fixed top-0 w-full z-50 bg-white/80 backdrop-blur-md py-4 px-6 flex justify-between items-center border-b border-slate-100">
        <div class="text-2xl font-extrabold tracking-tighter text-gradient">JarryLink 🚀</div>
        <div class="hidden md:flex space-x-8 text-[12px] font-bold uppercase tracking-widest text-slate-600">
            <a href="#" class="hover:text-emerald-600">Architect</a>
            <a href="#content" class="hover:text-emerald-600">SEO Strategy</a>
            <a href="#faq" class="hover:text-emerald-600">FAQs</a>
        </div>
        <a href="https://jarrylabs.com" class="text-xs font-bold bg-slate-900 text-white px-6 py-2.5 rounded-full hover:bg-emerald-600 transition">JARRYLABS TOOLS</a>
    </nav>

    <section class="pt-44 pb-24 px-6 text-center">
        <div class="inline-block px-4 py-1.5 rounded-full bg-emerald-50 border border-emerald-100 text-emerald-700 text-[11px] font-bold uppercase tracking-widest mb-8">
            Fastest Free URL Shortener 2026
        </div>
        <h1 class="text-5xl md:text-7xl font-extrabold mb-8 tracking-tight text-slate-900 leading-tight">
            Shorten Links. <span class="text-gradient">Grow Authority.</span>
        </h1>
        <p class="max-w-2xl mx-auto text-slate-500 text-lg mb-14 font-medium">
            The world's most robust <strong>Free Short URL maker</strong> designed to architect <strong>Branded Short Links & Analytics</strong> with unstoppable speed.
        </p>

        <div class="max-w-5xl mx-auto tool-card p-10 md:p-14 rounded-[2.5rem] relative">
            <div class="grid grid-cols-1 md:grid-cols-12 gap-6 items-end">
                <div class="md:col-span-6 text-left">
                    <label class="text-[11px] text-slate-400 uppercase font-bold tracking-widest ml-1">Paste Long URL</label>
                    <input type="text" id="longUrl" placeholder="https://example.com/your-long-content-link" 
                           class="w-full mt-2 p-4 bg-slate-50 rounded-xl transition text-slate-800 font-medium">
                </div>
                <div class="md:col-span-4 text-left">
                    <label class="text-[11px] text-slate-400 uppercase font-bold tracking-widest ml-1">Custom Alias (Optional)</label>
                    <div class="flex items-center bg-slate-50 rounded-xl mt-2 overflow-hidden border border-slate-200">
                        <span class="pl-4 text-emerald-600 font-bold text-sm">jarrylink/</span>
                        <input type="text" id="shortCode" placeholder="mybrand" class="w-full p-4 bg-transparent outline-none font-medium">
                    </div>
                </div>
                <div class="md:col-span-2">
                    <button onclick="shortenLink()" id="btn" class="w-full py-4 btn-primary rounded-xl font-bold text-xs uppercase tracking-widest shadow-lg">
                        Shorten
                    </button>
                </div>
            </div>

            <div id="result" class="mt-12 hidden p-8 bg-emerald-50 border border-emerald-100 rounded-3xl">
                <p class="text-[11px] text-emerald-600 font-bold uppercase mb-3 tracking-widest">Branded Link Ready</p>
                <div class="text-2xl md:text-3xl font-extrabold text-slate-900 mb-6 tracking-tight" id="linkSpan">jarrylink/custom</div>
                <button onclick="copyLink()" id="copyBtn" class="bg-slate-900 text-white px-10 py-3.5 rounded-xl font-bold text-xs uppercase tracking-widest hover:bg-emerald-600 transition">
                    Copy Branded URL
                </button>
            </div>
        </div>
    </section>

    <section id="content" class="py-24 px-6 max-w-6xl mx-auto">
        <div class="grid md:grid-cols-3 gap-16">
            <div class="md:col-span-2 space-y-10">
                <h2 class="text-4xl font-extrabold text-slate-900 tracking-tight">The Best Free URL Shortener for Modern Brands</h2>
                
                <div class="text-slate-600 leading-relaxed space-y-6 text-lg">
                    <p>In the digital age of 2026, a link is your identity. Whether you are searching for a <strong>Free Link Shortener</strong> or a professional <strong>Custom URL Shortener</strong>, JarryLink provides an unstoppable path for your traffic. Our engine is built to handle <strong>Unlimited Links</strong>, making it the premier choice for creators who want to <strong>Create Branded Short Links</strong> without the cost of premium subscriptions.</p>
                    
                    <h3 class="text-2xl font-bold text-slate-900">The Ultimate Bitly and Google URL Shortener Alternative</h3>
                    <p>Many users miss the simplicity of the <strong>Google URL Shortener free</strong> service. JarryLink fills that gap. As a superior <strong>Bitly</strong> alternative, we offer <strong>Custom Short Links</strong> that don't expire. If you need a <strong>Free Short URL maker</strong> that supports <strong>Custom Domain Link</strong> features, our architecture is optimized for your success.</p>

                    <h3 class="text-2xl font-bold text-slate-900">Branded Short Links & Analytics: Data that Matters</h3>
                    <p>Every link generated through JarryLink is "Google Ready." By using a <strong>Custom link shortener</strong>, you improve your click-through rate (CTR) by up to 34%. Our platform provides <strong>URL Shortener, Branded Short Links & Analytics</strong> that help you understand your traffic source.</p>
                </div>

                <div class="p-8 bg-slate-50 rounded-3xl border border-slate-100">
                    <h4 class="text-xl font-bold text-slate-900 mb-6">Key SEO Benefits</h4>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm font-semibold text-slate-700">
                        <div class="flex items-center"><i class="fas fa-check-circle text-emerald-500 mr-2"></i> Custom Short Links</div>
                        <div class="flex items-center"><i class="fas fa-check-circle text-emerald-500 mr-2"></i> Branded Short Links & Analytics</div>
                        <div class="flex items-center"><i class="fas fa-check-circle text-emerald-500 mr-2"></i> Unlimited Links Generation</div>
                        <div class="flex items-center"><i class="fas fa-check-circle text-emerald-500 mr-2"></i> High-Speed 301 Redirects</div>
                    </div>
                </div>
            </div>

            <aside class="space-y-8">
                <div class="bg-white border border-slate-100 p-8 rounded-3xl shadow-sm">
                    <h5 class="text-xs font-bold uppercase tracking-widest text-slate-400 mb-6">Explore Resources</h5>
                    <div class="space-y-4">
                        <a href="https://www.jarrylabs.com/p/best-seo-free-tools.html" class="block p-4 bg-slate-50 rounded-xl border border-transparent hover:border-emerald-500 transition text-xs font-bold uppercase text-slate-700">
                            SEO Tools Dashboard
                        </a>
                        <a href="https://www.jarrylabs.com/2026/02/advanced-keyword-research-strategies-2026-high-intent-seo-blueprint-usa.html" class="block p-4 bg-slate-50 rounded-xl border border-transparent hover:border-blue-500 transition text-xs font-bold uppercase text-slate-700">
                            View Case Studies
                        </a>
                        <a href="https://www.jarrylabs.com/2026/02/google-url-shortener-free-alternative-2026.html" class="block p-4 bg-slate-50 rounded-xl border border-transparent hover:border-purple-500 transition text-xs font-bold uppercase text-slate-700">
                            Local SEO Guide
                        </a>
                    </div>
                </div>
                <button onclick="window.location.href='https://jarrylabs.com'" class="w-full py-4 bg-emerald-600 text-white rounded-2xl font-bold text-xs uppercase tracking-widest hover:bg-slate-900 transition">
                    Connect More Tools
                </button>
            </aside>
        </div>
    </section>

    <section id="faq" class="py-24 px-6 bg-slate-50">
        <div class="max-w-4xl mx-auto">
            <h2 class="text-4xl font-extrabold mb-16 text-center text-slate-900 tracking-tight">Expert FAQs</h2>
            
            <div class="grid gap-6">
                <div class="faq-box">
                    <h4 class="text-slate-900 font-bold mb-2">How to use Link shortener free online no sign up?</h4>
                    <p class="text-slate-600 text-sm">Simply paste your URL in our tool above and click 'Shorten' to get your branded link instantly without any account.</p>
                </div>
                <div class="faq-box">
                    <h4 class="text-slate-900 font-bold mb-2">Is JarryLink a better Bitly alternative?</h4>
                    <p class="text-slate-600 text-sm">Yes, we provide <strong>Unlimited Links</strong> and custom aliases for free, making it the most powerful alternative to Bitly.</p>
                </div>
                <div class="faq-box">
                    <h4 class="text-slate-900 font-bold mb-2">What about Google URL Shortener?</h4>
                    <p class="text-slate-600 text-sm">Since the <strong>Google URL shortener free</strong> service is gone, JarryLink serves as the perfect modern replacement.</p>
                </div>
                <div class="faq-box">
                    <h4 class="text-slate-900 font-bold mb-2">Can I create a Custom link shortener for free?</h4>
                    <p class="text-slate-600 text-sm">Absolutely! Define your own <strong>Custom URL free</strong> slugs to match your brand identity perfectly.</p>
                </div>
                <div class="faq-box">
                    <h4 class="text-slate-900 font-bold mb-2">Is it like Tiny URL?</h4>
                    <p class="text-slate-600 text-sm">It's better. We offer <strong>Custom Short Links</strong> with advanced analytics that Tiny URL often restricts.</p>
                </div>
            </div>
        </div>
    </section>

    <footer class="py-16 text-center border-t border-slate-100">
        <div class="text-gradient font-extrabold text-2xl mb-8 tracking-tighter">JarryLink</div>
        <p class="text-xs text-slate-400 font-medium tracking-widest">&copy; 2026 JARRYLABS ARCHITECT. ALL RIGHTS RESERVED.</p>
    </footer>

    <script>
        async function shortenLink() {
            const url = document.getElementById('longUrl').value;
            let code = document.getElementById('shortCode').value.trim();
            const btn = document.getElementById('btn');

            if(!url) return alert("Please enter a URL!");
            if(!code) code = Math.random().toString(36).substring(7);

            btn.innerText = "...";
            btn.disabled = true;

            try {
                const res = await fetch('/shorten', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({original_url: url, short_code: code})
                });
                if(res.ok) {
                    document.getElementById('result').classList.remove('hidden');
                    document.getElementById('linkSpan').innerText = `jarrylink/${code}`;
                    btn.innerText = "DONE";
                    setTimeout(() => { btn.innerText = "SHORTEN"; }, 2000);
                } else {
                    alert("Alias taken! Try another name.");
                    btn.innerText = "ERROR";
                }
            } catch (e) {
                alert("Server Error!");
            }
            btn.disabled = false;
        }

        function copyLink() {
            const link = "https://" + document.getElementById('linkSpan').innerText;
            navigator.clipboard.writeText(link).then(() => {
                const copyBtn = document.getElementById('copyBtn');
                copyBtn.innerText = "COPIED!";
                setTimeout(() => { copyBtn.innerText = "COPY BRANDED URL"; }, 2000);
            });
        }
    </script>
</body>
</html>
"""

# Redirection Logic (Same as before)
@app.route('/')
def home():
    return render_template_string(HTML_TOOL)

@app.route('/<path:path>')
def handle_all_routes(path):
    if ".html" in path or path.startswith("p/") or path.startswith("20") or "/" in path:
        return redirect(f"https://www.jarrylabs.com/{path}", code=302)
    short_code = path 
    if short_code in ['shorten', 'favicon.ico']: return "", 204
    try:
        res = supabase.table('links').select("original_url").eq("short_code", short_code).execute()
        if res.data:
            url = res.data[0]['original_url']
            return redirect(url if url.startswith('http') else 'https://'+url, code=301)
    except Exception as e:
        print(f"Error: {e}")
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
