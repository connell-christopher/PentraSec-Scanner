from flask import Flask, render_template, request
import requests
import time

app = Flask(__name__)

def scan_site(url):
    if not url.startswith("http"):
        url = "https://" + url

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "*/*"
    }

    time.sleep(1)

    try:
        r = requests.get(url, headers=headers, timeout=5)
        res_headers = r.headers

        result = {
            "url": url,
            "status": r.status_code,
            "server": res_headers.get("Server", "Unknown"),
            "missing_headers": []
        }

        security_headers = [
            "Content-Security-Policy",
            "Strict-Transport-Security",
            "X-Frame-Options"
        ]

        for h in security_headers:
            if h not in res_headers:
                result["missing_headers"].append(h)

        return result

    except Exception as e:
        return {
            "url": url,
            "error": str(e)
        }

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        url = request.form["url"]
        result = scan_site(url)

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
