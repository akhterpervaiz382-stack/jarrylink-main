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
# 
PRIVACY_CONTENT = """
<div class="prose">
    <h1>Privacy Policy</h1>
    <p>Last updated: March 3, 2026</p>
    <p>At JarryLink, accessible from jarrylink.site, one of our main priorities is the privacy of our visitors. This Privacy Policy document contains types of information that is collected and recorded by JarryLink and how we use it.</p>
    
    <h2>Information We Collect</h2>
    <p>When you use our URL shortener, we collect the original URL you wish to shorten and the custom alias you choose. We also collect technical data such as IP addresses to prevent abuse of our service.</p>
    
    <h2>How We Use Your Information</h2>
    <ul>
        <li>To operate and maintain our website.</li>
        <li>To improve, personalize, and expand our website.</li>
        <li>To prevent fraud and abuse.</li>
    </ul>
</div>
"""

# 
TERMS_CONTENT = """
<div class="prose">
    <h1>Terms of Service</h1>
    <p>Last updated: March 3, 2026</p>
    <p>By accessing this website, we assume you accept these terms of service. Do not continue to use JarryLink if you do not agree to take all of the terms and conditions stated on this page.</p>
    
    <h2>License</h2>
    <p>Unless otherwise stated, JarryLink and/or its licensors own the intellectual property rights for all material on JarryLink. All intellectual property rights are reserved.</p>
    
    <h2>Restrictions</h2>
    <p>You are specifically restricted from all of the following:</p>
    <ul>
        <li>Using this service to shorten links to illegal content.</li>
        <li>Using this service for phishing or spreading malware.</li>
        <li>Attempting to reverse engineer the service.</li>
    </ul>
</div>
"""

