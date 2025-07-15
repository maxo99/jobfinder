# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

"""
Purpose

Shows how to use the AWS SDK for Python (Boto3) with Amazon Comprehend to run a
topic modeling job on sample data. After the job completes, the output is retrieved
from Amazon S3 and extracted from its compressed format.
"""

import logging
from pprint import pprint
import sys
import boto3

from jobfinder.adapters.comprehend.comprehend_demo_resources import ComprehendDemoResources
from jobfinder.adapters.comprehend.comprehend_topic_modeler import ComprehendTopicModeler, JobInputFormat

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

"""
Base class for implementing custom waiters for services that don't already have
prebuilt waiters. This class leverages botocore waiter code.
"""

from enum import Enum
import logging
import botocore.waiter

logger = logging.getLogger(__name__)


class WaitState(Enum):
    SUCCESS = "success"
    FAILURE = "failure"


class CustomWaiter:
    """
    Base class for a custom waiter that leverages botocore's waiter code. Waiters
    poll an operation, with a specified delay between each polling attempt, until
    either an accepted result is returned or the number of maximum attempts is reached.

    To use, implement a subclass that passes the specific operation, arguments,
    and acceptors to the superclass.

    For example, to implement a custom waiter for the transcription client that
    waits for both success and failure outcomes of the get_transcription_job function,
    create a class like the following:

        class TranscribeCompleteWaiter(CustomWaiter):
        def __init__(self, client):
            super().__init__(
                'TranscribeComplete', 'GetTranscriptionJob',
                'TranscriptionJob.TranscriptionJobStatus',
                {'COMPLETED': WaitState.SUCCESS, 'FAILED': WaitState.FAILURE},
                client)

        def wait(self, job_name):
            self._wait(TranscriptionJobName=job_name)

    """

    def __init__(
        self,
        name,
        operation,
        argument,
        acceptors,
        client,
        delay=10,
        max_tries=60,
        matcher="path",
    ):
        """
        Subclasses should pass specific operations, arguments, and acceptors to
        their superclass.

        :param name: The name of the waiter. This can be any descriptive string.
        :param operation: The operation to wait for. This must match the casing of
                          the underlying operation model, which is typically in
                          CamelCase.
        :param argument: The dict keys used to access the result of the operation, in
                         dot notation. For example, 'Job.Status' will access
                         result['Job']['Status'].
        :param acceptors: The list of acceptors that indicate the wait is over. These
                          can indicate either success or failure. The acceptor values
                          are compared to the result of the operation after the
                          argument keys are applied.
        :param client: The Boto3 client.
        :param delay: The number of seconds to wait between each call to the operation.
        :param max_tries: The maximum number of tries before exiting.
        :param matcher: The kind of matcher to use.
        """
        self.name = name
        self.operation = operation
        self.argument = argument
        self.client = client
        self.waiter_model = botocore.waiter.WaiterModel(
            {
                "version": 2,
                "waiters": {
                    name: {
                        "delay": delay,
                        "operation": operation,
                        "maxAttempts": max_tries,
                        "acceptors": [
                            {
                                "state": state.value,
                                "matcher": matcher,
                                "argument": argument,
                                "expected": expected,
                            }
                            for expected, state in acceptors.items()
                        ],
                    }
                },
            }
        )
        self.waiter = botocore.waiter.create_waiter_with_client(
            self.name, self.waiter_model, self.client
        )

    def __call__(self, parsed, **kwargs):
        """
        Handles the after-call event by logging information about the operation and its
        result.

        :param parsed: The parsed response from polling the operation.
        :param kwargs: Not used, but expected by the caller.
        """
        status = parsed
        for key in self.argument.split("."):
            if key.endswith("[]"):
                status = status.get(key[:-2])[0]
            else:
                status = status.get(key)
        logger.info("Waiter %s called %s, got %s.", self.name, self.operation, status)

    def _wait(self, **kwargs):
        """
        Registers for the after-call event and starts the botocore wait loop.

        :param kwargs: Keyword arguments that are passed to the operation being polled.
        """
        event_name = f"after-call.{self.client.meta.service_model.service_name}"
        self.client.meta.events.register(event_name, self)
        self.waiter.wait(**kwargs)
        self.client.meta.events.unregister(event_name, self)

logger = logging.getLogger(__name__)


class JobCompleteWaiter(CustomWaiter):
    """Waits for a job to complete."""

    def __init__(self, client):
        super().__init__(
            "JobComplete",
            "DescribeTopicsDetectionJob",
            "TopicsDetectionJobProperties.JobStatus",
            {"COMPLETED": WaitState.SUCCESS, "FAILED": WaitState.FAILURE},
            client,
            delay=60,
        )

    def wait(self, job_id):
        self._wait(JobId=job_id)


# snippet-start:[python.example_code.comprehend.Scenario_TopicModeler]
def usage_demo():
    print("-" * 88)
    print("Welcome to the Amazon Comprehend topic modeling demo!")
    print("-" * 88)

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    input_prefix = "input/"
    output_prefix = "output/"
    demo_resources = ComprehendDemoResources(
        boto3.resource("s3"), boto3.resource("iam")
    )
    topic_modeler = ComprehendTopicModeler(boto3.client("comprehend"))

    print("Setting up storage and security resources needed for the demo.")
    demo_resources.setup("jobfinder-comprehend-demo")
    
    
    print("Copying sample data from public bucket into input bucket.")
    demo_resources.bucket.copy(
        {"Bucket": "public-sample-us-west-2", "Key": "TopicModeling/Sample.txt"},
        f"{input_prefix}sample.txt",
    )

    print("Starting topic modeling job on sample data.")
    job_info = topic_modeler.start_job(
        "demo-topic-modeling-job",
        demo_resources.bucket.name,
        input_prefix,
        JobInputFormat.per_line,
        demo_resources.bucket.name,
        output_prefix,
        demo_resources.data_access_role.arn,
    )

    print(
        f"Waiting for job {job_info['JobId']} to complete. This typically takes "
        f"20 - 30 minutes."
    )
    job_waiter = JobCompleteWaiter(topic_modeler.comprehend_client)
    job_waiter.wait(job_info["JobId"])

    job = topic_modeler.describe_job(job_info["JobId"])
    print(f"Job {job['JobId']} complete:")
    pprint(job)

    print(
        f"Getting job output data from the output Amazon S3 bucket: "
        f"{job['OutputDataConfig']['S3Uri']}."
    )
    job_output = demo_resources.extract_job_output(job)
    lines = 10
    print(f"First {lines} lines of document topics output:")
    pprint(job_output["doc-topics.csv"]["data"][:lines])
    print(f"First {lines} lines of terms output:")
    pprint(job_output["topic-terms.csv"]["data"][:lines])

    print("Cleaning up resources created for the demo.")
    demo_resources.cleanup()

    print("Thanks for watching!")
    print("-" * 88)



if __name__ == "__main__":
    try:
        usage_demo()
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
    sys.exit(0)