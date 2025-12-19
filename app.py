import requests

# URL of the file in the GitHub release
file_url = "https://github.com/gauriwani3/Quality_report/releases/download/v1.0/Qual_Report_25LPLML281106_1__2025-12-01_06.17.42.dat"

# Step 1: Download the file from GitHub
response = requests.get(file_url)

# Check if the request was successful
if response.status_code == 200:
    # Save the file locally in the GitHub Codespace (in-memory or on disk in the workspace)
    file_path = "Quality report.dat"
    with open(file_path, "wb") as file:
        file.write(response.content)
    print(f"File downloaded and saved as {file_path}")
else:
    print("Failed to download the file.")

# Step 2: Read and process the downloaded .dat file
with open(file_path, "r") as file:
    data = file.readlines()  # Read all lines of the file (assuming text-based)
    for line in data:
        print(line.strip())  # Print each line (you can replace this with your own processing)
