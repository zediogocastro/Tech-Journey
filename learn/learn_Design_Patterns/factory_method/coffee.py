from abc import ABC, abstractmethod

class Coffee(ABC):
    def __init__(self, size, temperature, milk_type=None):
        self.size = size
        self.temperature = temperature
        self.milk_type = milk_type

    @abstractmethod
    def prepare(self):
        pass

    @abstractmethod
    def get_name(self):
        pass


class EspressoCoffee(Coffee):
    def __init__(self, size, temperature):
        super().__init__(size, temperature)
        self.milk_type = None  # Force no milk

    def prepare(self):
        print(f"Size: {self.size}, Temperature: {self.temperature}")
        print("Grinding beans...")
        print("Brewing espresso shot...")

    def get_name(self):
        return "Espresso"


class LatteCoffee(Coffee):
    def prepare(self):
        print(f"Size: {self.size}, Temperature: {self.temperature}, Milk: {self.milk_type}")
        print("Grinding beans...")
        print("Brewing espresso shot...")
        print("Steaming milk...")

    def get_name(self):
        return "Latte"