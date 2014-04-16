import commands
import re

def recognize_speech(duration):
    sample_rate = 16000
    cmd_output = commands.getoutput('arecord -f cd -t wav -d ' + str(duration) + ' -r ' + str(sample_rate) + ' | flac - -f --best --sample-rate=' + str(sample_rate) + ' -o out.flac; wget -O - -o /dev/null --post-file out.flac --header="Content-Type: audio/x-flac; rate=' + str(sample_rate) + '" http://www.google.com/speech-api/v1/recognize?lang=en')
    print cmd_output
    matches = re.findall("\"status\":0,.*?utterance\":\"([^\"]*)\"",cmd_output)
    if len(matches) == 0:
        print "no match found"
    else:
        print matches[0]

recognize_speech(5)

#from pygsr import Pygsr
#speech = Pygsr()
#
#speech.record(5) # durationin seconds (3)
#
#phrase, complete_response =speech.speech_to_text('en_US') # select the language
#
#print phrase
#print complete_response

#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#import httplib
#import json
#import sys
#
#def speech_to_text(audio):
#    url = "www.google.com"
#    path = "/speech-api/v1/recognize?xjerr=1&client=chromium&lang=en"
#    headers = { "Content-type": "audio/x-flac; rate=16000" };
#    params = {"xjerr": "1", "client": "chromium"}
#    conn = httplib.HTTPSConnection(url)
#    conn.request("POST", path, audio, headers)
#    response = conn.getresponse()
#    data = response.read()
#    jsdata = json.loads(data)
#    return jsdata["hypotheses"][0]["utterance"]
#
#if __name__ == "__main__":
#    if len(sys.argv) != 2 or "--help" in sys.argv:
#        print "Usage: stt.py <flac-audio-file>"
#        sys.exit(-1)
#    else:
#        with open(sys.argv[1], "r") as f:
#            speech = f.read()
#        text = speech_to_text(speech)
#        print text