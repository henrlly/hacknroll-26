import subprocess
import sys

if len(sys.argv) != 3:
    print("Usage: python mov_to_mp4.py input.mov output.mp4")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

cmd = [
    "ffmpeg",
    "-i", input_file,
    "-c:v", "libx264",
    "-crf", "23",
    "-preset", "medium",
    "-c:a", "aac",
    "-b:a", "192k",
    "-movflags", "+faststart",
    output_file
]

subprocess.run(cmd, check=True)
