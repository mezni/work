import os
import json
from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "tasks.json")

def load_tasks():
    if not os.path.exists(DATA_FILE):
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, "w") as f:
            json.dump({"toDo": [], "inProgress": [], "done": []}, f)
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

@app.route("/")
def index():
    tasks = load_tasks()
    return render_template("index.html", tasks=tasks)

@app.route("/api/tasks", methods=["GET"])
def api_tasks():
    return jsonify(load_tasks())

@app.route("/api/tasks", methods=["POST"])
def api_add_task():
    data = request.get_json()
    text = data.get("text", "").strip()
    column = data.get("column", "toDo")

    if not text:
        return jsonify({"error": "Task text is required"}), 400

    tasks = load_tasks()
    all_ids = []
    for col_tasks in tasks.values():
        for task in col_tasks:
            if isinstance(task.get("id"), str) and task["id"].isdigit():
                all_ids.append(int(task["id"]))
    new_id = max(all_ids, default=0) + 1

    task = {"id": str(new_id), "text": text, "column": column}
    tasks[column].append(task)
    save_tasks(tasks)
    return jsonify(task), 201

@app.route("/api/tasks/<task_id>", methods=["PUT"])
def api_update_task(task_id):
    data = request.get_json()
    new_column = data.get("column")

    tasks = load_tasks()
    found = False
    for column, col_tasks in tasks.items():
        for task in col_tasks:
            if task["id"] == task_id:
                if new_column and task["column"] != new_column:
                    task["column"] = new_column
                found = True
                break
        if found:
            break

    if found:
        save_tasks(tasks)
        return jsonify({"success": True})
    return jsonify({"error": "Task not found"}), 404

@app.route("/api/tasks/<task_id>", methods=["DELETE"])
def api_delete_task(task_id):
    tasks = load_tasks()
    original_count = sum(len(col) for col in tasks.values())

    tasks = {col: [t for t in col_tasks if t["id"] != task_id] for col, col_tasks in tasks.items()}

    if sum(len(col) for col in tasks.values()) < original_count:
        save_tasks(tasks)
        return jsonify({"success": True})
    return jsonify({"error": "Task not found"}), 404

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
