import sys
import config
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

DEVELOPER_KEY = config.API_KEY
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def youtube_search(query_term, max_results, start_page, end_page):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    # Initialize page_token None for the first iteration
    page_token = None
    current_page = 1  # Start at page 1
    all_videos = []  # List to hold all videos from all pages

    while current_page < start_page:  # Go through each page until we are at the start page
        search_response = youtube.search().list(
            q=query_term,
            part='id,snippet',
            maxResults=max_results,
            type='video',
            pageToken=page_token
        ).execute()
        page_token = search_response.get('nextPageToken','')
        current_page += 1

    
    # Since we are at the start page we need to grab every page until we hit the end page
    while current_page <= end_page:
        # Fetch the search results
        search_response = youtube.search().list(
            q=query_term,
            part='id,snippet',
            maxResults=max_results,
            type='video',
            pageToken=page_token
        ).execute()

        # extract video details from search response
        videos = []
        for search_result in search_response.get('items', []):
            videos.append({
                'videoId': search_result['id']['videoId'],
                'title': search_result['snippet']['title'],
                'description': search_result['snippet']['description'],
                'thumbnail': search_result['snippet']['thumbnails']['default']['url'],
                'publishedAt': search_result['snippet']['publishedAt']
            })
        all_videos.append((current_page, videos))

        page_token = search_response.get('nextPageToken','')
        if not page_token:  # Break loop if there is not a page token
            break
        current_page += 1

    return all_videos

if __name__ == "__main__":
    query_term = sys.argv[1]
    max_results = int(sys.argv[2])
    start_page = int(sys.argv[3])
    end_page = int(sys.argv[4])

    if start_page < 1 or end_page < start_page:
        raise ValueError("Start page cannot be less then 1 and also cannot be greater then the end page")
    
    try:
        page_videos = youtube_search(query_term, max_results, start_page, end_page)
        for page_num, videos in page_videos:
            print(f"Page {page_num} results:")
            for video in videos:
                print(video)
    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))
    except ValueError as e:
        print(e)