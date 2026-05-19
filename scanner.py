import requests

def scan(url):
    if not url.startswith("http"):
        url = "https://" + url

    print(f"\nScanning: {url}\n")

    try:
        r = requests.get(url, timeout=5)
        headers = r.headers

        print("Status Code:", r.status_code)

        security_headers = [
            "Content-Security-Policy",
            "Strict-Transport-Security",
            "X-Frame-Options"
        ]

        print("\nMissing Security Headers:")
        for h in security_headers:
            if h not in headers:
                print("-", h)

        print("\nServer:", headers.get("Server", "Unknown"))

    except requests.exceptions.RequestException:
        print("BLOCKED / UNREACHABLE (possible WAF or network restriction)")


if __name__ == "__main__":
    target = input("Enter URL: ")
    scan(target)
