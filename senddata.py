import requests
import json
import urllib2
import base64

class SendData:
    url = "https://api-gamexp.worldticket.com.br/api/events/27/activations/{0}/matches"
    username = "bizsys"
    password = "P3wl1#]2Fx3jL)x0"

    def send_to_calindra(self, data, activationCode):
        try:
            print(data)
            req = urllib2.Request(self.url.format(activationCode))
            credentials = '{username}:{password}'.format(username=self.username, password=self.password).encode()
            req.add_header('Authorization', 'Basic ' + base64.b64encode(credentials))
            req.add_header('Content-Type','application/json;charset=UTF-8')
            req.add_header('Content-Length', str(len(data)))
            response = urllib2.urlopen(req, data)
            print(response)
        except urllib2.HTTPError, e:
            print e