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

# --- JARRYLABS CLEAN PROFESSIONAL INTERFACE ---
HTML_TOOL = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JarryLink | Best Free URL Shortener & Custom Branded Short Links</title>
    
    <meta name="description" content="JarryLink is the best free URL shortener with custom names. Use our link shortener free online to create branded links, shorten sentences, and paragraphs.">
    <meta name="keywords" content="link shortener free online, url shortener free, custom url shortener, ai video shortener free online, sentence shortener, paragraph shortener, google url shortener free, bitly alternative, best free url shortener, url shortener with custom name, url shortener chrome extension, link shortener highest paying">
    
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
        body { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #ffffff; color: #1e293b; scroll-behavior: smooth; }
        .hero-gradient { background: radial-gradient(circle at 50% 0%, #f0fdf4 0%, #ffffff 70%); }
        .tool-card { background: #ffffff; border: 2px solid #e2e8f0; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.05); transition: 0.4s; }
        .text-gradient { background: linear-gradient(90deg, #059669, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .btn-primary { background: linear-gradient(90deg, #10b981, #059669); color: white; transition: 0.3s; }
        .btn-primary:hover { transform: translateY(-2px); box-shadow: 0 10px 20px rgba(16, 185, 129, 0.2); }
        .faq-box { background: #f8fafc; border-left: 4px solid #10b981; padding: 1.5rem; border-radius: 0.75rem; margin-bottom: 1rem; }
        input { border: 1.5px solid #e2e8f0 !important; }
        input:focus { border-color: #10b981 !important; outline: none; }
        .sidebar-link { display: block; padding: 1rem; background: white; border: 1px solid #e2e8f0; border-radius: 0.75rem; transition: 0.3s; }
        .sidebar-link:hover { border-color: #10b981; box-shadow: 0 4px 6px -1px rgba(16, 185, 129, 0.1); }
    </style>
</head>
<body class="hero-gradient">

    <nav class="fixed top-0 w-full z-50 bg-white/80 backdrop-blur-md py-4 px-6 flex justify-between items-center border-b border-slate-100">
        <div class="text-2xl font-extrabold tracking-tighter text-gradient">JarryLink 🚀</div>
        <div class="hidden md:flex space-x-8 text-[12px] font-bold uppercase tracking-widest text-slate-600">
            <a href="#" class="hover:text-emerald-600">Home</a>
            <a href="https://www.jarrylabs.com/search?max-results=120" target="_blank" class="hover:text-emerald-600">Blog</a>
            <a href="#faq" class="hover:text-emerald-600">FAQs</a>
        </div>
        <a href="https://jarrylabs.com" class="text-xs font-bold bg-slate-900 text-white px-6 py-2.5 rounded-full hover:bg-emerald-600 transition">JARRYLABS TOOLS</a>
    </nav>

    <section class="pt-44 pb-24 px-6">
        <div class="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-4 gap-10">
            
            <div class="lg:col-span-3 text-center lg:text-left">
                <div class="inline-block px-4 py-1.5 rounded-full bg-emerald-50 border border-emerald-100 text-emerald-700 text-[11px] font-bold uppercase tracking-widest mb-8">
                    Fastest Free URL Shortener 2026
                </div>
                <h1 class="text-5xl md:text-7xl font-extrabold mb-8 tracking-tight text-slate-900 leading-tight">
                    Shorten Links. <span class="text-gradient">Grow Authority.</span>
                </h1>
                
                <div class="tool-card p-10 md:p-14 rounded-[2.5rem] relative">
                    <div class="grid grid-cols-1 md:grid-cols-12 gap-6 items-end">
                        <div class="md:col-span-6 text-left">
                            <label class="text-[11px] text-slate-400 uppercase font-bold tracking-widest ml-1">Paste Long URL</label>
                            <input type="text" id="longUrl" placeholder="https://example.com/your-content" class="w-full mt-2 p-4 bg-slate-50 rounded-xl font-medium">
                        </div>
                        <div class="md:col-span-4 text-left">
                            <label class="text-[11px] text-slate-400 uppercase font-bold tracking-widest ml-1">Custom Alias</label>
                            <div class="flex items-center bg-slate-50 rounded-xl mt-2 overflow-hidden border border-slate-200">
                                <span class="pl-4 text-emerald-600 font-bold text-sm">jarrylink.site/</span>
                                <input type="text" id="shortCode" placeholder="mybrand" class="w-full p-4 bg-transparent outline-none font-medium">
                            </div>
                        </div>
                        <div class="md:col-span-2">
                            <button onclick="shortenLink()" id="btn" class="w-full py-4 btn-primary rounded-xl font-bold text-xs uppercase tracking-widest shadow-lg">Shorten</button>
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
            </div>

            <div class="space-y-6">
                <h3 class="text-xl font-bold text-slate-900">Top SEO Articles</h3>
                <a href="https://www.jarrylabs.com/2026/01/how-to-use-custom-url-shorteners.html" target="_blank" class="sidebar-link">
                    <p class="font-bold text-slate-800">Custom URL Strategy</p>
                    <p class="text-sm text-slate-500">Boost brand recognition with branded links.</p>
                </a>
                <a href="https://www.jarrylabs.com/2026/01/best-seo-tools-2026.html" target="_blank" class="sidebar-link">
                    <p class="font-bold text-slate-800">Best Free SEO Tools</p>
                    <p class="text-sm text-slate-500">List of top tools for local and technical SEO.</p>
                </a>
                <a href="https://www.jarrylabs.com/2026/01/url-shortener-highest-paying.html" target="_blank" class="sidebar-link">
                    <p class="font-bold text-slate-800">Highest Paying Shorteners</p>
                    <p class="text-sm text-slate-500">Guide to monetizing your link traffic.</p>
                </a>
            </div>
        </div>
    </section>

    <section id="faq" class="py-24 px-6 bg-slate-50">
        <div class="max-w-4xl mx-auto">
            <h2 class="text-4xl font-extrabold mb-12 text-center">Frequently Asked Questions</h2>
            <div class="grid grid-cols-1 md:grid-cols-1 gap-4">
                <div class="faq-box">
                    <h4 class="font-bold">What is JarryLink Custom URL Shortener?</h4>
                    <p class="text-slate-600 text-sm">JarryLink is a professional tool to create branded short links, making them easier to share and track.</p>
                </div>
                <div class="faq-box">
                    <h4 class="font-bold">Is JarryLink a free Bitly alternative?</h4>
                    <p class="text-slate-600 text-sm">Yes, it is one of the best free Bitly alternatives, offering custom aliases without any hidden costs.</p>
                </div>
                <div class="faq-box">
                    <h4 class="font-bold">How does the link shortener free online work?</h4>
                    <p class="text-slate-600 text-sm">Simply paste your long URL, choose a custom name, and click shorten to get your instant redirect link.</p>
                </div>
                <div class="faq-box">
                    <h4 class="font-bold">Can I use this as a sentence shortener?</h4>
                    <p class="text-slate-600 text-sm">While primarily for URLs, you can use it to create short codes that represent long sentences or paragraphs for easy sharing.</p>
                </div>
                <div class="faq-box">
                    <h4 class="font-bold">Is there a Google URL shortener free version?</h4>
                    <p class="text-slate-600 text-sm">Google has discontinued its service, but JarryLink serves as a reliable and unstoppable replacement.</p>
                </div>
                <div class="faq-box">
                    <h4 class="font-bold">Is this an AI video shortener free online tool?</h4>
                    <p class="text-slate-600 text-sm">You can shorten long video links from any platform using our AI-ready infrastructure for better branding.</p>
                </div>
                <div class="faq-box">
                    <h4 class="font-bold">Does it support custom names for links?</h4>
                    <p class="text-slate-600 text-sm">Absolutely! You can create custom branded URLs like jarrylink.site/YourBrandName.</p>
                </div>
                <div class="faq-box">
                    <h4 class="font-bold">Is this the highest paying link shortener?</h4>
                    <p class="text-slate-600 text-sm">We focus on clean redirection and branding. For monetization, stay tuned for our upcoming premium features.</p>
                </div>
                <div class="faq-box">
                    <h4 class="font-bold">Can I use a Chrome extension?</h4>
                    <p class="text-slate-600 text-sm">A dedicated JarryLink Chrome extension is currently in development to make shortening even faster.</p>
                </div>
                <div class="faq-box">
                    <h4 class="font-bold">Are my links permanent?</h4>
                    <p class="text-slate-600 text-sm">Yes, links created on JarryLink are designed to be permanent and fast.</p>
                </div>
            </div>
        </div>
    </section>

    <footer class="py-12 border-t border-slate-200 bg-white px-6">
        <div class="max-w-6xl mx-auto flex flex-col md:flex-row justify-between items-center">
            <div class="mb-4 md:mb-0 text-left">
                <div class="text-xl font-extrabold text-gradient">JarryLink 🚀</div>
                <p class="text-xs text-slate-500 mt-2">© 2026 JarryLabs. All rights reserved. Your link shortening partner.</p>
            </div>
            <div class="flex space-x-6 text-xs font-bold uppercase tracking-widest text-slate-400">
                <a href="https://jarrylabs.com" class="hover:text-emerald-600">Main Site</a>
                <a href="#" class="hover:text-emerald-600">Privacy Policy</a>
                <a href="#" class="hover:text-emerald-600">Terms</a>
            </div>
        </div>
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
                    alert("Alias taken!");
                    btn.innerText = "ERROR";
                }
            } catch (e) { alert("Server Error!"); }
            btn.disabled = false;
        }

        function copyLink() {
            const displayText = document.getElementById('linkSpan').innerText;
            const code = displayText.split('/')[1];
            const workingLink = "https://jarrylink.site/" + code;
            
            navigator.clipboard.writeText(workingLink).then(() => {
                const copyBtn = document.getElementById('copyBtn');
                copyBtn.innerText = "COPIED!";
                setTimeout(() => { copyBtn.innerText = "COPY BRANDED URL"; }, 2000);
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TOOL)

@app.route('/<path:path>')
def handle_all_routes(path):
    # Check if it's a blog redirect
    if ".html" in path or path.startswith("p/") or path.startswith("20") or "/" in path:
        return redirect(f"https://www.jarrylabs.com/{path}", code=302)
    
    short_code = path 
    if short_code in ['shorten', 'favicon.ico']: return "", 204
    
    try:
        res = supabase.table('links').select("original_url").eq("short_code", short_code).execute()
        if res.data:
            url = res.data[0]['original_url']
            target = url if url.startswith('http') else 'https://'+url
            return redirect(target, code=301)
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

if __name__ == "__main__":
    app.run(debug=True)
