class Singelton:
  """
  A Singelton class that allows only one instance of itself to be created.
  """
  _instance = None

  def __new__(cls):
    if cls._instance is None:
      cls._instance = super(Singelton, cls).__new__(cls)
      # Initialize instance variables here if needed
      cls._instance.value = 0 
    return cls._instance

  def increment_value(self):
    self.value += 1

  def get_value(self):
    return self.value
