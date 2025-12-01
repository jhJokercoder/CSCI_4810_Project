import os
import pandas as pd
from sklearn.preprocessing import StandardScaler

#Get the current working directory 
cwd = os.getcwd()

#Get the parent directory
parent_dir = os.path.dirname(cwd)

#Make a new folder for the standardized dataset
standardized_dataset_folder_path = os.path.join(parent_dir, "Standardized Dataset")
os.makedirs(standardized_dataset_folder_path, exist_ok = True)

#Get the absolute path to the Cleaned_Dataset folder
cleaned_dataset_folder_path = os.path.join(parent_dir, 'Cleaned Dataset')

#Get the list of subfolders in the Cleaned_Dataset folder
cleaned_dataset_subfolders_list = os.listdir(cleaned_dataset_folder_path)

#Create list that stores the dataframes containing the values for each feature 
feature_values = []

for folder in cleaned_dataset_subfolders_list:

	#Get the absolute path to the sensor_data subfolder
	sensor_data_subfolder_path = os.path.join(cleaned_dataset_folder_path, folder)

	#Get the list of files in the sensor_data subfolder
	sensor_data_subfolder_files_list = os.listdir(sensor_data_subfolder_path)

	for data_file in sensor_data_subfolder_files_list:

		#Get the absolute file path for the sensor_data file
		sd_file = os.path.join(sensor_data_subfolder_path, data_file)

		#Convert Excel file to Pandas Dataframe
		sd_dataframe = pd.read_csv(sd_file)

		#Select the specific rows and columns of the dataframe that contain the feature values and append that to the feature_values list
		features = sd_dataframe.iloc[:, 2:14]
		feature_values.append(features)

#Stack the dataframes on top of one another
feature_values_df = pd.concat(feature_values, ignore_index=True)

#Find the mean and standard deviation for each feature column
scaler = StandardScaler()
scaler.fit(feature_values_df)

print(scaler.mean_)
print(scaler.scale_)

for folder in cleaned_dataset_subfolders_list:

	#Make a new subfolder in the Standardized Dataset folder
	standardized_dataset_subfolder_path = os.path.join(standardized_dataset_folder_path, folder)
	os.makedirs(standardized_dataset_subfolder_path, exist_ok = True)

	#Get the absolute path to the sensor_data subfolder
	sensor_data_subfolder_path = os.path.join(cleaned_dataset_folder_path, folder)

	#Get the list of files in the sensor_data subfolder
	sensor_data_subfolder_files_list = os.listdir(sensor_data_subfolder_path)

	for data_file in sensor_data_subfolder_files_list:

		#Get the absolute file path for the sensor_data file
		sd_file = os.path.join(sensor_data_subfolder_path, data_file)

		#Convert Excel file to Pandas Dataframe
		sd_dataframe = pd.read_csv(sd_file)

		#Standardize the feature values
		features = sd_dataframe.iloc[:, 2:14]
		scaled_values = scaler.transform(features)

		#Replace feature values with standardized feature values
		sd_dataframe.iloc[:, 2:14] = pd.DataFrame(scaled_values, columns=features.columns, index=sd_dataframe.index)

		#Save the changes made to the Dataframe to a CSV file
		sd_dataframe.to_csv(os.path.join(standardized_dataset_subfolder_path, data_file), index = False)
