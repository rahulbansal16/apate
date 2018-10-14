import subprocess, os

YOUTUBE_DL = "./exe/youtube-dl.exe "
OUTPUT_DIR = " ./subtitles/"
OUTPUT_FILENAME="tmp"
OUTPUT_DIR_ARG = " -o "
DOWNLOAD_AUTO_SRT_ARG = " --write-auto-sub "
DOWNLOAD_EMB_SRT_ARG = " --all-subs "
VIDEO_TITLE_ARG = " --get-filename "
SKIP_DOWNLOAD_ARG = " --skip-download "
SUB_LANG_ARG = " --sub-lang "
SUB_LANG = " en "

def getSRTName(url):
    pass

def getFileName(url):
    return OUTPUT_DIR.strip() + getUniqueId(url) + ".en.vtt"

def getUniqueId(url):
    return url.split('https://www.youtube.com/watch?v=')[1]

def getOutputFileName(url):
    return OUTPUT_DIR + getUniqueId(url)

def getAutoSRTArg(url):
    return YOUTUBE_DL + DOWNLOAD_AUTO_SRT_ARG + OUTPUT_DIR_ARG + getOutputFileName(url) + SUB_LANG_ARG + SUB_LANG + SKIP_DOWNLOAD_ARG + url

def getEMBSrtArg(url):
    pass

def getVideoTitle(url):
    arg = YOUTUBE_DL + VIDEO_TITLE_ARG + SKIP_DOWNLOAD_ARG + url
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    # print("The current path is", dir_path)

    file = open(OUTPUT_FILENAME, "w+")
    runProcess(arg, file)
    file.seek(0)
    name = file.read()
    file.truncate(0)
    return name

def runProcess(arg, file=None):
    FNULL = file
    if file is None:
        FNULL = open(os.devnull, 'w')  # use this if you want to suppress output to stdout from the subprocess
    status = subprocess.call(arg, stdout=FNULL, stderr=FNULL, shell=False)
    if status != 0:
        print("The run process failed", arg)
    else:
        print("Video Downloaded Successfully")

def downloadSrt(url):
    pass

def downloadAutoSrt(url):
    arg = getAutoSRTArg(url)
    runProcess(arg)
    removeEmptyLines(getFileName(url))

def downloadEmbeddedSrt(url):
    downloadAutoSrt(url)


def removeEmptyLines(filename):
    """Overwrite the file, removing empty lines and lines that contain only whitespace."""
    exists = os.path.isfile(filename)
    if not exists:
        print("Auto Subtitles were not generated")
        return "Failed Not Working"
    with open(filename, errors='ignore', encoding="utf8") as in_file, open(filename, 'r+',errors='ignore' ,encoding="utf8") as out_file:
        out_file.writelines(line for line in in_file if line.strip())
        out_file.truncate()