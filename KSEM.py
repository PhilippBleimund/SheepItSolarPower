import pymodbus
from datetime import datetime
from pymodbus.client import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder

#-----------------------------------------
# Routine to read a float    
def readRegtister(client,myadr_dec, length):
    r1=client.read_holding_registers(myadr_dec,length)
    addedRegisters = 0
    for i in range(length):
        addedRegisters = addedRegisters + (r1.registers[(length-1) - i] * (2**(i * 16)))
        
    result_FloatRegister =round(addedRegisters,4)
    return(result_FloatRegister)   

def read(inverter_ip, inverter_port):  
    try:

        #connection Kostal
        client = ModbusTcpClient(inverter_ip,port=inverter_port)            
        client.connect()

        result = {}
        
        activePowerPlus = (readRegtister(client,0,2) / 10)
        #print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " dc1: ", activePowerPlus)
        result['activePower+'] = activePowerPlus
        activePowerMinus = (readRegtister(client,2,2) / 10) * -1
        #print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " dc1: ", activePowerMinus)
        result['activePower-'] = activePowerMinus
        result['activePower'] = activePowerPlus + activePowerMinus

        activePowerL1Plus = (readRegtister(client,40,2) / 10)
        #print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " dc1: ", activePowerL1Plus)
        result['activePowerL1+'] = activePowerL1Plus
        activePowerL1Minus = (readRegtister(client,42,2) / 10) * -1
        #print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " dc1: ", activePowerL1Minus)
        result['activePowerL1-'] = activePowerL1Minus
        result['activePowerL1'] = activePowerL1Plus + activePowerL1Minus

        activePowerL2Plus = (readRegtister(client,40,2) / 10)
        #print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " dc1: ", activePowerL2Plus)
        result['activePowerL2+'] = activePowerL1Plus
        activePowerL2Minus = (readRegtister(client,42,2) / 10) * -1
        #print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " dc1: ", activePowerL2Minus)
        result['activePowerL2-'] = activePowerL2Minus
        result['activePowerL2'] = activePowerL2Plus + activePowerL2Minus

        
        activeEnergiePlus = (readRegtister(client,512,4) / 10000)                               #Verbrauch in Wh
        #print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " dc1: ", activeEnergiePlus)
        result['activeEnergie+'] = activeEnergiePlus
        activeEnergieMinus = (readRegtister(client,516,4) / 10000) * -1                         #Einspeisung in Wh
        #print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " dc1: ", activeEnergieMinus)
        result['activeEnergie-'] = activeEnergieMinus

        
        
        return result      
    except Exception as ex:
        print ("ERROR Kostal: ", ex) 
    finally:
        client.close() 
      