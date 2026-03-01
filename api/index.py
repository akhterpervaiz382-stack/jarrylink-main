import os
from flask import Flask, request, jsonify, redirect, render_template_string
from flask_cors import CORS
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Database Connection (Logic remains untouched)
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")
supabase = create_client(supabase_url, supabase_key)

# --- JARRYLABS PREMIUM ARCHITECT INTERFACE ---
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
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
        body { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #050505; color: white; scroll-behavior: smooth; }
        .glass { background: rgba(255, 255, 255, 0.02); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.08); }
        .hero-bg { background: radial-gradient(circle at 50% -20%, #1e1b4b 0%, #050505 80%); }
        .emerald-glow { box-shadow: 0 0 30px rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.4); }
        .text-gradient { background: linear-gradient(to right, #38bdf8, #818cf8, #10b981); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .faq-box { border-left: 3px solid #10b981; transition: 0.3s; }
        .faq-box:hover { background: rgba(16, 185, 129, 0.05); transform: scale(1.01); }
        .btn-gradient { background: linear-gradient(90deg, #10b981, #3b82f6); }
    </style>
</head>
<body class="hero-bg">

    <nav class="fixed top-0 w-full z-50 glass py-4 px-6 flex justify-between items-center border-b border-white/5">
        <div class="text-2xl font-black italic tracking-tighter text-gradient">JarryLink 🚀</div>
        <div class="hidden md:flex space-x-8 text-[11px] font-bold uppercase tracking-[0.2em]">
            <a href="#" class="hover:text-emerald-400">Architect</a>
            <a href="#features" class="hover:text-emerald-400">Features</a>
            <a href="#content" class="hover:text-emerald-400">SEO Guide</a>
            <a href="#faq" class="hover:text-emerald-400 text-emerald-400">FAQs</a>
        </div>
        <a href="https://jarrylabs.com" class="text-xs font-bold border border-emerald-500/50 px-5 py-2 rounded-full hover:bg-emerald-500 hover:text-black transition">JARRYLABS TOOLSET</a>
    </nav>

    <section class="pt-40 pb-20 px-6 text-center">
        <div class="inline-block px-4 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-[10px] font-bold uppercase tracking-widest mb-6">
            The Best Free URL Shortener for 2026
        </div>
        <h1 class="text-6xl md:text-8xl font-black mb-6 tracking-tighter leading-tight">
            Infinite Links. <br><span class="text-gradient">Branded Authority.</span>
        </h1>
        <p class="max-w-3xl mx-auto text-gray-400 text-lg mb-12">
            Experience the ultimate <strong>Free URL Shortener</strong>. JarryLink is the world's most robust <strong>Free Short URL maker</strong> designed to architect <strong>Branded Short Links & Analytics</strong> with unstoppable speed.
        </p>

        <div class="max-w-5xl mx-auto emerald-glow glass p-8 md:p-16 rounded-[3.5rem] relative overflow-hidden">
            <div class="grid grid-cols-1 md:grid-cols-12 gap-6 items-end">
                <div class="md:col-span-6 text-left">
                    <label class="text-[10px] text-gray-500 uppercase font-black tracking-widest ml-4">Target Destination</label>
                    <input type="text" id="longUrl" placeholder="https://your-long-link.com/ai-video-shortener" 
                           class="w-full mt-2 p-5 bg-white/5 border border-white/10 rounded-2xl focus:border-emerald-500 outline-none transition text-emerald-100">
                </div>
                <div class="md:col-span-4 text-left">
                    <label class="text-[10px] text-gray-500 uppercase font-black tracking-widest ml-4">Custom Alias</label>
                    <div class="flex items-center bg-white/5 border border-white/10 rounded-2xl mt-2 overflow-hidden focus-within:border-emerald-500 transition">
                        <span class="pl-5 text-emerald-500 font-bold italic text-sm">jarrylink/</span>
                        <input type="text" id="shortCode" placeholder="mybrand" class="w-full p-5 bg-transparent outline-none">
                    </div>
                </div>
                <div class="md:col-span-2">
                    <button onclick="shortenLink()" id="btn" class="w-full py-5 btn-gradient text-white rounded-2xl font-black text-xs uppercase tracking-widest hover:brightness-110 transition active:scale-95 shadow-xl">
                        Architect
                    </button>
                </div>
            </div>

            <div id="result" class="mt-12 hidden p-10 bg-emerald-500/5 border border-emerald-500/20 rounded-[2.5rem] animate-pulse">
                <p class="text-[10px] text-emerald-400 font-black uppercase mb-4 tracking-[0.3em]">Branded Link Successfully Architected</p>
                <div class="text-3xl font-bold text-white mb-8 italic tracking-tighter" id="linkSpan">jarrylink.site/custom</div>
                <button onclick="copyLink()" id="copyBtn" class="bg-white text-black px-12 py-4 rounded-xl font-bold text-xs uppercase tracking-widest hover:bg-emerald-400 transition">
                    Copy Branded URL
                </button>
            </div>
        </div>
    </section>

    <section id="content" class="py-24 px-6 max-w-6xl mx-auto border-t border-white/5">
        <div class="grid md:grid-cols-3 gap-12">
            <div class="md:col-span-2 space-y-12">
                <h2 class="text-4xl font-black text-white italic tracking-tighter">Why JarryLink is the Best Free URL Shortener</h2>
                
                <div class="prose prose-invert max-w-none text-gray-400 leading-relaxed space-y-6">
                    <p>In the digital age of 2026, a link is your identity. Whether you are searching for a <strong>Free Link Shortener</strong> or a professional <strong>Custom URL Shortener</strong>, JarryLink provides an unstoppable path for your traffic. Our engine is built to handle <strong>Unlimited Links</strong>, making it the premier choice for creators who want to <strong>Create Branded Short Links</strong> without the cost of premium subscriptions.</p>
                    
                    <h3 class="text-2xl font-bold text-white tracking-tight">The Ultimate Bitly and Google URL Shortener Alternative</h3>
                    <p>Many users miss the simplicity of the <strong>Google URL Shortener free</strong> service. JarryLink fills that gap. As a superior <strong>Bitly</strong> alternative, we offer <strong>Custom Short Links</strong> that don't expire. If you need a <strong>Free Short URL maker</strong> that supports <strong>Custom Domain Link</strong> features, our architecture is optimized for your success.</p>

                    <h3 class="text-2xl font-bold text-white tracking-tight">Branded Short Links & Analytics: Data that Matters</h3>
                    <p>Every link generated through JarryLink is "Google Ready." By using a <strong>Custom link shortener</strong>, you improve your click-through rate (CTR) by up to 34%. Our platform provides <strong>URL Shortener, Branded Short Links & Analytics</strong> that help you understand where your traffic is coming from—be it Pinterest, YouTube, or Medium.</p>

                    <p>If you've been searching for a <strong>Link shortener free online no sign up</strong>, you are in the right place. Our <strong>Custom URL free</strong> logic allows you to bypass messy registration forms and get straight to building your brand. From <strong>Tiny URL</strong> simplicity to <strong>Google URL Shortener</strong> power, we combine the best of both worlds.</p>
                </div>

                <div class="p-8 glass rounded-[2rem] border border-emerald-500/20 bg-emerald-500/5">
                    <h4 class="text-xl font-bold text-emerald-400 mb-4">Key SEO Strategies for Link Architecture</h4>
                    <ul class="space-y-3 text-sm text-gray-300">
                        <li>✅ Use <strong>Custom Short Links</strong> to include target keywords.</li>
                        <li>✅ Leverage <strong>Branded Short Links & Analytics</strong> to track user behavior.</li>
                        <li>✅ Switch from <strong>Tiny URL</strong> to JarryLink for faster 301 redirects.</li>
                        <li>✅ Optimized for AI tools like <strong>sentence shortener</strong> and <strong>paragraph shortener</strong> outputs.</li>
                    </ul>
                </div>
            </div>

            <aside class="space-y-8">
                <div class="glass p-8 rounded-[2rem]">
                    <h5 class="text-sm font-black uppercase tracking-widest text-white mb-6">Explore Our Tools</h5>
                    <div class="space-y-4">
                        <a href="https://jarrylabs.com" class="block p-4 bg-white/5 rounded-xl border border-white/5 hover:border-emerald-500 transition text-xs font-bold uppercase tracking-widest">
                            SEO Tools Dashboard
                        </a>
                        <a href="https://jarrylabs.com/case-studies" class="block p-4 bg-white/5 rounded-xl border border-white/5 hover:border-blue-500 transition text-xs font-bold uppercase tracking-widest">
                            Case Studies
                        </a>
                        <a href="https://jarrylabs.com/local-seo" class="block p-4 bg-white/5 rounded-xl border border-white/5 hover:border-purple-500 transition text-xs font-bold uppercase tracking-widest">
                            Local SEO Guide
                        </a>
                    </div>
                </div>
                <div class="p-8 bg-gradient-to-br from-emerald-600/20 to-blue-600/20 rounded-[2rem] border border-white/10">
                    <p class="text-xs text-emerald-400 font-bold mb-2 uppercase italic">Pro Tip:</p>
                    <p class="text-sm text-gray-300">A <strong>Custom URL free</strong> link builds 3x more trust than a generic random slug.</p>
                </div>
            </aside>
        </div>
    </section>

    <section id="faq" class="py-24 px-6 bg-[#030303]">
        <div class="max-w-4xl mx-auto">
            <h2 class="text-4xl font-black mb-16 text-center italic tracking-tighter"><span class="text-emerald-400 underline">URL Shortener</span> Expert FAQ</h2>
            
            <div class="space-y-6">
                <div class="faq-box p-8 glass rounded-2xl">
                    <h4 class="text-white font-bold mb-2">How to use Link shortener free online no sign up?</h4>
                    <p class="text-gray-400 text-sm">Simply paste your URL in our Architect engine above and click 'Architect' to get a branded link instantly without any registration.</p>
                </div>
                <div class="faq-box p-8 glass rounded-2xl">
                    <h4 class="text-white font-bold mb-2">Is JarryLink a better Bitly alternative?</h4>
                    <p class="text-gray-400 text-sm">Yes, we provide unlimited custom aliases and zero ads, making us the most powerful free alternative to Bitly today.</p>
                </div>
                <div class="faq-box p-8 glass rounded-2xl">
                    <h4 class="text-white font-bold mb-2">What happened to Google URL Shortener?</h4>
                    <p class="text-gray-400 text-sm">Google shut down its service in 2019, but JarryLink offers a modern, faster <strong>Google URL shortener free</strong> replacement for the 2026 web.</p>
                </div>
                <div class="faq-box p-8 glass rounded-2xl">
                    <h4 class="text-white font-bold mb-2">Can I create a Custom link shortener for free?</h4>
                    <p class="text-gray-400 text-sm">Absolutely! Our platform allows you to define your own <strong>Custom URL free</strong> slugs to match your brand identity perfectly.</p>
                </div>
                <div class="faq-box p-8 glass rounded-2xl">
                    <h4 class="text-white font-bold mb-2">How does this compare to Tiny URL?</h4>
                    <p class="text-gray-400 text-sm">Unlike Tiny URL, JarryLink provides advanced branding options and is part of the robust JarryLabs SEO ecosystem for better search visibility.</p>
                </div>
            </div>
        </div>
    </section>

    <footer class="py-20 border-t border-white/5 text-center">
        <div class="text-gradient font-black text-3xl mb-8 italic tracking-tighter">JarryLink</div>
        <div class="flex flex-wrap justify-center gap-8 text-[10px] font-bold uppercase tracking-[0.3em] mb-12 text-gray-500">
            <a href="https://jarrylabs.com" class="hover:text-emerald-400 transition">Main Tools</a>
            <a href="#" class="hover:text-emerald-400 transition">Privacy Policy</a>
            <a href="#" class="hover:text-emerald-400 transition">Terms of Service</a>
            <a href="#content" class="hover:text-emerald-400 transition">Content Strategy</a>
        </div>
        <p class="text-[9px] text-gray-700 tracking-widest">&copy; 2026 JARRYLABS ARCHITECT ENGINE. ALL RIGHTS RESERVED.</p>
    </footer>

    <script>
        async function shortenLink() {
            const url = document.getElementById('longUrl').value;
            let code = document.getElementById('shortCode').value.trim();
            const btn = document.getElementById('btn');

            if(!url) return alert("Please enter a valid URL!");
            if(!code) code = Math.random().toString(36).substring(7);

            btn.innerText = "ARCHITECTING...";
            btn.disabled = true;

            try {
                const res = await fetch('/shorten', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({original_url: url, short_code: code})
                });
                if(res.ok) {
                    document.getElementById('result').classList.remove('hidden');
                    document.getElementById('linkSpan').innerText = `jarrylink.site/${code}`;
                    btn.innerText = "SUCCESS";
                    setTimeout(() => { btn.innerText = "ARCHITECT"; }, 2000);
                } else {
                    alert("Alias taken! Try another unique name.");
                    btn.innerText = "TRY AGAIN";
                }
            } catch (e) {
                alert("Engine Offline!");
                btn.innerText = "ERROR";
            }
            btn.disabled = false;
        }

        function copyLink() {
            const link = "https://" + document.getElementById('linkSpan').innerText;
            navigator.clipboard.writeText(link).then(() => {
                const copyBtn = document.getElementById('copyBtn');
                copyBtn.innerText = "COPIED TO CLIPBOARD!";
                setTimeout(() => { copyBtn.innerText = "COPY BRANDED URL"; }, 2000);
            });
        }
    </script>
</body>
</html>
"""

# Rest of the Python logic (Routes remain exactly as they were)
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
