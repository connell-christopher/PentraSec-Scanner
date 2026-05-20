import requests
import urllib3

# hides insecure SSL warnings (only for cleaner output)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def scan(url):
    if not url.startswith("http"):
        url = "https://" + url

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "*/*"
    }

    try:
        r = requests.get(url, headers=headers, timeout=6)

        res_headers = r.headers

        security_headers = [
            "Content-Security-Policy",
            "Strict-Transport-Security",
            "X-Frame-Options"
        ]

        missing = [h for h in security_headers if h not in res_headers]

        # status classification
        if r.status_code == 200:
            status_msg = "SUCCESS"
            risk = "LOW"

        elif r.status_code == 400:
            status_msg = "REJECTED (WAF likely)"
            risk = "MEDIUM"

        elif r.status_code in [403, 429]:
            status_msg = "BLOCKED"
            risk = "MEDIUM"

        else:
            status_msg = "UNKNOWN"
            risk = "LOW"

        return {
            "url": url,
            "status": r.status_code,
            "status_msg": status_msg,
            "risk": risk,
            "server": res_headers.get("Server", "Unknown"),
            "missing_headers": missing
        }

    except requests.exceptions.SSLError:
        return {
            "url": url,
            "status": "SSL_ERROR",
            "status_msg": "SSL CERTIFICATE ERROR",
            "risk": "HIGH",
            "server": "UNKNOWN",
            "missing_headers": [],
            "note": "Certificate verification failed (invalid or incomplete SSL chain)"
        }

    except requests.exceptions.Timeout:
        return {
            "url": url,
            "status": "TIMEOUT",
            "status_msg": "REQUEST TIMEOUT",
            "risk": "MEDIUM",
            "server": "UNKNOWN",
            "missing_headers": []
        }

    except requests.exceptions.RequestException as e:
        return {
            "url": url,
            "status": "ERROR",
            "status_msg": "REQUEST FAILED",
            "risk": "MEDIUM",
            "server": "UNKNOWN",
            "missing_headers": [],
            "error": str(e)
        }
