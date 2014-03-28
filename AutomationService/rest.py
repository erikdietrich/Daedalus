import web
import json
from index import Index
from lights import Lights

from CM19aDriver import CM19aDevice

REFRESH = 1.0               # Refresh rate (seconds) for polling the transceiver for inbound commands


urls = (
  '/lights', 'Lights',
  '/lights/(.*?)/(.*?)', 'Lights',
  '/lights/(.*?)', 'Lights',
  '/', 'Index',
  '/(.*?)', 'Index',
  '',  'Index')

app = web.application(urls, globals())
  

if __name__ == "__main__":
    app.run()
