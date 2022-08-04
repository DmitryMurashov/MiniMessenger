from django.db import models
from typing import Type
from channels.db import database_sync_to_async
from rest_framework.serializers import Serializer


@database_sync_to_async
def sync_to_async_get(model: Type[models.Model], **kwargs) -> models.Model:
    return model.objects.get(**kwargs)


@database_sync_to_async
def sync_to_async_filter(model: Type[models.Model], **kwargs) -> models.QuerySet:
    return model.objects.filter(**kwargs)


@database_sync_to_async
def sync_to_async_exists(model: Type[models.Model], **kwargs) -> bool:
    return model.objects.filter(**kwargs).exists()


@database_sync_to_async
def sync_to_async_serialize(instance: models.Model, serializer: Type[Serializer]) -> dict:
    return serializer(instance=instance).data

