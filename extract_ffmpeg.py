import tarfile

# Path to your downloaded .tar.xz file
filename = "ffmpeg-7.1.1.tar.xz"

# Extract to a folder named 'ffmpeg_extracted'
with tarfile.open(filename, "r:xz") as tar:
    tar.extractall("ffmpeg_extracted")

print("✅ Extraction complete!")
