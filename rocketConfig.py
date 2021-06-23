from dataclasses import dataclass

@dataclass
class vehicleProperties:
	mass: float
	mmoi: float
	com2TVC: float
	servo_lim: float
	servo_rate_lim: float


