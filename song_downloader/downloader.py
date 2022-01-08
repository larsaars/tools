#!/usr/bin/env python3

'''
specify a playlist and download
the songs from youtube
(sound of best result video)
'''

from __future__ import unicode_literals
import os
import sys
import youtube_dl
from argparse import ArgumentParser
from os.path import join, exists
from login_spotify import *
from time import sleep
from youtubesearchpython import VideosSearch


def download_video(urls):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': args.codec,
            'preferredquality': '192',
        }],
        'postprocessor_args': [
            '-ar', '32000'
        ],
        'prefer_ffmpeg': True,
        'keepvideo': False 
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(urls)


def log(msg, who='downloader'):
    print(f'[{who}]', msg)


def get_playlist_tracks():
    results = spotify.playlist(args.playlist)['tracks']
    tracks = results['items']
    while results['next']:
        log('scraping next 100 song names from Spotify playlist')
        results = spotify.next(results)
        tracks.extend(results['items'])
    return tracks



def find_first_result_yt(search):
    videosSearch = VideosSearch(search, limit=1)
    result = videosSearch.result()['result']

    if len(result) == 0:
        return None

    return 'https://www.youtube.com/watch?v=' + result[0]['id']


if __name__ == '__main__':
    try:
        # define valid args
        parser = ArgumentParser(
                description='Downloads songs from Spotify playlist as audio from YouTube.',
                epilog='I [the author] is not responsible for any illegal act commit with this script.'
        )
        
        parser.add_argument('-p', 
                '--playlist',
                type=str, 
                default='0xoT0ejOz9cTS288XQnffp',
                help='ID of a Spotify playlist')
        parser.add_argument('-o',
                '--outputdir',
                type=str,
                default='./download',
                help='folder in which the songs will be saved into')
        parser.add_argument('-c',
                '--codec',
                type=str,
                default='mp3',
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
        song_names = []
        for item in get_playlist_tracks():
            track = item['track']
            song_names.append(track['name'] + ' ' + track['artists'][0]['name'])

        log('Done scraping song names from Spotify.')
        
        # search first video result via youtubesearchpython library
        # do that looping through all playlist names
        for song in song_names:
            log(f'searching {song} on YouTube')
            link = find_first_result_yt(song)

            if link == None:
                log('No video found for song.')
                continue

            log(f'downloading {link}')
            download_video([link])
    except KeyboardInterrupt as e:
        log('Interrupted')
