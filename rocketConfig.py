from dataclasses import dataclass

@dataclass
class vehicleProperties:
	mass: float
	mmoi: float
	com_to_tvc: float
	servo_limit: float
	servo_rate_limit: float


