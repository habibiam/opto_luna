from multiprocessing import Process, Pipe
from random import randrange
class DataPublisher:
	def Publish(self,pipe):
		print('dataPublisher')
		while(1):
			pipe.send(randrange(0, 101, 2))
			#pipe.close()

dp = DataPublisher()
