import requests

def scan(url):
    if not url.startswith("http"):
        url = "https://" + url

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "*/*"
    }

    try:
        r = requests.get(url, headers=headers, timeout=5)
        res_headers = r.headers

        security_headers = [
            "Content-Security-Policy",
            "Strict-Transport-Security",
            "X-Frame-Options"
        ]

        missing = [h for h in security_headers if h not in res_headers]

        if r.status_code == 400:
            status_msg = "REJECTED (WAF likely)"
        elif r.status_code in [403, 429]:
            status_msg = "BLOCKED"
        elif r.status_code == 200:
            status_msg = "SUCCESS"
        else:
            status_msg = "UNKNOWN"

        return {
            "url": url,
            "status": r.status_code,
            "status_msg": status_msg,
            "server": res_headers.get("Server", "Unknown"),
            "missing_headers": missing
        }

    except Exception as e:
        return {
            "error": str(e)
        }
