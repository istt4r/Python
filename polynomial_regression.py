import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from config import WEIGHT_OUTPUT, WEIGHT_INPUT

# Input and Output file location definitions
data_path = Path(WEIGHT_INPUT)
output_path = Path(WEIGHT_OUTPUT)

# Read the data from the text file
data = np.genfromtxt(data_path, delimiter=',')

# Extract the x and y values from the data
x = data[:, 0]
y = data[:, 1]

# Debugging statements
print("First 5 entries of x:", x[:5])
print("Last 5 entries of x:", x[-5:])
print("First 5 entries of y:", y[:5])
print("Last 5 entries of y:", y[-5:])

# Use a lower degree polynomial fit
degree = 10
coefficients = np.polyfit(x, y, degree)

# Reuse y_fit and use broadcasting to write to the text file
y_fit = np.polyval(coefficients, x)
y_fit_range = np.polyval(coefficients, np.linspace(1, x[-1], 100))

# Use broadcasting to write to the text file
data = np.column_stack((x, y, y_fit))
np.savetxt(output_path, data, delimiter=',', header='x, y_data, y_fit', comments='',fmt='%0.0f, %.1f, %.1f')

# Calculate R-squared
y_mean = np.mean(y)
ss_res = np.sum((y - y_fit) ** 2)
ss_tot = np.sum((y - y_mean) ** 2)
r_squared = 1 - (ss_res / ss_tot)

# Print coefficients and R-squared
print("Coefficients:", np.flip(coefficients))
print("R-squared:", r_squared)

fig, ax = plt.subplots(figsize=(8, 6))
ax.grid(True)
plt.plot(x, y, 'o', markersize=4, label='Data Points', color='red')
plt.plot(x, y_fit, '-', linewidth=2, label='Line of Best Fit', color='blue')
ax.set_title('Weight Over Time')
ax.set_xlabel('Days')
ax.set_ylabel('Weight')
plt.legend()
plt.show()

print("Completed")