# myapp/smart_websocket.py

import websocket
import six
import base64
import zlib
import datetime
import time
import json
import threading
import ssl


class SmartWebSocket(object):
    ROOT_URI = 'wss://wsfeeds.angelbroking.com/NestHtml5Mobile/socket/stream'
    HB_INTERVAL = 30
    HB_THREAD_FLAG = False
    WS_RECONNECT_FLAG = False
    feed_token = None
    client_code = None
    ws = None
    task_dict = {}

    def __init__(self, FEED_TOKEN, CLIENT_CODE):
        self.root = self.ROOT_URI
        self.feed_token = FEED_TOKEN
        self.client_code = CLIENT_CODE
        if self.client_code is None or self.feed_token is None:
            raise ValueError("client_code or feed_token is missing")

    def _subscribe_on_open(self):
        request = {
            "task": "cn",
            "channel": "NONLM",
            "token": self.feed_token,
            "user": self.client_code,
            "acctid": self.client_code
        }
        print(request)
        self.ws.send(six.b(json.dumps(request)))

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        while True:
            if self.HB_THREAD_FLAG:
                break
            print(f"{datetime.datetime.now()} : Start task in the background")
            self.heartBeat()
            time.sleep(self.HB_INTERVAL)

    def subscribe(self, task, token):
        self.task_dict.update([(task, token)])
        if task in ("mw", "sfi", "dp"):
            try:
                request = {
                    "task": task,
                    "channel": token,
                    "token": self.feed_token,
                    "user": self.client_code,
                    "acctid": self.client_code
                }
                self.ws.send(six.b(json.dumps(request)))
                return True
            except Exception as e:
                self._close(reason=f"Error while request sending: {str(e)}")
                raise
        else:
            print("The task entered is invalid. Please enter correct task (mw, sfi, dp).")

    def resubscribe(self):
        for task, marketwatch in self.task_dict.items():
            try:
                request = {
                    "task": task,
                    "channel": marketwatch,
                    "token": self.feed_token,
                    "user": self.client_code,
                    "acctid": self.client_code
                }
                self.ws.send(six.b(json.dumps(request)))
                return True
            except Exception as e:
                self._close(reason=f"Error while request sending: {str(e)}")
                raise

    def heartBeat(self):
        try:
            request = {
                "task": "hb",
                "channel": "",
                "token": self.feed_token,
                "user": self.client_code,
                "acctid": self.client_code
            }
            print(request)
            self.ws.send(six.b(json.dumps(request)))
        except Exception as e:
            print("HeartBeat Sending Failed", e)

    def _parse_text_message(self, message):
        data = base64.b64decode(message)
        try:
            data = bytes((zlib.decompress(data)).decode("utf-8"), 'utf-8')
            data = json.loads(data.decode('utf8').replace("'", '"'))
        except (zlib.error, ValueError) as e:
            print("Failed to decompress or decode the message:", e)
            return
        self._on_message(self.ws, data)

    def connect(self):
        self.ws = websocket.WebSocketApp(
            self.ROOT_URI,
            on_message=self.__on_message,
            on_close=self.__on_close,
            on_open=self.__on_open,
            on_error=self.__on_error
        )
        self.ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

    def __on_message(self, ws, message):
        self._parse_text_message(message)

    def __on_open(self, ws):
        print("__on_open################")
        self.HB_THREAD_FLAG = False
        self._subscribe_on_open()
        if self.WS_RECONNECT_FLAG:
            self.WS_RECONNECT_FLAG = False
            self.resubscribe()
        else:
            self._on_open(ws)

    def __on_close(self, ws):
        self.HB_THREAD_FLAG = True
        print("__on_close################")
        self._on_close(ws)

    def __on_error(self, ws, error):
        if any(substring in str(error) for substring in ["timed", "Connection is already closed", "Connection to remote host was lost"]):
            self.WS_RECONNECT_FLAG = True
            self.HB_THREAD_FLAG = True
            if ws is not None:
                ws.close()
                ws.on_message = None
                ws.on_open = None
                ws.close = None
                del ws
            self.connect()
        else:
            print('Error info:', error)
            self._on_error(ws, error)

    def _on_message(self, ws, message):
        pass

    def _on_open(self, ws):
        pass

    def _on_close(self, ws):
        pass

    def _on_error(self, ws, error):
        pass
