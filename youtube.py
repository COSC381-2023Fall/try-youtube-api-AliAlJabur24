import sys
import config
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

DEVELOPER_KEY = config.API_KEY
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def youtube_search(query_term, max_results):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
        q=query_term,
        part='id,snippet',
        maxResults=max_results,
    ).execute()


    videoList = []
    # loop trough the results and check if there are items in the results; if search through []
    for search_result in search_response.get('items', []):
        # Make a dict of the relevant information we can pull from the result
        video_Info = {
            'videoId': search_result['id']['videoId'],
            'title': search_result['snippet']['title'],
            'description': search_result['snippet']['description'],
            'thumbnail': search_result['snippet']['thumbnails']['default']['url'],
            'publishedAt': search_result['snippet']['publishedAt']
        }
        # append the video information in the videoList
        videoList.append(video_Info)
    # return thee list of all the video dicts
    return videoList

if __name__ == "__main__":
    query_term = sys.argv[1]
    max_results = sys.argv[2]
    try:
        print(youtube_search(query_term, max_results))
    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))
