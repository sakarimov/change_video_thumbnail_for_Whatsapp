import subprocess
from os import listdir

# change these to your liking
video_dir = "path/to/videos"
output_dir = "path/to/output"
process_dir = "path/to/cache"


# function for filtering files based on extension
# output = list
def saring_file(directory, extension):
    # file list of directory
    file_list = listdir(f"{directory}")
    the_files = []
    for i in file_list:
        the_files.append(f'{i}')
        sorted_files = [f for f in the_files if (str(f))[-3:] == f"{extension}"]
    return sorted_files

# for the subrocess to be running the " " in directory path must be converted to "\ "
conv_video_dir = video_dir.replace(" ", "\ ")
conv_output_dir = output_dir.replace(" ", "\ ")
conv_cache_dir = process_dir.replace(" ", "\ ")
# files list variable
videonya = saring_file(directory=video_dir, extension="mp4")
for i in videonya:
    splited = i.split(".")
    subprocess.run(f"ffmpeg -sseof -3 -i {conv_video_dir}/{i} -update 1 -q:v 1 {conv_cache_dir}/{splited[0]}.jpg",
                   shell=True, check=True, encoding='utf-8')
    subprocess.run(f"ffmpeg -loop 1 -framerate 24 -i {conv_cache_dir}/{splited[0]}.jpg -c:v libx264 -t 0.04 -pix_fmt yuv420p {conv_cache_dir}/{splited[0]}.mp4",
                   shell=True, check=True, encoding='utf-8')
    subprocess.run(f"ffmpeg -i {conv_cache_dir}/{splited[0]}.mp4 -c copy -bsf:v h264_mp4toannexb -f mpegts {conv_cache_dir}/{splited[0]}_thumbnail.ts",
                   shell=True, check=True, encoding='utf-8')
    subprocess.run(f"ffmpeg -i {conv_video_dir}/{i} -c copy -bsf:v h264_mp4toannexb -f mpegts {conv_cache_dir}/{splited[0]}_video.ts",
                   shell=True, check=True, encoding='utf-8')
    subprocess.run(f"ffmpeg -fflags +igndts -i 'concat:{process_dir}/{splited[0]}_thumbnail.ts|{process_dir}/{splited[0]}_video.ts' -c copy {conv_output_dir}/{splited[0]}.mp4",
                   shell=True, check=True, encoding='utf-8')
#    subprocess.run(f"rm {conv_cache_dir}/{splited[0]}_thumbnail.ts {conv_cache_dir}/{splited[0]}_video.ts {conv_cache_dir}/{splited[0]}.mp4 {conv_cache_dir}/{splited[0]}.jpg",
#                   shell=True, check=True, encoding='utf-8')
