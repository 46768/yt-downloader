import yt_dlp
import time
from util import ensure_directory

ARG_PARSER = {
    "prog": "download",
    "description": "Video downloading tool",
    "help": "Video/playlist downloading tool"
}
ARGS = {
    "-u;--url": {
        "help": "Link to the video/playlist",
        "required": True},
    "-o;--outdir": {
        "help": "Download target directory",
        "default": "data/downloaded_files"},
    "-O;--outfmt": {
        "help": "Download file name format",
        "default": "%(title)s.%(ext)s"},
    "-l;--dlog": {
        "help": "Download log file",
        "default": "data/download.log"},
    "-x;--extract_audio": {
        "help": "Extract only audio. Uses yt-dlp's -x flag",
        "action": "store_true"},
    "-s;--subtitle": {
        "help": "Extract subtitles too",
        "action": "store_true"},
}


def run(args):
    ensure_directory(args.outdir)
    yt_dlp_outtmpl = args.outdir.rstrip('/')+'/'+args.outfmt
    ydl_download_config = {
        "outtmpl": yt_dlp_outtmpl,
        "writesubtitles": args.subtitle,
    }

    if args.extract_audio:
        ydl_download_config["postprocessors"] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
        ydl_download_config["format"] = "bestaudio/best"

    dlog = open(args.dlog, 'a')

    dlog_info = open(args.dlog, 'r')

    log_info = dlog_info.read()
    downloaded_url = [x.split('\t')[2] for x in log_info.split('\n')[:-1]]

    dlog_info.close()

    videos_to_download = []

    with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
        info = ydl.extract_info(args.url, download=False)

        if "entries" in info:
            videos_to_download = info["entries"]
        else:
            videos_to_download.append(info)

    with yt_dlp.YoutubeDL(ydl_download_config) as ydl_download:
        for video in videos_to_download:
            title = video["title"]
            uploader, uploader_id = video["uploader"], video["uploader_id"]
            url = video["webpage_url"]

            if url in downloaded_url:
                print(title+" is already downloaded")
                continue

            print("downloading "+title)
            ydl_download.download(url)
            dlog.write(f"[{time.asctime()}] {title}\t{uploader}"
                       f"/{uploader_id}\t{url}\n")

    dlog.close()
