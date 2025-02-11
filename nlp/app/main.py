#!/usr/bin/env python3
"""
 Copyright (C) 2021 Intel Corporation
 SPDX-License-Identifier: BSD-3-Clause
"""


import _config as config
from zmq_integration_lib import InputPortWithEvents, OutputPort
import os
import json
import re
import requests

requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning
)

log = config.get_logger()


def expand_acronym(texti):
    try:
        rdict = {
            "a": "ae",
            "b": "bee",
            "c": "see",
            "d": "dee",
            "e": "ee",
            "f": "ef",
            "g": "jee",
            "h": "eh",
            "i": "ayee",
            "j": "jay",
            "k": "kay",
            "l": "el",
            "m": "em",
            "n": "en",
            "o": "oh",
            "p": "pee",
            "q": "queue",
            "r": "aar",
            "s": "es",
            "t": "tee",
            "u": "you",
            "v": "we",
            "w": "double you",
            "x": "ex",
            "y": "why",
            "z": "zee",
            "0": "zero",
            "1": "one",
            "2": "two",
            "3": "three",
            "4": "four",
            "5": "five",
            "6": "six",
            "7": "seven",
            "8": "eight",
            "9": "nine",
        }
        text_chars = list(texti.lower())
        def replacer(x): return rdict[x]
        text_pronouceable = list(map(replacer, text_chars))
        texti = " ".join(text_pronouceable)
    except Exception as msg:
        log.debug("main:expand_acronym: %s", msg)
    return texti


def pretty_with_mask(text):
    mask = "****"
    info_to_be_masked = re.findall("[0-9]+", text)
    for info in info_to_be_masked:
        text = text.replace(info, mask)
    return text


def format_bot_reply_for_tts(reply):
    if "BP000" in reply:
        return expand_acronym(reply)
    if "ATM" in reply and "MG" in reply:
        reply = reply.replace("MG", expand_acronym("MG"))
        reply = reply.replace("ATM", expand_acronym("ATM"))
    return reply


def send_message(message):
    # TODO: remove setting proxies to somewhere else
    os.environ["http_proxy"] = ""
    os.environ["https_proxy"] = ""
    # curl localhost:5005/webhooks/rest/webhook -d '{"sender": "user1", "message":"show atms for Pune Bank"}'

    payload = {"sender": "user1", "message": message}
    jwt_token = config.get_jwt()
    headers = {
        "content-type": "application/json",
        "Authorization": "Bearer {}".format(jwt_token),
    }

    r = requests.post(
        config.SERVER_URL + "/webhooks/rest/webhook",
        headers=headers,
        data=json.dumps(payload),
        verify=config.get_cacert(),
        cert=config.get_cert(),
    )
    if r.ok:
        # output is of the form
        # [{"recipient_id":"user1","text":"Hey! How are you?"}]
        try:
            # TODO: take sender user as a variable and group the chat according to user
            return r.json()[0]["text"]
        except (KeyError, IndexError):
            log.debug("Post request failed")
            return ""
    else:
        return ""


def main():
    log.info("start nlp")
    log.info("Main: Start NLP app")

    ip = config.get_inputport()
    out = config.get_outputport()
    for data, event in ip.data_and_event_generator():
        try:
            # event can be INTERMEDIATE and FINAL
            # pick up data corresponding to FINAL event
            # log.info("-> {}".format(data.decode()))
            if event == "FINAL":
                text = data.decode()
                log.info("User: {}".format(text))
                reply = send_message(text)
                log.info("bot: {}".format(pretty_with_mask(reply)))
                # log.info ("send to tts: {}".format(format_bot_reply_for_tts(reply)))
                # Send output to the port
                formatted_reply = format_bot_reply_for_tts(reply)
                out.push(bytes(formatted_reply.lower(), encoding="utf-8"))
                # log.info("Main: Pushing reply on zmq outport")
        except Exception as msg:
            log.error("we got an exception %s", msg)


if __name__ == "__main__":
    main()
