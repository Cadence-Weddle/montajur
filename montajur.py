desc = """
montajur.py IMAGE_DIRECTORY -o OUTFILE="o.mp4" -d DURATION -t SPECIAL_PHOTOS -s RATIO=1.5 -a AUDIO_STREAMS -l LOG=FALSE -r RESOLUTION=1920,1080 -v OVERWRITE=TRUE

RATIO, defaults to 1.5
SPECIAL_PHOTOS: optional
AUDIO_STREAMS: optional
DURATION must be set
OVERWRITE: overwrite the existing OUTFILE

"""

import argparse
import glob
from math import floor, ceil
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import subprocess
import os

image_formats = ["jpg", "png", 'jpeg', 'tiff', "nef"]


def get_images(di, formats=image_formats):
    o = []
    for f in formats: 
        if (di[-1] == '/' or di[-1] == '\\'):
            filenames = glob.glob(di + "*." + f)
        else: 
            filenames = glob.glob(di + "/*." + f)
        o = o + filenames
    o = sorted(o)
    return o

def gen_timer_file(images, spi, face_ratio, timers):
    f = ""
    for image in tqdm(images):
        d = spi
        for i in timers:
            if i in image:
                d = spi * face_ratio
        f += ('file \'' + image + '\'\n') 
        f += ('duration ' + str(d) + '\n')
    return f

def process_args():
    """returns directory_name, timers_file, timers_ratio, audio_files, audio_lengths, outfile_name, resolution"""
    return

def assemble_audio_cmd(audio_streams):
    af = ''
    temp_audio_file = "_tmp_audio_file.mp3"
    input_list = []
    n = 0
    for stream in audio_streams:
        input_list.append('-i')
        input_list.append(stream)
        af += "[" + str(n) + ":0]" 
        n+=1
    af += 'concat=n=' + str(n) + ':v=0:a=1[outa]'
    audio_concat_command = ['C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe']+ input_list+\
                                    ["-filter_complex", af, "-map", "[outa]", temp_audio_file]

    return audio_concat_command, temp_audio_file

def assemble_slideshow_cmd(outfile, timer_file, overwrite=True, res=('1920','1080'), temp=False):
    pad_c = '\scale=' + res[0] + ':' + res[1] + ':force_original_aspect_ratio=decrease,pad=' + res[0] + ':' + res[1] + ':-1:-1'
    owrte = '-y' if overwrite else '-n' 
    ofile = outfile
    if (temp) ofile = "_" + ofile
    command = ['C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe', '-f', 'concat', '-safe', '0', '-i', timer_file,
                      '-vsync', 'vfr', '-pix_fmt', 'yuv420p', '-vf', pad_c, owrte, ofile]
    return command, ofile

def assemble_full_cmd(infile, tmp_audio_file):
    add_audio_command = ['C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe', '-i', "_" + infile, '-i', tmp_audio_file,
                    '-c', 'copy', '-map', '0:v:0', '-map', '1:a:0', '-y', infile]
    return add_audio_command

if __name__ == "__main__.py":
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("Image_dir")
    parser.add_argument("-o", default='o.mp4',help="Output file name (with format, e.g. OUTFILE.mp4)")
    parser.add_argument("-d", help="Duration, in seconds")
    parser.add_argument("-t", help='file which contains special photos. Optional.')
    parser.add_argument("-s", default=1.5,help='ratio for special photos. Defaults to 1.5')
    parser.add_argument("-a", help='file which contains a list of audio streams. Optional.')
    parser.add_argument("-l", action='store_false',help='Print ffmpeg logs while running.')
    parser.add_argument("-r", default='1920x1080', help='resolution in the format 1920x1080. Defaults to 1920x1080')
    parser.add_argument("-v", action='store_true', help='Overwrite any existing files if they are encountered')
    
    parser.parse_args()
    
    #Analyze arguments
    d_name = parser.Image_dir
    logging = parser.l
    has_audio = parser.a != None
    has_special_photos = parser.t != None
    duration = parser.d
    
    if has_special_photos: 
        ti = open(parser.t, 'r')
        gibberish = ti.readlines()
        timers = [x.strip() for x in gibberish]
    else: 
        timers = []
    res = parser.r.split('x')
    overwrite = parser.v
    outfile = parser.o
    
    #Process images
    print("Retrieving images")
    images = get_images(d_name)
    print("Found " + len(images) + " images.")
    spi = d / len(images)
    timerstring = gen_timer_file(images, spi, parser.s, timers)
    timer_file = "_temp_image_timer_file_concat_.con" #Probably nothing named this
    
    with open(timer_file, 'w+') as f:
        f.write(timerstring)
    f.close()
    
    #Run commands
    if(has_audio):
        print("Assembling audio file-----")
        audio_cmd, tmp_audio_file = assemble_audio_cmd(audio_streams)
        a = subprocess.run(audio_cmd, capture_output=True)
        if(logging):
              print(a.stderr.decode('utf-8')
        print("Done assembling audio file-----")
    print("Assembling slideshow----")
    fc, infile = assemble_slideshow_cmd(outfile, timer_file, overwrite, res, temp=has_audio)
    f = subprocess.run(fc, capture_output=True)
    if (logging) print(f.stderr.decode('utf-8'))
    print("Done assembling slideshow----")
    subprocess.run(["del",timer_file])

    if (has_audio): 
        print("Combining audio with slideshow-----")
        aa = assemble_full_cmd(infile, tmp_audio_file)
        asa = subprocess.run(aa, capture_output=True)
        if (logging) print(asa.stderr.decode('utf-8')
        print("Final Slideshow assembled---")

    if(has_audio):
        print("Deleting temporary files---")
        delete = subprocess.run(["del",infile,tmp_audio_file,'-y']
        if (logging) print(delete.stderr.decode('utf-8'))
                           
                           

                           