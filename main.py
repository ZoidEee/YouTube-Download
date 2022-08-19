'''
Author: Mckenzie Turner
Date Created: Aug 16, 2022
Name: You2Me-C
'''
import os.path

import pytube.extract
from pytube import YouTube, Search
import menu3

media_dir = os.path.expanduser('~/Desktop/You2Me')
audio_dir = os.path.expanduser(media_dir + '/Audio')
video_dir = os.path.expanduser(media_dir + '/Video')


def start():
    active_dir = os.path.isdir(media_dir)

    while active_dir:
        print(f'~~~[LOG]~~~  Directory {media_dir} located')
        search()
        break
    else:
        print(f'~~~[LOG]~~~  Directory {media_dir} not located')
        print(f'~~~[LOG]~~~  Directories:\n  -{media_dir}\n  -{audio_dir}\n  -{video_dir}\nHave now been created')
        os.mkdir(media_dir)
        os.mkdir(audio_dir)
        os.mkdir(video_dir)
        search()


def search():
    '''
    Process:
        -Download Audio Files
            -Search for video
                - Enter search term and search YouTube
                    - Create a dictionary "title_url" from the search results
                        - Title of search result = Key, URL of search result = Value
                    - Create a menu from the dictionary keys
                    - Download selected result to "audio_dir"
            -Download a specific video
                - Paste link
                - Try
                    - Check if "https://" is in link
                        - True
                            - Download to "audio_dir"
                        - False
                            - Paste link
                            - Retry
                - Except
                    - print error

        -Download Video Files
           -Search for video
                - Enter search term and search YouTube
                    - Create a dictionary "title_url" from the search results
                        - Title of search result = Key, URL of search result = Value
                    - Create a menu from the dictionary keys
                    - Download selected result to "video_dir"
            -Download a specific video
                - Paste link
                - Check if "https://" is in link
                - Download to "video_dir"
    '''

    sel_options = ['Download Audio Files', 'Download Video Files']
    type_options = ['Search for video?', 'Download a specific video?']
    title_url = {}

    core_search_menu = menu3.Menu(True)
    selection_menu = core_search_menu.menu('Please select one:', sel_options, "Press 'q' to quit now")

    if sel_options[selection_menu - 1] == sel_options[0]:
        ''' if Audio is selected '''
        print(f'~~~[LOG]~~~ {sel_options[selection_menu - 1]} selected')

        audio_sel_menu = core_search_menu.menu('Please select one:', type_options)

        if type_options[audio_sel_menu - 1] == type_options[0]:
            print(f'~~~[LOG]~~~ {sel_options[selection_menu - 1]} selected')

            youtube_search = Search(input("What would you like to search for: "))
            for res in youtube_search.results:
                print(f'~~~[LOG]~~~ adding {res.title} + {res.watch_url} to title_url --dict-- ')
                title_url[res.title] = res.watch_url

            audio_titles = [t for t in title_url.keys()]
            audio_title_menu = core_search_menu.menu('Please select one', audio_titles)
            if audio_titles[audio_title_menu - 1]:
                print(f'~~~[LOG]~~~ Downloading {audio_titles[audio_title_menu - 1]} to {audio_dir}')
                audio_download(audio_dir, title_url.get(audio_titles[audio_title_menu - 1]))

        elif type_options[audio_sel_menu - 1] == type_options[1]:
            ''' if Specific video is selected '''
            print(f'~~~[LOG]~~~ {sel_options[selection_menu - 1]} selected')

            try:
                audio_link = input('Please paste link to video here:')
                if 'https://' not in audio_link:
                    print(f"~~~[LOG]~~~ 'https://' not found in {audio_link}")
                else:
                    print(f"~~~[LOG]~~~ 'https://' found in {audio_link}")
                    print(f"~~~[LOG]~~~ Downloading now..........")
                    audio_download(audio_dir, audio_link)
            except EOFError as err:
                print(err)

    elif sel_options[selection_menu - 1] == sel_options[1]:
        ''' if Video is selected '''
        print(f'~~~[LOG]~~~ {sel_options[selection_menu - 1]} selected')
        vs_core_menu = menu3.Menu(True)
        vs_menu = vs_core_menu.menu('Please select an option now', type_options)

        if type_options[vs_menu - 1] == type_options[0]:
            print(f'~~~[LOG]~~~ {type_options[vs_menu - 1]} selected')
            video_search = Search(input("What would you like to search for: ")).results

            for res in video_search:
                print(f'~~~[LOG]~~~ adding {res.title} + {res.watch_url} to title_url --dict-- ')
                title_url[res.title] = res.watch_url

            video_search_results = [t for t in title_url.keys()]
            vs_title_menu = vs_core_menu.menu("Please select one to download: ", video_search_results)
            if video_search_results[vs_title_menu - 1]:
                print(f'~~~[LOG]~~~ Downloading {video_search_results[vs_title_menu - 1]} '
                      f'to {video_dir}')
                video_download(video_dir, title_url.get((video_search_results[vs_title_menu - 1])))

        elif type_options[vs_menu - 1] == type_options[1]:
            print(f'~~~[LOG]~~~ {type_options[vs_menu - 1]} selected')
            try:
                link = input('Please paste link to video here:')
                if 'https://' not in link:
                    print(f"~~~[LOG]~~~ 'https://' not found in {link}")
                else:
                    print(f"~~~[LOG]~~~ 'https://' found in {link}")
                    print(f"~~~[LOG]~~~ Downloading now..........")
                    video_download(audio_dir, link)
            except EOFError as err:
                print(err)


def video_download(path, link):
    print(f'~~~[LOG]~~~ Downloading to path: \n {path}')
    YouTube(link).streams.get_highest_resolution().download(path)


def audio_download(path, link):
    print(f'~~~[LOG]~~~ Downloading to:\n  {path}')
    YouTube(link).streams.get_audio_only().download(path)


start()
