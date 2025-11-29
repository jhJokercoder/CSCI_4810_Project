import os
import pandas as pd
import matplotlib.pyplot as plt

#Get the current working directory 
cwd = os.getcwd()

#Get the parent directory
parent_dir = os.path.dirname(cwd)

#Get the absolute path to the KFall Dataset folder, the label_data folder, and the sensor_data folder
kfall_folder_path = os.path.join(parent_dir, "KFall Dataset")
labels_folder_path = os.path.join(kfall_folder_path, "label_data")
sensor_data_folder_path = os.path.join(kfall_folder_path, "sensor_data")

#Get the list of subfolders in the sensor_data folder
sensor_data_subfolders_list = os.listdir(sensor_data_folder_path)

#Get the list of files in the label_data folder
label_data_files_list = os.listdir(labels_folder_path)

#This dictionary will have key-value pairs where the key is the sensor_data subfolder name and the value is the number of files in the folder
sensor_data_num_files = {}

#This list has the number of rows each sensor data file has
sample_lengths = []

#This list has the lengths of the "fall windows"
fall_window_lengths = []

for file in label_data_files_list:

	#Get the sensor_data subfolder name and Subject ID that corresponds to the current label file
	sensor_data_subfolder = file.split('_')[0]
	subject_id = sensor_data_subfolder.split('SA')[1]

	#Get the absolute path to the sensor_data subfolder
	sensor_data_subfolder_path = os.path.join(sensor_data_folder_path, sensor_data_subfolder)

	#Get the list of files in the sensor_data subfolder
	sensor_data_subfolder_files_list = os.listdir(sensor_data_subfolder_path)

	#Get the unique task id's from the file names in the sensor_data subfolder and count the number of files in the folder
	task_ids = []
	counter = 0
	for sensor_file in sensor_data_subfolder_files_list:
		split_filename = sensor_file.split('T')[1]
		tsk_id = split_filename.split('R')[0]

		if tsk_id in task_ids:
			pass
		else:
			task_ids.append(tsk_id)
		counter += 1

	#Add key value pair to sensor_data_num_files dictionary where the key is the current sensor_data subfolder name and the value is the number of files in the folder
	sensor_data_num_files['SA' + subject_id] = counter

	#Get the absolute file path for the current label file
	label_file = os.path.join(labels_folder_path, file)

	#Convert Excel file to Pandas Dataframe
	label_dataframe = pd.read_excel(label_file)

	#Find the number of rows in the Pandas Dataframe
	num_of_rows_label_dataframe = len(label_dataframe)

	current_task_id = ''
	for i in range(num_of_rows_label_dataframe):

		#Get the Task Code (Task ID)
		task_code_task_id = label_dataframe.at[i, "Task Code (Task ID)"]

		#Get the Trial ID 
		trial_id_num = label_dataframe.at[i, "Trial ID"]

		#Convert the Trial ID to a string and add 0 in front if the Trial ID is less than 10
		if trial_id_num	< 10:
			trial_id = '0' + str(trial_id_num)
		else:
			trial_id = str(trial_id_num)

		#Get the Onset Frame and Impact Frame
		onset_frame = label_dataframe.at[i, "Fall_onset_frame"]
		impact_frame = label_dataframe.at[i, "Fall_impact_frame"]

		#Calculate the length of the "fall window"
		window_length = impact_frame - onset_frame

		#Add the length of the "fall window" in seconds to the fall_window_lengths list
		fall_window_lengths.append(window_length)

		#If the Task Code (Task ID) column has a null value then keep the current Task ID, if not then get the new Task ID
		if pd.isnull(task_code_task_id):
			task_id = current_task_id
		else:

			#Get the Task Id from the Task Code (Task Id), make it the new current Task ID, and remove it from the task_ids list
			first_split = task_code_task_id.split('(')[1]
			task_id = first_split.split(')')[0]
			current_task_id = task_id
			task_ids.remove(task_id)

		#Get the sensor_data filename
		sensor_data_filename = 'S' + subject_id + 'T' + task_id + 'R' + trial_id + '.csv'

		#Get the sensor_data file path
		sensor_data_file_path = os.path.join(sensor_data_subfolder_path, sensor_data_filename)

		#Convert CSV file to Pandas Dataframe
		sensor_dataframe = pd.read_csv(sensor_data_file_path)

		#Find the number of rows in the Pandas Dataframe
		num_of_rows_sensor_dataframe = len(sensor_dataframe)

		#Add the number of rows to the sample_lengths folder
		sample_lengths.append(num_of_rows_sensor_dataframe)

	#For the remaining Task Ids find the number of rows for the files with the remaining Task Ids and append the number to the sample_lengths list 
	for i in task_ids:
		t_id = 'T' + i

		for sensor_file in sensor_data_subfolder_files_list:
			#Get the Task Id from the filename
			split_filename = sensor_file.split('T')[1]
			id_num = split_filename.split('R')[0]
			compare_task_id = 'T' + id_num

			#If the Task Id in the filename is the same as the current Task Id then create labels that are all 0's, if not then pass
			if t_id == compare_task_id:

				#Convert CSV file to Pandas Dataframe
				sensor_dataframe2 = pd.read_csv(os.path.join(sensor_data_subfolder_path, sensor_file))

				#Find the number of rows in the Pandas Dataframe
				num_of_rows = len(sensor_dataframe2)

				#Add the number of rows to the sample_lengths folder
				sample_lengths.append(num_of_rows)

			else:
				pass

print("Total number of files:", len(sample_lengths))
print("Total number of fall windows:", len(fall_window_lengths))
print("Minimum sample length:", min(sample_lengths))
print("Maximum sample length:", max(sample_lengths))
print("Minimum fall window length:", min(fall_window_lengths))
print("Maximum fall window length:", max(fall_window_lengths))

#Make a new folder for the Histograms
fig_absolute_path = os.path.join(parent_dir, "Histograms")
os.makedirs(fig_absolute_path, exist_ok = True)

#Create bar graph showing the number of files in each sensor_data subfolder
subfolder_names = list(sensor_data_num_files.keys())
num_of_files = list(sensor_data_num_files.values())
plt.figure(figsize=(12, 8))
plt.bar(subfolder_names, num_of_files)
plt.title("Number of Files per Folder")
plt.xlabel("Folder Name")
plt.ylabel("Number of Files")
plt.xticks(rotation=45)
plt.savefig(os.path.join(fig_absolute_path, "files_per_folder.png"))
plt.show()

#Specify bin start and end points
bin_ranges_samples = [0, 700, 1400, 2100, 2800, 3500, 4200]

#Create histogram of sample lengths
plt.figure(figsize=(12, 8))
plt.hist(sample_lengths, bins=bin_ranges_samples, edgecolor='black')
plt.title("Number of Samples per Length")
plt.xlabel("Length of Sample (# of rows)")
plt.ylabel("Number of Samples")
plt.savefig(os.path.join(fig_absolute_path, "sample_lengths_hist.png"))
plt.show()

#Specify bin start and end points
bin_ranges = [0, 30, 60, 90, 120, 150]

#Create histogram of lengths of fall windows
plt.figure(figsize=(12, 8))
plt.hist(fall_window_lengths, bins=bin_ranges, edgecolor='black')
plt.title("Number of Fall Windows per Length")
plt.xlabel("Length of Fall Window (# of rows)")
plt.ylabel("Number of Fall Windows")
plt.savefig(os.path.join(fig_absolute_path, "fall_windows_hist"))
plt.show()
