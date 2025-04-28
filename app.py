from flask import Flask, render_template, request, send_file, after_this_request
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form['url']
    quality = request.form['quality']
    
    # Path to your cookies.txt file
    cookie_path = r'C:\Users\as\vs code\youtube_downloader\cookies.txt'  # Update this path as needed
    
    # First, get the video info without downloading
    with yt_dlp.YoutubeDL({'cookiefile': cookie_path}) as ydl:  # Adding cookiefile to yt-dlp options
        info_dict = ydl.extract_info(url, download=False)
        video_title = info_dict.get('title', None)
    
    # Clean the title to make it safe for filename
    safe_title = "".join(x for x in video_title if x.isalnum() or x in " _-")
    filename = f"{safe_title}.mp4"

    # Set yt-dlp options with cookies and quality filter
    ydl_opts = {
        'cookiefile': cookie_path,  # Ensure the cookies are used here as well
        'format': f'bestvideo[height<={quality}]+bestaudio/best[height<={quality}]',
        'outtmpl': filename,
        'merge_output_format': 'mp4',
    }

    # Download the video
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # Remove the file after sending it to the user
    @after_this_request
    def remove_file(response):
        try:
            os.remove(filename)
        except Exception as e:
            print(f"Error deleting file: {e}")
        return response

    # Send the downloaded file to the user
    return send_file(filename, as_attachment=True, download_name=filename)

if __name__ == '__main__':
    app.run(debug=True)
