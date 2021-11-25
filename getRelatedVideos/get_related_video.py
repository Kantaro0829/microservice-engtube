#from googleapiclient.discovery import build
from apiclient.discovery import build

class GetRelatedVideos():
    def __init__(self, video_id, youtube_api_key):
        self.video_id = video_id
        self.youtube_api_key = youtube_api_key
        self.videoid_and_url = []

    def get_videoid_and_url(self):
        youtube = build('youtube', 'v3', developerKey=self.youtube_api_key)
        
        search_response = youtube.search().list(
            part='snippet',
            relatedToVideoId=self.video_id,
            order='viewCount',
            videoCaption='closedCaption',
            maxResults=10,
            type='video'
        ).execute()

        for i in search_response['items']:
            result = {}
            #関連のあるvideoIdを代入
            result['videoId'] = i['id']['videoId']
            #関連のあるvideoIdの動画のタイトル代入
            result['videoTittle'] = i['snippet']['title']
            #関連のあるvideoのサムネイル画像のURL代入
            result['videoThumbnail'] = i['snippet']['thumbnails']['default']['url']
            self.videoid_and_url.append(result)
        
        return self.videoid_and_url


