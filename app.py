from flask import Flask, request, render_template_string
from scanner import scan

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>PentraSec Scanner</title>

    <style>
        body {
            background-color: #0d0d0d;
            color: #00ff88;
            font-family: monospace;
            padding: 30px;
        }

        h1 {
            color: #00ff88;
            text-shadow: 0 0 10px #00ff88;
        }

        input {
            background: black;
            border: 1px solid #00ff88;
            color: #00ff88;
            padding: 10px;
            width: 300px;
        }

        button {
            background: #00ff88;
            border: none;
            padding: 10px 15px;
            cursor: pointer;
            font-weight: bold;
        }

        .box {
            margin-top: 20px;
            padding: 15px;
            border: 1px solid #00ff88;
            background: #111;
        }

        .error {
            color: red;
        }

        ul {
            list-style: none;
            padding-left: 0;
        }

        li::before {
            content: "⚠ ";
        }
    </style>
</head>

<body>

<h1>☠ PentraSec Scanner</h1>

<form method="POST">
    <input name="url" placeholder="Enter target (example.com)">
    <button type="submit">SCAN</button>
</form>

{% if result %}
<div class="box">

    {% if result.error %}
        <p class="error">ERROR: {{ result.error }}</p>
    {% else %}
        <p>Target: {{ result.url }}</p>
        <p>Status: {{ result.status }} | {{ result.status_msg }}</p>
        <p>Server: {{ result.server }}</p>

        <h3>Missing Security Headers</h3>
        {% if result.missing_headers %}
            <ul>
            {% for h in result.missing_headers %}
                <li>{{ h }}</li>
            {% endfor %}
            </ul>
        {% else %}
            <p>No missing headers detected ✔</p>
        {% endif %}

    {% endif %}

</div>
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
