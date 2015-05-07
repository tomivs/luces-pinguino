#import firmata			# Python API for the Firmata protocol
import commands			# Execute shell commands via os.popen() and return status, output.

from pynguino import PinguinoProcessing

class TAPinguino(object):
    def __init__(self, baud=115200):
        object.__init__(self)
        #self._dev='/dev/ttyUSB0'
        #self._baud = baud
        #self._pinguino = None # Do not initialize this now
        
		# PinguinoProcessing values
        self.HIGH = "high"
        self.LOW = "low"
        # pin modes
        self.INPUT = "input"
        self.OUTPUT = "output"
        
        #self.PWM = 2
        #self.SERVO = 3
        #self.MAX_DATA_BYTES = 32
        
        try:
		    self.conectar()
        except: pass

    def conectar(self):
        self.pinguino=PinguinoProcessing()
        
        if not self.pinguino.RecursiveConect(): self.criticalMessage()
        
    def criticalMessage(self):
        try:
            self.pinguino.reset()
            self.pinguino.ProcessingClose()
        except: pass
        #self.conectar()

    def _check_init(self):
        if self.pinguino is None:
            # self._pinguino = firmata.Arduino(port = self._dev, baudrate=self._baud)
            self.pinguino = PinguinoProcessing()
        #self._pinguino.parse()

    def delay(self, secs):
        # Do not use this. The firmata module uses time.sleep() to
        # implement this, which breaks gtk+ (unresponsive window)
        #self._check_init()
        self.pinguino.delay(secs)

    def pin_mode(self, pin, mode):
        #self._check_init()
        self.pinguino.pinMode(int(pin), mode)

    def analog_write(self, pin, value):
        #self._check_init()
        self.pinguino.analogWrite(int(pin), value)

    def digital_write(self, pin, value):
        #self._check_init()
        self.pinguino.digitalWrite(int(pin), value)

    def analog_read(self, pin):
        #self._check_init()
        #self.pinguino.parse()  
        return self._pinguino.analogRead(int(pin))

    def digital_read(self, pin):
        #self._check_init()
        #self.pinguino.parse()  
        return self.pinguino.digitalRead(int(pin))


