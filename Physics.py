import numpy as np
#input_force_vector = [Fx,Fz,Tau]
'''
		X+
		|
		|<=
		|	=
		| = Theta
		----------Z+

'''
class threeDofPhysics():
	def __init__(self,initial_state_vector,mass,mmoi):
		self.state_vector = initial_state_vector
		self.mass = mass
		self.mmoi = mmoi
		self.input_last = None
		self.actuator_state = []
	def inputForces(self,input_force_vector,dt,internal_gravity = True,negative_x_pos = False):
		G = -9.18 if internal_gravity else 0
		self.state_vector["ax"] = (input_force_vector[0] / self.mass) + G
		self.state_vector["az"] = input_force_vector[1] / self.mass
		self.state_vector["alpha"] = input_force_vector[2] / self.mmoi
		self.state_vector["vx"] += self.state_vector["ax"] * dt
		self.state_vector["vz"] += self.state_vector["az"] * dt
		self.state_vector["omega"] += self.state_vector["alpha"] * dt
		self.state_vector["px"] += self.state_vector["vx"] * dt
		if negative_x_pos and self.state_vector["px"] < 0:
			self.state_vector["px"] = 0
		self.state_vector["pz"] += self.state_vector["vz"] * dt
		self.state_vector["theta"] += self.state_vector["omega"] * dt
		return self.state_vector
	#maybe eventually replace this with an "Actuator" class or something that can command stuff
	def tvcPhysics(self,input_angle,thrust,vehicle,dt,print_warnings = False): #angle in rads
		if input_angle > vehicle.servo_lim:
			input_angle = vehicle.servo_lim
			print("WARNING: Acuator Limit Reached") if print_warnings else None
		if input_angle < - vehicle.servo_lim:
			input_angle = -vehicle.servo_lim
			print("WARNING: Acuator Limit Reached") if print_warnings else None
		if self.input_last is None:
			self.input_last = input_angle 
		servo_rate = (self.input_last - input_angle) / dt
		if servo_rate > vehicle.servo_rate_lim:
			input_angle = self.input_last - vehicle.servo_rate_lim*dt
			print("WARNING: Acuator Rate Limit Reached") if print_warnings else None
		if servo_rate < -vehicle.servo_rate_lim:
			input_angle = self.input_last + vehicle.servo_rate_lim*dt
			print("WARNING: Acuator Rate Limit Reached") if print_warnings else None
		Fz = np.sin(self.state_vector["theta"])*np.sin(input_angle) * thrust
		Fx = np.cos(self.state_vector["theta"])*np.cos(input_angle) * thrust
		Tau = np.sin(input_angle) * thrust * vehicle.com2TVC
		self.actuator_state = input_angle
		self.input_last = input_angle
		return [Fx,Fz,Tau]

if __name__ == "__main__":
	state_vector = {"ax" : 0 ,"vx" : 0,"px" : 0,"az" : 0 ,"vz" : 0,"pz" : 0 ,"alpha" : 0,"omega" : 0,"theta" : 0}
	dof = threeDofPhysics(state_vector,1,0.1)
	for i in range(10):
		print(dof.inputForces([10,1,1],1))