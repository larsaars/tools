#!/usr/bin/env python3

"""
specify a playlist and download
the songs from youtube
(sound of best result video)
"""

from __future__ import unicode_literals
import os
import sys
import youtube_dl
from argparse import ArgumentParser
from os.path import join, exists
from login_spotify import *


def download_video(urls):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': args.codec,
            'preferredquality': '192',
        }],
        #'postprocessor_args': [
        #    '-ar', '16000'
        #],
        #'prefer_ffmpeg': True,
        #'keepvideo': False
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(urls)


def log(msg, who='downloader'):
    print(f'[{who}]', msg)



if __name__ == '__main__':
    # define valid args
    parser = ArgumentParser(
            description='Downloads songs from Spotify playlist as audio from YouTube.',
            epilog='I [the author] is not responsible for any illegal act commit with this script.'
    )
    
    parser.add_argument('-p', 
            '--playlist',
            type=str, 
            default='7EgjP7oVG2w5Aj9gLyAS65',
            help='ID of a Spotify playlist')
    parser.add_argument('-o',
            '--outputdir',
            type=str,
            default='./download',
            help='folder in which the songs will be saved into')
    parser.add_argument('-c',
            '--codec',
            type=str,
            default='wav',
            help='preferred audio codec')

    args = parser.parse_args()

    # change working directory for download
    if args.outputdir.startswith('./'):
        new_cwd = join(os.getcwd(), args.outputdir.lstrip('./'))
    else:
        new_cwd = args.outputdir

    if not exists(new_cwd):
        os.mkdir(new_cwd)

    os.chdir(new_cwd)

    # log events
    log(f'Downloading songs of Spotify playlist with id {args.playlist} into {os.getcwd()} from YouTube with {args.codec} as codec.')

    # get a list of names from the spotify playlist

