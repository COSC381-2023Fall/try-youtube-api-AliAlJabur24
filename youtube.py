import sys
import config
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

DEVELOPER_KEY = config.API_KEY
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def youtube_search(query_term, max_results, page_number):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
        q=query_term,
        part='id,snippet',
        maxResults=max_results,
    ).execute()

    page_token = None  # Initialize page_token None for the first iteration
    current_page = 0
    while current_page < page_number:
        search_response = youtube.search().list(
            q=query_term,
            part='id,snippet',
            maxResults=max_results,
            type='video',
            pageToken=page_token
        ).execute()

        page_token = search_response.get('nextPageToken')
        current_page += 1
        if not page_token:  # Break loop if there is not a page token
            break

    if current_page != page_number:
        raise ValueError("The specified page number is out of range.")

    # Extract video information from the search response
    videos = []
    for search_result in search_response.get('items', []):
        video_info = {
            'videoId': search_result['id']['videoId'],
            'title': search_result['snippet']['title'],
            'description': search_result['snippet']['description'],
            'thumbnail': search_result['snippet']['thumbnails']['default']['url'],
            'publishedAt': search_result['snippet']['publishedAt']
        }
        videos.append(video_info)

    return videos

if __name__ == "__main__":
    query_term = sys.argv[1]
    max_results = int(sys.argv[2])  
    page_number = int(sys.argv[3])

    if page_number < 1:
        raise ValueError("Page number must be a positive integer.")

    try:
        videos = youtube_search(query_term, max_results, page_number)
        print(f"Page {page_number} results:")
        print(videos)
    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))
    except ValueError as e:
        print(e)