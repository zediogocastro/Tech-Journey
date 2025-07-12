from stores import EspressoStore, LatteStore

def main():
    espresso_store = EspressoStore()
    latte_store = LatteStore()

    espresso_store.order_coffee(size="small", temperature="hot")
    latte_store.order_coffee(size="large", temperature="hot", milk_type="Oat Milk")

    # This would raise an error because espresso does not support milk:
    # espresso_store.order_coffee(size="medium", temperature="hot", milk_type="Almond Milk")

if __name__ == "__main__":
    main()