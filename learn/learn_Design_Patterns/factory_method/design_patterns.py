class CoffeeStore(ABC):
    @abstractmethod
    def create_coffee(self, item: Coffee) -> Coffee:
        pass

    def order_coffee(self) -> Coffee:
        coffee = self.create_coffee()
        print(f"--- Making a {coffee.get_name()} ---")
        return coffee

class ExpressoStore(CoffeeStore):
    def create_coffee(self) -> Coffee:
        return ExpressoCoffee
        
        
expresso_store = ExpressoStore()

expresso = expresso_store.order_coffee()