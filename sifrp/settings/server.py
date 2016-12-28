DEVELOPMENT, STAGING, PRODUCTION = 0, 1, 2

class Server:
    def __init__(self, type, time_zone, language_code):
        self.TYPE = type
        self.TIME_ZONE = time_zone
        self.LANGUAGE_CODE = language_code

default = Server(PRODUCTION, 'America/New_York', 'en-us')
servers = {}

def register(name, type, time_zone, language_code):
    servers[name] = Server(type, time_zone, language_code)

def select(name):
    return servers.get(name, default)
