"""
Basic example of a Vehicle registration system
"""
from enum import Enum, auto
from dataclasses import dataclass

class FuelType(Enum):
    """Types of fuel used in a vehicle."""

    ELECTRIC = auto()
    PETROL = auto()


class RegistryStatus(Enum):
    """Possible statuses for the vehicle registry system."""

    ONLINE = auto()
    CONNECTION_ERROR = auto()
    OFFLINE = auto()

taxes = {FuelType.ELECTRIC: 0.02, FuelType.PETROL: 0.05}


@dataclass
class VehicleInfoMissingError(Exception):
    """Custom error that is raised when vehicle information is missing for a particular brand."""

    brand: str
    model: str
    message: str = "Vehicle information is missing."

@dataclass
class VehicleModelInfo:
    """Class that contains basic information about a vehicle model."""

    brand: str
    model: str
    catalogue_price: int
    fuel_type: FuelType
    prduction_year: int

    @property
    def tax(self) -> float:
        """Tax to be paid whe registering a vehicle of this type"""
        tax_percentage = taxes[self.fuel_type]
        return tax_percentage * self.catalogue_price
    
    def get_info_str(self) -> str:
        """String represantation of this instance"""
        return f"Brand: {self.brand} - Type: {self.model} - tax: {self.tax}"
    
@dataclass
class Vehicle:
    """Class representing a vehicle (electric or fossil fuel)."""

    vehicle_id: int
    license_plate: str
    info: VehicleModelInfo

    def to_string(self) -> str:
        """String representation of this instance"""
        info_str = self.info.get_info_str()
        return f"Id: {self.vehicle_id}. License plate: {self.license_plate}. Info: {info_str}"