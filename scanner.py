import requests

def scan(url):
    if not url.startswith("http"):
        url = "https://" + url

    try:
        r = requests.get(url, timeout=5)
        h = r.headers

        security_headers = [
            "Content-Security-Policy",
            "Strict-Transport-Security",
            "X-Frame-Options"
        ]

        missing = [x for x in security_headers if x not in h]

        status_msg = (
            "REJECTED" if r.status_code == 400 else
            "BLOCKED" if r.status_code in [403, 429] else
            "SUCCESS" if r.status_code == 200 else
            "UNKNOWN"
        )

        return {
            "url": url,
            "status": r.status_code,
            "status_msg": status_msg,
            "server": h.get("Server", "Unknown"),
            "missing_headers": missing
        }

    except Exception as e:
        return {"error": str(e)}
