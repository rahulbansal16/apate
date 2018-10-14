from constants import db
import uuid
from util.srtParser import parseEmbSrt, parseAutoSrt
from util.utility import isTimeEqual
from util.youtubeExtractor import downloadEmbeddedSrt, getVideoTitle

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
VIDEO_NAME = "name"
USERNAME = "userName"
ANNOTATIONS = "annotations"
START_TIME = "startTime"
END_TIME = "endTime"
MOTION = "motion"
TRUTH = "truth"
LIE = "lie"
HATE_SPEECH = "hate_speech"
UNCERTAIN = "uncertain"
EXAGGERATED_PROMISE ="exaggerated_promise"
POSITIVE_SPEECH = "positive_speech"

def postVideo(url, userName):
    if db[url] is not None:
        return
    downloadEmbeddedSrt(url)
    response = parseAutoSrt(url)
    response[URL] = url
    response[USERNAME] = userName
    response[VIDEO_NAME] = getVideoTitle(url)
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
    if "truth" in motion.lower():
        return TRUTH
    if "lie" in motion.lower():
        return LIE
    if "hate" in motion.lower():
        return HATE_SPEECH
    if "exagge" in motion.lower() and "promise" in motion.lower():
        return EXAGGERATED_PROMISE
    if "posit" in motion.lower() and "speech" in motion.lower():
        return POSITIVE_SPEECH
    return UNCERTAIN

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
        MOTION : getMotion(motion)
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


def getAllVideos():
     urls = []
     for key, value in db.items():
         urls.append({
             URL: key,
             VIDEO_NAME: value[VIDEO_NAME]
         })
     return urls
