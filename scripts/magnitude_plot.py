import os
import pandas as pd
import matplotlib.pyplot as plt

#Get the current working directory 
cwd = os.getcwd()

#Get the parent directory
parent_dir = os.path.dirname(cwd)

#Dataset Folder Path
dataset_folder_path = os.path.join(parent_dir, 'Cleaned Dataset')

#Make a new folder that will store the magnitude plots
magnitude_plots_folder_path = os.path.join(parent_dir, "Magnitude Plots")
os.makedirs(magnitude_plots_folder_path, exist_ok = True)

#Get the list of subfolders in the Dataset folder
dataset_subfolders_list = os.listdir(dataset_folder_path)

for folder in dataset_subfolders_list:

	#Make a new subfolder in the Magnitude Plots folder
	magnitude_plots_subfolder_path = os.path.join(magnitude_plots_folder_path, folder)
	os.makedirs(magnitude_plots_subfolder_path, exist_ok = True)

	#Get the absolute path to the Dataset subfolder
	dataset_subfolder_path = os.path.join(dataset_folder_path, folder)

	#Get the list of files in the Dataset subfolder
	dataset_subfolder_files_list = os.listdir(dataset_subfolder_path)

	for data_file in dataset_subfolder_files_list:

		#Create filename for image of plot
		split_filename = data_file.split('.')[0]
		filename = split_filename + '.png'

		#Get the absolute file path for the sensor data file
		sd_file = os.path.join(dataset_subfolder_path, data_file)

		#Convert Excel file to Pandas Dataframe
		sd_dataframe = pd.read_csv(sd_file)

		#Get the x-values for the plot from the "TimeStamp(s)" column in CSV file
		x_values = sd_dataframe['TimeStamp(s)']

		#Plot the acceleration, gyroscope, and euler angle magnitude by the time in seconds

		#Set the figure size to 12 inches in width by 8 inches in length
		plt.figure(figsize=(12, 8))
		plt.plot(x_values, sd_dataframe['Acc_Mag'], label='Acc_Mag', color='red')
		plt.plot(x_values, sd_dataframe['Gyr_Mag'], label='Gyro_Mag', color='green')
		plt.plot(x_values, sd_dataframe['Euler_Mag'], label='Euler_Mag', color='blue')

		#If the CSV file has a 1 in the 'Label' column then find the time of the fall onset frame and fall impact frame
		if 1 in sd_dataframe['Label'].values:

			#Make a list of all the indicies where the row has a 1 in the Label column  
			rows = sd_dataframe.index[sd_dataframe['Label'] == 1].tolist()

			#The mimimum of the list will be the index where the time of the fall onset frame can be found
			first_row = min(rows)

			#The maximum of the list will be the index where the time of the fall impact frame can be found
			last_row = max(rows)

			#Find the time of the fall onset frame and fall impact frame
			first_x_value_vl = sd_dataframe.at[first_row, 'TimeStamp(s)']
			second_x_value_vl = sd_dataframe.at[last_row, 'TimeStamp(s)']

			#Plot vertical black lines at the time of the fall onset frame and fall impact frame
			plt.axvline(x=first_x_value_vl, color='black')
			plt.axvline(x=second_x_value_vl, color='black')

		#Set the x-label, y-label, title, and legend postion of the plot
		plt.xlabel('Time (seconds)')
		plt.ylabel('Magnitude')
		plt.title(split_filename)
		plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

		#Save the figure and close it so too much memory isn't consumed
		plt.tight_layout()
		plt.savefig(os.path.join(magnitude_plots_subfolder_path, filename))
		plt.close()
