import os
from supabase import create_client
from dotenv import load_dotenv

# 1. Setup
load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

# 2. AAPKI NAYI 100+ KEYWORDS LIST
keywords_list = [
    'url-shortener', 'link-shortener', 'bitly-alternative', 'tinyurl-alternative', 'free-url-shortener',
    'best-url-shortener-2026', 'custom-url-shortener', 'branded-links', 'short-url-generator',
    'ai-url-shortener', 'smart-links-ai', 'ai-video-shortener', 'automated-link-manager', 
    'ai-link-optimizer', 'deep-link-generator', 'tech-link-shortener', 'sentence-shortener', 
    'paragraph-shortener', 'text-compressor', 'word-shortener-online', 'essay-link-shortener',
    'bio-link-tool', 'instagram-link-in-bio', 'youtube-link-shortener', 'twitter-url-cutter',
    'whatsapp-link-maker', 'facebook-url-shortener', 'tiktok-link-optimizer',
    'highest-paying-url-shortener', 'earn-money-online-links', 'link-monetization', 
    'best-payout-shortener', 'passive-income-links', 'ad-link-shortener', 'affiliate-link-cloaker',
    'marketing-tracker-links', 'vanity-url-service', 'enterprise-link-management',
    'google-url-shortener-free', 'link-shortener-without-ads', 'private-link-shortener',
    'bulk-url-shortener', 'api-link-shortener', 'link-shortener-chrome-extension',
    'qr-code-link-shortener', 'url-masking-tool', 'link-rotator-free', 'secure-links-generator'
]

target_url = "https://jarrylink.site"

def bulk_insert():
    print(f"🚀 Starting Injection of {len(keywords_list)} keywords...")
    for code in keywords_list:
        try:
            entry = {"short_code": code, "original_url": target_url, "clicks": 0}
            supabase.table('links').insert(entry).execute()
            print(f"✅ Created: {code}")
        except Exception:
            print(f"⚠️ Skip: {code} (Already exists)")

if __name__ == "__main__":
    bulk_insert()