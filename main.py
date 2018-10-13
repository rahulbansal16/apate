from flask import Flask, request, Response, jsonify
import os
from services.youtubeServices import postVideo, getVideo, submitClaim, voteClaim
from util.srtParser import parseAutoSrt
from util.youtubeExtractor import getFileName

AUTOMATIC_SRT_YOUTUBE_URL = "https://www.youtube.com/watch?v=DZN17YFIJnQ"
EMBEDDED_SRT_YOUTUBE_URL = "https://www.youtube.com/watch?v=Ye8mB6VsUHw"

app = Flask(__name__)



@app.route("/video", methods = ['POST'])
def video_post():
    json = request.json
    url = json["videoLink"]
    userName = json["userName"]
    postVideo(url, userName)
    return "200 OK"

@app.route("/video", methods = ['GET'])
def video_get():
    url = request.args.get('url')
    return jsonify(getVideo(url))


@app.route("/claim", methods=['POST'])
def claim_submit():
    json = request.json
    startTime = json["startTime"]
    endTime = json["endTime"]
    claimComment = json["claimComment"]
    claimCreatorUserName = json["claimCreatorUserName"]
    url = json["url"]
    motion = json["motion"]
    return jsonify(submitClaim(startTime, endTime, claimComment, claimCreatorUserName, url, motion))

@app.route("/claim/vote", methods = ['POST'])
def claim_vote():
    json = request.json
    url = json["url"]
    claimId = json["claimId"]
    vote = json["vote"]
    return jsonify(voteClaim(url, claimId, vote))


@app.route("/")
def hello():
    return "200 OK"





def getCurrentDir():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print("The current path is", dir_path)


if __name__ == '__main__':
   app.run(host= '0.0.0.0')
   # parseAutoSrt(getFileName(AUTOMATIC_SRT_YOUTUBE_URL))
   # downloadAutoSrt(AUTOMATIC_SRT_YOUTUBE_URL)
   # getCurrentDir()
   # removeEmptyLines(getFileName(EMBEDDED_SRT_YOUTUBE_URL))
   # parseEmbSrt(getFileName(EMBEDDED_SRT_YOUTUBE_URL))
