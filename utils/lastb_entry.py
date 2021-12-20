class LastbEntry:
    username = None
    host = None
    timestamp = None

    def __init__(self, username, host, timestamp):
        self.username = username
        self.host = host
        self.timestamp = timestamp

    def is_equal(self, entry):
        return self.username == entry.username and self.host == entry.host and self.timestamp == entry.timestamp

    def is_empty(self):
        return self.username is None and self.host is None and self.timestamp is None

    def __str__(self):
        return '{"username": "%s", "host": "%s", "timestamp": "%s"}' % (self.username, self.host, self.timestamp)