class dataFromSerial:
    def verifyData(self, data):
        sensor = ""
        cmd = ""
        commaIdx = 0
        startIdx = data.find('>')
        if (int(startIdx) != -1):
            for idx, val in enumerate(data):
                if idx > startIdx:
                    if val != ',':
                        if commaIdx == 0:
                            sensor += val
                        else:
                            cmd += val
                    else:
                        commaIdx = idx

            if int(sensor) - 100 > 0:
                if cmd.strip(' \n\r\t')[:-1] == "ok":
                    print("cmd: " + cmd)
                    return cmd.strip(' \n\r\t')[:-1]
                if "hit" in cmd:
                    print("cmd hit: " + cmd)
                    print(cmd.strip(' \n\r\t')[:-1] + "-" + sensor)
                    return cmd.strip(' \n\r\t')[:-1] + "-" + sensor