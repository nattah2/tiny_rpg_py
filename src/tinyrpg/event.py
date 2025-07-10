#!/usr/bin/env python3

from dataclasses import dataclass
from typing import Callable, Type, TypeVar, Dict, List, Any, Optional
# from tinyrpg import effect

# Base event class
class Event:
    pass

# Type variable for event types
E = TypeVar('E', bound=Event)

class EventEmitter:
    def __init__(self):
        # Maps event types to their handlers
        self._handlers: Dict[Type[Event], List[Callable]] = {}
        self._once_handlers: Dict[Type[Event], List[Callable]] = {}

    def on(self, event_type: Type[E], handler: Callable[[E], None]):
        """Register a persistent handler for an event type"""
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    def once(self, event_type: Type[E], handler: Callable[[E], None]):
        """Register a one-time handler for an event type"""
        if event_type not in self._once_handlers:
            self._once_handlers[event_type] = []
        self._once_handlers[event_type].append(handler)

    def emit(self, event: E):
        """Dispatch an event to all registered handlers"""
        event_type = type(event)

        # Call persistent handlers
        if event_type in self._handlers:
            for handler in self._handlers[event_type]:
                handler(event)

        # Call one-time handlers and clear them
        if event_type in self._once_handlers:
            handlers = self._once_handlers[event_type][:]
            self._once_handlers[event_type].clear()
            for handler in handlers:
                handler(event)

    def off(self, event_type: Type[E], handler: Callable[[E], None]):
        """Unregister a handler for an event type"""
        if event_type in self._handlers and handler in self._handlers[event_type]:
            self._handlers[event_type].remove(handler)

@dataclass
class onTurnBegin(Event):
    cycle_counter: int


@dataclass
class onTurnEnd(Event):
    cycle_counter: int

@dataclass
class onAttackDeclaration(Event):
    pass

@dataclass
class onDamage(Event):
    pass

@dataclass
class onBegin(Event):
    cycle_counter: int

@dataclass
class onCycleEnd(Event):
    cycle_counter: int

@dataclass
class onApply(Event):
    cycle_counter: int
