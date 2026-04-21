from datetime import datetime
from typing import Optional
from marshmallow import Schema, fields, validate, validates, ValidationError, EXCLUDE


VALID_STATUSES = ["todo", "in_progress", "done"]
VALID_PRIORITIES = ["low", "medium", "high", "critical"]
HEX_COLOR_REGEX = r"^#[0-9A-Fa-f]{6}$"


class TagSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    color = fields.Str(
        load_default="#6366f1",
        validate=validate.Regexp(HEX_COLOR_REGEX, error="Color must be a valid hex code like #aabbcc"),
    )


class TaskCreateSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    title = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    description = fields.Str(load_default=None, allow_none=True)
    status = fields.Str(
        load_default="todo",
        validate=validate.OneOf(VALID_STATUSES),
    )
    priority = fields.Str(
        load_default="medium",
        validate=validate.OneOf(VALID_PRIORITIES),
    )
    due_date = fields.DateTime(load_default=None, allow_none=True)
    tag_ids = fields.List(fields.Int(), load_default=[])
    use_ai_priority = fields.Bool(load_default=False)


class TaskUpdateSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    title = fields.Str(validate=validate.Length(min=1, max=200))
    description = fields.Str(allow_none=True)
    status = fields.Str(validate=validate.OneOf(VALID_STATUSES))
    priority = fields.Str(validate=validate.OneOf(VALID_PRIORITIES))
    due_date = fields.DateTime(allow_none=True)
    tag_ids = fields.List(fields.Int())
    use_ai_priority = fields.Bool()


class TaskFilterSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    status = fields.Str(validate=validate.OneOf(VALID_STATUSES + [""]))
    priority = fields.Str(validate=validate.OneOf(VALID_PRIORITIES + [""]))
    tag_id = fields.Int()
    search = fields.Str()
    page = fields.Int(load_default=1, validate=validate.Range(min=1))
    per_page = fields.Int(load_default=20, validate=validate.Range(min=1, max=100))
