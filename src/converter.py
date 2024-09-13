import ffmpeg
import os

def convert(src, dst_folder, filetype):

    dst = f'{dst_folder}/{os.path.splitext(os.path.basename(src))[0]}{filetype}'

    if os.path.exists(dst):
        return

    (
        ffmpeg
        .input(src)
        .output(dst)
        .run()
    )

