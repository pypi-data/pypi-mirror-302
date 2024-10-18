class DualStream:
    def __init__(self, file_stream, console_stream):
        self.file_stream = file_stream
        self.console_stream = console_stream

    def write(self, message):
        self.file_stream.write(message)
        self.console_stream.write(message)

    def flush(self):
        self.file_stream.flush()
        self.console_stream.flush()