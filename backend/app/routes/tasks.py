from flask import Blueprint, jsonify, request, current_app
from marshmallow import ValidationError
from ..database import db
from ..models import Task, Tag, TaskStatus, Priority
from ..schemas import TaskCreateSchema, TaskUpdateSchema, TaskFilterSchema
from ..services.ai_service import suggest_priority

tasks_bp = Blueprint("tasks", __name__)
create_schema = TaskCreateSchema()
update_schema = TaskUpdateSchema()
filter_schema = TaskFilterSchema()


def _resolve_tags(tag_ids: list[int]) -> tuple[list[Tag], list[str]]:
    """Return (found_tags, error_messages)."""
    tags, errors = [], []
    for tid in tag_ids:
        tag = db.session.get(Tag, tid)
        if tag is None:
            errors.append(f"Tag id={tid} not found.")
        else:
            tags.append(tag)
    return tags, errors


@tasks_bp.get("/")
def list_tasks():
    try:
        filters = filter_schema.load(request.args)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 422

    query = Task.query

    if filters.get("status"):
        query = query.filter(Task.status == TaskStatus(filters["status"]))
    if filters.get("priority"):
        query = query.filter(Task.priority == Priority(filters["priority"]))
    if filters.get("tag_id"):
        query = query.filter(Task.tags.any(Tag.id == filters["tag_id"]))
    if filters.get("search"):
        term = f"%{filters['search']}%"
        query = query.filter(
            db.or_(Task.title.ilike(term), Task.description.ilike(term))
        )

    query = query.order_by(Task.created_at.desc())
    pagination = query.paginate(page=filters["page"], per_page=filters["per_page"], error_out=False)

    return jsonify({
        "items": [t.to_dict() for t in pagination.items],
        "total": pagination.total,
        "page": pagination.page,
        "pages": pagination.pages,
        "per_page": pagination.per_page,
    })


@tasks_bp.post("/")
def create_task():
    try:
        data = create_schema.load(request.get_json(force=True) or {})
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 422

    tags, tag_errors = _resolve_tags(data.get("tag_ids", []))
    if tag_errors:
        return jsonify({"errors": {"tag_ids": tag_errors}}), 422

    priority = data["priority"]
    ai_reason = None

    if data.get("use_ai_priority"):
        api_key = current_app.config.get("OPENAI_API_KEY", "")
        priority, ai_reason = suggest_priority(
            title=data["title"],
            description=data.get("description"),
            due_date=data.get("due_date"),
            api_key=api_key,
        )
        current_app.logger.info("AI priority suggestion: %s — %s", priority, ai_reason)

    task = Task(
        title=data["title"],
        description=data.get("description"),
        status=TaskStatus(data["status"]),
        priority=Priority(priority),
        ai_priority_reason=ai_reason,
        due_date=data.get("due_date"),
        tags=tags,
    )
    db.session.add(task)
    db.session.commit()
    current_app.logger.info("Created task id=%s title=%s", task.id, task.title)
    return jsonify(task.to_dict()), 201


@tasks_bp.get("/<int:task_id>")
def get_task(task_id: int):
    task = db.session.get(Task, task_id)
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task.to_dict())


@tasks_bp.patch("/<int:task_id>")
def update_task(task_id: int):
    task = db.session.get(Task, task_id)
    if task is None:
        return jsonify({"error": "Task not found"}), 404

    try:
        data = update_schema.load(request.get_json(force=True) or {})
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 422

    if "tag_ids" in data:
        tags, tag_errors = _resolve_tags(data["tag_ids"])
        if tag_errors:
            return jsonify({"errors": {"tag_ids": tag_errors}}), 422
        task.tags = tags

    if data.get("use_ai_priority"):
        api_key = current_app.config.get("OPENAI_API_KEY", "")
        title = data.get("title", task.title)
        description = data.get("description", task.description)
        due_date = data.get("due_date", task.due_date)
        priority, ai_reason = suggest_priority(title, description, due_date, api_key)
        task.priority = Priority(priority)
        task.ai_priority_reason = ai_reason
    else:
        if "priority" in data:
            task.priority = Priority(data["priority"])
            task.ai_priority_reason = None  # clear AI reason on manual override

    for field in ("title", "description", "due_date"):
        if field in data:
            setattr(task, field, data[field])
    if "status" in data:
        task.status = TaskStatus(data["status"])

    db.session.commit()
    current_app.logger.info("Updated task id=%s", task_id)
    return jsonify(task.to_dict())


@tasks_bp.delete("/<int:task_id>")
def delete_task(task_id: int):
    task = db.session.get(Task, task_id)
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    db.session.delete(task)
    db.session.commit()
    current_app.logger.info("Deleted task id=%s", task_id)
    return "", 204
