import re

from util.youtubeExtractor import removeEmptyLines, getFileName

EMB_REGEX = '([0-9]{2}:[0-9]{2}:[0-9]{2}[.][0-9]{3}) --> ([0-9]{2}:[0-9]{2}:[0-9]{2}[.][0-9]{3})([^->]*)\n'
# EMB_REGEX = '([0-9:.]+) --> ([0-9:.]+)([^->]*)\n'
# EMB_REGEX = '(.*)-->(.*)([^->]*)\n'
# AUTO_REGEX = '((.*)-->(.*))align:start position:0%'
TAG_REPLACE_REGEX = '<.*?>'
ALIGN_TEXT_REGEX = 'align:start position:0%'

def parseSrt():
    pass


def readFile(filename):
    file = open(filename,encoding="utf8")
    return file

def parseAutoSrt(url):
    filename = getFileName(url)
    autoSrt = readFile(filename).read()
    text, n = re.subn(TAG_REPLACE_REGEX,'',autoSrt)
    text, n = re.subn(ALIGN_TEXT_REGEX, '', text)
    print(text, n)
    matches = re.findall(EMB_REGEX, text)
    if len(matches) == 0:
        print("Failed to parse the Regex")
    return parse(matches)



#
#
#   { text:"", annotations: [  d  ] }
#   d = { "startTime": , "endTime":, startIndex: , endIndex:, text   }
#
#
#
#
#
# Input is list of matchText[ [ startTime, endTime, text  ],  ]
def parse(matches):
    annotations = []
    wholeText = ""
    startIndex, endIndex = 0, 0
    for match in matches:
        startTime, endTime, text = match
        endIndex = startIndex + len(text)
        annotations.append(
            {
                "startTime": parseTimeStamp(startTime),
                "endTime": parseTimeStamp(endTime),
                "text": text,
                "startIndex": startIndex,
                "endIndex": endIndex,
                "claims": []
            }
        )
        startIndex = endIndex
        wholeText = wholeText + text
    return {'text': wholeText, "annotations": annotations}

# def parseSrt(url):

def parseEmbSrt(url):
    filename = getFileName(url)
    embSrt = readFile(filename).read()
    matches = re.findall(EMB_REGEX, embSrt)
    if len(matches) == 0:
        print("Failed to parse the Regex")
    return parse(matches)


# return the timestamp in milliseconds
def parseTimeStamp(timeStamp):
    # return 12
    timeStamp = timeStamp.strip()
    print (timeStamp)
    times = timeStamp.split(".")
    nontimes = times[0].split(':')
    return int(times[1]) + int(nontimes[2])*1000 + int(nontimes[1])*60*1000 + int(nontimes[0])*60*60*1000


