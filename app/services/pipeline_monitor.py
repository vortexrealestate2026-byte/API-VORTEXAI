import datetime

pipeline_logs = []


def log_pipeline(name):

    pipeline_logs.append({
        "pipeline": name,
        "time": datetime.datetime.utcnow()
    })


def get_logs():

    return pipeline_logs
