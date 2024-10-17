import sys

from .name_generator import make_dir
from .core import read_argv, check_cmd, lossy_compress

def main():
    cmd = read_argv(sys.argv[1:])
    cmd_dict = check_cmd(cmd)  # checks Namespace. Can also be dict
    dir_name = make_dir('compressions')
    lossy_compress(cmd_dict['file'], cmd_dict['output'],
                   cmd_dict['iterations'], cmd_dict['extra'],
                   cmd_dict['colors'], cmd_dict['reverse'],
                   cmd_dict['preprocess'], dir_name)
    print("Done!")

