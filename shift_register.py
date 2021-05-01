class ShiftRegister:
    def __init__(self):
        self.low = 0
        self.high = 0
        self.offset = 0

    def set_offset(self, offset):
        self.offset = offset & 0x07

    def write(self, val):
        self.low = self.high
        self.high = val

    def get_result(self):
        val = (self.high << 8) | self.low
        val >>= (8 - self.offset)
        return val & 0xff
