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

    # Function to extract video details from search response
    def extract_video_details(search_response):
        videoList = []
        for search_result in search_response.get('items', []):
            video_info = {
                'videoId': search_result['id']['videoId'],
                'title': search_result['snippet']['title'],
                'description': search_result['snippet']['description'],
                'thumbnail': search_result['snippet']['thumbnails']['default']['url'],
                'publishedAt': search_result['snippet']['publishedAt']
            }
            videoList.append(video_info)
        return videoList

    # # extract video details for page 1
    first_page_videos = extract_video_details(search_response)

    # Attempt to get the second page of videos
    next_page_token = search_response.get('nextPageToken', '')
    second_page_videos = []

    if next_page_token:
        # get the new results with the next page
        search_response = youtube.search().list(
            q=query_term,
            part='id,snippet',
            maxResults=max_results,
            type='video',
            pageToken=next_page_token
        ).execute()

        # extract video details for page 2
        second_page_videos = extract_video_details(search_response)

    # Return both lists of page video details
    return first_page_videos, second_page_videos

if __name__ == "__main__":
    query_term = sys.argv[1]
    max_results = sys.argv[2]
    try:
        print(youtube_search(query_term, max_results))
    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))