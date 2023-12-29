from logic import *
import os
from datetime import datetime
import getopt
import sys

download_directory = 'Voorivex_Videos_' + datetime.today().strftime('%Y_%m_%d_%H_%M_%S')

username = ''
password = ''
is_live_included = False
keyword = ''
class_name = ''
argv = sys.argv[1:]

print('Voorivex Video Downloader')
print('Made by: Milad')
print('-' * 20)
print('Initializing ...')

try:
    options, args = getopt.getopt(argv, "u:p:k:c:l",
                                  ["user=", "password=", "keyword=", 'keyword=', 'class_name=', 'include_live'])

    for name, value in options:
        if name in ['-u', '--user']:
            username = value
        elif name in ['-p', '--password']:
            password = value
        elif name in ['-l', '--include_live']:
            is_live_included = True
        elif name in ['-k', '--keyword']:
            keyword = value
        elif name in ['-c', '--class_name']:
            class_name = value

    if username == '' or password == '':
        raise Exception("Invalid credential")

    user_access_token = login_in_voorivex(username, password)
    video_access_token = get_video_access_token(user_access_token)
    videos = get_user_video_list(video_access_token, is_live_included, class_name)
    filtered_videos = filter_videos(videos, keyword)
    os.mkdir(download_directory)
    print(f'Create directory to save files. Directory Name: {download_directory}')
    save_videos(download_directory, filtered_videos, video_access_token)

    print('The requested task completed. Thanks for use this tools')
except BaseException as e:
    print('-' * 20)
    print(f'Somethings went wrong')
    print(f'{e}')
    raise
