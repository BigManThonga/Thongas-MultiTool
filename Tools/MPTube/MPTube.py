import os
import subprocess
import sys

def download_video():
    # Create outputs folder if it doesn't exist
    output_dir = "outputs"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Get video URL and format choice
    url = input("Enter the YouTube video URL: ").strip()
    print("Choose format:")
    print("1. MP4 (Video and Audio)")
    print("2. MP3 (Audio only)")
    choice = input("Enter 1 or 2: ").strip()

    try:
        if choice == "1":
            # Download video and audio (MP4)
            subprocess.run([
                "yt-dlp", "-f", "mp4",
                "-o", f"{output_dir}/%(title)s.%(ext)s", url
            ])
            print(f"Video downloaded successfully to {output_dir}\n")
        elif choice == "2":
            # Download audio only (MP3)
            subprocess.run([
                "yt-dlp", "-x", "--audio-format", "mp3",
                "-o", f"{output_dir}/%(title)s.%(ext)s", url
            ])
            print(f"Audio downloaded successfully to {output_dir}\n")
        else:
            print("Invalid choice. Please select 1 or 2.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    download_video()
