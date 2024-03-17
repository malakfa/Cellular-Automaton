import numpy as np
import matplotlib.pyplot as plt

# Load temperature data from file
temperature_file_path = 'temperature.txt'  
temperature_data = np.loadtxt(temperature_file_path)

# Load air pollution data from file
air_pollution_file_path = 'air_pollution.txt' 
air_pollution_data = np.loadtxt(air_pollution_file_path)

# 1. Calculate and display statistical information
temperature_mean = np.mean(temperature_data)
temperature_std = np.std(temperature_data)
air_pollution_mean = np.mean(air_pollution_data)
air_pollution_std = np.std(air_pollution_data)

print(f"Temperature Mean: {temperature_mean}")
print(f"Temperature Standard Deviation: {temperature_std}")
print(f"Air Pollution Mean: {air_pollution_mean}")
print(f"Air Pollution Standard Deviation: {air_pollution_std}")

# 2. Display the graph
normalized_temperature = (temperature_data - temperature_mean) / temperature_std
normalized_air_pollution = (air_pollution_data - air_pollution_mean) / air_pollution_std

plt.plot(normalized_temperature, label='Normalized Temperature')
plt.plot(normalized_air_pollution, label='Normalized Air Pollution')
plt.title("Normalized Parameters Over the Year")
plt.xlabel("Day of the Year")
plt.ylabel("Normalized Value (Standard Deviation)")
plt.legend()
plt.show()

correlation_coefficient = np.corrcoef(normalized_temperature, normalized_air_pollution)[0, 1]
print(f"Pearson Correlation Coefficient: {correlation_coefficient}")
