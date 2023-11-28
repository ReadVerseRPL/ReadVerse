from functools import wraps
import typing as t
from flask import Response, jsonify, request
from pydantic import BaseModel, ValidationError

from werkzeug.datastructures import MultiDict

P = t.ParamSpec("P")
K = t.TypeVar("K")
V = t.TypeVar("V")
TResponse = t.TypeVar("TResponse")
ValidateModel = t.Type[BaseModel] | None


def multidict_to_dict(multidict: MultiDict[K, V]) -> dict[K, list[V] | V]:
    obj: dict[K, list[V] | V] = {}
    for key, val in multidict.lists():
        obj[key] = val
        if len(val) == 1:
            obj[key] = val[0]

    return obj


def validate(f: t.Callable[P, TResponse]):
    types = t.get_type_hints(f)
    form_model: ValidateModel = types.get("form")
    query_model: ValidateModel = types.get("query")
    json_model: ValidateModel = types.get("json")

    @wraps(f)
    def inner(*args: P.args, **kwargs: P.kwargs):
        try:
            if form_model:
                kwargs["form"] = form_model.model_validate(
                    multidict_to_dict(request.form)
                )

            if query_model:
                kwargs["query"] = query_model.model_validate(
                    multidict_to_dict(request.args)
                )

            if json_model:
                kwargs["json"] = json_model.model_validate_json(request.data)
        except ValidationError as e:
            return jsonify(e.errors()), 400

        return f(*args, **kwargs)

    return inner
