"""Define functions to use in redis queue."""

import time

from rq import get_current_job
from app.blob_storage import *

def some_long_function(some_input):
    """An example function for redis queue."""
    job = get_current_job()
    print("some_long_function is getting called")
    print("Blender Project Path {}".format(some_input))
    # Pass uploaded filename to function to download it first
    downloaded_file = blob_download_handler(some_input)
    os.system("blender " + downloaded_file + " -b -P app/gpu_test.py")
    # os.system("blender " + downloaded_file + " -b -P app/bake_all.py")
    print("File has been downloaded at path : {}".format(downloaded_file))

    # time.sleep(20)
    print("some_long_function is executed")

    return {
        "job_id": job.id,
        "job_enqueued_at": job.enqueued_at.isoformat(),
        "job_started_at": job.started_at.isoformat(),
        "input": some_input,
        "result": some_input,
    }