# --- HOME PAGE HTML ---
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
        .hero-gradient { background: radial-gradient(circle at 50% -20%, #f0fdf4 0%, #ffffff 50%); }
        .tool-card { background: #ffffff; border: 2px solid #e2e8f0; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.05); }
        .text-gradient { background: linear-gradient(90deg, #059669, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .btn-primary { background: linear-gradient(90deg, #10b981, #059669); color: white; transition: 0.3s; }
        .btn-primary:hover { transform: translateY(-2px); box-shadow: 0 10px 20px rgba(16, 185, 129, 0.2); }
        .faq-box { background: #ffffff; border: 1px solid #e2e8f0; padding: 1.5rem; border-radius: 1rem; transition: 0.3s; }
        .faq-box:hover { border-color: #10b981; box-shadow: 0 10px 15px -3px rgba(16, 185, 129, 0.1); }
        input { border: 1.5px solid #e2e8f0 !important; }
        input:focus { border-color: #10b981 !important; outline: none; }
        .stat-card { background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%); border: 1px solid #e2e8f0; transition: 0.3s; }
        .stat-card:hover { transform: translateY(-5px); border-color: #10b981; }
        .testimonial-card { background: white; border: 1px solid #e2e8f0; }
    </style>
</head>
<body class="hero-gradient">
    <nav class="fixed top-0 w-full z-50 bg-white/90 backdrop-blur-sm py-4 px-6 flex justify-between items-center border-b border-slate-100">
        <div class="text-2xl font-extrabold tracking-tighter text-gradient">JarryLink 🚀</div>
        <div class="hidden md:flex space-x-8 text-[13px] font-bold uppercase tracking-widest text-slate-700">
            <a href="#" class="hover:text-emerald-600">Home</a>
            <a href="#features" class="hover:text-emerald-600">Features</a>
            <a href="#tool" class="hover:text-emerald-600">Shortener</a>
            <a href="#faq" class="hover:text-emerald-600">FAQs</a>
        </div>
        <a href="https://jarrylabs.com" class="text-xs font-bold bg-slate-900 text-white px-6 py-2.5 rounded-full hover:bg-emerald-600 transition">JARRYLABS</a>
    </nav>
    <header class="pt-40 pb-20 px-6 text-center">
        <div class="inline-block px-4 py-1.5 rounded-full bg-emerald-50 border border-emerald-100 text-emerald-700 text-[11px] font-bold uppercase tracking-widest mb-6">Fastest Free URL Shortener 2026</div>
        <h1 class="text-5xl md:text-7xl font-extrabold mb-6 tracking-tight text-slate-900 leading-tight">Shorten Links. <span class="text-gradient">Grow Authority.</span></h1>
        <p class="text-lg text-slate-600 max-w-2xl mx-auto mb-10">JarryLink helps you create branded, short, and memorable links to boost your online presence and track your traffic effortlessly.</p>
    </header>
    <section id="tool" class="py-10 px-6">
        <div class="max-w-5xl mx-auto">
            <div class="tool-card p-10 md:p-14 rounded-[2.5rem]">
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
                    <button onclick="copyLink()" id="copyBtn" class="bg-slate-900 text-white px-10 py-3.5 rounded-xl font-bold text-xs uppercase tracking-widest hover:bg-emerald-600 transition">Copy Branded URL</button>
                </div>
            </div>
        </div>
    </section>
    <section id="features" class="py-20 px-6">
        <div class="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-8">
            <div class="stat-card p-8 rounded-3xl text-center"><div class="text-5xl font-extrabold text-gradient mb-3">10,000+</div><p class="text-slate-600 font-bold">Links Generated</p></div>
            <div class="stat-card p-8 rounded-3xl text-center"><div class="text-5xl font-extrabold text-gradient mb-3">99.9%</div><p class="text-slate-600 font-bold">Uptime Guaranteed</p></div>
            <div class="stat-card p-8 rounded-3xl text-center"><div class="text-5xl font-extrabold text-gradient mb-3">100%</div><p class="text-slate-600 font-bold">Free to Use</p></div>
        </div>
    </section>
    <section class="py-20 px-6 bg-slate-50">
        <div class="max-w-7xl mx-auto">
            <h2 class="text-4xl font-extrabold mb-12 text-center text-slate-900">Trusted by Happy Users</h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div class="testimonial-card p-8 rounded-3xl">
                    <div class="flex items-center mb-6"><div><div class="font-bold text-slate-900">2000+ Reviews</div><div class="flex text-amber-400"><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><span class="ml-2 text-slate-700 font-bold">4.9 / 5</span></div></div></div>
                    <p class="text-slate-600">"JarryLink completely changed how I share my content on social media. Simple and fast!"</p>
                </div>
                <div class="testimonial-card p-8 rounded-3xl">
                    <div class="flex items-center mb-6"><div><div class="font-bold text-slate-900">2000+ Reviews</div><div class="flex text-amber-400"><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><span class="ml-2 text-slate-700 font-bold">4.9 / 5</span></div></div></div>
                    <p class="text-slate-600">"Finally a reliable, free alternative to Bitly. The custom alias feature is amazing."</p>
                </div>
                <div class="testimonial-card p-8 rounded-3xl">
                    <div class="flex items-center mb-6"><div><div class="font-bold text-slate-900">2000+ Reviews</div><div class="flex text-amber-400"><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><span class="ml-2 text-slate-700 font-bold">4.9 / 5</span></div></div></div>
                    <p class="text-slate-600">"Great tool for tracking clicks. Very user-friendly interface."</p>
                </div>
            </div>
        </div>
    </section>
    <section class="py-20 px-6">
        <div class="max-w-4xl mx-auto text-center">
            <h2 class="text-4xl font-extrabold mb-8 text-slate-900">More Tools to Grow Your Brand</h2>
            <p class="text-slate-600 mb-12">Discover our suite of free tools designed to streamline your workflow and enhance your content.</p>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <a href="https://jarrylabs.com" class="faq-box block"><h4 class="font-bold text-lg mb-2">YT Thumbnail Downloader</h4><p class="text-sm text-slate-500">Get high-quality thumbnails in seconds.</p></a>
                <a href="https://www.jarrylabs.com/p/background-remover.html"faq-box block"><h4 class="font-bold text-lg mb-2">Background Remover</h4><p class="text-sm text-slate-500">Instantly remove backgrounds from images.</p></a>
                <a href="https://www.jarrylabs.com/p/image-enhancer.html" class="faq-box block"><h4 class="font-bold text-lg mb-2">Image Enhancer</h4><p class="text-sm text-slate-500">Boost your image quality automatically.</p></a>
            </div>
        </div>
    </section>
    <section id="faq" class="py-20 px-6 bg-slate-900 text-white rounded-t-[3rem]">
        <div class="max-w-6xl mx-auto">
            <h2 class="text-4xl font-extrabold mb-12 text-center">Frequently Asked Questions</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="faq-box bg-slate-800 border-slate-700"><h4 class="font-bold text-lg mb-2">What is JarryLink Custom URL Shortener?</h4><p class="text-slate-300 text-sm">JarryLink is a professional tool to create branded short links, making them easier to share and track.</p></div>
                <div class="faq-box bg-slate-800 border-slate-700"><h4 class="font-bold text-lg mb-2">Is JarryLink a free Bitly alternative?</h4><p class="text-slate-300 text-sm">Yes, it is one of the best free Bitly alternatives, offering custom aliases without any hidden costs.</p></div>
                <div class="faq-box bg-slate-800 border-slate-700"><h4 class="font-bold text-lg mb-2">How does the link shortener free online work?</h4><p class="text-slate-300 text-sm">Simply paste your long URL, choose a custom name, and click shorten to get your instant redirect link.</p></div>
                <div class="faq-box bg-slate-800 border-slate-700"><h4 class="font-bold text-lg mb-2">Can I use this as a sentence shortener?</h4><p class="text-slate-300 text-sm">While primarily for URLs, you can use it to create short codes that represent long sentences or paragraphs for easy sharing.</p></div>
                <div class="faq-box bg-slate-800 border-slate-700"><h4 class="font-bold text-lg mb-2">Is there a Google URL shortener free version?</h4><p class="text-slate-300 text-sm">Google has discontinued its service, but JarryLink serves as a reliable and unstoppable replacement.</p></div>
                <div class="faq-box bg-slate-800 border-slate-700"><h4 class="font-bold text-lg mb-2">Is this an AI video shortener free online tool?</h4><p class="text-slate-300 text-sm">You can shorten long video links from any platform using our AI-ready infrastructure for better branding.</p></div>
                <div class="faq-box bg-slate-800 border-slate-700"><h4 class="font-bold text-lg mb-2">Does it support custom names for links?</h4><p class="text-slate-300 text-sm">Absolutely! You can create custom branded URLs like jarrylink.site/YourBrandName.</p></div>
                <div class="faq-box bg-slate-800 border-slate-700"><h4 class="font-bold text-lg mb-2">Is this the highest paying link shortener?</h4><p class="text-slate-300 text-sm">We focus on clean redirection and branding. For monetization, stay tuned for our upcoming premium features.</p></div>
                <div class="faq-box bg-slate-800 border-slate-700"><h4 class="font-bold text-lg mb-2">Can I use a Chrome extension?</h4><p class="text-slate-300 text-sm">A dedicated JarryLink Chrome extension is currently in development to make shortening even faster.</p></div>
                <div class="faq-box bg-slate-800 border-slate-700"><h4 class="font-bold text-lg mb-2">Are my links permanent?</h4><p class="text-slate-300 text-sm">Yes, links created on JarryLink are designed to be permanent and fast.</p></div>
            </div>
        </div>
    </section>
    <footer class="py-12 border-t border-slate-200 bg-white px-6">
        <div class="max-w-6xl mx-auto flex flex-col md:flex-row justify-between items-center">
            <div class="mb-4 md:mb-0 text-left"><div class="text-xl font-extrabold text-gradient">JarryLink 🚀</div><p class="text-xs text-slate-500 mt-2">© 2026 JarryLabs. All rights reserved.</p></div>
            <div class="flex space-x-6 text-xs font-bold uppercase tracking-widest text-slate-400">
                <a href="https://jarrylabs.com" class="hover:text-emerald-600">Main Site</a>
                <a href="/privacy" class="hover:text-emerald-600">Privacy</a>
                <a href="/terms" class="hover:text-emerald-600">Terms</a>
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
                    document.getElementById('linkSpan').innerText = `jarrylink.site/${code}`;
                    btn.innerText = "DONE";
                    setTimeout(() => { btn.innerText = "SHORTEN"; }, 2000);
                } else { alert("Alias taken!"); btn.innerText = "ERROR"; }
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
