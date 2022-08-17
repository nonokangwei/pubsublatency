from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
from google.cloud import bigquery
from google.oauth2 import service_account

import json
import time

# TODO(developer)
project_id = "project-kangwe-poc"
subscription_id = "cpslatency-sub"
table_id = "project-kangwe-poc.cpslatency.result"
# Number of seconds the subscriber should listen for messages
timeout = 5.0

credentials = service_account.Credentials.from_service_account_file(
    'serviceaccount.json')

subscriber = pubsub_v1.SubscriberClient(credentials=credentials)
# The `subscription_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/subscriptions/{subscription_id}`
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    decode_message = message.data.decode("utf-8")
    json_message = json.loads(decode_message)
    sent_timestamp = json_message["jsonPayload"]["__time__"]
    latency_time = time.time() - sent_timestamp

    print(f"Received {message.data}. Latency: {latency_time}")
    message.ack()

    client = bigquery.Client(project=project_id, credentials=credentials)
    table_obj = client.get_table(table_id)

    data = [{
        "latency": latency_time,
        "messagepayload": json.dumps(json_message)
    }]
    print(data)
    errors = client.insert_rows(table=table_obj, rows=data)
    if errors == []:
        print("New rows have been added.")
    else:
        print("Encountered errors while inserting rows: {}".format(errors))

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}..\n")

# Wrap subscriber in a 'with' block to automatically call close() when done.
with subscriber:
    try:
        # When `timeout` is not set, result() will block indefinitely,
        # unless an exception is encountered first.
        streaming_pull_future.result()
    except TimeoutError:
        streaming_pull_future.cancel()  # Trigger the shutdown.
        streaming_pull_future.result()  # Block until the shutdown is complete.