from flask import Flask, request, render_template_string
from scanner import scan

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>PentraSec</title>
</head>
<body>
<h1>PentraSec Scanner</h1>

<form method="POST">
    <input name="url" placeholder="Enter URL">
    <button type="submit">Scan</button>
</form>

{% if result %}
<pre>{{ result }}</pre>
{% endif %}

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        url = request.form.get("url", "").strip()
        if url:
            result = scan(url)

    return render_template_string(HTML, result=result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
