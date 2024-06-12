import time
import serial.tools.list_ports


class Devices:
    
    prv_status1 = False
    prv_status2 = False
    prv_status3 = False
    
    cur_status1 = False
    cur_status2 = False
    cur_status3 = False

    def __init__(self):
        port_name = self.getPort()
        try:
            self.ser = serial.Serial(port=port_name, baudrate=9600)
            print("Open port successfully")
        except Exception:
            print("Can not open the port")

    relay1_ON = [2, 6, 0, 0, 0, 255, 200, 91]
    relay1_OFF = [2, 6, 0, 0, 0, 0, 136, 27]

    relay2_ON = [3, 6, 0, 0, 0, 255, 200, 91]
    relay2_OFF = [3, 6, 0, 0, 0, 0, 136, 27]

    relay3_ON = [4, 6, 0, 0, 0, 255, 200, 91]
    relay3_OFF = [4, 6, 0, 0, 0, 0, 136, 27]

    def getPort(self):
        ports = serial.tools.list_ports.comports()
        N = len(ports)
        commPort = "None"
        for i in range(0, N):
            port = ports[i]
            strPort = str(port)
            if "USB" in strPort:
                splitPort = strPort.split(" ")
                commPort = splitPort[0]
        return commPort

    def serial_read_data(self, ser):
        bytesToRead = ser.inWaiting()
        if bytesToRead > 0:
            output = ser.read(bytesToRead)
            data_arr = [byte for byte in output]
            print(data_arr)
            arr_size = len(data_arr)
            if arr_size >= 7:
                value = data_arr[arr_size - 4] * 256 + data_arr[arr_size - 3]
                return value
            else:
                return -1
        return 0

    def setDevice1(self, status):
        if status:
            self.ser.write(self.relay1_ON)
        else:
            self.ser.write(self.relay1_OFF)
        time.sleep(1)
        print(self.serial_read_data(self.ser))

    def setDevice2(self, status):
        if status:
            self.ser.write(self.relay2_ON)
        else:
            self.ser.write(self.relay2_OFF)
        time.sleep(1)
        print(self.serial_read_data(self.ser))

    def setDevice3(self, status):
        if status:
            self.ser.write(self.relay3_ON)
        else:
            self.ser.write(self.relay3_OFF)
        time.sleep(1)
        print(self.serial_read_data(self.ser))
        
    def controlDevices(self, listMixers):
        for index, mixer in enumerate(listMixers):
            if index == 0:
                self.cur_status1 = True if mixer else False    
            if index == 1:
                self.cur_status2 = True if mixer else False
            if index == 2:
                self.cur_status3 = True if mixer else False
            
            if self.cur_status1 != self.prv_status1:
                self.prv_status1 = self.cur_status1
                self.setDevice1(self.cur_status1)                    
            
            if self.cur_status2 != self.prv_status2:
                self.prv_status2 = self.cur_status2
                self.setDevice2(self.cur_status2)                    
            
            if self.cur_status3 != self.prv_status3:
                self.prv_status3 = self.cur_status3
                self.setDevice3(self.cur_status3)                    
            
        
