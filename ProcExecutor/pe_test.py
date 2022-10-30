import datetime
import time

from proc_executor import PeSession, PeServer, MessageBase


class MultRequestMessage(MessageBase):
    MESSAGE_CODE_MULT = 1

    def __init__(self, a: float, b: float):
        super().__init__(MultRequestMessage.MESSAGE_CODE_MULT)
        self.a = a
        self.b = b
        self.r = None


class MultServer(PeServer):
    def process_message(self, message):
        if message.service_code == MultRequestMessage.MESSAGE_CODE_MULT:
            message.r = message.a * message.b
            self.response_queue.put(message)


class MultServerSession(PeSession):
    def __init__(self):
        super().__init__({"server_class": MultServer})

    def mult(self, a: float, b: float) -> float:
        request_message = MultRequestMessage(a, b)
        response_message = self.transaction(request_message)
        return response_message.r


if __name__ == "__main__":
    session = MultServerSession()
    session.start()
    start_time = datetime.datetime.utcnow()
    for n in range(10**4):
        r = session.mult(5.0, 6.0)
    elapsed = datetime.datetime.utcnow() - start_time
    print(f'Operation took {elapsed}, i.e. {(elapsed / n).microseconds} microseconds per transaction')
    print(f"r={r}")
    session.stop()
