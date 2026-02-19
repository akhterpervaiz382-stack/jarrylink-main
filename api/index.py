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

# --- JARRYLABS PREMIUM INTERFACE (Updated with Real Links) ---
HTML_TOOL = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JarryLabs | Make Your Link Cutest & Branded</title>
    
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
        .dropdown:hover .dropdown-menu { display: block; }
    </style>
</head>
<body class="flex flex-col min-h-screen">

    <header class="border-b border-white/5 sticky top-0 z-50 bg-black/80 backdrop-blur-md">
        <nav class="max-w-7xl mx-auto px-6 py-5 flex justify-between items-center">
            <a href="https://www.jarrylabs.com" class="text-3xl font-extrabold tracking-tighter">Jarry<span class="fiverr-text">Labs.</span></a>
            
            <div class="hidden md:flex space-x-8 text-[11px] font-bold uppercase tracking-[0.2em] items-center">
                <a href="https://www.jarrylabs.com" class="hover:text-[#1dbf73] transition">Home</a>
                
                <div class="relative dropdown">
                    <a href="https://www.jarrylabs.com/p/home.html" class="hover:text-[#1dbf73] transition cursor-pointer">More Tools ▾</a>
                    <div class="dropdown-menu hidden absolute left-0 mt-2 w-56 bg-[#121212] border border-white/10 rounded-xl py-2 shadow-2xl z-50">
                        <a href="https://www.jarrylabs.com/p/free-text-case-converter-online.html" class="block px-4 py-2 hover:bg-white/5 text-[10px]">Text Case Converter</a>
                        <a href="https://www.jarrylabs.com/p/best-free-markdown-editor-online-2026.html" class="block px-4 py-2 hover:bg-white/5 text-[10px]">Markdown Editor</a>
                        <a href="https://www.jarrylabs.com/p/json-formatte.html" class="block px-4 py-2 hover:bg-white/5 text-[10px]">JSON Formatter</a>
                        <a href="https://www.jarrylabs.com/p/the-secure-password-generator-free.html" class="block px-4 py-2 hover:bg-white/5 text-[10px]">Password Generator</a>
                        <a href="https://www.jarrylabs.com/p/free-base64-encoderdecoder.html" class="block px-4 py-2 hover:bg-white/5 text-[10px]">Base64 Encoder</a>
                        <a href="https://www.jarrylabs.com/p/qr-code-generator.html" class="block px-4 py-2 hover:bg-white/5 text-[10px]">QR Code Generator</a>
                        <a href="https://www.jarrylabs.com/p/free-word-counter-tool.html" class="block px-4 py-2 hover:bg-white/5 text-[10px]">Word Counter</a>
                    </div>
                </div>

                <a href="https://www.jarrylabs.com/p/social-suite-pro-content-creator-tools.html" class="hover:text-[#1dbf73] transition">Social Suite</a>
                <a href="https://www.jarrylabs.com/p/about-us.html" class="hover:text-[#1dbf73] transition">About</a>
            </div>
            
            <a href="https://www.jarrylabs.com/p/contact-us_18.html" class="bg-white text-black px-5 py-2 rounded-full text-[10px] font-black uppercase hover:bg-fiverr-green hover:text-white transition-all">Contact</a>
        </nav>
    </header>

    <main class="flex-grow flex items-center justify-center py-20 px-4">
        <div class="max-w-4xl w-full text-center">
            <h1 class="text-6xl md:text-8xl font-extrabold mb-8 tracking-tighter leading-tight">
                Make Your <br><span class="fiverr-text italic">Link Cutest</span>
            </h1>
            <p class="text-gray-400 mb-10 font-bold uppercase tracking-widest text-xs">Simple • Sweet • Shortened</p>
            
            <div class="glass-card p-4 rounded-[2.5rem] max-w-3xl mx-auto">
                <div class="bg-[#181818] rounded-[2.2rem] p-8 md:p-12 space-y-8">
                    <div class="text-left space-y-6">
                        <div>
                            <label class="text-[10px] uppercase tracking-widest font-bold text-gray-500 ml-2">Destination URL</label>
                            <input type="text" id="longUrl" placeholder="https://..." class="w-full bg-black/40 border border-white/10 p-5 rounded-2xl focus:border-fiverr-green outline-none transition-all text-sm">
                        </div>
                        <div>
                            <label class="text-[10px] uppercase tracking-widest font-bold text-gray-500 ml-2">Your Branded Name</label>
                            <div class="flex items-center bg-black/40 border border-white/10 rounded-2xl overflow-hidden focus-within:border-fiverr-green">
                                <span class="pl-6 fiverr-text font-black italic">jarrylabs/</span>
                                <input type="text" id="shortCode" placeholder="alias" class="w-full bg-transparent p-5 outline-none text-white font-bold">
                            </div>
                        </div>
                    </div>

                    <button onclick="shortenLink()" id="btn" class="btn-main w-full py-5 rounded-2xl uppercase tracking-widest text-sm shadow-xl shadow-emerald-500/10">
                        Generate Cute Link
                    </button>

                    <div id="result" class="hidden mt-10 p-8 border border-fiverr-green/30 bg-fiverr-green/5 rounded-3xl">
                        <p class="text-[10px] font-bold fiverr-text uppercase tracking-widest mb-3">Your Link is Ready!</p>
                        <div class="text-4xl font-extrabold mb-8 italic" id="linkSpan">jarrylabs/name</div>
                        <div class="flex gap-4">
                             <button onclick="copyLink()" id="copyBtn" class="flex-grow fiverr-bg text-white py-4 rounded-xl font-bold text-xs uppercase tracking-widest">Copy Now</button>
                             <button onclick="visitLink()" class="bg-white text-black px-8 rounded-xl font-bold text-xs uppercase">Visit</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </main>

    <footer class="bg-[#050505] border-t border-white/5 py-12 px-6">
        <div class="max-w-7xl mx-auto grid md:grid-cols-4 gap-10">
            <div class="col-span-2">
                <span class="text-2xl font-black italic text-white">JarryLabs.</span>
                <p class="text-gray-500 mt-4 text-sm max-w-xs">Premium SEO tools and URL management. Powered by JarryLabs Architecture.</p>
            </div>
            <div>
                <h4 class="text-white font-bold text-xs uppercase tracking-widest mb-4">Legal</h4>
                <ul class="text-sm text-gray-500 space-y-2">
                    <li><a href="https://www.jarrylabs.com/p/privacy-policy_18.html" class="hover:text-white transition">Privacy Policy</a></li>
                    <li><a href="https://www.jarrylabs.com/p/terms.html" class="hover:text-white transition">Terms of Service</a></li>
                    <li><a href="https://www.jarrylabs.com/p/disclaimer_22.html" class="hover:text-white transition">Disclaimer</a></li>
                </ul>
            </div>
            <div>
                <h4 class="text-white font-bold text-xs uppercase tracking-widest mb-4">Quick Links</h4>
                <ul class="text-sm text-gray-500 space-y-2">
                    <li><a href="https://www.jarrylabs.com/p/about-us.html" class="hover:text-white transition">About Us</a></li>
                    <li><a href="https://www.jarrylabs.com/p/contact-us_18.html" class="hover:text-white transition">Contact Us</a></li>
                    <li class="fiverr-text font-bold">Fiverr Professional</li>
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
            if(!l_url) return alert("Pehle URL dalo bhai!");
            
            btn.innerText = "BEAUTIFYING..."; btn.disabled = true;
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
            const final = window.location.origin + "/" + currentAlias;
            navigator.clipboard.writeText(final).then(() => {
                document.getElementById('copyBtn').innerText = "COPIED!";
                setTimeout(() => { document.getElementById('copyBtn').innerText = "COPY NOW"; }, 2000);
            });
        }
        function visitLink() { window.open(window.location.origin + "/" + currentAlias, '_blank'); }
    </script>
</body>
</html>
"""
# ... Baqi Flask Logic wahi hai ...
