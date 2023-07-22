import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns

# Define a custom function to convert seconds to "days-HH:MM:SS" format
def seconds_to_time_str(total_seconds):
    days, remainder = divmod(total_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(days)}-{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

# Function to convert a time string in "days-HH:MM:SS" format to seconds
def time_str_to_seconds(time_str):
    time_components = time_str.split('-')

    if len(time_components) == 2:
        days = int(time_components[0])
        time_str = time_components[1]
    else:
        days = 0
        time_str = time_components[0]
    
    # Parse time string into a datetime object
    time_obj = datetime.strptime(time_str, '%H:%M:%S')

    # Calculate total seconds
    total_seconds = timedelta(hours=time_obj.hour, minutes=time_obj.minute, seconds=time_obj.second).total_seconds()

    if len(time_components) == 2:
        total_seconds += days * 24 * 60 * 60

    return total_seconds

# Define a custom function to convert megabytes to gigabytes
def convert_to_gigabytes(req_mem):
    if req_mem.endswith('Mn'):
        # Convert megabytes to gigabytes and append 'Gn'
        return str(float(req_mem[:-2]) / 1000) + 'Gn'
    elif req_mem.endswith('Mc'):
        # Convert megabytes to gigabytes and append 'Gc'
        return str(float(req_mem[:-2]) / 1000) + 'Gc'
    else:
        # Return unchanged for other cases
        return req_mem

# Define a custom function to convert megabytes to gigabytes
def convert_to_gigabytes_float(req_mem):
    if req_mem.endswith('Mn'):
        # Convert megabytes to gigabytes and append 'Gn'
        return float(req_mem[:-2]) / 1000
    elif req_mem.endswith('Mc'):
        # Convert megabytes to gigabytes and append 'Gc'
        return float(req_mem[:-2]) / 1000
    elif req_mem.endswith('Gn'):
        # Convert megabytes to gigabytes and append 'Gc'
        return float(req_mem[:-2])
    else:
        # Return unchanged for other cases
        return float(req_mem[:-2])

# Convert the Time (Days-HH:MM;SS) column to seconds
def convert_time_seconds(selected_rows_copy, column_header):
    return selected_rows_copy[column_header].apply(time_str_to_seconds)

def plot_frequency_job_partition(selected_rows, title, xlabel, ylabel):
    # Find the frequency of each Partition
    partition_frequency = selected_rows['Partition'].value_counts()

    # # Print the user frequency
    # print("Partition Frequency:")
    # print(partition_frequency)

    # Set the Seaborn style to include gridlines
    sns.set_style('whitegrid')
    # Plot the user frequency using a bar plot
    plt.figure(figsize=(12, 6))
    plt.subplots_adjust(bottom=0.25)
    sns.barplot(x=partition_frequency.index, y=partition_frequency.values)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(rotation=45, ha='right')  # Rotate the x-axis labels and align them to the right
    # Set the y-axis to log scale
    plt.yscale('log')
    # Enable grid for the x-axis
    plt.grid(axis='x')
    plt.tight_layout()  # Adjust the spacing between the bars and the plot borders
    plt.show()

def plot_reqcpus_frequency(selected_rows_copy, title, xlabel, ylabel):
    reqCPU_frequency= selected_rows_copy['ReqCPUS'].value_counts()

    # Sort the reqCPU_frequency Series in ascending order by index (which contains the ReqCPUS values)
    reqCPU_frequency.index = reqCPU_frequency.index.astype(int)
    reqCPU_frequency = reqCPU_frequency.sort_index()

    # # Print ReqCPUs freqyency
    # print("ReqCPUs frequency:")
    # print(reqCPU_frequency)

    # Set the Seaborn style to include gridlines
    sns.set_style('whitegrid')
    # Plot the user frequency using a bar plot
    plt.figure(figsize=(16, 6))
    plt.subplots_adjust(bottom=0.25)
    sns.barplot(x=reqCPU_frequency.index, y=reqCPU_frequency.values)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(rotation=45, ha='right')  # Rotate the x-axis labels and align them to the right
    # Set the y-axis to log scale
    plt.yscale('log')
    # Enable grid for the x-axis
    plt.grid(axis='x')
    plt.tight_layout()  # Adjust the spacing between the bars and the plot borders
    plt.show()

def plot_user_frequency(selected_rows_copy, title, xlabel, ylabel):
    user_frequency = selected_rows_copy['User'].value_counts()

    # Sort the user_frequency Series in ascending order by index (which contains the User values)
    user_frequency = user_frequency.sort_index()

    # # Print the user frequency
    # print("User Frequency:")
    # print(user_frequency)

    # Set the Seaborn style to include gridlines
    sns.set_style('whitegrid')
    # Plot the user frequency using a bar plot
    plt.figure(figsize=(16, 6))
    plt.subplots_adjust(bottom=0.25)
    sns.barplot(x=user_frequency.index, y=user_frequency.values)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(rotation=45, ha='right')  # Rotate the x-axis labels and align them to the right
    # Set the y-axis to log scale
    plt.yscale('log')
    # Enable grid for the x-axis
    plt.grid(axis='x')
    plt.tight_layout()  # Adjust the spacing between the bars and the plot borders
    plt.show()

def plot_reqmem_bin_count(selected_rows_copy, title, xlabel, ylabel):
    # Apply the custom conversion funtion to the 'ReqMem' colum in to convent string to float where cpu==1
    selected_rows_copy['ReqMem'] = selected_rows_copy['ReqMem'].apply(convert_to_gigabytes_float)

    # Define the bin edges for the 'ReqMem' column (up to 200G)
    bin_edges = np.arange(0, 201, 5, dtype=float)  # up to 200G

    # Define the labels for each bin range
    bin_labels = [f'{i}-{i+5} G' for i in bin_edges[:-1]]

    # Use pd.cut to assign each row to the appropriate bin based on 'Elapsed' values
    selected_rows_copy['ReqMem Bin'] = pd.cut(selected_rows_copy['ReqMem'], bins=bin_edges, labels=bin_labels, right=False)

    # # Print the DataFrame with the 'Elapsed Bin' column
    # print(selected_rows_copy[['ReqMem', 'ReqMem Bin']])

    # Count the occurrences of each bin label
    bin_counts = selected_rows_copy['ReqMem Bin'].value_counts()

    # # Print the counts for each bin
    # print("Bin Counts:")
    # print(bin_counts)

    # Set the Seaborn style to include gridlines
    sns.set_style('whitegrid')
    # Increase the figure size and adjust margins to accommodate longer x-axis labels
    plt.figure(figsize=(16, 6))
    plt.subplots_adjust(bottom=0.25)
    # Plot the bin counts with automatically chosen distinct colors using Seaborn
    sns.barplot(x=bin_counts.index, y=bin_counts.values)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(rotation=45, ha='right')
    # Set the y-axis to log scale
    plt.yscale('log')
    # Enable grid for the x-axis
    plt.grid(axis='x')
    plt.tight_layout()  # Adjust the spacing between the bars and the plot borders
    plt.show()

def plot_elapsed_bin_count(selected_rows_copy, bin_edges, bin_labels, title, xlabel, ylabel):
    # Use pd.cut to assign each row to the appropriate bin based on 'Elapsed' values
    selected_rows_copy['Elapsed Bin'] = pd.cut(selected_rows_copy['Elapsed'], bins=bin_edges, labels=bin_labels, right=False)

    # Print the DataFrame with the 'Elapsed Bin' column
    print(selected_rows_copy[['Elapsed', 'Elapsed Bin']])

    # Count the occurrences of each bin label
    bin_counts = selected_rows_copy['Elapsed Bin'].value_counts()

    # Print the counts for each bin
    print("Bin Counts:")
    print(bin_counts)

    # Set the Seaborn style to include gridlines
    sns.set_style('whitegrid')
    # Increase the figure size and adjust margins to accommodate longer x-axis labels
    plt.figure(figsize=(12, 6))
    plt.subplots_adjust(bottom=0.25)
    # Plot the bin counts with automatically chosen distinct colors using Seaborn
    sns.barplot(x=bin_counts.index, y=bin_counts.values)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(rotation=45, ha='right')
    # Set the y-axis to log scale
    plt.yscale('log')
    # Enable grid for the x-axis
    plt.grid(axis='x')
    plt.tight_layout()  # Adjust the spacing between the bars and the plot borders
    plt.show()

def calculate_cputime_per_user(selected_rows):
    # Group the DataFrame by 'User' and calculate the total 'CPUTime' for each user
    total_cputime_per_user = selected_rows.groupby('User')['CPUTime'].sum()

    # Convert the total CPUTime back to "days-HH:MM:SS" format
    total_cputime_per_user = total_cputime_per_user.apply(seconds_to_time_str)

    return total_cputime_per_user

def calculate_elapsedtime_per_user(selected_rows):
    # Group the DataFrame by 'User' and calculate the total 'ElapsedTime' for each user
    total_elapsedtime_per_user = selected_rows.groupby('User')['Elapsed'].sum()

    # Convert the total ElapsedTime back to "days-HH:MM:SS" format
    total_elapsedtime_per_user = total_elapsedtime_per_user.apply(seconds_to_time_str)

    return total_elapsedtime_per_user

def plot_elapsedtime_cputime_per_user(selected_rows_copy):
    total_cputime_per_user = selected_rows_copy.groupby('User')['CPUTime'].sum()
    total_elapsedtime_per_user = selected_rows_copy.groupby('User')['Elapsed'].sum()

    # Find the maximum y-axis value between total_cputime_per_user and total_elapsedtime_per_user
    max_y = max(total_cputime_per_user.max(), total_elapsedtime_per_user.max())

    # Create two subplots (side by side)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Plot the total CPUTime for each user using a line chart with log scale and solid dots
    sns.scatterplot(x=total_cputime_per_user.index, y=total_cputime_per_user.values, color='blue', marker='o', s=30, ax=ax1)
    ax1.set_xlabel('User')
    ax1.set_ylabel('Total CPUTime (seconds)')
    ax1.set_title(f'Total CPUTime of Each User {ncpu} [Year: {year}]')
    ax1.set_xticks(range(len(total_cputime_per_user.index)))
    ax1.set_xticklabels(total_cputime_per_user.index, rotation=45, ha='right')
    ax1.set_yscale('log')
    ax1.set_ylim(0.1, max_y*10)  # Set y-axis limits based on the maximum value
    ax1.grid(True)

    # Annotate each data point on the plot with its corresponding value
    for x, y in zip(total_cputime_per_user.index, total_cputime_per_user.values):
        ax1.text(x, y, f'{seconds_to_time_str(y)}', ha='right', va='center', fontsize=8, rotation=90)
    
    # Plot the total ElapsedTime for each user using a line chart with log scale and solid dots
    sns.scatterplot(x=total_elapsedtime_per_user.index, y=total_elapsedtime_per_user.values, color='blue', marker='o', s=30, ax=ax2)
    ax2.set_xlabel('User')
    ax2.set_ylabel('Total ElapsedTime (seconds)')
    ax2.set_title(f'Total ElapsedTime of Each User {ncpu} [Year: {year}]')
    ax2.set_xticks(range(len(total_elapsedtime_per_user.index)))
    ax2.set_xticklabels(total_elapsedtime_per_user.index, rotation=45, ha='right')
    ax2.set_yscale('log')
    ax2.set_ylim(0.1, max_y*10)  # Set y-axis limits based on the maximum value
    ax2.grid(True)

    # Annotate each data point on the plot with its corresponding value
    for x, y in zip(total_elapsedtime_per_user.index, total_elapsedtime_per_user.values):
        ax2.text(x, y, f'{seconds_to_time_str(y)}', ha='right', va='center', fontsize=8, rotation=90)

    plt.tight_layout()
    plt.show()


def plot_elapsedtime_vs_cputime_box(selected_rows_copy, bin_edges, bin_labels, title, xlabel, ylabel):
    # Use pd.cut to assign each row to the appropriate bin based on 'Elapsed' values
    selected_rows_copy['Elapsed Bin'] = pd.cut(selected_rows_copy['Elapsed'], bins=bin_edges, labels=bin_labels, right=False)
    print(selected_rows_copy)

    # Create the box plot using Seaborn
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='Elapsed Bin', y='Elapsed', data=selected_rows_copy, order=bin_labels)
    # sns.scatterplot(data=selected_rows_copy, color='blue', marker='o', s=30)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(rotation=45, ha='right')
    # Set the y-axis to log scale
    plt.yscale('log')
    plt.tight_layout()
    plt.show()


