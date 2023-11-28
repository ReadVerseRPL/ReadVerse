from functools import wraps
import typing as t
from flask import Response, jsonify, request
from pydantic import BaseModel, ValidationError

P = t.ParamSpec("P")
TResponse = t.TypeVar("TResponse")
ValidateModel = t.Type[BaseModel] | None


def validate(f: t.Callable[P, TResponse]):
    types = t.get_type_hints(f)
    form_model: ValidateModel = types.get("form")
    query_model: ValidateModel = types.get("query")
    json_model: ValidateModel = types.get("json")

    @wraps(f)
    def inner(*args: P.args, **kwargs: P.kwargs):
        try:
            if form_model:
                kwargs["form"] = form_model(**request.form)

            if query_model:
                kwargs["query"] = query_model(**request.args)

            if json_model:
                kwargs["json"] = json_model.model_validate_json(request.data)
        except ValidationError as e:
            return jsonify(e.errors()), 400

        return f(*args, **kwargs)

    return inner
