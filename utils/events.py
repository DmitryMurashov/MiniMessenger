from django.db import models
from typing import Type
from djangochannelsrestframework.observer import ModelObserver
from functools import wraps
from rest_framework.serializers import Serializer


def event_handler(model: Type[models.Model], serializer_class: Type[Serializer], selected_action: str = None):
    def decorator(func):
        @wraps(func)
        async def wrapper(customer, *args, **kwargs):
            if not selected_action or selected_action == kwargs.get("action"):
                return await func(customer, *args, **kwargs)

        def serialize(customer, instance, action, **_):
            return {
                'event': func.__name__.replace('_', "."),
                'object': serializer_class(instance=instance).data,
                'db_action': action.value
            }

        observer = ModelObserver(wrapper, model)
        observer.serializer(serialize)
        return observer
    return decorator
