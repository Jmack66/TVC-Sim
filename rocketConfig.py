from dataclasses import dataclass
#Vehicle Properties
# MASS = 1 #kg
# MMOI = 0.1 #kg m^2
# THRUST = 12 # Newtons
# COM2TVC = 0.5 # meters
# SERVO_LIMIT = 15 #degrees
@dataclass
class rocket:
	mass: float
	mmoi: float
	com2TVC: float
	servo_lim: float
	servo_rate_lim: float


