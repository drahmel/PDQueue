import memcache

class Cache(object):
	mc = None
	
	@staticmethod
	def init():
		if Cache.mc is None:
			Cache.mc = memcache.Client(['127.0.0.1:11211'], debug=0)
			print "Init Cache"
	@staticmethod
	def add(key,data):
		Cache.init()
		Cache.mc.add(key,data)
	@staticmethod
	def set(key,data,ttl):
		Cache.init()
		Cache.mc.set(key,data)
	@staticmethod
	def get(key):
		Cache.init()
		return Cache.mc.get(key)
	@staticmethod
	def inc(key,num=1):
		Cache.init()
		Cache.add(key,"1")
		total = Cache.mc.incr(key,num)
		return total

