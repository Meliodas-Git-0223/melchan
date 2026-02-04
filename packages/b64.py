import base64

def encode(txt, coding='utf-8'):
	return (str(base64.b64encode(txt.encode(coding)))[2:-1])

def decode(txt, coding='utf-8'):
	return base64.b64decode(txt.encode(coding)).decode('utf-8')