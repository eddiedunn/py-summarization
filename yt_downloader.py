

class YouTubeDownloader:
    def __init__(self, url):
        self.url = url
        self.yt = YouTube(self.url)

    def download(self):
        self.yt.streams.first().download()
        print("Download completed!!")