""" 
Just a simple script to batch read tdms files from a given directory, 
plot them and save them as csv files.

author: Fabrizio Musacchio
date:   Feb 25, 2025

for reproducibility:

conda create -n tdms -y python mamba
conda activate tdms
mamba install -y numpy pandas matplotlib ipykernel nptdms
"""
# %% IMPORTS
import os
import matplotlib.pyplot as plt
import pandas as pd
from nptdms import TdmsFile

# set global properties for all plots:
plt.rcParams.update({'font.size': 14})
plt.rcParams["axes.spines.top"]    = False
plt.rcParams["axes.spines.bottom"] = False
plt.rcParams["axes.spines.left"]   = False
plt.rcParams["axes.spines.right"]  = False
# %% DEFINE PATHS
# set paths:
ROOT_PATH = "/Volumes/.../"   # MODIFY THIS PATH
input_folder    = os.path.join(ROOT_PATH, "Data")  # AND MODIFY THIS PATH

# save to excel? (True/False):
save_to_excel = False

# DO NOT MODIFY BELOW THIS LINE
analysis_folder = os.path.join(ROOT_PATH, "Analysis")
table_folder    = os.path.join(analysis_folder, "excel")
# create output directories if they don't exist:
os.makedirs(analysis_folder, exist_ok=True)
if save_to_excel:
    os.makedirs(table_folder, exist_ok=True)
# %% MAIN
# Get all TDMS files (ignore index files and hidden files):
tdms_files = [f for f in os.listdir(input_folder) 
              if f.endswith(".tdms") and not f.startswith(".")]

# process each TDMS file:
for tdms_filename_i, tdms_filename in enumerate(tdms_files):
    # tdms_filename = tdms_files[0]
    tdms_path = os.path.join(input_folder, tdms_filename)

    try:
        # read TDMS file:
        tdms_file = TdmsFile.read(tdms_path)

        for group in tdms_file.groups():
            # group = tdms_file.groups()[0]
            for channel in group.channels():
                # channel = group.channels()[0]
                data = channel[:]
                
                print(f"   Processing Group: {group.name}, Channel: {channel.name}")
                
                # attempt to get timestamps:
                try:
                    timestamps = channel.time_track()
                except KeyError:
                    timestamps = None  # No time track available

                # convert to DataFrame and save CSV file (if enabled):
                if save_to_excel:
                    df = pd.DataFrame({"Time": timestamps, "Value": data} if timestamps is not None else {"Value": data})
                    
                    # save CSV file:
                    csv_filename = f"{tdms_filename}_{group.name}_{channel.name}.csv"
                    # replace "/" with "_" in the filename:
                    csv_filename = csv_filename.replace("/", "_")
                    df.to_csv(os.path.join(table_folder, csv_filename), index=False)

                # plot data:
                plt.figure(figsize=(10, 5))
                plt.plot(timestamps, data, label=f"{group.name} - {channel.name}" if timestamps is not None else "Data")
                plt.xlabel("Time" if timestamps is not None else "Index")
                plt.ylabel("Value")
                # Remove .tdms extension from filename for display
                display_name = tdms_filename.replace(".tdms", "")
                plt.title(f"{display_name} - {group.name} - {channel.name}")
                plt.legend(loc="lower right")
                plt.grid()

                # save plot:
                plot_filename = f"{display_name}_{group.name}_{channel.name}.pdf"
                # replace "/" with "_" in the filename:
                plot_filename = plot_filename.replace("/", "_")
                plt.savefig(os.path.join(analysis_folder, plot_filename), transparent=True)
                plt.close()

        print(f"Processed {tdms_filename_i+1}/{len(tdms_files)}: {tdms_filename}")

    except Exception as e:
        print(f"Error processing {tdms_filename}: {e}")

print("Processing complete.")
# %% END