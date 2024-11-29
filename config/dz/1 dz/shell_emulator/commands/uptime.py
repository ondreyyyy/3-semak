import time
start_time = time.time()


def execute():
    uptime = time.time() - start_time
    hours, remainder = divmod(uptime, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"Uptime: {int(hours)}h {int(minutes)}m {int(seconds)}s"
