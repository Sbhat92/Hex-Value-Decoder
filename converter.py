
import struct

class message:
    def __init__(self,packet=None):


        self.hexData=packet 
        assert len(packet)==22        
        self.data={}

    def twos_complement(self, hexstr, bits):
        value = int(hexstr, 16)
        if value & (1 << (bits - 1)):
            value -= 1 << bits
        return value

    def unpack_packet(self):
        if not self.hexData:
            return "No Hex data"
        
        #calculate packet type
        hex_packet_type = self.hexData[0:2]
        self.data["packet_type"]=int(hex_packet_type,16)

        #calculate packet version
        hex_packet_version = self.hexData[2:4]
        self.data["packet_version"]=int(hex_packet_version,16)

        #calculate total energy
        hex_energy=self.hexData[10:12]+self.hexData[8:10]+self.hexData[6:8]+self.hexData[4:6]
        self.data["total_energy_used_watt_hour"]=int(hex_energy,16)

        #calculate time
        hex_time=self.hexData[18:20]+self.hexData[16:18]+self.hexData[14:16]+self.hexData[12:14]
        
        self.data["time_drift_milli_seconds"]=self.twos_complement(hex_time, 32)
        
        #calculate flags
        hex_flags = self.hexData[20:22]
        self.data["flags"]=int(hex_flags,16)

        binary_string="{0:b}".format(self.data["flags"])
        self.data["geyser_is_warm"]=int(binary_string[-1])
        self.data["geyser_is_drawing_power"]=int(binary_string[-2])        

        return {i:self.data[i] for i in self.data if i!='flags'}

    def pack_packet(self,data):
        self.data=data
        hex_value=""

        #calculate packet type
        hex_packet_type=f'{self.data["packet_type"]:x}'
        l=len(hex_packet_type)
        padding=""
        for i in range(2-l):
            padding+="0"
        hex_value+=padding 
        hex_value+=hex_packet_type
 

        #calculate packet version
        hex_packet_v=f'{self.data["packet_version"]:x}'
        l=len(hex_packet_v)
        padding=""
        for i in range(2-l):
            padding+="0"
        hex_value+=padding 
        hex_value+=hex_packet_v
    
        
        #calculate total energy
        hex_energy=f'{self.data["total_energy_used_watt_hour"]:x}'
        l=len(hex_energy)
        padding=""
        for i in range(8-l):
            padding+="0"
        hex_energy=padding+hex_energy        
        for i in range(7,0,-2):
            hex_value+=hex_energy[i-1:i+1]
     


        #calculate time
        hex_time=f'{self.data["time_drift_milli_seconds"]:x}'
        l=len(hex_time)
        padding=""
        for i in range(8-l):
            padding+="0"
        hex_time=padding+hex_time 
        for i in range(7,0,-2):
            hex_value+=hex_time[i-1:i+1]
        
        #calculate flags
        hex_flags=f'{self.data["flags"]:x}'
        l=len(hex_flags)
        padding=""
        for i in range(2-l):
            padding+="0"
        hex_value+=padding 
        hex_value+=hex_flags

        return hex_value



