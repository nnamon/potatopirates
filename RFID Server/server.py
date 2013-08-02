import tornado.ioloop
import tornado.web
import tornado.websocket as websocket
import serial
import threading

class Arduino:
	def __init__(self, port='COM4', baud_rate=9600, timeout=1):
		self.port = port
		self.baud_rate = baud_rate
		self.timeout = timeout
		self.wsList = []
		self.connect()
		threading.Thread(target=self.wait_for_data).start()
		
	def connect(self):
		self.conn = serial.Serial(self.port, self.baud_rate, timeout=self.timeout)
	
	def read(self):
		return self.conn.readline()
		
	def close(self):
		self.conn.close()
		
	def add_to_list(self, ws):
		self.wsList.append(ws)
		
	def wait_for_data(self):
		while True:
			msg = self.read().rstrip()
			if not msg == '':
				drop_ws_list = []
				for i, ws in enumerate(self.wsList):
					try:
						ws.write_message(msg);
					except:
						drop_ws_list.append(i)
						
				for i in reversed(drop_ws_list):
					del self.wsList[i]


duino = Arduino()

	
class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("Hello, world")

class EchoWebSocket(websocket.WebSocketHandler):
	def open(self):
		print "WebSocket opened"
		duino.add_to_list(self)
		

	def on_message(self, message):
		self.write_message(u"You said: " + message)

	def on_close(self):
		print "WebSocket closed"
		
application = tornado.web.Application([
	(r"/", MainHandler),
	(r"/websocket", EchoWebSocket),
])

if __name__ == "__main__":
	application.listen(8888)
	tornado.ioloop.IOLoop.instance().start()