import numpy as np
import plot_grating_results
import matplotlib.pyplot as plt

class Data:
	"""Class to store data from a spectrum"""
	def __init__(self, file_suffix, diffracted = True):
		self.filename = '/Users/Oakley/Documents/Work/ViSP/gratings_tests/' + file_suffix
		self.read_spectrum(file_suffix)

		if (file_suffix[0:10]=='03_29_2013'):
			self.diffracted_exposure_length = 400000.
			self.direct_exposure_length = 25000.
			self.peak_limit = 5000.
		elif (file_suffix[0:10]=='04_05_2013'):
			self.diffracted_exposure_length = 50000.
			self.direct_exposure_length = 3000.	
			self.peak_limit = 2000.
		else:
			print 'ERROR, no exposure lengths set for this date'

		if diffracted == False:
			self.intensity = self.intensity / self.direct_exposure_length
		else:
			self.line_indices = []
			self.line_centers = []
			self.line_intensities = []
			self.find_peaks()
			self.intensity = self.intensity / self.diffracted_exposure_length
			self.line_intensities = np.array(self.line_intensities) / self.diffracted_exposure_length

		
	def read_spectrum(self,file_suffix):
		#Read the data from .txt file
		vibe_data_file = open(self.filename,'r')
		print "Opening File: ", self.filename
		data_array = np.genfromtxt(vibe_data_file,delimiter=',',dtype='f')
		self.wavelength = data_array[:,0]
		self.intensity = data_array[:,1]		

	
	def find_peaks(self):
		#Determine the location (wavelength and index) and intensity of each emission line


		lines = [k for k,j in enumerate(self.intensity) if j > self.peak_limit]
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

		# print self.line_centers
		# plt.plot(self.wavelength,self.intensity)
		# plt.show()	

def record_efficiencies(pol0_centers, pol45_centers, pol90_centers, pol0_efficiencies, pol45_efficiencies, pol90_efficiencies):
	if (date == '3_29_2013'):
		for k in range(0,39,3):
			for j in range(len(data_list[k].line_centers)):
				pol0_centers = np.append(pol0_centers,data_list[k].line_centers[j])
				pol0_efficiencies = np.append(pol0_efficiencies,data_list[k].efficiencies[j])
				

		for k in range(1,39,3):
			for j in range(len(data_list[k].line_centers)):
				pol45_centers = np.append(pol45_centers,data_list[k].line_centers[j])
				pol45_efficiencies = np.append(pol45_efficiencies,data_list[k].efficiencies[j])
		
		for k in range(2,39,3):
			for j in range(len(data_list[k].line_centers)):
				pol90_centers = np.append(pol90_centers, data_list[k].line_centers[j])
				pol90_efficiencies = np.append(pol90_efficiencies, data_list[k].efficiencies[j])

	elif (date == '04_05_2013'):
		for k in range(0,18,2):
			for j in range(len(data_list[k].line_centers)):
				pol0_centers = np.append(pol0_centers, data_list[k].line_centers[j])
				pol0_efficiencies = np.append(pol0_efficiencies, data_list[k].efficiencies[j])
				

		for k in range(1,18,2):
			for j in range(len(data_list[k].line_centers)):
				pol90_centers = np.append(pol90_centers, data_list[k].line_centers[j])
				pol90_efficiencies = np.append(pol90_efficiencies, data_list[k].efficiencies[j])
	else:
		print 'ERROR - No efficiency recording for this date'
	
	return pol0_centers, pol45_centers, pol90_centers, pol0_efficiencies, pol45_efficiencies, pol90_efficiencies

def load_incident_data(date):
	if (date == '03_29_2013'):
		incident_pol0 = Data(date + '/' + 'intensity_25000_pol0.txt',diffracted = False)
		incident_pol45 = Data(date + '/' + 'intensity_25000_pol45.txt',diffracted = False)
		incident_pol90 = Data(date + '/' + 'intensity_25000_pol90.txt',diffracted = False)

	elif (date == '04_05_2013'):
		incident_pol0 = Data(date + '/' + 'noF_3000_intensity_pol0.txt',diffracted = False)
		incident_pol90 = Data(date + '/' + 'noF_3000_intensity_pol90.txt',diffracted = False)
		incident_pol45 = 0
	else:
		print 'ERROR - No incident light dataset loaded'
		
	return incident_pol0, incident_pol45, incident_pol90

