import os
import subprocess

# Get the current working directory
HOME = os.getcwd()
print(HOME)

# Create the directory if it doesn't exist
weights_dir = os.path.join(HOME, 'weights')
os.makedirs(weights_dir, exist_ok=True)

# URLs to download the files from
urls = [
    "https://github.com/THU-MIG/yolov10/releases/download/v1.1/yolov10n.pt",
    "https://github.com/THU-MIG/yolov10/releases/download/v1.1/yolov10s.pt",
    "https://github.com/THU-MIG/yolov10/releases/download/v1.1/yolov10m.pt",
    "https://github.com/THU-MIG/yolov10/releases/download/v1.1/yolov10b.pt",
    "https://github.com/THU-MIG/yolov10/releases/download/v1.1/yolov10x.pt",
    "https://github.com/THU-MIG/yolov10/releases/download/v1.1/yolov10l.pt"
]

# Function to download a file
def download_file(url, dest_folder):
    command = ["wget", "-P", dest_folder, "-q", url]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(f"Error downloading {url}")
        print(result.stderr.decode())
    else:
        print(f"Downloaded {url}")

# Download each file
for url in urls:
    download_file(url, weights_dir)

# List the files in the weights directory
files = os.listdir(weights_dir)
for file in files:
    print(f"{file} - {os.path.getsize(os.path.join(weights_dir, file)) / 1024:.2f} KB")