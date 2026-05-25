# encoding: utf-8

"""Utilities for testing Marrow Mailer and applications that use it."""

from __future__ import print_function

from threading import Thread
from socket import socket
from threading import Event, RLock
from datetime import datetime
from collections import namedtuple, deque
from smtpd import SMTPServer
from email.parser import Parser
from asyncore import loop

try:
	from pytest import fixture
except:  # We don't honestly care if pytest is installed.
	def fixture(fn):
		return fn


TestMessage = namedtuple('TestMessage', ('sender', 'recipients', 'time', 'message', 'raw'))


class DebuggingSMTPServer(SMTPServer, Thread):
	"""A generalized testing SMTP server that captures messages delivered to it."""
	
	POLL_TIMEOUT = 0.001
	
	def __init__(self, host='127.0.0.1', port=2526):
		# Initialize the SMTP component.
		# My face that asyncore doesn't use new style classes!
		SMTPServer.__init__(self, (host, port), None)
		
		# Retrieve the actually-bound socket address. May, in some circumstances, use a reverse DNS name.
		if self._localaddr[1] == 0:
			self.address = self.socket.getsockname()
		else:
			self.address = (host, port)
		
		# Create a place to store messages.
		self.messages = deque()
		
		# Setup threading.
		self._stop = Event()
		self._lock = RLock()
		Thread.__init__(self, name=self.__class__.__name__)
	
	@classmethod
	def main(cls):
		server = cls()
		
		print("Debugging SMTP server is running on ", server.address[0], ":", server.address[1], sep="")
		print("Press Control+C to stop.")
		
		try:
			loop()
		except KeyboardInterrupt:
			pass
	
	
	
	
	def __getitem__(self, i):
		return self.messages.__getitem__(i)
	
	def __len__(self):
		return len(self.messages)
	
	def __iter__(self):
		return iter(self.messages)
	
	






if __name__ == '__main__':  # pragma: no cover
	DebuggingSMTPServer.main()
