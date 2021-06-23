import numpy as np
import time
import PID as pid
import Graphics as gh
import Physics as phys
import rocketConfig
#Units are SI units... m/s/radians/kg

time_ret = []
angles_ret = []
vert_pos_ret = []
hori_pos_ret = []

ori_labels = {"xlab" : "time(s)", "ylab" : "angle(theta)", "title" : "Theta"}
translate_labels = {"xlab" : "time(s)", "ylab" : "Pos Z", "title" : "Position Z"}
vertical_labels = {"xlab" : "time(s)", "ylab" : "Pos X", "title" : "Position X"}

graphs_dict = [ori_labels,translate_labels,vertical_labels]

graphics = gh.GraphicHandler()
graphics.graphsHandler(3,graphs_dict) #number of graphs and their labels

rocket = graphics.createAgent('black')
targe = graphics.createAgent('red')

vehicle = rocketConfig.vehicleProperties(1,0.1,0.5,np.deg2rad(15),np.deg2rad(150))
#mass(kg),mmoi(kg m^2),com2TVC(meters),servo_lim(rad),servo_rate_lim(rad/s)

THRUST = 12 # Newtons


#initial state vector
state_vector = {"ax" : 0 ,"vx" : 0,"px" : 0,"az" : 0 ,"vz" : 1,"pz" : 0 ,"alpha" : 0.0,"omega" : 0.5,"theta" : 0.0}

rocket_phys = phys.threeDofPhysics(state_vector,vehicle.mass,vehicle.mmoi)

#Controller setup
controller = pid.PID(0.07,0.01,0.01,0) #KP,KI,KD,setpoint
controller.setLims(-10,10)#output limits
#our TVC is also limited by SERVO_LIMIT but we might want to change the the two independently

sim_time = 0.0
time_lim = 10.0
delta_t = 0.1
tvc_input = 0


if __name__ == "__main__":
	while(sim_time < time_lim):

		#Physics
		forces = rocket_phys.tvcPhysics(tvc_input,THRUST,vehicle,delta_t) # Compute Forces	from TVC	
		rocket_phys.inputForces(forces,delta_t) # Apply Forces to body	
		graphics.moveAgent(rocket,rocket_phys.state_vector["pz"],rocket_phys.state_vector["px"])# Update Graphics and Plots
		graphics.rotateAgent(rocket,rocket_phys.state_vector["theta"])

		#Saving data we want to plot
		angles_ret.append(np.rad2deg(rocket_phys.state_vector['theta']))
		hori_pos_ret.append(rocket_phys.state_vector["pz"])
		vert_pos_ret.append(rocket_phys.state_vector["px"])
		graphs = [(time_ret,angles_ret),(time_ret,hori_pos_ret),(time_ret,vert_pos_ret)]

		#Real-time plotting is slow right now -> need to look into blit for matplotlib
		#graphics.updateGraphs(graphs)

		# Compute Control Logic
		tvc_input = controller.compute(rocket_phys.state_vector['theta'],delta_t)


		time_ret.append(sim_time)
		sim_time += delta_t

	graphics.showGraphs(graphs)