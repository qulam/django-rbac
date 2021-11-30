from rest_framework import serializers
from rest_framework.decorators import api_view as drf_api_view
from types import MethodType
from typing import Optional, List, Callable, Any


def default_response(status, status_code, message, data):
    return {
        "success": status,
        "status_code": status_code,
        "message": message,
        "data": data
    }


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


Function = Callable[..., Any]


def api_view(
        http_method_names: Optional[List[str]] = None,
        use_serializer: Optional[serializers.BaseSerializer] = None
) -> Function:
    if use_serializer is None:
        return drf_api_view(http_method_names)

    def api_view_deco_wrap(view: Function) -> Function:
        nonlocal http_method_names, use_serializer

        decorated_view = drf_api_view(http_method_names)(view)

        if use_serializer:
            decorated_view.cls.get_serializer = \
                MethodType(lambda s: use_serializer(), decorated_view.cls)

        return decorated_view

    return api_view_deco_wrap
