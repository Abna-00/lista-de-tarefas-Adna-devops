"""API REST de Lista de Tarefas."""
from flask import Flask, jsonify, request


def create_app():
    app = Flask(__name__)
    tasks = {}
    counter = {"next_id": 1}

    @app.get("/health")
    def health():
        return jsonify(status="ok")

    @app.post("/tasks")
    def create_task():
        data = request.get_json(silent=True) or {}
        title = (data.get("title") or "").strip()
        if not title:
            return jsonify(error="O campo 'title' é obrigatório"), 400
        task = {
            "id": counter["next_id"],
            "title": title,
            "description": data.get("description", ""),
            "done": False,
        }
        tasks[task["id"]] = task
        counter["next_id"] += 1
        return jsonify(task), 201

    @app.get("/tasks")
    def list_tasks():
        done = request.args.get("done")
        result = list(tasks.values())
        if done is not None:
            flag = done.lower() == "true"
            result = [t for t in result if t["done"] == flag]
        return jsonify(result)

    @app.get("/tasks/<int:task_id>")
    def get_task(task_id):
        task = tasks.get(task_id)
        if task is None:
            return jsonify(error="Tarefa não encontrada"), 404
        return jsonify(task)

    @app.put("/tasks/<int:task_id>")
    def update_task(task_id):
        task = tasks.get(task_id)
        if task is None:
            return jsonify(error="Tarefa não encontrada"), 404
        data = request.get_json(silent=True) or {}
        if "title" in data:
            title = (data["title"] or "").strip()
            if not title:
                return jsonify(error="O campo 'title' não pode ser vazio"), 400
            task["title"] = title
        if "description" in data:
            task["description"] = data["description"]
        if "done" in data:
            task["done"] = bool(data["done"])
        return jsonify(task)

    @app.post("/tasks/<int:task_id>/complete")
    def complete_task(task_id):
        task = tasks.get(task_id)
        if task is None:
            return jsonify(error="Tarefa não encontrada"), 404
        task["done"] = True
        return jsonify(task)

    @app.delete("/tasks/<int:task_id>")
    def delete_task(task_id):
        if tasks.pop(task_id, None) is None:
            return jsonify(error="Tarefa não encontrada"), 404
        return "", 204

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
