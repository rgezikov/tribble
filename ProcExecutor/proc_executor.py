import queue
from multiprocessing import Process, Queue


class MessageBase:
    SERVICE_CODE_DONE = 0

    def __init__(self, sc: int):
        self.service_code = sc


class PeServerException(RuntimeError):
    pass


class PeServer:
    def __init__(self, start_parameters):
        self.start_parameters = start_parameters
        self.message_queue = start_parameters['request_queue']
        self.response_queue = start_parameters['response_queue']
        self.server_process = Process(target=self.server_proc, args=(start_parameters,))
        self.server_process.daemon = True
        self.server_process.start()

    def server_proc(self, start_parameters):
        while True:
            new_message = self.message_queue.get()
            if new_message.service_code == MessageBase.SERVICE_CODE_DONE:
                break
            self.process_message(new_message)

    def process_message(self, message):
        pass

    def stop(self):
        self.start_parameters['request_queue'].put(MessageBase(MessageBase.SERVICE_CODE_DONE))
        self.server_process.join()


class PeSession:
    def __init__(self, start_parameters):
        self.start_parameters = start_parameters
        self.server_request_queue = Queue()
        self.server_response_queue = Queue()
        self.start_parameters['request_queue'] = self.server_request_queue
        self.start_parameters['response_queue'] = self.server_response_queue
        self.server = None

    def start(self):
        if 'server_class' in self.start_parameters:
            server_class = self.start_parameters['server_class']
            self.server = server_class(self.start_parameters)
        else:
            raise PeServerException(f'No server class specified')

    def transaction(self, request_message):
        self.server_request_queue.put(request_message)
        return self.server_response_queue.get(block=True)

    def stop(self):
        self.server.stop()
