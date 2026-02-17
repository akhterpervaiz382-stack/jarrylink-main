let finalTargetUrl = ""; // Ismein asli target save hoga

async function shortenLink() {
    const original_url = document.getElementById('longUrl').value;
    let short_code = document.getElementById('shortCode').value.trim();
    const btn = document.getElementById('btn');

    if(!original_url) return alert("Pehle URL dalein!");
    
    btn.innerText = "ARCHITECTING...";
    btn.disabled = true;

    const res = await fetch('/shorten', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ original_url, short_code })
    });

    if(res.ok) {
        document.getElementById('result').classList.remove('hidden');
        document.getElementById('displayLink').innerText = `jarrylink/${short_code}`;
        
        // Asli target URL ko memory mein save kar liya (Browser ko nahi dikhaya)
        finalTargetUrl = original_url.startsWith('http') ? original_url : 'https://' + original_url;
        
        btn.innerText = "GENERATE LINK";
    } else {
        alert("Error: Try another name!");
        btn.innerText = "TRY AGAIN";
    }
    btn.disabled = false;
}

// Ye function bina hamari site dikhaye seedha target khol dega
function openDirectly() {
    if(finalTargetUrl) {
        window.open(finalTargetUrl, '_blank');
    }
}

function copyLink() {
    const display = document.getElementById('displayLink').innerText;
    const code = display.split('/')[1];
    const final = "https://www.jarrylink.site/" + code;
    navigator.clipboard.writeText(final);
    alert("Copied: " + final);
}
