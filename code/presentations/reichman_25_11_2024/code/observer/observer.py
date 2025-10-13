from abc import ABC, abstractmethod

class Subject:
  """
  The Subject keeps track of its observers and notifies them when its state changes.
  """

  def __init__(self):
    self._observers = []
    self._state = None

  def attach(self, observer):
    """
    Attaches an observer to the subject.
    """
    self._observers.append(observer)

  def detach(self, observer):
    """
    Detaches an observer from the subject.
    """
    self._observers.remove(observer)

  def notify(self):
    """
    Notifies all observers about a change in the subject's state.
    """
    for observer in self._observers:
      observer.update(self)

  @property
  def state(self):
    return self._state

  @state.setter
  def state(self, state):
    self._state = state
    self.notify()


class Observer(ABC):
  """
  Abstract Observer class.
  """

  @abstractmethod
  def update(self, subject):
    """
    Receives updates from the subject.
    """
    pass


class ConcreteObserverA(Observer):
  """
  Concrete Observer implementation.
  """

  def update(self, subject):
    print(f"ConcreteObserverA: got the event (state: {subject.state})")
    if subject.state < 3:
      print(f"ConcreteObserverA: Reacted to the event (state: {subject.state})")


class ConcreteObserverB(Observer):
  """
  Another Concrete Observer implementation.
  """

  def update(self, subject):
    print(f"ConcreteObserverB: got the event (state: {subject.state})")
    if subject.state == 0 or subject.state >= 2:
      print(f"ConcreteObserverB: Reacted to the event (state: {subject.state})")
