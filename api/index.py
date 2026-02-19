@app.route('/<short_code>')
def redirect_logic(short_code):
    if short_code in ["favicon.ico", "status", "shorten", "static"]:
        return "", 204
    
    try:
        # Database se URL nikalna
        res = supabase.table('links').select("original_url").eq("short_code", short_code).execute()
        
        if res.data and len(res.data) > 0:
            target = res.data[0]['original_url']
            
            # URL fix (http check)
            if not target.startswith(('http://', 'https://')):
                target = 'https://' + target
            
            # --- YAHAN HAI ASLI JADOO ---
            # Hum direct redirect return kar rahe hain bina kisi HTML ke
            response = make_response(redirect(target, code=301)) 
            
            # Browser ko order dena ke is link ko yaad na rakhe aur foran jump kare
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            return response
            
    except Exception as e:
        print(f"Error: {e}")
    
    # Agar link na mile to wapis home par
    return redirect('https://jarrylink.site', code=302)
