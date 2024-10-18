import subprocess
import glob
import os
from datetime import datetime
import shutil

def clear_directory(directory):
    if os.path.exists(directory):
        files = glob.glob(os.path.join(directory, '*'))
        for f in files:
            if os.path.isfile(f) or os.path.islink(f):
                os.remove(f)
            elif os.path.isdir(f):
                shutil.rmtree(f)


def gif(model_name, start_date, end_date, frame_rate, line_or_area, output_directory_fronts):
    if model_name is None:
        model_name = "MyData"
    input_directory = os.path.join(output_directory_fronts,'figures')
    output_directory = os.path.join(output_directory_fronts,'figures/gif')
    temp_directory = os.path.join(output_directory_fronts,'figures/temp')
    out_file_name = f'{model_name}_fronts'

    start_date = datetime.strptime(start_date, '%Y-%m-%d %H')
    end_date = datetime.strptime(end_date, '%Y-%m-%d %H')

    os.makedirs(input_directory, exist_ok=True)
    os.makedirs(output_directory, exist_ok=True)
    os.makedirs(temp_directory, exist_ok=True)

    clear_directory(temp_directory)

    image_files = sorted(glob.glob(os.path.join(input_directory, f'{model_name}_fronts_satellite_{line_or_area}_*.png')))

    for image in image_files:
        filename = os.path.basename(image)
        date_str = filename[-14:-4]
        date = datetime.strptime(date_str, "%Y%m%d%H")

        if start_date <= date <= end_date:
            destination = os.path.join(temp_directory, filename)
            shutil.copy2(image, destination)

    gif_file_path = os.path.join(output_directory, f'{out_file_name}_{line_or_area}.gif')

    ffmpeg_command = (
        f'ffmpeg -framerate {frame_rate} -pattern_type glob -i "{temp_directory}/{model_name}_fronts_satellite_{line_or_area}_*.png" '
        f'-vf "fps={frame_rate},scale=640:-1:flags=lanczos,palettegen" -y palette.png && '
        f'ffmpeg -framerate {frame_rate} -pattern_type glob -i "{temp_directory}/{model_name}_fronts_satellite_{line_or_area}_*.png" '
        f'-i palette.png -lavfi "fps={frame_rate},paletteuse" -y "{gif_file_path}"'
    )

    subprocess.run(ffmpeg_command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    print(f"GIF saved in: {output_directory}")

    if os.path.exists("palette.png"):
        try:
            os.remove("palette.png")
        except Exception:
            pass
