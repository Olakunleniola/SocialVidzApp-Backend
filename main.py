from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

def download_video(url, output_path='videos/'):
    ydl_opts = {
        'outtmpl': f'{output_path}%(title)s.%(ext)s',
        'format': 'best',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def get_video_info(url):
    ydl_opts = {'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            return {
                'title': info.get('title', 'Unknown'),
                'url': info.get('url'),
                'platform': info.get('extractor', 'Unknown'),
                'status': 'success'
            }
        except yt_dlp.utils.DownloadError as e:
            return e

@app.route('/social_vids/api/download', methods=['POST'])
def download_video():
    data = request.get_json()
    url = data.get('url')
    platform = data.get('platform')
    
    print(url, "\n", platform)

    if platform.lower() == 'tiktok':
        return jsonify({'status': 'error', 'message': 'Unsupported platform.'})
    else:
        download_video(url)
        return jsonify({'status': 'success', 'message': 'video download successful.'})

@app.route('/social_vidz/api/get_info')
async def get_info():
    data = request.get_json()
    url = data.get('url')
    await video_info = get_video_info(url)
    if video_info.error:
         return jsonify({'status': video_info.error, 'message': 'Error Retrieving video info'})            
    return jsonify({'status': 'success', 'data': video_info})

if __name__ == '__main__':
    if not os.path.exists('videos'):
        os.makedirs('videos')
    app.run(debug=True, port=6000)
    
# https://youtu.be/lH-yovOnlwI