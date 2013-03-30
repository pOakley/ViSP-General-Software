import numpy as np
import matplotlib.pyplot as plt


class Data:
	"""Class to store data from a spectrum"""
	def __init__(self, file_suffix, diffracted = True):
		self.filename = '/Users/Oakley/Documents/Work/ViSP/gratings_tests/3_29_2013/' + file_suffix
		self.read_spectrum(file_suffix)

		if diffracted == False:
			self.intensity = self.intensity / 25000.
		else:
			self.line_indices = []
			self.line_centers = []
			self.line_intensities = []
			self.find_peaks()
			self.intensity = self.intensity / 400000.
			self.line_intensities = np.array(self.line_intensities) / 400000.

		
	def read_spectrum(self,file_suffix):
		#Read the data from .txt file
		vibe_data_file = open(self.filename,'r')
		print "Opening File: ", self.filename
		data_array = np.genfromtxt(vibe_data_file,delimiter=',',dtype='f')
		self.wavelength = data_array[:,0]
		self.intensity = data_array[:,1]		

	
	def find_peaks(self):
		#Determine the location (wavelength and index) and intensity of each emission line
		lines = [k for k,j in enumerate(self.intensity) if j > 5000]
		self.line_indices.append(lines[0])
		self.line_centers.append(self.wavelength[lines[0]])
		self.line_intensities.append(self.intensity[lines[0]])
		
		prev_wave = lines[0] - 1
		for wave in lines:
			if wave == (prev_wave + 1):
				if self.intensity[wave] > self.line_intensities[-1]:
					self.line_indices[-1] = wave
					self.line_intensities[-1] = self.intensity[wave]
					self.line_centers[-1] = self.wavelength[wave]
			else:
				self.line_indices.append(wave)
				self.line_centers.append(self.wavelength[wave])
				self.line_intensities.append(self.intensity[wave])
			prev_wave = wave		

def record_efficiencies():
	for k in range(0,39,3):
		for j in range(len(data_list[k].line_centers)):
			pol0_centers.append(data_list[k].line_centers[j])
			pol0_efficiencies.append(data_list[k].efficiencies[j])
			

	for k in range(1,39,3):
		for j in range(len(data_list[k].line_centers)):
			pol45_centers.append(data_list[k].line_centers[j])
			pol45_efficiencies.append(data_list[k].efficiencies[j])
	
	for k in range(2,39,3):
		for j in range(len(data_list[k].line_centers)):
			pol90_centers.append(data_list[k].line_centers[j])
			pol90_efficiencies.append(data_list[k].efficiencies[j])

def plot_summary():
	#Summary Plot
	plt.figure()
	ax = plt.subplot(311)
	plt.plot(pol0_centers,pol0_efficiencies,'x')
	plt.ylabel("Efficiency")
	plt.title("Polarization 0")
	plt.ylim(0,.1)
	ax.grid()
	
	ax2 = plt.subplot(312)
	plt.plot(pol45_centers,pol45_efficiencies,'x')
	plt.ylabel("Efficiency")
	plt.title("Polarization 45")
	plt.ylim(0,.1)
	ax2.grid()
	
	ax3 = plt.subplot(313)
	plt.plot(pol90_centers,pol90_efficiencies,'x')
	plt.xlabel("Wavelength")
	plt.ylabel("Efficiency")
	plt.title("Polarization 90")
	plt.xlim(500,1100)
	plt.ylim(0,.1)
	ax3.grid()

def plot_example():
	#Example Plot
	plt.figure()
	plt.subplot(421)
	plt.plot(data_list[0].wavelength,data_list[0].intensity*400000.)
	plt.title("Diffracted Light - Polarization 0")
	plt.ylabel("Intensity [in 400000 uS]")
	plt.subplot(422)
	plt.plot(data_list[0].wavelength,data_list[0].intensity)
	plt.title("Diffracted Light - Polarization 0")
	plt.ylabel("Intensity [in 1 uS]")
	plt.subplots_adjust(hspace=0.5)

	plt.subplot(423)
	plt.plot(data_list[1].wavelength,data_list[1].intensity*400000.)
	plt.title("Diffracted Light - Polarization 45")
	plt.ylabel("Intensity [in 400000 uS]")
	plt.subplot(424)
	plt.plot(data_list[1].wavelength,data_list[1].intensity)
	plt.title("Diffracted Light - Polarization 45")
	plt.ylabel("Intensity [in 1 uS]")

	plt.subplot(425)
	plt.plot(data_list[2].wavelength,data_list[2].intensity*400000.)
	plt.title("Diffracted Light - Polarization 90")
	plt.ylabel("Intensity [in 400000 uS]")
	plt.subplot(426)
	plt.plot(data_list[2].wavelength,data_list[2].intensity)
	plt.title("Diffracted Light - Polarization 90")
	plt.ylabel("Intensity [in 1 uS]")
	
	plt.subplot(427)
	plt.plot(incident_pol90.wavelength,incident_pol90.intensity*25000.)
	plt.title("Incident Light")
	plt.xlabel("Wavelength")
	plt.ylabel("Intensity [in 25000 uS]")
	plt.subplot(428)
	plt.plot(incident_pol90.wavelength,incident_pol90.intensity)
	plt.title("Incident Light")
	plt.ylabel("Intensity [in 1 uS]")
	plt.xlabel("Wavelength")
	
	
if __name__ == "__main__":

	#Load the data from the direct mirror bounce at each polarization
	incident_pol0 = Data('intensity_25000_pol0.txt',diffracted = False)
	incident_pol45 = Data('intensity_25000_pol45.txt',diffracted = False)
	incident_pol90 = Data('intensity_25000_pol90.txt',diffracted = False)
	
	#List of diffracted data sets	
	data_list = []
	
	#Load the data from each of the diffracted spectrum
	for k in range(0,39):
		data_list.append(Data(str(k+1)+'.txt'))
		
		if k % 3 == 1:
			data_list[k].efficiencies = data_list[k].line_intensities / incident_pol0.intensity[data_list[k].line_indices]
		if k % 3 == 2:
			data_list[k].efficiencies = data_list[k].line_intensities / incident_pol45.intensity[data_list[k].line_indices]
		if k % 3 == 0:
			data_list[k].efficiencies = data_list[k].line_intensities / incident_pol90.intensity[data_list[k].line_indices]

	#Lists for the wavelengths and intensities of each measured efficiency
	pol0_centers = []
	pol45_centers = []
	pol90_centers = []
	pol0_efficiencies = []
	pol45_efficiencies = []
	pol90_efficiencies = []

	#Actually store values in the lists above
	record_efficiencies()

	#Plot the summary of all efficiencies for each polarization state
	plot_summary()
	
	#Plot all the data for 1 observation
	plot_example()
	
	#Show the plots
	plt.show()