def load_data(data_list, date):
	
	if (date == '03_29_2013'):
		for k in range(0,39):
			data_list.append(Data(date + '/' + str(k+1)+'.txt'))
			
			if k % 3 == 1:
				data_list[k].efficiencies = data_list[k].line_intensities / incident_pol0.intensity[data_list[k].line_indices]
			if k % 3 == 2:
				data_list[k].efficiencies = data_list[k].line_intensities / incident_pol45.intensity[data_list[k].line_indices]
			if k % 3 == 0:
				data_list[k].efficiencies = data_list[k].line_intensities / incident_pol90.intensity[data_list[k].line_indices]

	elif (date == '04_05_2013'):
		for k in range(0,18):
			data_list.append(Data(date + '/' + str(k+1)+'.txt'))
			if k % 2 == 1:
				data_list[k].efficiencies = data_list[k].line_intensities / incident_pol0.intensity[data_list[k].line_indices]
			if k % 2 == 0:
				data_list[k].efficiencies = data_list[k].line_intensities / incident_pol90.intensity[data_list[k].line_indices]
	else:
		print 'ERROR - no data for this date!'
		

def sort_results(pol0_centers, pol45_centers, pol90_centers, pol0_efficiencies, pol45_efficiencies, pol90_efficiencies):
	print np.argsort(pol0_centers)



	pol0_efficiencies = pol0_efficiencies[np.argsort(pol0_centers)]
	pol0_centers = pol0_centers[np.argsort(pol0_centers)]

	pol90_efficiencies = pol90_efficiencies[np.argsort(pol90_centers)]
	pol90_centers = pol90_centers[np.argsort(pol90_centers)]

	return pol0_centers, pol45_centers, pol90_centers, pol0_efficiencies, pol45_efficiencies, pol90_efficiencies

if __name__ == "__main__":

	#Select the data set
	date = '04_05_2013'

	#Load the data from the direct mirror bounce at each polarization
	incident_pol0, incident_pol45, incident_pol90 = load_incident_data(date)
	
	#List of diffracted data sets	
	data_list = []
	
	#Load the data from each of the diffracted spectrum
	load_data(data_list, date)

	print data_list[0].line_centers, data_list[0].line_intensities
	print data_list[1].line_centers, data_list[1].line_intensities

	#Lists for the wavelengths and intensities of each measured efficiency
	pol0_centers = np.array([])
	pol45_centers = pol0_centers
	pol90_centers = pol0_centers
	pol0_efficiencies = pol0_centers
	pol45_efficiencies = pol0_centers
	pol90_efficiencies = pol0_centers

	#Actually store values in the lists above
	pol0_centers, pol45_centers, pol90_centers, pol0_efficiencies, pol45_efficiencies, pol90_efficiencies = record_efficiencies(pol0_centers, pol45_centers, pol90_centers, pol0_efficiencies, pol45_efficiencies, pol90_efficiencies)

	# print pol0_centers, pol0_efficiencies
	# print pol90_centers, pol90_efficiencies

	pol0_centers, pol45_centers, pol90_centers, pol0_efficiencies, pol45_efficiencies, pol90_efficiencies = sort_results(pol0_centers, pol45_centers, pol90_centers, pol0_efficiencies, pol45_efficiencies, pol90_efficiencies)

	# print pol0_centers
	# print pol0_efficiencies

	#Plot the summary of all efficiencies for each polarization state
	plot_grating_results.plot_summary(pol0_centers, pol0_efficiencies,pol45_centers,pol45_efficiencies,pol90_centers,pol90_efficiencies)
	
	#Plot all the data for 1 observation
	plot_grating_results.plot_example(data_list,incident_pol90)
