from constants import db
import uuid
from util.srtParser import parseEmbSrt, parseAutoSrt
from util.utility import isTimeEqual
from util.youtubeExtractor import downloadEmbeddedSrt

TIME_DIFF = 3
UP_VOTE = "upvote"
DOWN_VOTE = "downvote"
UP_VOTE_COUNT = "upVoteCount"
DOWN_VOTE_COUNT = "downVoteCount"
CLAIM_COMMENT = "comment"
UUID = "uuid"
CLAIM_CREATOR_USER_NAME = "claimCreatorUserName"
CLAIMS = "claims"
URL = "url"
USERNAME = "userName"
ANNOTATIONS = "annotations"
START_TIME = "startTime"
END_TIME = "endTime"
MOTION = "motion"
TRUTH = "truth"
LIE = "lie"

def postVideo(url, userName):
    if db[url] is not None:
        return
    downloadEmbeddedSrt(url)
    response = parseAutoSrt(url)
    response[URL] = url
    response[USERNAME] = userName
    db[url] = response
    return

def getVideo(url):
    if db[url] is None:
        postVideo(url, "unknown")
    return db[url]


# Adding some comments for helping the user to achieve something
def getUUID():
    return uuid.uuid1()


def getMotion(motion):
    if "truth" in motion:
        return TRUTH
    return LIE

def submitClaim(startTime, endTime, claimComment, claimCreatorUserName, url, motion):
    if db[url] is None:
        return "Error"
    ob = db[url]
    annotations = ob[ANNOTATIONS]
    claim = {
        UP_VOTE_COUNT: 1,
        DOWN_VOTE_COUNT: 0,
        CLAIM_COMMENT: claimComment,
        UUID: getUUID(),
        CLAIM_CREATOR_USER_NAME: claimCreatorUserName,
        motion: getMotion(motion)
    }
    for annotation in annotations:
        annotationStartTime = annotation[START_TIME]
        annotationEndTime = annotation[END_TIME]
        if isTimeEqual(startTime, annotationStartTime, TIME_DIFF) and isTimeEqual(endTime, annotationEndTime, TIME_DIFF):
            annotationClaims = annotation[CLAIMS]
            for annotationClaim in annotationClaims:
                if annotationClaim[CLAIM_CREATOR_USER_NAME] == claim[CLAIM_CREATOR_USER_NAME]:
                    print("Error Claim already submitted by the user at that point")
                    return
            annotationClaims.append(claim)
            annotation[CLAIMS] = annotationClaims
            return claim
    print("TimeStamp did not match with any annotation")
    return


def voteClaim(url, claimId, vote):
    if db[url] is None:
        return "Error"
    ob = db[url]
    annotations = ob[ANNOTATIONS]
    for annotation in annotations:
        annotationClaims = annotation[CLAIMS]
        for annotationClaim in annotationClaims:
            if str(annotationClaim[UUID]) == claimId:
                if vote == UP_VOTE:
                    annotationClaim[UP_VOTE_COUNT] = annotationClaim[UP_VOTE_COUNT] + 1
                else:
                    annotationClaim[DOWN_VOTE_COUNT] = annotationClaim[DOWN_VOTE_COUNT] + 1
    return "200 OK"