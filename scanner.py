import requests
import time

def scan(url):
    if not url.startswith("http"):
        url = "https://" + url

    print(f"\nScanning: {url}\n")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9"
    }

    session = requests.Session()
    session.headers.update(headers)

    try:
        time.sleep(1)

        r = session.get(url, timeout=5, allow_redirects=True)
        headers = r.headers

        print("Status Code:", r.status_code)

        # Status classification
        if r.status_code == 400:
            print("REJECTED (likely WAF / bot protection)")

        elif r.status_code in [403, 429]:
            print("BLOCKED (access denied or rate limited)")

        elif r.status_code == 200:
            print("SUCCESS (accessible)")

        else:
            print("UNKNOWN RESPONSE")

        # 🔥 PentraSec insight message (professional + curiosity-driven)
        print("\n--- PentraSec Insight ---")
        print("Modern web applications often contain hidden misconfigurations,")
        print("exposed endpoints, or access control gaps that are not visible")
        print("through surface-level checks or automated scanning alone.")
        print("A focused manual security review helps uncover real-world risk\n")

        security_headers = [
            "Content-Security-Policy",
            "Strict-Transport-Security",
            "X-Frame-Options"
        ]

        print("Missing Security Headers:")
        for h in security_headers:
            if h not in headers:
                print("-", h)

        print("\nServer:", headers.get("Server", "Unknown"))

    except requests.exceptions.RequestException:
        print("\nBLOCKED / UNREACHABLE (possible WAF or network restriction)")

        # Even on failure, still show professional insight
        print("\n--- PentraSec Insight ---")
        print("Some applications actively filter automated traffic or restrict access.")
        print("This does not always indicate absence of risk — only that deeper testing may be required.")

if __name__ == "__main__":
    target = input("Enter URL: ")
    scan(target)
