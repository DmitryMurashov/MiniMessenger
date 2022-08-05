from django.db import models
from typing import Type
from djangochannelsrestframework.observer import ModelObserver
from functools import wraps
from utils.sync_to_async import sync_to_async_get


def event_handler(model: Type[models.Model], selected_action: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(customer, message: dict, action: str, **kwargs):
            if selected_action == action:
                instance = await sync_to_async_get(model, id=message['pk'])
                return await func(customer, instance, **{'message': message, 'model_action': action, **kwargs})
        return ModelObserver(wrapper, model)
    return decorator
