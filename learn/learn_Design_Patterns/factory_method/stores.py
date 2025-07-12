from abc import ABC, abstractmethod
from coffee import Coffee, EspressoCoffee, LatteCoffee


class CoffeeStore(ABC):
    @abstractmethod
    def create_coffee(self, size, temperature, milk_type=None) -> Coffee:
        pass

    def order_coffee(self, size, temperature, milk_type=None) -> Coffee:
        coffee = self.create_coffee(size, temperature, milk_type)
        print(f"--- Making a {coffee.get_name()} ---")
        coffee.prepare()
        return coffee
    
class EspressoStore(CoffeeStore):
    def create_coffee(self, size, temperature, milk_type=None) -> Coffee:
        if milk_type:
            raise ValueError("Espresso does not support milk options!")
        return EspressoCoffee(size, temperature)


class LatteStore(CoffeeStore):
    def create_coffee(self, size, temperature, milk_type=None) -> Coffee:
        if milk_type is None:
            raise ValueError("Latte requires a milk type!")
        return LatteCoffee(size, temperature, milk_type)