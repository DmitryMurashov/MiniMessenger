from django.db import models
from dataclasses import dataclass
from rest_framework.serializers import ModelSerializer
from typing import Type, Union


@dataclass
class Event:
    event_type: str
    instance: models.Model
    serializer_class: Type[ModelSerializer]

    def serialize(self) -> dict:
        return {
            'event_type': self.event_type,
            'instance': self.serializer_class(instance=self.instance).data
        }


class EventManager:
    def __init__(self, accepted_events: list):
        self.accepted_events = accepted_events
        self.last_events = []

    def add(self, event: Event) -> None:
        assert event.event_type in self.accepted_events
        self.last_events.append(event)

    def get_events(self) -> list:
        events = self.last_events[:]
        self.last_events.clear()
        return [event.serialize() for event in events]

    def get_last_event(self) -> Union[Event, None]:
        if self.last_events:
            return self.last_events.pop()
