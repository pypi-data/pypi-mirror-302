import time

class Timer:

    def __init__(self, payload) -> None:
        self.payload = payload

    def __enter__(self):
        self.start_timestamp = time.time()

    def __exit__(self):
        print(f"{self.payload} levou {time.time() - self.start_timestamp} segundos para executar")