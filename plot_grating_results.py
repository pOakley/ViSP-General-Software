import matplotlib.pyplot as plt
def plot_summary(pol0_centers, pol0_efficiencies,pol45_centers,pol45_efficiencies,pol90_centers,pol90_efficiencies):
	#Summary Plot
	plt.figure()

	# ax = plt.subplot(311)
	# plt.plot(pol0_centers,pol0_efficiencies,'x')
	# plt.ylabel("Efficiency")
	# plt.title("Polarization 0")
	# plt.ylim(0,.3)
	# ax.grid()
	
	# if (pol45_centers != []):
	# 	ax2 = plt.subplot(312)
	# 	plt.plot(pol45_centers,pol45_efficiencies,'x')
	# 	plt.ylabel("Efficiency")
	# 	plt.title("Polarization 45")
	# 	plt.ylim(0,.3)
	# 	ax2.grid()
	
	# ax3 = plt.subplot(313)
	# plt.plot(pol90_centers,pol90_efficiencies,'x')
	# plt.xlabel("Wavelength")
	# plt.ylabel("Efficiency")
	# plt.title("Polarization 90")
	# plt.xlim(500,1100)
	# plt.ylim(0,.3)
	# ax3.grid()

	plt.plot(pol0_centers,pol0_efficiencies,'rx-')
	plt.plot(pol90_centers,pol90_efficiencies,'bx-')


def plot_example(data_list,incident_pol90):
	#Example Plot

	sample = 2

	plt.figure()
	plt.subplot(321)
	plt.plot(data_list[sample].wavelength,data_list[sample].intensity*data_list[sample].diffracted_exposure_length)
	plt.title("Diffracted Light - Polarization 0")
	plt.ylabel("Intensity [in 400000 uS]")
	plt.subplot(322)
	plt.plot(data_list[sample].wavelength,data_list[sample].intensity)
	plt.title("Diffracted Light - Polarization 0")
	plt.ylabel("Intensity [in 1 uS]")
	plt.subplots_adjust(hspace=0.5)

	# plt.subplot(323)
	# plt.plot(data_list[1].wavelength,data_list[1].intensity*400000.)
	# plt.title("Diffracted Light - Polarization 45")
	# plt.ylabel("Intensity [in 400000 uS]")
	# plt.subplot(324)
	# plt.plot(data_list[1].wavelength,data_list[1].intensity)
	# plt.title("Diffracted Light - Polarization 45")
	# plt.ylabel("Intensity [in 1 uS]")

	plt.subplot(323)
	plt.plot(data_list[sample+1].wavelength,data_list[sample+1].intensity*data_list[sample].diffracted_exposure_length)
	plt.title("Diffracted Light - Polarization 90")
	plt.ylabel("Intensity [in 400000 uS]")
	plt.subplot(324)
	plt.plot(data_list[sample+1].wavelength,data_list[sample+1].intensity)
	plt.title("Diffracted Light - Polarization 90")
	plt.ylabel("Intensity [in 1 uS]")
	
	plt.subplot(325)
	plt.plot(incident_pol90.wavelength,incident_pol90.intensity*data_list[sample].direct_exposure_length)
	plt.title("Incident Light")
	plt.xlabel("Wavelength")
	plt.ylabel("Intensity [in 25000 uS]")
	plt.subplot(326)
	plt.plot(incident_pol90.wavelength,incident_pol90.intensity)
	plt.title("Incident Light")
	plt.ylabel("Intensity [in 1 uS]")
	plt.xlabel("Wavelength")


	#Show the plots
	plt.show()
