import subprocess, os

YOUTUBE_DL = "./exe/youtube-dl.exe "
OUTPUT_DIR = " ./subtitles/"
OUTPUT_DIR_ARG = " -o "
DOWNLOAD_AUTO_SRT_ARG = " --write-auto-sub "
DOWNLOAD_EMB_SRT_ARG = " --all-subs "
SKIP_DOWNLOAD_ARG = " --skip-download "

def getSRTName(url):
    pass

def getFileName(url):
    return OUTPUT_DIR.strip() + getUniqueId(url) + ".en.vtt"

def getUniqueId(url):
    return url.split('https://www.youtube.com/watch?v=')[1]

def getOutputFileName(url):
    return OUTPUT_DIR + getUniqueId(url)

def getAutoSRTArg(url):
    return YOUTUBE_DL + DOWNLOAD_AUTO_SRT_ARG + OUTPUT_DIR_ARG + getOutputFileName(url) + SKIP_DOWNLOAD_ARG + url

def getEMBSrtArg(url):
    pass


def runProcess(arg):
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
    with open(filename) as in_file, open(filename, 'r+') as out_file:
        out_file.writelines(line for line in in_file if line.strip())
        out_file.truncate()