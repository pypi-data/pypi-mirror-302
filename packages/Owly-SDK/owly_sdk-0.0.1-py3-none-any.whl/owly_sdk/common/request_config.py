class RequestConfig:
    def __init__(self, connection_retry=3, connection_retry_time=5):
        self.connection_retry = connection_retry
        self.connection_retry_time = connection_retry_time
