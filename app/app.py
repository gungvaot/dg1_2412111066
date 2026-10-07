import json
import os
from flask import Flask, render_template, jsonify, request, abort

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "students.json")

MSSV = "2412111066"
HO_TEN = "Ngo Xuan Loc"      # <-- sua thanh ho ten that

app = Flask(__name__, static_folder="static", template_folder="templates")


def load_students():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_students(students):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(students, f, ensure_ascii=False, indent=2)


@app.route("/")
def index():
    title = f"DG1 – {HO_TEN} – {MSSV}"
    return render_template("index.html", title=title, students=load_students())


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
