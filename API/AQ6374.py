import pyvisa
import time

class OSA():
    def __init__(self) -> None:
        self.osa = None
        self.rm = pyvisa.ResourceManager()
        self.info = self.discover_and_connect()


    def discover_and_connect(self) -> bool:
        if self._discover() is True:
            if self._connect(self.instrument_identifier) is True:
                return True
            else:
                print("Unable to connect.")
                return False
        else:

            return False

    def _connect(self, identifier) -> bool:
        if self.instrument_identifier is not None:
            self.osa = self.rm.open_resource(identifier)
            self.info = self.smu.query('*IDN?').split(',')
            self.osa.write("*RST")
            self.osa.write("CFORM1")
            return True
        else:
            return False

    def _discover(self) -> bool:
        if self.osa is not None:
            return True
        else: 
            devices = self.rm.list_resources()
            for i in devices:
                if 'AQ6374' in i:
                    self.instrument_identifier = i
                    return True
                else:
                    print(
                        'Available devices: {devices}'.format(devices=devices))
                    return False
                
    def wavelength_range(self, wavelength_start: int, wavelength_end: int):
        # calculate center wavelength and wavelength span
        center_wavelength = (wavelength_start + wavelength_end) / 2
        wavelength_span = wavelength_end - wavelength_start

        self.osa.write(f":TRAC:ACTive TRA")
        self.osa.write(f":SENS:WAV:STAR {wavelength_start};STOP {wavelength_end}NM")
        self.osa.write(":sens:sweep:points:auto on")
    
    def do_sweep(self) -> tuple:
        self.osa.write(":init:smode 1")
        self.osa.write("*CLS")
        self.osa.write(":init")

        sweep_status = 0

        while sweep_status != 1:
            time.sleep(0.01)
            status_response = self.osa.query_ascii_values(":stat:oper:even?")[0]
            sweep_status = int(status_response)

        data_x = self.osa.query_ascii_values("TRAC:X? TRA")
        data_y = self.osa.query_ascii_values("TRAC:Y? TRA")

        return (data_x, data_y)

        

    
    
