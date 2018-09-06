import requests
import json
import urllib2
import base64
import threading
from flata import Flata, where
from flata.storages import JSONStorage
from zabbix_gmxp import SendDataZabbix

class SendData:
    url = "http://10.210.0.17:5000/api/events/27/activations/{0}/matches"
    username = "bizsys"
    password = "P3wl1#]2Fx3jL)x0"
    db = Flata('db.json', storage=JSONStorage)

    def send_to_calindra(self, data, activationCode):
        try:
            print(data)
            req = urllib2.Request(self.url.format(activationCode))
            credentials = '{username}:{password}'.format(username=self.username, password=self.password).encode()
            req.add_header('Authorization', 'Basic ' + base64.b64encode(credentials))
            req.add_header('Content-Type','application/json;charset=UTF-8')
            req.add_header('Content-Length', str(len(data)))
            response = urllib2.urlopen(req, data)
            if response.getcode() != 201:
                d = json.loads(data)
                self.db.table('errors').insert(d)
                threading.Thread(target=SendDataZabbix().send_zabbix, args=("gxp-pm01", "http", 9), kwargs={}).start()
            else:
                threading.Thread(target=SendDataZabbix().send_zabbix, args=("gxp-pm01", "http", 1), kwargs={}).start()
                print(response.getcode())
        except urllib2.HTTPError, e:
            d = json.loads(data)
            self.db.table('errors').insert(d)
            threading.Thread(target=SendDataZabbix().send_zabbix, args=("gxp-pm01", "http", 99), kwargs={}).start()
            print e.code