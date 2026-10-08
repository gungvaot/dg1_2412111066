import json
import os
from flask import Flask, render_template, jsonify, request, abort

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "students.json")

MSSV = "2412111066"
HO_TEN = "Ngo Xuan Loc"      # <-- sua thanh ho ten that

app = Flask(__name__, static_folder="static", template_folder="templates")
//yaboi

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


@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "student": MSSV})


@app.route("/api/students")
def list_students():
    students = load_students()
    lop = request.args.get("lop")
    if lop:
        students = [s for s in students if s["lop"].lower() == lop.lower()]
    return jsonify(students)


@app.route("/api/students/<int:student_id>")
def get_student(student_id):
    for s in load_students():
        if s["id"] == student_id:
            return jsonify(s)
    return jsonify({"error": "Student not found"}), 404


@app.route("/api/students", methods=["POST"])
def create_student():
    data = request.get_json(silent=True)
    required = ["mssv", "ho_ten", "lop", "diem"]
    if not isinstance(data, dict) or any(k not in data for k in required):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        diem = float(data["diem"])
    except (TypeError, ValueError):
        return jsonify({"error": "diem must be a number"}), 400
    if not 0 <= diem <= 10:
        return jsonify({"error": "diem must be between 0 and 10"}), 400

    students = load_students()
    new_id = max((s["id"] for s in students), default=0) + 1
    student = {
        "id": new_id,
        "mssv": str(data["mssv"]),
        "ho_ten": str(data["ho_ten"]),
        "lop": str(data["lop"]),
        "diem": diem,
    }
    students.append(student)
    save_students(students)
    return jsonify(student), 201


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
