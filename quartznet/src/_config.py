"""
 Copyright (C) 2021 Intel Corporation
 SPDX-License-Identifier: BSD-3-Clause
"""


from envparse import Env
from zmq_integration_lib import get_inpad, get_outpad


def _validate_env_addr_variable(INPUT_ADDR, OUTPUT_ADDR, AUTHZ_SERVER_ADDR):
    for variable in [INPUT_ADDR, OUTPUT_ADDR, AUTHZ_SERVER_ADDR]:
        if (
            not (type(variable) == str)
            or not (len(variable.split()) == 1)
            or not (("tcp" in variable.split(":")) or ("ipc" in variable.split(":")))
        ):
            raise ValueError("Please check {} address".format(variable))


def _validate_env_topic_variable(INPUT_TOPIC, OUTPUT_TOPIC):
    for variable in [INPUT_TOPIC, OUTPUT_TOPIC]:
        if not (type(variable) == str) or not (len(variable.split()) == 1):
            raise ValueError("Please check {} topic".format(variable))


def _validate_env_log_level_variable(LOG_LEVEL):
    if not LOG_LEVEL.lower() in ["info", "error", "debug"] or not (
        len(LOG_LEVEL.split()) == 1
    ):
        raise ValueError("Please provide correct Log level")


def get_inputport():
    ip = get_inpad(INPUT_ADDR, INPUT_TOPIC, AUTHZ_SERVER_ADDR)
    return ip


def get_outputport():
    op = get_outpad(OUTPUT_ADDR, OUTPUT_TOPIC)
    return op



def display_help():
    print("The application needs the following environment variables.")
    print("INPUT_ADDR, INPUT_TOPIC, OUTPUT_ADDR, OUTPUT_TOPIC")
    print("Please set the variables and try again.")


def _read_env_variables():
    # Can set schema
    env = Env(
        INPUT_ADDR=str,
        INPUT_TOPIC=str,
        OUTPUT_ADDR=str,
        OUTPUT_TOPIC=str,
        AUTHZ_SERVER_ADDR=str,
        LOG_LEVEL=dict(cast=str, default="ERROR"),
    )

    INPUT_ADDR = env("INPUT_ADDR")
    INPUT_TOPIC = env("INPUT_TOPIC")
    OUTPUT_ADDR = env("OUTPUT_ADDR")
    OUTPUT_TOPIC = env("OUTPUT_TOPIC")
    AUTHZ_SERVER_ADDR = env("AUTHZ_SERVER_ADDR")
    LOG_LEVEL = env("LOG_LEVEL")

    # Validate the environment variables
    _validate_env_addr_variable(INPUT_ADDR, OUTPUT_ADDR, AUTHZ_SERVER_ADDR)

    # validate environment topics variables
    _validate_env_topic_variable(INPUT_TOPIC, OUTPUT_TOPIC)

    # validate log level enviroment variables
    _validate_env_log_level_variable(LOG_LEVEL)
    return (
        INPUT_ADDR,
        INPUT_TOPIC,
        OUTPUT_ADDR,
        OUTPUT_TOPIC,
        AUTHZ_SERVER_ADDR,
        LOG_LEVEL,
    )


def get_logger():
    import logging

    global LOG_LEVEL  # string
    level = logging.ERROR
    if LOG_LEVEL.upper() == "WARNING":
        level = logging.WARNING
    if LOG_LEVEL.upper() == "DEBUG":
        level = logging.DEBUG
    if LOG_LEVEL.upper() == "INFO":
        level = logging.INFO

    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s", level=level)
    logging.root.setLevel(level)
    logger = logging.getLogger()
    logger.setLevel(level)
    return logger


(
    INPUT_ADDR,
    INPUT_TOPIC,
    OUTPUT_ADDR,
    OUTPUT_TOPIC,
    AUTHZ_SERVER_ADDR,
    LOG_LEVEL,
) = _read_env_variables()


model_loc="/Models/quartznet-15x5-en.xml"
sample_rate=16000
nchannels = 1
samplewidth=2
