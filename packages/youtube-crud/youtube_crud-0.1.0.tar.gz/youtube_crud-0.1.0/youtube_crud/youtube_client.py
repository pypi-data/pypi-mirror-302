from googleapiclient.discovery import build

class YouTubeClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)

    def create_video(self, title, description, category_id, tags):
        # Code to create a video
        pass

    def read_video(self, video_id):
        # Retrieve video details
        request = self.youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_id
        )
        response = request.execute()
        return response

    def update_video(self, video_id, title=None, description=None):
        # Update video details (title/description)
        pass

    def delete_video(self, video_id):
        # Code to delete a video
        pass
 
