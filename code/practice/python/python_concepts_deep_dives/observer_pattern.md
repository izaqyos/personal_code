# Observer Pattern (Observable) in Python

**Purpose**: A behavioral design pattern where an object (subject/observable) maintains a list of dependents (observers) and notifies them automatically of state changes.

**Also Known As**: Publish-Subscribe, Event-Subscriber, Listener

---

## Table of Contents

1. [When to Use](#when-to-use)
2. [Basic Implementation](#basic-implementation)
3. [Real-World Examples](#real-world-examples)
4. [Advanced Patterns](#advanced-patterns)
5. [Python-Specific Implementations](#python-specific-implementations)
6. [Comparison with Other Patterns](#comparison-with-other-patterns)
7. [Common Pitfalls](#common-pitfalls)
8. [Best Practices](#best-practices)

---

## When to Use

### Use Observer Pattern When:
- Changes in one object require changing others, and you don't know how many objects need to change
- An object should notify other objects without making assumptions about who those objects are
- You need a broadcast communication mechanism
- You want loose coupling between objects

### Real-World Analogies:
- **Newsletter subscription**: Subscribers get notified when new content is published
- **Stock ticker**: Multiple displays update when stock prices change
- **Event systems**: GUI buttons notify handlers when clicked

---

## Basic Implementation

### Minimal Example

```python
from abc import ABC, abstractmethod
from typing import List


class Observer(ABC):
    """Abstract observer interface."""
    
    @abstractmethod
    def update(self, subject: 'Subject') -> None:
        """Called when the subject state changes."""
        pass


class Subject:
    """Observable that maintains a list of observers."""
    
    def __init__(self):
        self._observers: List[Observer] = []
        self._state: str = ""
    
    def attach(self, observer: Observer) -> None:
        """Subscribe an observer."""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer: Observer) -> None:
        """Unsubscribe an observer."""
        self._observers.remove(observer)
    
    def notify(self) -> None:
        """Notify all observers of state change."""
        for observer in self._observers:
            observer.update(self)
    
    @property
    def state(self) -> str:
        return self._state
    
    @state.setter
    def state(self, value: str) -> None:
        self._state = value
        self.notify()  # Auto-notify on state change


# Concrete observers
class LoggingObserver(Observer):
    def update(self, subject: Subject) -> None:
        print(f"[LOG] State changed to: {subject.state}")


class AlertObserver(Observer):
    def update(self, subject: Subject) -> None:
        if "error" in subject.state.lower():
            print(f"[ALERT] Error detected: {subject.state}")


# Usage
subject = Subject()
logger = LoggingObserver()
alerter = AlertObserver()

subject.attach(logger)
subject.attach(alerter)

subject.state = "System started"     # Only logger reacts
subject.state = "Error: DB failed"   # Both react
subject.state = "System recovered"   # Only logger reacts

# Output:
# [LOG] State changed to: System started
# [LOG] State changed to: Error: DB failed
# [ALERT] Error detected: Error: DB failed
# [LOG] State changed to: System recovered
```

---

## Real-World Examples

### Example 1: Stock Price Monitor

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class StockPrice:
    symbol: str
    price: float
    change: float


class StockObserver(ABC):
    @abstractmethod
    def on_price_update(self, stock: StockPrice) -> None:
        pass


class StockExchange:
    """Observable stock exchange."""
    
    def __init__(self):
        self._stocks: Dict[str, float] = {}
        self._observers: List[StockObserver] = []
    
    def subscribe(self, observer: StockObserver) -> None:
        self._observers.append(observer)
    
    def unsubscribe(self, observer: StockObserver) -> None:
        self._observers.remove(observer)
    
    def update_price(self, symbol: str, new_price: float) -> None:
        old_price = self._stocks.get(symbol, new_price)
        self._stocks[symbol] = new_price
        
        change = ((new_price - old_price) / old_price * 100) if old_price else 0
        stock = StockPrice(symbol, new_price, change)
        
        # Notify all observers
        for observer in self._observers:
            observer.on_price_update(stock)


class PriceDisplay(StockObserver):
    """Displays current prices."""
    
    def __init__(self, name: str):
        self.name = name
    
    def on_price_update(self, stock: StockPrice) -> None:
        direction = "↑" if stock.change > 0 else "↓" if stock.change < 0 else "→"
        print(f"[{self.name}] {stock.symbol}: ${stock.price:.2f} {direction} ({stock.change:+.2f}%)")


class AlertSystem(StockObserver):
    """Alerts on significant price movements."""
    
    def __init__(self, threshold: float = 5.0):
        self.threshold = threshold
    
    def on_price_update(self, stock: StockPrice) -> None:
        if abs(stock.change) >= self.threshold:
            print(f"⚠️ ALERT: {stock.symbol} moved {stock.change:+.2f}% - significant movement!")


class TradingBot(StockObserver):
    """Automated trading based on price changes."""
    
    def __init__(self, buy_threshold: float = -3.0, sell_threshold: float = 3.0):
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold
    
    def on_price_update(self, stock: StockPrice) -> None:
        if stock.change <= self.buy_threshold:
            print(f"🤖 BOT: BUY signal for {stock.symbol} (dropped {stock.change:.2f}%)")
        elif stock.change >= self.sell_threshold:
            print(f"🤖 BOT: SELL signal for {stock.symbol} (gained {stock.change:.2f}%)")


# Usage
exchange = StockExchange()

display = PriceDisplay("Main Board")
alerts = AlertSystem(threshold=5.0)
bot = TradingBot(buy_threshold=-3.0, sell_threshold=4.0)

exchange.subscribe(display)
exchange.subscribe(alerts)
exchange.subscribe(bot)

print("=== Stock Market Updates ===\n")
exchange.update_price("AAPL", 150.00)
exchange.update_price("AAPL", 145.50)  # -3% drop
exchange.update_price("AAPL", 153.00)  # +5.1% gain
exchange.update_price("GOOGL", 2800.00)
exchange.update_price("GOOGL", 2650.00)  # -5.3% drop
```

### Example 2: Event System for GUI/Applications

```python
from collections import defaultdict
from typing import Callable, Dict, List, Any


class EventEmitter:
    """
    A flexible event system similar to Node.js EventEmitter.
    Supports multiple event types with multiple listeners each.
    """
    
    def __init__(self):
        self._listeners: Dict[str, List[Callable]] = defaultdict(list)
        self._once_listeners: Dict[str, List[Callable]] = defaultdict(list)
    
    def on(self, event: str, callback: Callable) -> 'EventEmitter':
        """Subscribe to an event."""
        self._listeners[event].append(callback)
        return self  # Allow chaining
    
    def once(self, event: str, callback: Callable) -> 'EventEmitter':
        """Subscribe to an event, but only fire once."""
        self._once_listeners[event].append(callback)
        return self
    
    def off(self, event: str, callback: Callable) -> 'EventEmitter':
        """Unsubscribe from an event."""
        if callback in self._listeners[event]:
            self._listeners[event].remove(callback)
        return self
    
    def emit(self, event: str, *args, **kwargs) -> None:
        """Emit an event to all listeners."""
        # Regular listeners
        for callback in self._listeners[event]:
            callback(*args, **kwargs)
        
        # One-time listeners
        once = self._once_listeners[event]
        self._once_listeners[event] = []
        for callback in once:
            callback(*args, **kwargs)
    
    def listener_count(self, event: str) -> int:
        """Get number of listeners for an event."""
        return len(self._listeners[event]) + len(self._once_listeners[event])


# Usage: User Authentication System
class AuthService(EventEmitter):
    def __init__(self):
        super().__init__()
        self._logged_in_user = None
    
    def login(self, username: str, password: str) -> bool:
        # Simulate authentication
        if password == "secret":  # Demo only!
            self._logged_in_user = username
            self.emit("login", username=username)
            return True
        else:
            self.emit("login_failed", username=username, reason="Invalid password")
            return False
    
    def logout(self) -> None:
        user = self._logged_in_user
        self._logged_in_user = None
        self.emit("logout", username=user)


# Event handlers
def log_login(username: str):
    print(f"📝 Audit: User '{username}' logged in at {__import__('datetime').datetime.now()}")

def send_welcome_email(username: str):
    print(f"📧 Sending welcome email to {username}")

def update_last_login(username: str):
    print(f"💾 Updated last_login for {username}")

def alert_failed_login(username: str, reason: str):
    print(f"⚠️ SECURITY: Failed login for '{username}': {reason}")

def goodbye_message(username: str):
    print(f"👋 Goodbye {username}!")


# Wire up the system
auth = AuthService()
auth.on("login", log_login)
auth.on("login", send_welcome_email)
auth.on("login", update_last_login)
auth.on("login_failed", alert_failed_login)
auth.once("logout", goodbye_message)  # Only fires once

print("=== Authentication Events ===\n")
auth.login("alice", "wrong")     # Triggers login_failed
auth.login("alice", "secret")    # Triggers login (3 handlers)
auth.logout()                    # Triggers logout (goodbye)
auth.login("bob", "secret")
auth.logout()                    # No goodbye (was once)
```

### Example 3: Data Pipeline with Reactive Streams

```python
from typing import TypeVar, Generic, Callable, Optional, List

T = TypeVar('T')
R = TypeVar('R')


class Observable(Generic[T]):
    """
    Reactive Observable that supports map, filter, and subscribe operations.
    Similar to RxPy but simplified.
    """
    
    def __init__(self):
        self._subscribers: List[Callable[[T], None]] = []
    
    def subscribe(self, callback: Callable[[T], None]) -> 'Subscription':
        """Subscribe to receive values."""
        self._subscribers.append(callback)
        return Subscription(self, callback)
    
    def next(self, value: T) -> None:
        """Emit a value to all subscribers."""
        for subscriber in self._subscribers:
            subscriber(value)
    
    def map(self, transform: Callable[[T], R]) -> 'Observable[R]':
        """Transform values with a function."""
        mapped = Observable[R]()
        self.subscribe(lambda x: mapped.next(transform(x)))
        return mapped
    
    def filter(self, predicate: Callable[[T], bool]) -> 'Observable[T]':
        """Filter values based on a predicate."""
        filtered = Observable[T]()
        self.subscribe(lambda x: filtered.next(x) if predicate(x) else None)
        return filtered
    
    def tap(self, side_effect: Callable[[T], None]) -> 'Observable[T]':
        """Perform side effect without changing the value."""
        tapped = Observable[T]()
        def handler(x: T):
            side_effect(x)
            tapped.next(x)
        self.subscribe(handler)
        return tapped


class Subscription:
    """Represents a subscription that can be unsubscribed."""
    
    def __init__(self, observable: Observable, callback: Callable):
        self._observable = observable
        self._callback = callback
    
    def unsubscribe(self) -> None:
        if self._callback in self._observable._subscribers:
            self._observable._subscribers.remove(self._callback)


# Usage: Sensor Data Pipeline
class TemperatureSensor(Observable[float]):
    """Simulated temperature sensor."""
    
    def read(self, celsius: float) -> None:
        self.next(celsius)


# Build reactive pipeline
sensor = TemperatureSensor()

pipeline = (
    sensor
    .tap(lambda c: print(f"📊 Raw reading: {c}°C"))
    .filter(lambda c: c > 0)  # Only positive temps
    .map(lambda c: c * 9/5 + 32)  # Convert to Fahrenheit
    .filter(lambda f: f > 100)  # Only high temps
)

# Subscribe to processed data
pipeline.subscribe(lambda f: print(f"🔥 HIGH TEMP ALERT: {f:.1f}°F"))

print("=== Temperature Sensor Data ===\n")
sensor.read(25.0)   # 77°F - no alert
sensor.read(-5.0)   # Filtered (negative)
sensor.read(38.5)   # 101.3°F - alert!
sensor.read(40.0)   # 104°F - alert!
sensor.read(35.0)   # 95°F - no alert
```

---

## Advanced Patterns

### Weak References (Prevent Memory Leaks)

```python
import weakref
from typing import Set


class WeakObserver:
    """Observer that uses weak references to prevent memory leaks."""
    
    def __init__(self):
        self._observers: Set[weakref.ref] = set()
    
    def subscribe(self, observer) -> None:
        # Create weak reference with cleanup callback
        ref = weakref.ref(observer, self._cleanup)
        self._observers.add(ref)
    
    def _cleanup(self, ref: weakref.ref) -> None:
        """Called when observer is garbage collected."""
        self._observers.discard(ref)
    
    def notify(self, *args, **kwargs) -> None:
        dead_refs = set()
        for ref in self._observers:
            observer = ref()
            if observer is not None:
                observer.update(*args, **kwargs)
            else:
                dead_refs.add(ref)
        # Clean up dead references
        self._observers -= dead_refs


class MyObserver:
    def __init__(self, name: str):
        self.name = name
    
    def update(self, message: str) -> None:
        print(f"{self.name} received: {message}")


# Usage
subject = WeakObserver()

obs1 = MyObserver("Observer 1")
obs2 = MyObserver("Observer 2")

subject.subscribe(obs1)
subject.subscribe(obs2)

subject.notify("First message")

# Delete one observer
del obs1

subject.notify("Second message")  # Only obs2 receives this
```

### Async Observers

```python
import asyncio
from typing import List, Callable, Awaitable


class AsyncObservable:
    """Observable that supports async observers."""
    
    def __init__(self):
        self._observers: List[Callable[..., Awaitable[None]]] = []
    
    def subscribe(self, observer: Callable[..., Awaitable[None]]) -> None:
        self._observers.append(observer)
    
    async def notify(self, *args, **kwargs) -> None:
        """Notify all observers concurrently."""
        await asyncio.gather(
            *[observer(*args, **kwargs) for observer in self._observers]
        )


# Usage
async def slow_logger(message: str) -> None:
    await asyncio.sleep(0.1)
    print(f"[Slow Logger] {message}")


async def fast_logger(message: str) -> None:
    await asyncio.sleep(0.01)
    print(f"[Fast Logger] {message}")


async def main():
    observable = AsyncObservable()
    observable.subscribe(slow_logger)
    observable.subscribe(fast_logger)
    
    print("Notifying observers...")
    await observable.notify("Hello async world!")
    print("All observers completed")


# asyncio.run(main())
```

### Priority Observers

```python
from dataclasses import dataclass, field
from typing import Callable, List
import heapq


@dataclass(order=True)
class PriorityObserver:
    priority: int
    callback: Callable = field(compare=False)


class PriorityObservable:
    """Observable where observers are notified in priority order."""
    
    def __init__(self):
        self._observers: List[PriorityObserver] = []
    
    def subscribe(self, callback: Callable, priority: int = 0) -> None:
        """Lower priority number = higher priority (called first)."""
        heapq.heappush(self._observers, PriorityObserver(priority, callback))
    
    def notify(self, *args, **kwargs) -> None:
        # Process in priority order (without modifying the heap)
        for observer in sorted(self._observers):
            observer.callback(*args, **kwargs)


# Usage
observable = PriorityObservable()

observable.subscribe(lambda msg: print(f"[LOW] {msg}"), priority=10)
observable.subscribe(lambda msg: print(f"[HIGH] {msg}"), priority=1)
observable.subscribe(lambda msg: print(f"[MEDIUM] {msg}"), priority=5)
observable.subscribe(lambda msg: print(f"[CRITICAL] {msg}"), priority=0)

observable.notify("System starting...")

# Output:
# [CRITICAL] System starting...
# [HIGH] System starting...
# [MEDIUM] System starting...
# [LOW] System starting...
```

---

## Python-Specific Implementations

### Using Property Decorators

```python
class ObservableProperty:
    """Descriptor that notifies observers when property changes."""
    
    def __init__(self, initial_value=None):
        self.value = initial_value
        self.name = None
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, obj, owner):
        if obj is None:
            return self
        return getattr(obj, f'_{self.name}', self.value)
    
    def __set__(self, obj, value):
        old_value = getattr(obj, f'_{self.name}', None)
        setattr(obj, f'_{self.name}', value)
        if hasattr(obj, '_notify_change'):
            obj._notify_change(self.name, old_value, value)


class Model:
    """Base model with observable properties."""
    
    def __init__(self):
        self._observers = []
    
    def observe(self, callback):
        self._observers.append(callback)
    
    def _notify_change(self, prop_name, old_value, new_value):
        for observer in self._observers:
            observer(self, prop_name, old_value, new_value)


class User(Model):
    name = ObservableProperty("")
    email = ObservableProperty("")
    age = ObservableProperty(0)


# Usage
def log_changes(obj, prop, old, new):
    print(f"Property '{prop}' changed: {old!r} → {new!r}")


user = User()
user.observe(log_changes)

user.name = "Alice"
user.email = "alice@example.com"
user.age = 30
user.age = 31

# Output:
# Property 'name' changed: '' → 'Alice'
# Property 'email' changed: '' → 'alice@example.com'
# Property 'age' changed: 0 → 30
# Property 'age' changed: 30 → 31
```

### Using Signals (Qt-style)

```python
from typing import Callable, List, Any


class Signal:
    """Qt-style signal implementation."""
    
    def __init__(self):
        self._slots: List[Callable] = []
    
    def connect(self, slot: Callable) -> None:
        """Connect a slot (callback) to this signal."""
        if slot not in self._slots:
            self._slots.append(slot)
    
    def disconnect(self, slot: Callable) -> None:
        """Disconnect a slot from this signal."""
        if slot in self._slots:
            self._slots.remove(slot)
    
    def emit(self, *args, **kwargs) -> None:
        """Emit the signal, calling all connected slots."""
        for slot in self._slots:
            slot(*args, **kwargs)
    
    def __call__(self, *args, **kwargs) -> None:
        """Allow signal() as shorthand for signal.emit()"""
        self.emit(*args, **kwargs)


class Button:
    """Simulated GUI button with signals."""
    
    def __init__(self, label: str):
        self.label = label
        self.clicked = Signal()
        self.double_clicked = Signal()
    
    def click(self):
        print(f"Button '{self.label}' clicked")
        self.clicked.emit(self)
    
    def double_click(self):
        print(f"Button '{self.label}' double-clicked")
        self.double_clicked.emit(self)


# Usage
def on_button_click(button: Button):
    print(f"  → Handling click for: {button.label}")


def on_submit():
    print("  → Form submitted!")


def on_double_click(button: Button):
    print(f"  → Double-click action for: {button.label}")


# Create buttons and connect signals
submit_btn = Button("Submit")
submit_btn.clicked.connect(on_button_click)
submit_btn.clicked.connect(on_submit)
submit_btn.double_clicked.connect(on_double_click)

cancel_btn = Button("Cancel")
cancel_btn.clicked.connect(on_button_click)

# Simulate user interactions
print("=== Button Interactions ===\n")
submit_btn.click()
submit_btn.double_click()
cancel_btn.click()
```

---

## Comparison with Other Patterns

| Pattern | Purpose | Key Difference |
|---------|---------|----------------|
| **Observer** | Notify multiple objects of state changes | One-to-many, subject doesn't know observer details |
| **Mediator** | Centralize complex communications | Many-to-many through central mediator |
| **Pub/Sub** | Decoupled event distribution | Complete decoupling via message broker |
| **Callback** | Simple notification | One-to-one, specific callback known |

### When to Use Each

```python
# Observer: When subject shouldn't know about observers
class DataStore:
    def set_data(self, data):
        self._data = data
        self.notify_observers()  # Don't care who's listening

# Pub/Sub: When you need complete decoupling
class EventBus:
    def publish(self, topic, data):
        # Route to subscribers by topic
        pass

# Callback: When you have a specific known handler
def fetch_data(url, on_complete):
    data = ...
    on_complete(data)  # Specific callback
```

---

## Common Pitfalls

### 1. Memory Leaks

```python
# BAD: Observer holds reference, never garbage collected
class LeakySubject:
    def __init__(self):
        self.observers = []  # Strong references

# GOOD: Use weak references
import weakref

class SafeSubject:
    def __init__(self):
        self.observers = weakref.WeakSet()
```

### 2. Notification Order Dependency

```python
# BAD: Observers depend on execution order
class BadObserver1:
    def update(self, subject):
        self.value = subject.state * 2

class BadObserver2:
    def update(self, subject):
        # Assumes BadObserver1 already ran!
        print(bad_observer1.value)  # Undefined behavior!

# GOOD: Observers are independent
class GoodObserver:
    def update(self, subject):
        # Only use subject's data, not other observers
        result = subject.state * 2
        self.handle(result)
```

### 3. Infinite Notification Loops

```python
# BAD: Observer modifies subject, triggering more notifications
class InfiniteLoopObserver:
    def update(self, subject):
        subject.state = subject.state + 1  # Triggers notify() again!

# GOOD: Use guards or separate state changes from notifications
class SafeObserver:
    def update(self, subject):
        # Read-only access or modify without triggering notification
        local_copy = subject.state + 1
        self.process(local_copy)
```

### 4. Exception Handling

```python
# BAD: One failing observer stops all notifications
def bad_notify(self):
    for observer in self.observers:
        observer.update(self)  # Exception stops loop!

# GOOD: Isolate failures
def good_notify(self):
    for observer in self.observers:
        try:
            observer.update(self)
        except Exception as e:
            print(f"Observer {observer} failed: {e}")
```

---

## Best Practices

### 1. Define Clear Interfaces

```python
from abc import ABC, abstractmethod
from typing import Protocol


# Option 1: ABC
class Observer(ABC):
    @abstractmethod
    def update(self, subject) -> None:
        pass


# Option 2: Protocol (structural typing)
class ObserverProtocol(Protocol):
    def update(self, subject) -> None:
        ...
```

### 2. Provide Rich Event Data

```python
from dataclasses import dataclass
from typing import Any


@dataclass
class ChangeEvent:
    source: Any
    property_name: str
    old_value: Any
    new_value: Any
    timestamp: float


# Pass complete event, not just subject
def update(self, event: ChangeEvent) -> None:
    if event.property_name == "price":
        self.handle_price_change(event.old_value, event.new_value)
```

### 3. Support Unsubscription

```python
class Subscription:
    def __init__(self, unsubscribe_fn):
        self._unsubscribe = unsubscribe_fn
        self._active = True
    
    def unsubscribe(self):
        if self._active:
            self._unsubscribe()
            self._active = False


class Observable:
    def subscribe(self, observer) -> Subscription:
        self._observers.append(observer)
        return Subscription(lambda: self._observers.remove(observer))
```

### 4. Consider Thread Safety

```python
import threading


class ThreadSafeObservable:
    def __init__(self):
        self._observers = []
        self._lock = threading.RLock()
    
    def subscribe(self, observer):
        with self._lock:
            self._observers.append(observer)
    
    def notify(self, *args):
        with self._lock:
            observers = list(self._observers)  # Copy under lock
        
        for observer in observers:  # Notify outside lock
            observer.update(*args)
```

---

## Summary

### Key Takeaways

1. **Observer pattern** enables loose coupling between subjects and observers
2. **Use weak references** to prevent memory leaks
3. **Handle exceptions** in individual observers to prevent cascade failures
4. **Consider async** for I/O-bound observers
5. **Python-specific**: Use descriptors, signals, or EventEmitter patterns

### Quick Reference

```python
# Minimal implementation
class Subject:
    def __init__(self):
        self._observers = []
    
    def attach(self, obs): self._observers.append(obs)
    def detach(self, obs): self._observers.remove(obs)
    def notify(self): 
        for obs in self._observers:
            obs.update(self)
```

---

## Further Reading

- **Design Patterns**: Gang of Four book, Observer chapter
- **RxPy**: Reactive Extensions for Python
- **PyDispatcher**: Python implementation of multi-producer multi-consumer signal dispatching
- **Blinker**: Fast Python in-process signal/event dispatching system

---

**When to Read**: When building event-driven systems, GUIs, or reactive data pipelines.

**Last Updated**: 2026-01-05

