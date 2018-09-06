from pyzabbix import ZabbixMetric, ZabbixSender
# zabbix-srv.brazilsouth.cloudapp.azure.com

class SendDataZabbix:
    def send_zabbix(self, localhost, item, data):
        packet = [
            ZabbixMetric(localhost, item, data),
        ]
        result = ZabbixSender(zabbix_server='10.210.2.41',zabbix_port=10051,use_config=None).send(packet)
        print result