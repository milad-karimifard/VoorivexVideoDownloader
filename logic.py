import requests
import os
import shutil
from tqdm.auto import tqdm
import time

baseApiUrl = 'https://api.voorivex.academy/'
downloadServerBaseUrl = 'https://dl-api.voorivex.academy/'
video_access_token_endpoint = 'https://voorivex.academy/_next/data/DvIxrnXr72lF6zOXsCwLg/download.json'


def login_in_voorivex(username, password):
    body = {'username': username, 'password': password}
    res = requests.post(baseApiUrl + 'auth/login', data=body)
    if res.ok is False:
        raise Exception('Entered user/pass invalid')
    res_in_json = res.json()
    return res_in_json['access_token']


def get_user_video_list(access_token, is_live_included, class_name):
    res = requests.get(downloadServerBaseUrl + 'video', headers=get_auth_headers(access_token))
    class_videos = res.json()
    return extract_video_from_payload(class_videos, is_live_included, class_name)


def extract_video_from_payload(class_videos, is_live_included, class_name):
    result = []
    for item in class_videos:
        if item['type'] == 'file':
            is_live = 'lives' in item['key']
            if is_live_included is False and is_live:
                continue

            item_class_name = item['key'].split('/')[0]
            if class_name != '' and class_name != item_class_name:
                continue

            video_item = {'title': item['title'], 'resource_key': item['key'], 'class': item_class_name}
            result.append(video_item)
        else:
            sub_videos = extract_video_from_payload(item['children'], is_live_included, class_name)
            for subItem in sub_videos:
                result.append(subItem)

    return result


def get_auth_headers(access_token):
    return {'Authorization': 'Bearer ' + access_token}


def filter_videos(video_list_for_filter, keyword):
    if keyword == '':
        return video_list_for_filter

    result = []
    for item in video_list_for_filter:
        if keyword in item['title']:
            result.append(item)
    return result


def get_video_link(resource_key, access_token):
    auth_headers = get_auth_headers(access_token)
    requests.post(downloadServerBaseUrl + 'video/ganerate', data={'key': resource_key}, headers=auth_headers)
    is_link_ready = False
    while is_link_ready is False:
        check_response = requests.get(downloadServerBaseUrl + 'video/getActiveLink', headers=auth_headers)
        if check_response.status_code == 304:
            time.sleep(2)
            continue
        elif check_response.status_code == 200:
            res_in_json = check_response.json()
            if res_in_json['type'] == 'pending':
                time.sleep(2)
                continue
            elif res_in_json['type'] == 'active':
                return res_in_json['videos'][0]['url']

        else:
            time.sleep(3)
            continue


def save_videos(download_directory, videos_for_download, access_token):
    for video in videos_for_download:
        url_to_download = get_video_link(video['resource_key'], access_token)
        download_video(download_directory, url_to_download, video['title'])


def download_video(download_directory, url_to_download, file_name):
    with requests.get(url_to_download, stream=True) as r:
        # check header to get content length, in bytes
        total_length = int(r.headers.get("Content-Length"))

        # implement progress bar via tqdm
        with tqdm.wrapattr(r.raw, "read", total=total_length, desc="") as raw:
            # save the output to a file
            path = os.path.join(download_directory, file_name)
            with open(f"{path}", 'wb') as output:
                shutil.copyfileobj(raw, output)

    print(f"Download {file_name} completed")


def get_video_access_token(user_access_token):
    headers = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://voorivex.academy/'}
    cookie = {'token': user_access_token}
    res = requests.post(video_access_token_endpoint, data=headers, cookies=cookie)
    if res.ok is False:
        raise Exception('Failed to authenticate user to download video')
    res_in_json = res.json()
    return res_in_json['pageProps']['token']
