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
    {% if result.error %}
        <p style="color:red">{{ result.error }}</p>
    {% else %}
        <p><b>URL:</b> {{ result.url }}</p>
        <p><b>Status:</b> {{ result.status }} - {{ result.status_msg }}</p>
        <p><b>Server:</b> {{ result.server }}</p>

        <h3>Missing Headers</h3>
        <ul>
        {% for h in result.missing_headers %}
            <li>{{ h }}</li>
        {% endfor %}
        </ul>
    {% endif %}
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
