# encoding: utf-8

"""MIME-encoded electronic mail message class."""

from __future__ import unicode_literals

import imghdr
import os
import sys
import time
import base64

from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.nonmultipart import MIMENonMultipart
from email.utils import make_msgid, formatdate
from mimetypes import guess_type

from marrow.mailer import release
from marrow.mailer.address import Address, AddressList, AutoConverter
from marrow.util.compat import basestring, unicode, native


__all__ = ['Message']


class Message(object):
	"""Represents an e-mail message."""

	sender = AutoConverter('_sender', Address, False)
	author = AutoConverter('_author', AddressList)
	authors = author
	to = AutoConverter('_to', AddressList)
	cc = AutoConverter('_cc', AddressList)
	bcc = AutoConverter('_bcc', AddressList)
	reply = AutoConverter('_reply', AddressList)
	notify = AutoConverter('_notify', AddressList)

	def __init__(self, author=None, to=None, subject=None, **kw):
		"""Instantiate a new Message object.

		No arguments are required, as everything can be set using class
		properties.  Alternatively, __everything__ can be set using the
		constructor, using named arguments.  The first three positional
		arguments can be used to quickly prepare a simple message.
		"""

		# Internally used attributes
		self._id = None
		self._processed = False
		self._dirty = False
		self.mailer = None

		# Default values
		self.subject = None
		self.date = datetime.now()
		self.encoding = 'utf-8'
		self.organization = None
		self.priority = None
		self.plain = None
		self.rich = None
		self.attachments = []
		self.embedded = []
		self.headers = []
		self.retries = 3
		self.brand = True

		self._sender = None
		self._author = AddressList()
		self._to = AddressList()
		self._cc = AddressList()
		self._bcc = AddressList()
		self._reply = AddressList()
		self._notify = AddressList()

		# Overrides at initialization time
		if author is not None:
			self.author = author

		if to is not None:
			self.to = to

		if subject is not None:
			self.subject = subject

		for k in kw:
			if not hasattr(self, k):
				raise TypeError("Unexpected keyword argument: %s" % k)

			setattr(self, k, kw[k])

	def __setattr__(self, name, value):
		"""Set the dirty flag as properties are updated."""
		object.__setattr__(self, name, value)
		if name not in ('bcc', '_id', '_dirty', '_processed'):
			object.__setattr__(self, '_dirty', True)
	
	def __str__(self):
		return self.mime.as_string()
	
	__unicode__ = __str__
	
	def __bytes__(self):
		return self.mime.as_string().encode('ascii')
	

	@property
	def envelope(self):
		"""Returns the address of the envelope sender address (SMTP from, if
		not set the sender, if this one isn't set too, the author)."""
		pass



	def _build_date_header_string(self, date_value):
		"""Gets the date_value (may be None, basestring, float or
		datetime.datetime instance) and returns a valid date string as per
		RFC 2822."""
		pass



	@property
	def mime(self):
		"""Produce the final MIME message."""
		pass

	def attach(self, name, data=None, maintype=None, subtype=None,
		inline=False, filename=None, filename_charset='', filename_language='',
		encoding=None):
		"""Attach a file to this message.

		:param name: Path to the file to attach if data is None, or the name
					 of the file if the ``data`` argument is given
		:param data: Contents of the file to attach, or None if the data is to
					 be read from the file pointed to by the ``name`` argument
		:type data: bytes or a file-like object
		:param maintype: First part of the MIME type of the file -- will be
						 automatically guessed if not given
		:param subtype: Second part of the MIME type of the file -- will be
						automatically guessed if not given
		:param inline: Whether to set the Content-Disposition for the file to
					   "inline" (True) or "attachment" (False)
		:param filename: The file name of the attached file as seen
									by the user in his/her mail client.
		:param filename_charset: Charset used for the filename parameter. Allows for 
						attachment names with characters from UTF-8 or Latin 1. See RFC 2231.
		:param filename_language: Used to specify what language the filename is in. See RFC 2231.
		:param encoding: Value of the Content-Encoding MIME header (e.g. "gzip"
						 in case of .tar.gz, but usually empty)
		"""
		pass

	def embed(self, name, data=None):
		"""Attach an image file and prepare for HTML embedding.

		This method should only be used to embed images.

		:param name: Path to the image to embed if data is None, or the name
					 of the file if the ``data`` argument is given
		:param data: Contents of the image to embed, or None if the data is to
					 be read from the file pointed to by the ``name`` argument
		"""
		pass


	def send(self):
		if not self.mailer:
			raise NotImplementedError("Message instance is not bound to " \
				"a Mailer. Use mailer.send() instead.")
		return self.mailer.send(self)
