import threading


def thread_info():
    current_thread = threading.current_thread()
    return f" Thread = [{current_thread.ident}/ {current_thread.name}]"
