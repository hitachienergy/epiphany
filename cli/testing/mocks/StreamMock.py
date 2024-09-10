from typing import List


class StreamBuffer:
    def __init__(self):
        self.buffer: List[bytes] = []

    def write(self, data: bytes):
        self.buffer.append(data)


class StreamMock:
    def __init__(self):
        self.__sbuffer: StreamBuffer = StreamBuffer()

    def __enter__(self):
        return self.__sbuffer

    def __exit__(self, arg1, arg2, hue):
        pass

    @property
    def data(self) -> str:
        return ''.join(byte.decode() for byte in self.__sbuffer.buffer)
