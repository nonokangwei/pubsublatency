#!/usr/bin/env python

# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This application demonstrates how to perform basic operations on logs and
log entries with Cloud Logging.

For more information, see the README.md under /logging and the
documentation at https://cloud.google.com/logging/docs.
"""

import argparse
import time

from google.oauth2 import service_account
from google.cloud import logging


# [START logging_write_log_entry]
def write_entry(logger_name):
    credentials = service_account.Credentials.from_service_account_file(
    'serviceaccount.json')

    """Writes log entries to the given logger."""
    logging_client = logging.Client(credentials=credentials)

    # This log can be found in the Cloud Logging console under 'Custom Logs'.
    # logger = logging_client.logger(logger_name)

    # # Make a simple text log
    # logger.log_text("Hello, world!")

    # # Simple text log with severity.
    # logger.log_text("Goodbye, world!", severity="ERROR")

    # Struct log. The struct can be any JSON-serializable dictionary.
    for i in range (10):
        logging_client.logger(logger_name).log_struct(
            {
                "code": "0",
                "status_code": "200",
                "logger": "gateway",
                "elapsed": "7.999000",
                "hostname": "plat-sg03-infra-prod-data-opgateway001",
                "file": "log.go:77",
                "remote_ip": "10.171.154.23",
                "__pack_meta__": "3|MTY1OTQyNTU1ODYxOTY3MjI4OA==|155|147",
                "function": "Log.func1",
                "host": "sg-data-op.private.hoyoverse.com",
                "client_ip": "10.171.106.122",
                "__tag__:__pack_id__": "B03FA280BFE98B11-F88",
                "content_length": "1379",
                "user_agent": "Go-http-client/1.1",
                "timestamp": "1660632263",
                "__time__": time.time(),
                "__topic__": "",
                "method": "POST",
                "level": "info",
                "__source__": "10.171.154.212",
                "message": "http request",
                "env": "prod-os",
                "url": "/rec-sys-global/recommend/rec",
                "app_name": "gateway",
                "__tag__:__hostname__": "plat-sg03-infra-prod-data-opgateway001",
                "time": "2022-08-16 06:44:23.872",
                "module_name": "gopkg.mihoyo.com/plat/kit/http/middleware",
                "request_id": "250ad6b3e9ac4f4",
                "__tag__:__path__": "/home/data/logs/takumi/gateway/gateway.log"
            }
        )

    print("Wrote logs to {}.".format(logger_name))


# [END logging_write_log_entry]


# [START logging_list_log_entries]
def list_entries(logger_name):
    """Lists the most recent entries for a given logger."""
    logging_client = logging.Client()
    logger = logging_client.logger(logger_name)

    print("Listing entries for logger {}:".format(logger.name))

    for entry in logger.list_entries():
        timestamp = entry.timestamp.isoformat()
        print("* {}: {}".format(timestamp, entry.payload))


# [END logging_list_log_entries]


# [START logging_delete_log]
def delete_logger(logger_name):
    """Deletes a logger and all its entries.

    Note that a deletion can take several minutes to take effect.
    """
    logging_client = logging.Client()
    logger = logging_client.logger(logger_name)

    logger.delete()

    print("Deleted all logging entries for {}".format(logger.name))


# [END logging_delete_log]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("logger_name", help="Logger name", default="example_log")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("list", help=list_entries.__doc__)
    subparsers.add_parser("write", help=write_entry.__doc__)
    subparsers.add_parser("delete", help=delete_logger.__doc__)

    args = parser.parse_args()

    if args.command == "list":
        list_entries(args.logger_name)
    elif args.command == "write":
        write_entry(args.logger_name)
    elif args.command == "delete":
        delete_logger(args.logger_name)