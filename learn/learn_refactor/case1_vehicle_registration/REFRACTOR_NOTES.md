# Refactor Notes

## Introduction
This document outlines the refactoring process from `before.py` to `after.py`. The goal was to improve the code's maintainability, readability, and adherence to OOP principles.

## Summary of problems
1. Too many parameters
2. Too deep nesting
3. Not using the right data structure
4. Nested Coditional Expressions
5. Using Wildcard Imports
6. Asymetrical Code


## Detailed Explanation
### 1. Too many parameters
```python
# Before
def add_vehicle_model_info(
            self,
            brand: str,
            model: str,
            catalogue_price: int,
            fuel_type: FuelType,
            year: int,
    ) -> None:
```

```python
# After
def add_vehicle_model_info(self, model_info: VehicleModelInfo) -> None:
    """Helper method for adding a VehicleModelInfo object to a list."""
    self.vehicle_models.append(model_info)
```


### 2. Too deep nesting
- It gives more focus on the primary goal of the method ratehr than conditions
- creates a new method to handle auxiliary tasks
- Condences logical operation into a single line

```python
# Before
def register_vehicle(self, brand: str, model: str) -> Vehicle:
        """Create a new vehicle and generate an id and a license plate."""
        for vehicle_info in self.vehicle_models:
            if vehicle_info.brand == brand:
                if vehicle_info.model == model:
                    vehicle_id = self.generate_vehicle_id(12)
                    license_plate = self.generate_vehicle_license(vehicle_id)
                    return Vehicle(vehicle_id, license_plate, vehicle_info)
        raise VehicleInfoMissingError(brand, model)
```

```python
# After
def find_model_info(self, brand: str, model: str) -> Optional[VehicleModelInfo]:
        """Finds model info for a brand and model. If no info can be found, None is returned."""
        for vehicle_info in self.vehicle_models:
            if vehicle_info.brand != brand or vehicle_info.model != model:
                continue
            return vehicle_info
        return None
    
    def register_vehicle(self, brand: str, model: str) -> Vehicle:
        """Create a new vehicle and generate an id and a license plate."""
        vehicle_model = self.find_model_info(brand, model)
        if not vehicle_model:
            raise VehicleInfoMissingError(brand, model)
        
        # Generate the vehicle id and license plate
        vehicle_id = self.generate_vehicle_id(12)
        license_plate = self.generate_vehicle_license(vehicle_id)
        return Vehicle(vehicle_id, license_plate, vehicle_model)
```

### 3. Not using the right data structure
- By changing the list into a dictionary we can easily acess elements and add them.
- The `find_model_info` makes use of the `get`method that returns `None` in the case of not finding the keys.

```python
# Before
def find_model_info(self, brand: str, model: str) -> Optional[VehicleModelInfo]:
        """Finds model info for a brand and model. If no info can be found, None is returned."""
        for vehicle_info in self.vehicle_models:
            if vehicle_info.brand != brand or vehicle_info.model != model:
                continue
            return vehicle_info
        return None
```

```python
# After
def find_model_info(self, brand: str, model: str) -> Optional[VehicleModelInfo]:
        """Finds model info for a brand and model. If no info can be found, None is returned."""
        return self.vehicle_models.get((brand, model)) 
```

### 4. Nested Coditional Expressions
```python
# Before
def online_status(self) -> RegistryStatus:
        """Report whether the registry system is online."""
        return (
            RegistryStatus.OFFLINE
            if not self.online
            else (
                RegistryStatus.CONNECTION_ERROR
                if len(self.vehicle_models) == 0
                else RegistryStatus.ONLINE
            )
        )
```
```python
# After
def online_status(self) -> RegistryStatus:
        """Report whether the registry system is online."""
        if not self.online:
            return RegistryStatus.OFFLINE
        else:
            return (
                RegistryStatus.CONNECTION_ERROR
                if len(self.vehicle_models) == 0
                else RegistryStatus.ONLINE
            )
```

### 5. Using Wildcard Imports
- Pollutes the namespace in the module
```python
# Before
from random import *
from string import *

return f"{_id[:2]}-{''.join(choices(digits, k=2))}-{''.join(choices(ascii_uppercase, k=2))}"

```
```python
# After
import random
import string

return f"{_id[:2]}-{''.join(random.choices(string.digits, k=2))}-{''.join(random.choices(string.ascii_uppercase, k=2))}"
```

### 6. Asymetrical Code
- Doing the same thing in different ways
- Makes use of `__str__()` method

```python
# Before
# Class VehicleModelInfo
def get_info_str(self) -> str:
        """String represantation of this instance"""
        return f"Brand: {self.brand} - Type: {self.model} - tax: {self.tax}"

# Class Vehicle
def to_string(self) -> str:
        """String representation of this instance"""
        info_str = self.info.get_info_str()
        return f"Id: {self.vehicle_id}. License plate: {self.license_plate}. Info: {info_str}"

```
```python
# After
# Class VehicleModelInfo
def __str__(self) -> str:
    return f"Brand: {self.brand} - Type: {self.model} - tax: {self.tax}"

# Class Vehicle
def __str__(self) -> str:
    return f"Id: {self.vehicle_id}. License plate: {self.license_plate}. Info: {self.info}"
```


### 7. Using self when not needed

```python
# Before
def generate_vehicle_id(self, length: int) -> str:
        """Helper method for generating a random vehicle id."""
        return "".join(choices(ascii_uppercase, k=length))

    def generate_vehicle_license(self, _id: str) -> str:
        """Helper method for generating a vehicle license number."""
        return f"{_id[:2]}-{''.join(choices(digits, k=2))}-{''.join(choices(ascii_uppercase, k=2))}"
```

```python
@staticmethod
    def generate_vehicle_id(length: int) -> str:
        """Helper method for generating a random vehicle id."""
        return "".join(random.choices(string.ascii_uppercase, k=length))

    @staticmethod
    def generate_vehicle_license(_id: str) -> str:
        """Helper method for generating a vehicle license number."""
        digit_part = ''.join(random.choices(string.digits, k=2))
        letter_part = ''.join(random.choices(string.ascii_uppercase, k=2))
        return f"{_id[:2]}-{digit_part}-{letter_part}"

```

### 8. Not using a main function
```python
# Before
if __name__ == "__main__":

    # create a registry instance
    registry = VehicleRegistry()

    # add a couple of different vehicle models
    registry.add_vehicle_model_info(
        VehicleModelInfo("Tesla", "Model 3", 50_000, FuelType.ELECTRIC, 2021)
    )
```


```python
# After
def main():
    # create a registry instance
    registry = VehicleRegistry()

    # add a couple of different vehicle models
    registry.add_vehicle_model_info(
        VehicleModelInfo("Tesla", "Model 3", 50_000, FuelType.ELECTRIC, 2021)
    )

if __name__ == "__main__":
    main()
```
