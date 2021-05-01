from shift_register import ShiftRegister

S_FLAG = 0x80
Z_FLAG = 0x40
AC_FLAG = 0x10
P_FLAG = 0x04
CY_FLAG = 0x01

All_FLAG = Z_FLAG | S_FLAG | P_FLAG | CY_FLAG | AC_FLAG


class I8080Chip:
    SCREEN_WIDTH = 224
    SCREEN_HEIGHT = 256

    COIN_KEY = 0x01
    D1_KEY = 0x02
    SHOOT_KEY = 0x10
    RIGHT_KEY = 0x40
    LEFT_KEY = 0x20

    CYCLES = [
        4, 10, 7, 5, 5, 5, 7, 4, 4, 10, 7, 5, 5, 5, 7, 4,
        4, 10, 7, 5, 5, 5, 7, 4, 4, 10, 7, 5, 5, 5, 7, 4,
        4, 10, 16, 5, 5, 5, 7, 4, 4, 10, 16, 5, 5, 5, 7, 4,
        4, 10, 7, 5, 10, 10, 7, 4, 4, 10, 13, 5, 5, 5, 7, 4,

        5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
        5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
        5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
        5, 5, 7, 7, 7, 7, 7, 5, 5, 5, 5, 5, 5, 5, 5, 5,

        4, 4, 4, 4, 4, 4, 7, 4, 4, 4, 4, 4, 4, 4, 7, 4,
        4, 4, 4, 4, 4, 4, 7, 4, 4, 4, 4, 4, 4, 4, 7, 4,
        4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 7, 4,
        4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 7, 4,

        11, 10, 10, 10, 17, 11, 7, 11, 11, 10, 10, 10, 17, 17, 7, 11,
        11, 10, 10, 10, 17, 11, 7, 11, 11, 10, 10, 10, 10, 17, 7, 11,
        11, 10, 10, 18, 17, 11, 7, 11, 11, 5, 10, 5, 17, 17, 7, 11,
        11, 10, 10, 4, 17, 11, 7, 11, 11, 5, 10, 4, 17, 17, 7, 11,
    ]

    def __init__(self, memory):
        self.count = 0
        # 8-bit registers
        self.a = 0
        self.b = 0
        self.c = 0
        self.d = 0
        self.e = 0
        self.high = 0
        self.low = 0
        # 16-bit registers
        self.sp = 0
        self.pc = 0
        # flags
        self.S = False
        self.Z = False
        self.AC = False
        self.P = False
        self.CY = False

        self.interrupt_index = None
        self.interrupt_enable = True

        self.ram = memory
        self.opcode_handlers = {
            0x00: self.i0x00,
            0x01: self.i0x01,
            0x02: self.i0x02,
            0x03: self.i0x03,
            0x04: self.i0x04,
            0x05: self.i0x05,
            0x06: self.i0x06,
            0x07: self.i0x07,
            0x08: self._not_used,
            0x09: self.i0x09,
            0x0a: self.i0x0a,
            0x0b: self.i0x0b,
            0x0c: self.i0x0c,
            0x0d: self.i0x0d,
            0x0e: self.i0x0e,
            0x0f: self.i0x0f,
            0x10: self._not_used,
            0x11: self.i0x11,
            0x12: self.i0x12,
            0x13: self.i0x13,
            0x14: self.i0x14,
            0x15: self.i0x15,
            0x16: self.i0x16,
            0x17: self.i0x17,
            0x18: self._not_used,
            0x19: self.i0x19,
            0x1a: self.i0x1a,
            0x1b: self.i0x1b,
            0x1c: self.i0x1c,
            0x1d: self.i0x1d,
            0x1e: self.i0x1e,
            0x1f: self.i0x1f,
            0x20: self._not_used,
            0x21: self.i0x21,
            0x22: self.i0x22,
            0x23: self.i0x23,
            0x24: self.i0x24,
            0x25: self.i0x25,
            0x26: self.i0x26,
            0x27: self.i0x27,
            0x28: self._not_used,
            0x29: self.i0x29,
            0x2a: self.i0x2a,
            0x2b: self.i0x2b,
            0x2c: self.i0x2c,
            0x2d: self.i0x2d,
            0x2e: self.i0x2e,
            0x2f: self.i0x2f,
            0x30: self._not_used,
            0x31: self.i0x31,
            0x32: self.i0x32,
            0x33: self.i0x33,
            0x34: self.i0x34,
            0x35: self.i0x35,
            0x36: self.i0x36,
            0x37: self.i0x37,
            0x38: self._not_used,
            0x39: self.i0x39,
            0x3a: self.i0x3a,
            0x3b: self.i0x3b,
            0x3c: self.i0x3c,
            0x3d: self.i0x3d,
            0x3e: self.i0x3e,
            0x3f: self.i0x3f,
            0x40: self.i0x40,
            0x41: self.i0x41,
            0x42: self.i0x42,
            0x43: self.i0x43,
            0x44: self.i0x44,
            0x45: self.i0x45,
            0x46: self.i0x46,
            0x47: self.i0x47,
            0x48: self.i0x48,
            0x49: self.i0x49,
            0x4a: self.i0x4a,
            0x4b: self.i0x4b,
            0x4c: self.i0x4c,
            0x4d: self.i0x4d,
            0x4e: self.i0x4e,
            0x4f: self.i0x4f,
            0x50: self.i0x50,
            0x51: self.i0x51,
            0x52: self.i0x52,
            0x53: self.i0x53,
            0x54: self.i0x54,
            0x55: self.i0x55,
            0x56: self.i0x56,
            0x57: self.i0x57,
            0x58: self.i0x58,
            0x59: self.i0x59,
            0x5a: self.i0x5a,
            0x5b: self.i0x5b,
            0x5c: self.i0x5c,
            0x5d: self.i0x5d,
            0x5e: self.i0x5e,
            0x5f: self.i0x5f,
            0x60: self.i0x60,
            0x61: self.i0x61,
            0x62: self.i0x62,
            0x63: self.i0x63,
            0x64: self.i0x64,
            0x65: self.i0x65,
            0x66: self.i0x66,
            0x67: self.i0x67,
            0x68: self.i0x68,
            0x69: self.i0x69,
            0x6a: self.i0x6a,
            0x6b: self.i0x6b,
            0x6c: self.i0x6c,
            0x6d: self.i0x6d,
            0x6e: self.i0x6e,
            0x6f: self.i0x6f,
            0x70: self.i0x70,
            0x71: self.i0x71,
            0x72: self.i0x72,
            0x73: self.i0x73,
            0x74: self.i0x74,
            0x75: self.i0x75,
            0x76: self.i0x76,
            0x77: self.i0x77,
            0x78: self.i0x78,
            0x79: self.i0x79,
            0x7a: self.i0x7a,
            0x7b: self.i0x7b,
            0x7c: self.i0x7c,
            0x7d: self.i0x7d,
            0x7e: self.i0x7e,
            0x7f: self.i0x7f,
            0x80: self.i0x80,
            0x81: self.i0x81,
            0x82: self.i0x82,
            0x83: self.i0x83,
            0x84: self.i0x84,
            0x85: self.i0x85,
            0x86: self.i0x86,
            0x87: self.i0x87,
            0x88: self.i0x88,
            0x89: self.i0x89,
            0x8a: self.i0x8a,
            0x8b: self.i0x8b,
            0x8c: self.i0x8c,
            0x8d: self.i0x8d,
            0x8e: self.i0x8e,
            0x8f: self.i0x8f,
            0x90: self.i0x90,
            0x91: self.i0x91,
            0x92: self.i0x92,
            0x93: self.i0x93,
            0x94: self.i0x94,
            0x95: self.i0x95,
            0x96: self.i0x96,
            0x97: self.i0x97,
            0x98: self.i0x98,
            0x99: self.i0x99,
            0x9a: self.i0x9a,
            0x9b: self.i0x9b,
            0x9c: self.i0x9c,
            0x9d: self.i0x9d,
            0x9e: self.i0x9e,
            0x9f: self.i0x9f,
            0xa0: self.i0xa0,
            0xa1: self.i0xa1,
            0xa2: self.i0xa2,
            0xa3: self.i0xa3,
            0xa4: self.i0xa4,
            0xa5: self.i0xa5,
            0xa6: self.i0xa6,
            0xa7: self.i0xa7,
            0xa8: self.i0xa8,
            0xa9: self.i0xa9,
            0xaa: self.i0xaa,
            0xab: self.i0xab,
            0xac: self.i0xac,
            0xad: self.i0xad,
            0xae: self.i0xae,
            0xaf: self.i0xaf,
            0xb0: self.i0xb0,
            0xb1: self.i0xb1,
            0xb2: self.i0xb2,
            0xb3: self.i0xb3,
            0xb4: self.i0xb4,
            0xb5: self.i0xb5,
            0xb6: self.i0xb6,
            0xb7: self.i0xb7,
            0xb8: self.i0xb8,
            0xb9: self.i0xb9,
            0xba: self.i0xba,
            0xbb: self.i0xbb,
            0xbc: self.i0xbc,
            0xbd: self.i0xbd,
            0xbe: self.i0xbe,
            0xbf: self.i0xbf,
            0xc0: self.i0xc0,
            0xc1: self.i0xc1,
            0xc2: self.i0xc2,
            0xc3: self.i0xc3,
            0xc4: self.i0xc4,
            0xc5: self.i0xc5,
            0xc6: self.i0xc6,
            0xc7: self.i0xc7,
            0xc8: self.i0xc8,
            0xc9: self.i0xc9,
            0xca: self.i0xca,
            0xcb: self._not_used,
            0xcc: self.i0xcc,
            0xcd: self.i0xcd,
            0xce: self.i0xce,
            0xcf: self.i0xcf,
            0xd0: self.i0xd0,
            0xd1: self.i0xd1,
            0xd2: self.i0xd2,
            0xd3: self.i0xd3,
            0xd4: self.i0xd4,
            0xd5: self.i0xd5,
            0xd6: self.i0xd6,
            0xd7: self.i0xd7,
            0xd8: self.i0xd8,
            0xd9: self._not_used,
            0xda: self.i0xda,
            0xdb: self.i0xdb,
            0xdc: self.i0xdc,
            0xdd: self._not_used,
            0xde: self.i0xde,
            0xdf: self.i0xdf,
            0xe0: self.i0xe0,
            0xe1: self.i0xe1,
            0xe2: self.i0xe2,
            0xe3: self.i0xe3,
            0xe4: self.i0xe4,
            0xe5: self.i0xe5,
            0xe6: self.i0xe6,
            0xe7: self.i0xe7,
            0xe8: self.i0xe8,
            0xe9: self.i0xe9,
            0xea: self.i0xea,
            0xeb: self.i0xeb,
            0xec: self.i0xec,
            0xed: self._not_used,
            0xee: self.i0xee,
            0xef: self.i0xef,
            0xf0: self.i0xf0,
            0xf1: self.i0xf1,
            0xf2: self.i0xf2,
            0xf3: self.i0xf3,
            0xf4: self.i0xf4,
            0xf5: self.i0xf5,
            0xf6: self.i0xf6,
            0xf7: self.i0xf7,
            0xf8: self.i0xf8,
            0xf9: self.i0xf9,
            0xfa: self.i0xfa,
            0xfb: self.i0xfb,
            0xfc: self.i0xfc,
            0xfd: self._not_used,
            0xfe: self.i0xfe,
            0xff: self.i0xff,
        }

        self.video_ram = [None] * \
            (I8080Chip.SCREEN_WIDTH * I8080Chip.SCREEN_HEIGHT)
        self.shift_register = ShiftRegister()
        self.port1 = 8

    def step_run(self):
        if self.interrupt_enable and self.interrupt_index is not None:
            table = {
                0: 0xc7,
                1: 0xcf,
                2: 0xd7,
                3: 0xdf,
                4: 0xe7,
                5: 0xef,
                6: 0xf7,
                7: 0xff,
            }
            if self.interrupt_index in table:
                opcode = table[self.interrupt_index]
            else:
                print('Invalid interrupt')
            self.interrupt_index = None
        else:
            opcode = self._read()
        handler = self.opcode_handlers[opcode]
        ret = handler()
        if is not ret:
            return I8080Chip.CYCLES[opcode] - 6
        else:
            return I8080Chip.CYCLES[opcode]

    def key_down(self, key):
        self.port1 |= key

    def key_up(self, key):
        self.port1 &= ~key

    def convert(self):
        base_ptr = 0x2400
        for i in range(0x1c00):
            value = self.ram[base_ptr + i]
            pixel_index = i * 8
            src_row = pixel_index // 256
            src_col = pixel_index % 256

            dst_col = src_row
            dst_row = 256 - 1 - src_col
            for j in range(8):
                index = (dst_row - j) * 224 + dst_col
                self.video_ram[index] = (value & 0x01) == 0x01
                value >>= 1

    def screen(self, index):
        return self.video_ram[index]

    def trigger_interrupt(self, index):
        self.interrupt_index = index

    # Implementation
    # NOP
    def i0x00(self):
        # print('Nop')
        pass
    # RLC

    def i0x07(self):
        bit7 = self.a >> 7
        self.CY = bit7 == 1
        self.a = (self.a << 1 | bit7) & 0xff
    # RRC

    def i0x0f(self):
        bit0 = self.a & 0x01
        self.CY = bit0 == 1
        self.a = (self.a >> 1 | (bit0 << 7)) & 0xff
    # RAL

    def i0x17(self):
        bit7 = self.a >> 7
        val = (self.a << 1) & 0xff
        if self.CY:
            val |= 0x01
        self.CY = bit7 == 0x01
    # RAR

    def i0x1f(self):
        bit0 = self.a & 0x01
        self.a = self.a >> 1
        if self.CY:
            self.a |= 0x80
        self.CY = bit0 == 0x01
    # SHLD adr

    def i0x22(self):
        address = self._get_address16()
        self.ram[address] = self.low
        self.ram[address + 1] = self.high
    # DAA

    def i0x27(self):
        low_nibble = self.a & 0x0f
        if low_nibble or self.AC:
            val = self.a + 6
            self._update_arith_flag(val, All_FLAG)
            self.a = val & 0xff
        high_nibble = self.a >> 4
        if high_nibble > 9 or self.CY:
            high_nibble += 6
        val = high_nibble << 4 | low_nibble
        self._update_arith_flag(val, All_FLAG)
        self.a = val & 0xff
    # LHLD adr

    def i0x2a(self):
        address = self._get_address16()
        self.low = self.ram[address]
        self.high = self.ram[address + 1]
    # CMA

    def i0x2f(self):
        self.a = (~self.a) & 0xff
    # STA adr

    def i0x32(self):
        address = self._get_address16()
        self.ram[address] = self.a
    # STC

    def i0x37(self):
        self.CY = True
    # LDA adr

    def i0x3a(self):
        address = self._get_address16()
        self.a = self.ram[address]
    # CMC

    def i0x3f(self):
        self.CY = not self.CY
    # HLT

    def i0x76(self):
        print('Halt')
        while True:
            pass

    # RNZ
    def i0xc0(self):
        if not self.Z:
            self._ret()
        else:
            return False
    # JNZ adr

    def i0xc2(self):
        address = self._get_address16()
        if not self.Z:
            self.pc = address
    # JMP adr

    def i0xc3(self):
        address = self._get_address16()
        self.pc = address
    # CNZ adr

    def i0xc4(self):
        address = self._get_address16()
        if not self.Z:
            self._call(address)
        else:
            return False
    # ADI D8

    def i0xc6(self):
        val = self.a + self._read()
        self._update_arith_flag(val, All_FLAG)
        self.a = val & 0xff
    # RZ

    def i0xc8(self):
        if self.Z:
            self._ret()
        else:
            return False
    # RET

    def i0xc9(self):
        self._ret()
    # JZ adr

    def i0xca(self):
        address = self._get_address16()
        if self.Z:
            self.pc = address
    # CZ adr

    def i0xcc(self):
        address = self._get_address16()
        if self.Z:
            self._call(address)
        else:
            return False
    # CALL adr

    def i0xcd(self):
        address = self._get_address16()
        self._call(address)
    # ACI D8

    def i0xce(self):
        val = self.a + self._read()
        if self.CY:
            val += 1
        self._update_arith_flag(val, All_FLAG)
        self.a = val & 0xff
    # RNC

    def i0xd0(self):
        if not self.CY:
            self._ret()
        else:
            return False
    # JNC adr

    def i0xd2(self):
        address = self._get_address16()
        if not self.CY:
            self.pc = address
    # OUT D8

    def i0xd3(self):
        val = self._read()
        if val == 2:
            self.shift_register.set_offset(self.a)
        elif val == 3:
            pass
        elif val == 4:
            self.shift_register.write(self.a)
        elif val == 5:
            pass
        elif val == 6:
            pass
        else:
            print(f'Not expected in out d8, val = {val}')
    # CNC adr

    def i0xd4(self):
        address = self._get_address16()
        if not self.CY:
            self._call(address)
        else:
            return False
    # SUI D8

    def i0xd6(self):
        byte = self._read()
        val = self.a - byte
        self._update_arith_flag(val, All_FLAG ^ CY_FLAG)
        self.CY = val < 0
        self.a = val & 0xff
    # RC

    def i0xd8(self):
        if self.CY:
            self._ret()
        else:
            return False
    # JC adr

    def i0xda(self):
        address = self._get_address16()
        if self.CY:
            self.pc = address
    # IN D8

    def i0xdb(self):
        # Fixme
        val = self._read()
        if val == 0:
            self.a = 14
        elif val == 1:
            self.a = self.port1
        elif val == 2:
            self.a = 0
        elif val == 3:
            self.a = self.shift_register.get_result()
        else:
            print(f'Not expected in IN D8, val = {val}')
            while True:
                pass
    # CC adr

    def i0xdc(self):
        address = self._get_address16()
        if self.CY:
            self._call(address)
        else:
            return False
    # SBI D8

    def i0xde(self):
        val = self.a - self._read()
        if self.CY:
            val -= 1
        self._update_arith_flag(val, All_FLAG ^ CY_FLAG)
        self.CY = val < 0
        self.a = val & 0xff
    # RPO

    def i0xe0(self):
        if not self.P:
            self._ret()
        else:
            return False
    # JPO adr

    def i0xe2(self):
        address = self._get_address16()
        if not self.P:
            self.pc = address
    # XTHL

    def i0xe3(self):
        tmp = self.low
        self.low = self.ram[self.sp]
        self.ram[self.sp] = tmp

        tmp = self.high
        self.high = self.ram[self.sp + 1]
        self.ram[self.sp + 1] = tmp
    # CPO adr

    def i0xe4(self):
        address = self._get_address16()
        if not self.P:
            self._call(address)
        else:
            return False
    # ANI D8

    def i0xe6(self):
        val = self.a & self._read()
        self._update_logic_flag(val, All_FLAG)
        self.a = val & 0xff
    # RPE

    def i0xe8(self):
        if self.P:
            self._ret()
        else:
            return False
    # PCHL

    def i0xe9(self):
        address = (self.high << 8) | self.low
        self.pc = address
    # JPE adr

    def i0xea(self):
        address = self._get_address16()
        if self.P:
            self.pc = address
    # XCHG

    def i0xeb(self):
        tmp = self.d
        self.d = self.high
        self.high = tmp

        tmp = self.e
        self.e = self.low
        self.low = tmp
    # CPE adr

    def i0xec(self):
        address = self._get_address16()
        if self.P:
            self._call(address)
        else:
            return False
    # XRI D8

    def i0xee(self):
        val = self.a ^ self._read()
        self._update_logic_flag(val, All_FLAG)
        self.a = val & 0xff
    # RP

    def i0xf0(self):
        if not self.S:
            self._ret()
        else:
            return False
    # JP adr

    def i0xf2(self):
        address = self._get_address16()
        if not self.S:
            self.pc = address
    # DI

    def i0xf3(self):
        self.interrupt_enable = False
        print('Disable interrupt')
    # CP adr

    def i0xf4(self):
        address = self._get_address16()
        if not self.S:
            self._call(address)
        else:
            return False
    # ORI D8

    def i0xf6(self):
        val = self.a | self._read()
        self._update_logic_flag(val, All_FLAG)
        self.a = val & 0xff
    # RM

    def i0xf8(self):
        if self.S:
            self._ret()
        else:
            return False
    # SPHL

    def i0xf9(self):
        self.sp = (self.high << 8) | self.low
    # JM adr

    def i0xfa(self):
        address = self._get_address16()
        if self.S:
            self.pc = address
    # EI

    def i0xfb(self):
        self.interrupt_enable = True
    # CM adr

    def i0xfc(self):
        address = self._get_address16()
        if self.S:
            self._call(address)
        else:
            return False
    # CPI D8

    def i0xfe(self):
        val = self.a - self._read()
        self._update_arith_flag(val, All_FLAG)
        self.CY = val < 0
    # End

    def _read(self):
        val = self.ram[self.pc]
        self.pc += 1
        return val

    def _get_address16(self):
        low = self._read()
        high = self._read()
        return (high << 8) | low

    def _call(self, address):
        ret_address = self.pc
        self.ram[self.sp - 1] = (ret_address >> 8) & 0xff
        self.ram[self.sp - 2] = ret_address & 0xff
        self.sp -= 2
        self.pc = address

    def _ret(self):
        low = self.ram[self.sp]
        high = self.ram[self.sp + 1]
        address = (high << 8) | low
        self.sp += 2
        self.pc = address

    def _update_arith_flag(self, val, flags):
        if (flags & Z_FLAG) == Z_FLAG:
            self.Z = (val & 0xff) == 0
        if (flags & S_FLAG) == S_FLAG:
            self.S = (val & 0x80) == 0x80
        if (flags & P_FLAG) == P_FLAG:
            self.P = I8080Chip.parity(val)
        if (flags & CY_FLAG) == CY_FLAG:
            self.CY = val > 0xff
        if (flags & AC_FLAG) == AC_FLAG:
            self.AC = I8080Chip.aux_cyrry(val)

    def _update_logic_flag(self, val, flags):
        if (flags & Z_FLAG) == Z_FLAG:
            self.Z = (val & 0xff) == 0
        if (flags & S_FLAG) == S_FLAG:
            self.S = (val & 0x80) == 0x80
        if (flags & P_FLAG) == P_FLAG:
            self.P = I8080Chip.parity(val)
        if (flags & CY_FLAG) == CY_FLAG:
            self.CY = False
        if (flags & AC_FLAG) == AC_FLAG:
            self.AC = False

    def _not_used(self):
        print('Not used instruction')

    @staticmethod
    def parity(val):
        cnt = 0
        for _ in range(8):
            if val & 0x01 == 0x01:
                cnt += 1
            val >>= 1
        return cnt % 2 == 0

    @staticmethod
    def aux_cyrry(val):
        val &= 0xff
        return (val & 0b00011111) > 0x0f
    #     uint8_t last8, cleaned;
    # last8 = answer & 0xff;
    # // zero out first three bits
    # //                  76543210
    # cleaned = last8 & 0b00011111;
    # return cleaned > 0xf;

    # Auto gen ------------------------------------------------------------
    # LXI B,D16
    def i0x01(self):
        self.c = self._read()
        self.b = self._read()

    # STAX B

    def i0x02(self):
        ptr = (self.b << 8) | self.c
        self.ram[ptr] = self.a

    # INX B

    def i0x03(self):
        val = (self.b << 8) | self.c
        val += 1
        self.c = val & 0xff
        self.b = (val >> 8) & 0xff

    # INR B

    def i0x04(self):
        val = self.b + 1
        self._update_arith_flag(val, Z_FLAG | S_FLAG | P_FLAG | AC_FLAG)
        self.b = val & 0xff

    # DCR B

    def i0x05(self):
        val = self.b - 1
        self._update_arith_flag(val, Z_FLAG | S_FLAG | P_FLAG | AC_FLAG)
        self.b = val & 0xff

    # MVI B,D8

    def i0x06(self):
        self.b = self._read()

    # DAD B

    def i0x09(self):
        val = (self.high << 8) + self.low
        val += (self.b << 8) | self.c
        self.CY = val > 0xffff
        self.low = val & 0xff
        self.high = (val >> 8) & 0xff

    # LDAX B

    def i0x0a(self):
        ptr = (self.b << 8) | self.c
        self.a = self.ram[ptr]

    # DCX B

    def i0x0b(self):
        val = (self.b << 8) | self.c
        val -= 1
        self.c = val & 0xff
        self.b = (val >> 8) & 0xff

    # INR C

    def i0x0c(self):
        val = self.c + 1
        self._update_arith_flag(val, Z_FLAG | S_FLAG | P_FLAG | AC_FLAG)
        self.c = val & 0xff

    # DCR C

    def i0x0d(self):
        val = self.c - 1
        self._update_arith_flag(val, Z_FLAG | S_FLAG | P_FLAG | AC_FLAG)
        self.c = val & 0xff

    # MVI C,D8

    def i0x0e(self):
        self.c = self._read()

    # LXI D,D16

    def i0x11(self):
        self.e = self._read()
        self.d = self._read()

    # STAX D

    def i0x12(self):
        ptr = (self.d << 8) | self.e
        self.ram[ptr] = self.a

    # INX D

    def i0x13(self):
        val = (self.d << 8) | self.e
        val += 1
        self.e = val & 0xff
        self.d = (val >> 8) & 0xff

    # INR D

    def i0x14(self):
        val = self.d + 1
        self._update_arith_flag(val, Z_FLAG | S_FLAG | P_FLAG | AC_FLAG)
        self.d = val & 0xff

    # DCR D

    def i0x15(self):
        val = self.d - 1
        self._update_arith_flag(val, Z_FLAG | S_FLAG | P_FLAG | AC_FLAG)
        self.d = val & 0xff

    # MVI D,D8

    def i0x16(self):
        self.d = self._read()

    # DAD D

    def i0x19(self):
        val = (self.high << 8) + self.low
        val += (self.d << 8) | self.e
        self.CY = val > 0xffff
        self.low = val & 0xff
        self.high = (val >> 8) & 0xff

    # LDAX D

    def i0x1a(self):
        ptr = (self.d << 8) | self.e
        self.a = self.ram[ptr]

    # DCX D

    def i0x1b(self):
        val = (self.d << 8) | self.e
        val -= 1
        self.e = val & 0xff
        self.d = (val >> 8) & 0xff

    # INR E

    def i0x1c(self):
        val = self.e + 1
        self._update_arith_flag(val, Z_FLAG | S_FLAG | P_FLAG | AC_FLAG)
        self.e = val & 0xff

    # DCR E

    def i0x1d(self):
        val = self.e - 1
        self._update_arith_flag(val, Z_FLAG | S_FLAG | P_FLAG | AC_FLAG)
        self.e = val & 0xff

    # MVI E,D8

    def i0x1e(self):
        self.e = self._read()

    # LXI H,D16

    def i0x21(self):
        self.low = self._read()
        self.high = self._read()

    # INX H

    def i0x23(self):
        val = (self.high << 8) | self.low
        val += 1
        self.low = val & 0xff
        self.high = (val >> 8) & 0xff

    # INR H

    def i0x24(self):
        val = self.high + 1
        self._update_arith_flag(val, Z_FLAG | S_FLAG | P_FLAG | AC_FLAG)
        self.high = val & 0xff

    # DCR H

    def i0x25(self):
        val = self.high - 1
        self._update_arith_flag(val, Z_FLAG | S_FLAG | P_FLAG | AC_FLAG)
        self.high = val & 0xff

    # MVI H,D8

    def i0x26(self):
        self.high = self._read()

    # DAD H

    def i0x29(self):
        val = (self.high << 8) + self.low
        val *= 2
        self.CY = val > 0xffff
        self.low = val & 0xff
        self.high = (val >> 8) & 0xff

    # DCX H

    def i0x2b(self):
        val = (self.high << 8) | self.low
        val -= 1
        self.low = val & 0xff
        self.high = (val >> 8) & 0xff

    # INR L

    def i0x2c(self):
        val = self.low + 1
        self._update_arith_flag(val, Z_FLAG | S_FLAG | P_FLAG | AC_FLAG)
        self.low = val & 0xff

    # DCR L

    def i0x2d(self):
        val = self.low - 1
        self._update_arith_flag(val, Z_FLAG | S_FLAG | P_FLAG | AC_FLAG)
        self.low = val & 0xff

    # MVI L,D8

    def i0x2e(self):
        self.low = self._read()

    # LXI SP,D16

    def i0x31(self):
        low = self._read()
        high = self._read()
        val = (high << 8) | low
        self.sp = val

    # INX SP

    def i0x33(self):
        self.sp = (self.sp + 1) & 0xff

    # INR M

    def i0x34(self):
        ptr = (self.high << 8) | self.low
        val = self.ram[ptr] + 1
        self._update_arith_flag(val, Z_FLAG | S_FLAG | P_FLAG | AC_FLAG)
        self.ram[ptr] = val & 0xff

    # DCR M

    def i0x35(self):
        ptr = (self.high << 8) | self.low
        val = self.ram[ptr] - 1
        self._update_arith_flag(val, Z_FLAG | S_FLAG | P_FLAG | AC_FLAG)
        self.ram[ptr] = val & 0xff

    # MVI M,D8

    def i0x36(self):
        ptr = (self.high << 8) | self.low
        self.ram[ptr] = self._read()

    # DAD SP

    def i0x39(self):
        val = (self.high << 8) + self.low
        val += self.sp
        self.CY = val > 0xffff
        self.low = val & 0xff
        self.high = (val >> 8) & 0xff

    # DCX SP

    def i0x3b(self):
        self.sp = (self.sp - 1) & 0xff

    # INR A

    def i0x3c(self):
        val = self.a + 1
        self._update_arith_flag(val, Z_FLAG | S_FLAG | P_FLAG | AC_FLAG)
        self.a = val & 0xff

    # DCR A

    def i0x3d(self):
        val = self.a - 1
        self._update_arith_flag(val, Z_FLAG | S_FLAG | P_FLAG | AC_FLAG)
        self.a = val & 0xff

    # MVI A,D8

    def i0x3e(self):
        self.a = self._read()

    # MOV B,B

    def i0x40(self):
        self.b = self.b

    # MOV B,C

    def i0x41(self):
        self.b = self.c

    # MOV B,D

    def i0x42(self):
        self.b = self.d

    # MOV B,E

    def i0x43(self):
        self.b = self.e

    # MOV B,H

    def i0x44(self):
        self.b = self.high

    # MOV B,L

    def i0x45(self):
        self.b = self.low

    # MOV B,M

    def i0x46(self):
        ptr = (self.high << 8) | self.low
        self.b = self.ram[ptr]

    # MOV B,A

    def i0x47(self):
        self.b = self.a

    # MOV C,B

    def i0x48(self):
        self.c = self.b

    # MOV C,C

    def i0x49(self):
        self.c = self.c

    # MOV C,D

    def i0x4a(self):
        self.c = self.d

    # MOV C,E

    def i0x4b(self):
        self.c = self.e

    # MOV C,H

    def i0x4c(self):
        self.c = self.high

    # MOV C,L

    def i0x4d(self):
        self.c = self.low

    # MOV C,M

    def i0x4e(self):
        ptr = (self.high << 8) | self.low
        self.c = self.ram[ptr]

    # MOV C,A

    def i0x4f(self):
        self.c = self.a

    # MOV D,B

    def i0x50(self):
        self.d = self.b

    # MOV D,C

    def i0x51(self):
        self.d = self.c

    # MOV D,D

    def i0x52(self):
        self.d = self.d

    # MOV D,E

    def i0x53(self):
        self.d = self.e

    # MOV D,H

    def i0x54(self):
        self.d = self.high

    # MOV D,L

    def i0x55(self):
        self.d = self.low

    # MOV D,M

    def i0x56(self):
        ptr = (self.high << 8) | self.low
        self.d = self.ram[ptr]

    # MOV D,A

    def i0x57(self):
        self.d = self.a

    # MOV E,B

    def i0x58(self):
        self.e = self.b

    # MOV E,C

    def i0x59(self):
        self.e = self.c

    # MOV E,D

    def i0x5a(self):
        self.e = self.d

    # MOV E,E

    def i0x5b(self):
        self.e = self.e

    # MOV E,H

    def i0x5c(self):
        self.e = self.high

    # MOV E,L

    def i0x5d(self):
        self.e = self.low

    # MOV E,M

    def i0x5e(self):
        ptr = (self.high << 8) | self.low
        self.e = self.ram[ptr]

    # MOV E,A

    def i0x5f(self):
        self.e = self.a

    # MOV H,B

    def i0x60(self):
        self.high = self.b

    # MOV H,C

    def i0x61(self):
        self.high = self.c

    # MOV H,D

    def i0x62(self):
        self.high = self.d

    # MOV H,E

    def i0x63(self):
        self.high = self.e

    # MOV H,H

    def i0x64(self):
        self.high = self.high

    # MOV H,L

    def i0x65(self):
        self.high = self.low

    # MOV H,M

    def i0x66(self):
        ptr = (self.high << 8) | self.low
        self.high = self.ram[ptr]

    # MOV H,A

    def i0x67(self):
        self.high = self.a

    # MOV L,B

    def i0x68(self):
        self.low = self.b

    # MOV L,C

    def i0x69(self):
        self.low = self.c

    # MOV L,D

    def i0x6a(self):
        self.low = self.d

    # MOV L,E

    def i0x6b(self):
        self.low = self.e

    # MOV L,H

    def i0x6c(self):
        self.low = self.high

    # MOV L,L

    def i0x6d(self):
        self.low = self.low

    # MOV L,M

    def i0x6e(self):
        ptr = (self.high << 8) | self.low
        self.low = self.ram[ptr]

    # MOV L,A

    def i0x6f(self):
        self.low = self.a

    # MOV M,B

    def i0x70(self):
        ptr = (self.high << 8) | self.low
        self.ram[ptr] = self.b

    # MOV M,C

    def i0x71(self):
        ptr = (self.high << 8) | self.low
        self.ram[ptr] = self.c

    # MOV M,D

    def i0x72(self):
        ptr = (self.high << 8) | self.low
        self.ram[ptr] = self.d

    # MOV M,E

    def i0x73(self):
        ptr = (self.high << 8) | self.low
        self.ram[ptr] = self.e

    # MOV M,H

    def i0x74(self):
        ptr = (self.high << 8) | self.low
        self.ram[ptr] = self.high

    # MOV M,L

    def i0x75(self):
        ptr = (self.high << 8) | self.low
        self.ram[ptr] = self.low

    # MOV M,A

    def i0x77(self):
        ptr = (self.high << 8) | self.low
        self.ram[ptr] = self.a

    # MOV A,B

    def i0x78(self):
        self.a = self.b

    # MOV A,C

    def i0x79(self):
        self.a = self.c

    # MOV A,D

    def i0x7a(self):
        self.a = self.d

    # MOV A,E

    def i0x7b(self):
        self.a = self.e

    # MOV A,H

    def i0x7c(self):
        self.a = self.high

    # MOV A,L

    def i0x7d(self):
        self.a = self.low

    # MOV A,M

    def i0x7e(self):
        ptr = (self.high << 8) | self.low
        self.a = self.ram[ptr]

    # MOV A,A

    def i0x7f(self):
        self.a = self.a

    # ADD B

    def i0x80(self):
        val = self.a + self.b
        self._update_arith_flag(val, All_FLAG)
        self.a = val & 0xff

    # ADD C

    def i0x81(self):
        val = self.a + self.c
        self._update_arith_flag(val, All_FLAG)
        self.a = val & 0xff

    # ADD D

    def i0x82(self):
        val = self.a + self.d
        self._update_arith_flag(val, All_FLAG)
        self.a = val & 0xff

    # ADD E

    def i0x83(self):
        val = self.a + self.e
        self._update_arith_flag(val, All_FLAG)
        self.a = val & 0xff

    # ADD H

    def i0x84(self):
        val = self.a + self.high
        self._update_arith_flag(val, All_FLAG)
        self.a = val & 0xff

    # ADD L

    def i0x85(self):
        val = self.a + self.low
        self._update_arith_flag(val, All_FLAG)
        self.a = val & 0xff

    # ADD M

    def i0x86(self):
        ptr = (self.high << 8) | self.low
        val = self.a + self.ram[ptr]
        self._update_arith_flag(val, All_FLAG)
        self.a = val & 0xff

    # ADD A

    def i0x87(self):
        val = self.a + self.a
        self._update_arith_flag(val, All_FLAG)
        self.a = val & 0xff

    # ADC B

    def i0x88(self):
        val = self.a + self.b
        if self.CY:
            val += 1
        self._update_arith_flag(val, All_FLAG)
        self.a = val & 0xff

    # ADC C

    def i0x89(self):
        val = self.a + self.c
        if self.CY:
            val += 1
        self._update_arith_flag(val, All_FLAG)
        self.a = val & 0xff

    # ADC D

    def i0x8a(self):
        val = self.a + self.d
        if self.CY:
            val += 1
        self._update_arith_flag(val, All_FLAG)
        self.a = val & 0xff

    # ADC E

    def i0x8b(self):
        val = self.a + self.e
        if self.CY:
            val += 1
        self._update_arith_flag(val, All_FLAG)
        self.a = val & 0xff

    # ADC H

    def i0x8c(self):
        val = self.a + self.high
        if self.CY:
            val += 1
        self._update_arith_flag(val, All_FLAG)
        self.a = val & 0xff

    # ADC L

    def i0x8d(self):
        val = self.a + self.low
        if self.CY:
            val += 1
        self._update_arith_flag(val, All_FLAG)
        self.a = val & 0xff

    # ADC M

    def i0x8e(self):
        ptr = (self.high << 8) | self.low
        val = self.a + self.ram[ptr]
        if self.CY:
            val += 1
        self._update_arith_flag(val, All_FLAG)
        self.a = val & 0xff

    # ADC A

    def i0x8f(self):
        val = self.a + self.a
        if self.CY:
            val += 1
        self._update_arith_flag(val, All_FLAG)
        self.a = val & 0xff

    # SUB B

    def i0x90(self):
        val = self.a - self.b
        self._update_arith_flag(val, All_FLAG)
        self.CY = val < 0
        self.a = val & 0xff

    # SUB C

    def i0x91(self):
        val = self.a - self.c
        self._update_arith_flag(val, All_FLAG)
        self.CY = val < 0
        self.a = val & 0xff

    # SUB D

    def i0x92(self):
        val = self.a - self.d
        self._update_arith_flag(val, All_FLAG)
        self.CY = val < 0
        self.a = val & 0xff

    # SUB E

    def i0x93(self):
        val = self.a - self.e
        self._update_arith_flag(val, All_FLAG)
        self.CY = val < 0
        self.a = val & 0xff

    # SUB H

    def i0x94(self):
        val = self.a - self.high
        self._update_arith_flag(val, All_FLAG)
        self.CY = val < 0
        self.a = val & 0xff

    # SUB L

    def i0x95(self):
        val = self.a - self.low
        self._update_arith_flag(val, All_FLAG)
        self.CY = val < 0
        self.a = val & 0xff

    # SUB M

    def i0x96(self):
        ptr = (self.high << 8) | self.low
        val = self.a - self.ram[ptr]
        self._update_arith_flag(val, All_FLAG)
        self.CY = val < 0
        self.a = val & 0xff

    # SUB A

    def i0x97(self):
        val = self.a - self.a
        self._update_arith_flag(val, All_FLAG)
        self.CY = val < 0
        self.a = val & 0xff

    # SBB B

    def i0x98(self):
        val = self.a - self.b
        if self.CY:
            val -= 1
        self._update_arith_flag(val, All_FLAG)
        self.CY = val < 0
        self.a = val & 0xff

    # SBB C

    def i0x99(self):
        val = self.a - self.c
        if self.CY:
            val -= 1
        self._update_arith_flag(val, All_FLAG)
        self.CY = val < 0
        self.a = val & 0xff

    # SBB D

    def i0x9a(self):
        val = self.a - self.d
        if self.CY:
            val -= 1
        self._update_arith_flag(val, All_FLAG)
        self.CY = val < 0
        self.a = val & 0xff

    # SBB E

    def i0x9b(self):
        val = self.a - self.e
        if self.CY:
            val -= 1
        self._update_arith_flag(val, All_FLAG)
        self.CY = val < 0
        self.a = val & 0xff

    # SBB H

    def i0x9c(self):
        val = self.a - self.high
        if self.CY:
            val -= 1
        self._update_arith_flag(val, All_FLAG)
        self.CY = val < 0
        self.a = val & 0xff

    # SBB L

    def i0x9d(self):
        val = self.a - self.low
        if self.CY:
            val -= 1
        self._update_arith_flag(val, All_FLAG)
        self.CY = val < 0
        self.a = val & 0xff

    # SBB M

    def i0x9e(self):
        ptr = (self.high << 8) | self.low
        val = self.a - self.ram[ptr]
        if self.CY:
            val -= 1
        self._update_arith_flag(val, All_FLAG)
        self.CY = val < 0
        self.a = val & 0xff

    # SBB A

    def i0x9f(self):
        val = self.a - self.a
        if self.CY:
            val -= 1
        self._update_arith_flag(val, All_FLAG)
        self.CY = val < 0
        self.a = val & 0xff

    # ANA B

    def i0xa0(self):
        val = self.a & self.b
        self._update_logic_flag(val, All_FLAG)
        self.a = val & 0xff

    # ANA C

    def i0xa1(self):
        val = self.a & self.c
        self._update_logic_flag(val, All_FLAG)
        self.a = val & 0xff

    # ANA D

    def i0xa2(self):
        val = self.a & self.d
        self._update_logic_flag(val, All_FLAG)
        self.a = val & 0xff

    # ANA E

    def i0xa3(self):
        val = self.a & self.e
        self._update_logic_flag(val, All_FLAG)
        self.a = val & 0xff

    # ANA H

    def i0xa4(self):
        val = self.a & self.high
        self._update_logic_flag(val, All_FLAG)
        self.a = val & 0xff

    # ANA L

    def i0xa5(self):
        val = self.a & self.low
        self._update_logic_flag(val, All_FLAG)
        self.a = val & 0xff

    # ANA M

    def i0xa6(self):
        ptr = (self.high << 8) | self.low
        val = self.a & self.ram[ptr]
        self._update_logic_flag(val, All_FLAG)
        self.a = val & 0xff

    # ANA A

    def i0xa7(self):
        val = self.a & self.a
        self._update_logic_flag(val, All_FLAG)
        self.a = val & 0xff

    # XRA B

    def i0xa8(self):
        val = self.a ^ self.b
        self._update_logic_flag(val, All_FLAG)
        self.a = val & 0xff

    # XRA C

    def i0xa9(self):
        val = self.a ^ self.c
        self._update_logic_flag(val, All_FLAG)
        self.a = val & 0xff

    # XRA D

    def i0xaa(self):
        val = self.a ^ self.d
        self._update_logic_flag(val, All_FLAG)
        self.a = val & 0xff

    # XRA E

    def i0xab(self):
        val = self.a ^ self.e
        self._update_logic_flag(val, All_FLAG)
        self.a = val & 0xff

    # XRA H

    def i0xac(self):
        val = self.a ^ self.high
        self._update_logic_flag(val, All_FLAG)
        self.a = val & 0xff

    # XRA L

    def i0xad(self):
        val = self.a ^ self.low
        self._update_logic_flag(val, All_FLAG)
        self.a = val & 0xff

    # XRA M

    def i0xae(self):
        ptr = (self.high << 8) | self.low
        val = self.a ^ self.ram[ptr]
        self._update_logic_flag(val, All_FLAG)
        self.a = val & 0xff

    # XRA A

    def i0xaf(self):
        val = self.a ^ self.a
        self._update_logic_flag(val, All_FLAG)
        self.a = val & 0xff

    # ORA B

    def i0xb0(self):
        val = self.a | self.b
        self._update_logic_flag(val, All_FLAG)
        self.a = val & 0xff

    # ORA C

    def i0xb1(self):
        val = self.a | self.c
        self._update_logic_flag(val, All_FLAG)
        self.a = val & 0xff

    # ORA D

    def i0xb2(self):
        val = self.a | self.d
        self._update_logic_flag(val, All_FLAG)
        self.a = val & 0xff

    # ORA E

    def i0xb3(self):
        val = self.a | self.e
        self._update_logic_flag(val, All_FLAG)
        self.a = val & 0xff

    # ORA H

    def i0xb4(self):
        val = self.a | self.high
        self._update_logic_flag(val, All_FLAG)
        self.a = val & 0xff

    # ORA L

    def i0xb5(self):
        val = self.a | self.low
        self._update_logic_flag(val, All_FLAG)
        self.a = val & 0xff

    # ORA M

    def i0xb6(self):
        ptr = (self.high << 8) | self.low
        val = self.a | self.ram[ptr]
        self._update_logic_flag(val, All_FLAG)
        self.a = val & 0xff

    # ORA A

    def i0xb7(self):
        val = self.a | self.a
        self._update_logic_flag(val, All_FLAG)
        self.a = val & 0xff

    # CMP B

    def i0xb8(self):
        val = self.a - self.b
        self._update_arith_flag(val, All_FLAG)
        self.CY = val < 0

    # CMP C

    def i0xb9(self):
        val = self.a - self.c
        self._update_arith_flag(val, All_FLAG)
        self.CY = val < 0

    # CMP D

    def i0xba(self):
        val = self.a - self.d
        self._update_arith_flag(val, All_FLAG)
        self.CY = val < 0

    # CMP E

    def i0xbb(self):
        val = self.a - self.e
        self._update_arith_flag(val, All_FLAG)
        self.CY = val < 0

    # CMP H

    def i0xbc(self):
        val = self.a - self.high
        self._update_arith_flag(val, All_FLAG)
        self.CY = val < 0

    # CMP L

    def i0xbd(self):
        val = self.a - self.low
        self._update_arith_flag(val, All_FLAG)
        self.CY = val < 0

    # CMP M

    def i0xbe(self):
        ptr = (self.high << 8) | self.low
        val = self.a - self.ram[ptr]
        self._update_arith_flag(val, All_FLAG)
        self.CY = val < 0

    # CMP A

    def i0xbf(self):
        val = self.a - self.a
        self._update_arith_flag(val, All_FLAG)
        self.CY = val < 0

    # POP B

    def i0xc1(self):
        self.c = self.ram[self.sp]
        self.b = self.ram[self.sp + 1]
        self.sp += 2

    # PUSH B

    def i0xc5(self):
        self.ram[self.sp - 2] = self.c
        self.ram[self.sp - 1] = self.b
        self.sp -= 2

    # RST 0

    def i0xc7(self):
        self._call(0x00)

    # RST 1

    def i0xcf(self):
        self._call(0x08)

    # POP D

    def i0xd1(self):
        self.e = self.ram[self.sp]
        self.d = self.ram[self.sp + 1]
        self.sp += 2

    # PUSH D

    def i0xd5(self):
        self.ram[self.sp - 2] = self.e
        self.ram[self.sp - 1] = self.d
        self.sp -= 2

    # RST 2

    def i0xd7(self):
        self._call(0x10)

    # RST 3

    def i0xdf(self):
        self._call(0x18)

    # POP H

    def i0xe1(self):
        self.low = self.ram[self.sp]
        self.high = self.ram[self.sp + 1]
        self.sp += 2

    # PUSH H

    def i0xe5(self):
        self.ram[self.sp - 2] = self.low
        self.ram[self.sp - 1] = self.high
        self.sp -= 2

    # RST 4

    def i0xe7(self):
        self._call(0x20)

    # RST 5

    def i0xef(self):
        self._call(0x28)

    # POP PSW

    def i0xf1(self):
        val = self.ram[self.sp]
        self.S = (val & S_FLAG) == S_FLAG
        self.Z = (val & Z_FLAG) == Z_FLAG
        self.AC = (val & AC_FLAG) == AC_FLAG
        self.P = (val & P_FLAG) == P_FLAG
        self.CY = (val & CY_FLAG) == CY_FLAG
        self.a = self.ram[self.sp + 1]
        self.sp += 2

    # PUSH PSW

    def i0xf5(self):
        val = 0
        if self.S:
            val |= S_FLAG
        if self.Z:
            val |= Z_FLAG
        if self.AC:
            val |= AC_FLAG
        if self.P:
            val |= P_FLAG
        if self.CY:
            val |= CY_FLAG
        self.ram[self.sp - 2] = val
        self.ram[self.sp - 1] = self.a
        self.sp -= 2

    # RST 6

    def i0xf7(self):
        self._call(0x30)

    # RST 7

    def i0xff(self):
        self._call(0x38)
    # End
