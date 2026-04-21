from flask import Blueprint, jsonify, request, current_app
from marshmallow import ValidationError
from ..database import db
from ..models import Tag
from ..schemas import TagSchema

tags_bp = Blueprint("tags", __name__)
tag_schema = TagSchema()


@tags_bp.get("/")
def list_tags():
    tags = Tag.query.order_by(Tag.name).all()
    return jsonify([t.to_dict() for t in tags])


@tags_bp.post("/")
def create_tag():
    try:
        data = tag_schema.load(request.get_json(force=True) or {})
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 422

    if Tag.query.filter_by(name=data["name"]).first():
        return jsonify({"errors": {"name": ["Tag name already exists."]}}), 409

    tag = Tag(name=data["name"], color=data["color"])
    db.session.add(tag)
    db.session.commit()
    current_app.logger.info("Created tag id=%s name=%s", tag.id, tag.name)
    return jsonify(tag.to_dict()), 201


@tags_bp.delete("/<int:tag_id>")
def delete_tag(tag_id: int):
    tag = db.session.get(Tag, tag_id)
    if tag is None:
        return jsonify({"error": "Tag not found"}), 404
    db.session.delete(tag)
    db.session.commit()
    current_app.logger.info("Deleted tag id=%s", tag_id)
    return "", 204