# Data of the Year
year= 2021
# Number of CPU 'eq 1' or 'gt 1'
ncpu= 'gt 1'

def main():
    # Read the data from the file.txt file
    filename = '2021/dt20210101-20211231.txt'
    with open(filename, 'r') as file:
        data = file.readlines()

    # Split the data into individual columns using the "|" separator
    data = [line.strip().split('|') for line in data]

    # Create a Pandas DataFrame with the column headers and the extracted data
    headers = data[0]  # Assuming the first row contains the column headers
    data = data[1:]  # Remove the header row from the data
    # print(headers)

    # Create the DataFrame
    df = pd.DataFrame(data, columns=headers)
    # print(df)

    # Select rows where 'ReqCPUS' is 1 and 'State' is COMPLETED and 'Partition' isn't devel
    selected_rows = df[(df['ReqCPUS'] != '1') & (df['State'] == 'COMPLETED') & (df['Partition'] != "devel")]
    # selected_rows = df[(df['ReqCPUS'] != '1') & (df['State'] == 'TIMEOUT') & (df['Partition'] != "devel")]

    # Print the selected data
    print(selected_rows)

    # PART 0.1: Find the frequency of each Job in Partition
    xlabel = 'Partition'
    ylabel = 'Job Count'
    title = (f'Job Frequency of Partition of ReqCPU {ncpu} [Year: {year}]')
    plot_frequency_job_partition(selected_rows, title, xlabel, ylabel)

    # Create a copy of the selected_rows DataFrame
    selected_rows_copy = selected_rows.copy()

    # Convert the 'ElapsedTime' column to seconds
    selected_rows_copy['Elapsed']= convert_time_seconds(selected_rows_copy, 'Elapsed')
    # print(selected_rows_copy['Elapsed'])

    # Convert the 'CPUTime' column to seconds
    selected_rows_copy['CPUTime']= convert_time_seconds(selected_rows_copy, 'CPUTime')
    # print(selected_rows_copy['CPUTime'])

    # Find the Total CPU Time oer User
    total_cputime_per_user= calculate_cputime_per_user(selected_rows_copy)

    # Print the total ElapsedTime for each user
    # print("Total CPUTime per User:")
    # print(total_cputime_per_user)

    # Find the Total Elapsed Time oer User
    total_elapsedtime_per_user= calculate_elapsedtime_per_user(selected_rows_copy)

    # Print the total ElapsedTime for each user
    # print("Total ElapsedTime per User:")
    # print(total_elapsedtime_per_user)

    # Plot 0.2: Plot total CPUTime and total ElapsedTime for each user using a line/scatter chart
    plot_elapsedtime_cputime_per_user(selected_rows_copy)


    # PART 1: Great Then Then 1 Day Elapsed Time Jobs
    # Create a copy of the selected_rows DataFrame
    selected_rows_copy_gt1 = selected_rows_copy.copy()

    # Filter rows where the 'Elapsed' column is greater than or equal to 1 day (86400 seconds)
    selected_rows_copy_gt1 = selected_rows_copy_gt1[selected_rows_copy_gt1['Elapsed'] > 86400.0]

    # Print the DataFrame with the modified 'ReqMem' column
    # print(selected_rows_copy_gt1)

    # PART 1.1: Find the frequency of each Job Elapsed Time of job Elapsed time gt 24H to 30Days
    # Define the bin edges for the 'Elapsed' column (up to 30 days)
    bin_edges = np.arange(0, 30*24*60*60 + 1, 86400)
    # Define the labels for each bin range
    bin_labels = [f'{i}-{i+1} days' for i in range(30)]
    xlabel = 'Time Bin'
    ylabel = 'Job Count'
    title = (f'Job Count of Elapsed Time gt 24h - up to 30 days and ReqCPU {ncpu} [Year: {year}]')
    plot_elapsed_bin_count(selected_rows_copy_gt1, bin_edges, bin_labels, title, xlabel, ylabel)

    # PART 1.1.1: Find the frequency of each Job Elapsed Time of job Elapsed time gt 24H to Greater Than 30Days
    # selected_rows_copy_gt30 = selected_rows_copy.copy()
    # selected_rows_copy_gt30 = selected_rows_copy_gt30[selected_rows_copy_gt30['Elapsed'] > (86400.0*30.0)]
    # print(selected_rows_copy_gt30)
    # Define the bin edges for the 'Elapsed' column (gt 30 days)
    bin_edges = np.append(np.arange(0, 31) * 86400, selected_rows_copy['Elapsed'].max() + 1)
    # Define the labels for each bin range
    bin_labels = [f'{i}-{i+1} days' for i in range(30)] + [f'>30 days']
    xlabel = 'Time Bin'
    ylabel = 'Job Count'
    title = (f'Job Count of Elapsed Time gt 24h a (including >30 days) nd ReqCPU {ncpu} [Year: {year}]')
    plot_elapsed_bin_count(selected_rows_copy_gt1, bin_edges, bin_labels, title, xlabel, ylabel)

    # # Filter rows where the 'Elapsed' column is greater than or equal to 1 day (86400 seconds)
    # selected_rows_copy_gt20 = selected_rows_copy.copy()
    # selected_rows_copy_gt20 = selected_rows_copy_gt20[selected_rows_copy_gt20['Elapsed'] > (86400.0*10.0)]
    # # print(selected_rows_copy_gt20)
    # # Define the bin edges for the 'Elapsed' column (up to 10 days)
    # # bin_edges = np.arange(86400*10, 30*24*60*60 + 1, 86400)
    # bin_edges = np.append(np.arange(10, 31) * 86400, selected_rows_copy['Elapsed'].max() + 1)
    # # print(bin_edges)
    # # Define the labels for each bin range
    # # bin_labels = [f'{i+10}-{i+11} days' for i in range(20)]
    # bin_labels = [f'{i+10}-{i+11} days' for i in range(20)] + [f'>30 days']
    # # print(bin_labels)
    # xlabel = 'ElapseTime Bin'
    # ylabel = 'ElapsedTIme'
    # title = (f'Job Count of Elapsed Time gt 30h and ReqCPU {ncpu} [Year: {year}]')
    # plot_elapsedtime_vs_cputime_box(selected_rows_copy_gt20, bin_edges, bin_labels, title, xlabel, ylabel)

    # PART 1.2: Find the frequency of each Job ReqMem of job Elapsed time gt 24H
    xlabel = 'ReqMem Bin'
    ylabel = 'Job Count'
    title = (f'Job Count of ReqMem bins Elapsed Time gt 24h and ReqCPU {ncpu} [Year: {year}]')
    plot_reqmem_bin_count(selected_rows_copy_gt1, title, xlabel, ylabel)

    # PART 1.3: Find the frequency of each User of job Elapsed time gt 24H
    xlabel = 'User'
    ylabel = 'Frequency'
    title = (f'User Frequency of Elapsed Time gt 24h and ReqCPU {ncpu} [Year: {year}]')
    plot_user_frequency(selected_rows_copy_gt1, title, xlabel, ylabel)

    # PART 1.4: Find the frequency of each ReqCPUs of job Elapsed time gt 24H
    xlabel= 'ReqCPUs'
    ylabel= 'Frequency'
    title = (f'ReqCPUs Frequency of gt 24h ReqCPU {ncpu} [Year: {year}]')
    plot_reqcpus_frequency(selected_rows_copy_gt1, title, xlabel, ylabel)


    # PART 2: Less Then 1 Day Elapsed Time Jobs
    # Create a copy of the selected_rows DataFrame
    selected_rows_copy_lt1 = selected_rows_copy.copy()

    # # Filter rows where the 'Elapsed' column is greater than or equal to 1 day (86400 seconds)
    # selected_rows_copy_lt1 = selected_rows_copy_lt1[selected_rows_copy_lt1['Elapsed'] < 86400.0]

    # Filter rows where the 'Elapsed' column is greater than or equal to 1 day (86400 seconds) and less than equal to 30mim (1800 seconds)
    selected_rows_copy_lt1 = selected_rows_copy_lt1[(selected_rows_copy_lt1['Elapsed'] >= 1800.0) & (selected_rows_copy_lt1['Elapsed'] <= 86400.0)]

    # Print the DataFrame with the modified 'ReqMem' column
    # print(selected_rows_copy_lt1)

    # PART 2.1: Find the frequency of each Job Elapsed Time of job Elapsed time lt 24h
    # Define the bin edges for the 'Elapsed' column (up to 24h)
    bin_edges = np.arange(0, 24*60*60 + 1, 60*60)
    # Define the labels for each bin range
    bin_labels = [f'{i}-{i+1} H' for i in range(24)]
    xlabel = 'Time Bin'
    ylabel = 'Job Count'
    title = (f'Job Count of Elapsed Time lt 24h and ReqCPU {ncpu} [Year: {year}]')
    plot_elapsed_bin_count(selected_rows_copy_lt1, bin_edges, bin_labels, title, xlabel, ylabel)


    # PART 2.2: Find the frequency of each Job ReqMem of job Elapsed time lt 24H 
    xlabel = 'ReqMem Bin'
    ylabel = 'Job Count'
    title = (f'Job Count of ReqMem bins Elapsed Time lt 24h and ReqCPU {ncpu} [Year: {year}]')
    plot_reqmem_bin_count(selected_rows_copy_lt1, title, xlabel, ylabel)

    # PART 2.3: Find the frequency of each User of job Elapsed time lt 24H
    xlabel = 'User'
    ylabel = 'Frequency'
    title = (f'User Frequency of Elapsed Time lt 24h and ReqCPU {ncpu} [Year: {year}]')
    plot_user_frequency(selected_rows_copy_lt1, title, xlabel, ylabel)

    # PART 2.4: Find the frequency of each ReqCPUs of job Elapsed time lt 24H
    xlabel= 'ReqCPUs'
    ylabel= 'Frequency'
    title = (f'ReqCPUs Frequency of lt 24h ReqCPU {ncpu} [Year: {year}]')
    plot_reqcpus_frequency(selected_rows_copy_lt1, title, xlabel, ylabel)


    # # Find the largest value in the 'ElapsedTimeInSeconds' column
    # largest_value = df['ElapsedTimeInSeconds'].max()
    # print("Largest value in ElapsedTimeInSeconds column:", largest_value)

if __name__ == "__main__":
    main()