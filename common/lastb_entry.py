import utmp


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

    @staticmethod
    def get_last_btmp_entry():
        with open('/var/log/btmp', 'rb') as fd:
            buf = fd.read()
            for entry in utmp.read(buf):
                pass
                # print(entry.time, entry.type, entry)
        last_entry = LastbEntry(username=entry.user, host=entry.host, timestamp=entry.sec)
        return last_entry

    def __str__(self):
        return f'{{"username": "{self.username}", "host": "{self.host}", "timestamp": "{self.timestamp}"}}'
