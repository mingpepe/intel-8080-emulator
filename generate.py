INDENT = '    '
DECLARE_PTR_FROM_HIGH_LOW = 'ptr = (self.high << 8) | self.low'


def h_l2high_low(s):
    if s == 'h':
        return 'high'
    if s == 'l':
        return 'low'
    return s


def operation_on_str(s, val):
    tmp = ord(s) + val
    return chr(tmp)


def to_function_str(data):
    global not_implement_count
    opcode = data[0]
    desc = data[1]
    key = desc.split(' ')[0]

    handlers = {
        'LXI': lxi,
        'STAX': stax,
        'INX': inx,
        'INR': inr,
        'DCR': dcr,
        'MVI': mvi,
        'DAD': dad,
        'LDAX': ldax,
        'DCX': dcx,
        'MOV': mov,
        'ADD': add,
        'ADC': adc,
        'SUB': sub,
        'SBB': sbb,
        'ANA': ana,
        'XRA': xra,
        'ORA': ora,
        'CMP': cmp,
        'POP': pop,
        'PUSH': push,
        'RST': rst,
    }
    buffer = ''
    buffer += f'# {desc}\n'
    buffer += f'def i{opcode}(self):\n'
    if key in handlers:
        code = handlers[key](desc)
        for line in code:
            buffer += f'{INDENT}{line}\n'
        buffer += '\n\n'
        return True, buffer
    else:
        buffer += f'{INDENT}pass\n'
        buffer += '\n\n'
        return False, buffer


def lxi(desc):
    # Always D16
    dst = desc.split(' ')[1].split(',')[0].lower()
    if dst == 'b' or dst == 'd':
        code = [
            f'self.{chr(ord(dst) + 1)} = self._read()',
            f'self.{dst} = self._read()',
        ]
    elif dst == 'h':
        code = [
            'self.low = self._read()',
            'self.high = self._read()',
        ]
    elif dst == 'sp':
        code = [
            'low = self._read()',
            'high = self._read()',
            'val = (high << 8) | low',
            'self.sp = val',
        ]
    else:
        raise Exception('Not expected in lxi')
    return code


def stax(desc):
    item = desc.split(' ')[1]
    item = item.lower()
    next = chr(ord(item) + 1)
    return [
        f'ptr = (self.{item} << 8) | self.{next}',
        'self.ram[ptr] = self.a',
    ]


def inx(desc):
    dst = desc.split(' ')[1]
    dst = dst.lower()
    if dst == 'h':
        return [
            'val = (self.high << 8) | self.low',
            'val += 1',
            'self.low = val & 0xff',
            'self.high = (val >> 8) & 0xff',
        ]
        pass
    elif dst == 'sp':
        return [
            'self.sp = (self.sp + 1) & 0xff',
        ]
    else:
        next = operation_on_str(dst, 1)
        return [
            f'val = (self.{dst} << 8) | self.{next}',
            'val += 1',
            f'self.{next} = val & 0xff',
            f'self.{dst} = (val >> 8) & 0xff',
        ]


def inr(desc):
    dst = desc.split(' ')[1]
    dst = dst.lower()
    if dst == 'm':
        code = [
            DECLARE_PTR_FROM_HIGH_LOW,
            'val = self.ram[ptr] + 1',
            'self._update_arith_flag(val, Z_FLAG | S_FLAG | P_FLAG | AC_FLAG)',
            f'self.ram[ptr] = val & 0xff',
        ]
    else:
        dst = h_l2high_low(dst)
        code = [
            f'val = self.{dst} + 1',
            'self._update_arith_flag(val, Z_FLAG | S_FLAG | P_FLAG | AC_FLAG)',
            f'self.{dst} = val & 0xff',
        ]
    return code


def dcr(desc):
    dst = desc.split(' ')[1]
    dst = dst.lower()
    if dst == 'm':
        code = [
            DECLARE_PTR_FROM_HIGH_LOW,
            'val = self.ram[ptr] - 1',
            'self._update_arith_flag(val, Z_FLAG | S_FLAG | P_FLAG | AC_FLAG)',
            f'self.ram[ptr] = val & 0xff',
        ]
    else:
        dst = h_l2high_low(dst)
        code = [
            f'val = self.{dst} - 1',
            'self._update_arith_flag(val, Z_FLAG | S_FLAG | P_FLAG | AC_FLAG)',
            f'self.{dst} = val & 0xff',
        ]
    return code


def mvi(desc):
    dst = desc.split(' ')[1].split(',')[0]
    dst = dst.lower()
    if dst == 'm':
        code = [
            DECLARE_PTR_FROM_HIGH_LOW,
            'self.ram[ptr] = self._read()',
        ]
    else:
        dst = h_l2high_low(dst)
        code = [
            f'self.{dst} = self._read()',
        ]
    return code


def dad(desc):
    src = desc.split(' ')[1].lower()
    pre_common = [
        'val = (self.high << 8) + self.low',
    ]
    if src == 'sp':
        code = [
            'val += self.sp',
        ]
    elif src == 'h':
        code = [
            'val *= 2',
        ]
    else:
        next = operation_on_str(src, 1)
        code = [
            f'val += (self.{src} << 8) | self.{next}',
        ]
    post_common = [
        'self.CY = val > 0xffff',
        'self.low = val & 0xff',
        'self.high = (val >> 8) & 0xff',
    ]
    return pre_common + code + post_common


def ldax(desc):
    src = desc.split(' ')[1]
    src = src.lower()
    next = operation_on_str(src, 1)
    return [
        f'ptr = (self.{src} << 8) | self.{next}',
        'self.a = self.ram[ptr]',
    ]


def dcx(desc):
    dst = desc.split(' ')[1]
    dst = dst.lower()
    if dst == 'h':
        return [
            'val = (self.high << 8) | self.low',
            'val -= 1',
            'self.low = val & 0xff',
            'self.high = (val >> 8) & 0xff',
        ]
        pass
    elif dst == 'sp':
        return [
            'self.sp = (self.sp - 1) & 0xff',
        ]
    else:
        next = operation_on_str(dst, 1)
        return [
            f'val = (self.{dst} << 8) | self.{next}',
            'val -= 1',
            f'self.{next} = val & 0xff',
            f'self.{dst} = (val >> 8) & 0xff',
        ]


def mov(desc):
    dst, src = desc.split(' ')[1].split(',')
    src = src.lower()
    dst = dst.lower()
    src = h_l2high_low(src)
    dst = h_l2high_low(dst)
    if src == 'm':
        code = [
            DECLARE_PTR_FROM_HIGH_LOW,
            f'self.{dst} = self.ram[ptr]',
        ]
    elif dst == 'm':
        code = [
            DECLARE_PTR_FROM_HIGH_LOW,
            f'self.ram[ptr] = self.{src}',
        ]
    else:
        code = [f'self.{dst} = self.{src}']
    return code


def add(desc):
    add_item = desc.split(' ')[1]
    add_item = add_item.lower()
    if add_item == 'm':
        code = [
            DECLARE_PTR_FROM_HIGH_LOW,
            'val = self.a + self.ram[ptr]',
            'self._update_arith_flag(val, All_FLAG)',
            'self.a = val & 0xff',
        ]
    else:
        add_item = h_l2high_low(add_item)
        code = [
            f'val = self.a + self.{add_item}',
            'self._update_arith_flag(val, All_FLAG)',
            'self.a = val & 0xff',
        ]
    return code


def adc(desc):
    add_item = desc.split(' ')[1]
    add_item = add_item.lower()
    if add_item == 'm':
        code = [
            DECLARE_PTR_FROM_HIGH_LOW,
            'val = self.a + self.ram[ptr]',
            'if self.CY:',
            f'{INDENT}val += 1',
            'self._update_arith_flag(val, All_FLAG)',
            'self.a = val & 0xff',
        ]
    else:
        add_item = h_l2high_low(add_item)
        code = [
            f'val = self.a + self.{add_item}',
            'if self.CY:',
            f'{INDENT}val += 1',
            'self._update_arith_flag(val, All_FLAG)',
            'self.a = val & 0xff',
        ]
    return code


def sub(desc):
    sub_item = desc.split(' ')[1]
    sub_item = sub_item.lower()
    sub_item = h_l2high_low(sub_item)
    if sub_item == 'm':
        code = [
            DECLARE_PTR_FROM_HIGH_LOW,
            'val = self.a - self.ram[ptr]',
            'self._update_arith_flag(val, All_FLAG)',
            'self.CY = val < 0',
            'self.a = val & 0xff',
        ]
    else:
        sub_item = h_l2high_low(sub_item)
        code = [
            f'val = self.a - self.{sub_item}',
            'self._update_arith_flag(val, All_FLAG)',
            'self.CY = val < 0',
            'self.a = val & 0xff',
        ]
    return code


def sbb(desc):
    sub_item = desc.split(' ')[1]
    sub_item = sub_item.lower()
    if sub_item == 'm':
        code = [
            DECLARE_PTR_FROM_HIGH_LOW,
            'val = self.a - self.ram[ptr]',
            'if self.CY:',
            f'{INDENT}val -= 1',
            'self._update_arith_flag(val, All_FLAG)',
            'self.CY = val < 0',
            'self.a = val & 0xff',
        ]
    else:
        sub_item = h_l2high_low(sub_item)
        code = [
            f'val = self.a - self.{sub_item}',
            'if self.CY:',
            f'{INDENT}val -= 1',
            'self._update_arith_flag(val, All_FLAG)',
            'self.CY = val < 0',
            'self.a = val & 0xff',
        ]
    return code


def ana(desc):
    and_item = desc.split(' ')[1]
    and_item = and_item.lower()
    if and_item == 'm':
        code = [
            DECLARE_PTR_FROM_HIGH_LOW,
            'val = self.a & self.ram[ptr]',
            'self._update_logic_flag(val, All_FLAG)',
            'self.a = val & 0xff',
        ]
    else:
        and_item = h_l2high_low(and_item)
        code = [
            f'val = self.a & self.{and_item}',
            'self._update_logic_flag(val, All_FLAG)',
            'self.a = val & 0xff',
        ]
    return code


def xra(desc):
    xor_item = desc.split(' ')[1]
    xor_item = xor_item.lower()
    if xor_item == 'm':
        code = [
            DECLARE_PTR_FROM_HIGH_LOW,
            'val = self.a ^ self.ram[ptr]',
            'self._update_logic_flag(val, All_FLAG)',
            'self.a = val & 0xff',
        ]
    else:
        xor_item = h_l2high_low(xor_item)
        code = [
            f'val = self.a ^ self.{xor_item}',
            'self._update_logic_flag(val, All_FLAG)',
            'self.a = val & 0xff',
        ]
    return code


def ora(desc):
    or_item = desc.split(' ')[1]
    or_item = or_item.lower()
    if or_item == 'm':
        code = [
            DECLARE_PTR_FROM_HIGH_LOW,
            'val = self.a | self.ram[ptr]',
            'self._update_logic_flag(val, All_FLAG)',
            'self.a = val & 0xff',
        ]
    else:
        or_item = h_l2high_low(or_item)
        code = [
            f'val = self.a | self.{or_item}',
            'self._update_logic_flag(val, All_FLAG)',
            'self.a = val & 0xff',
        ]
    return code


def cmp(desc):
    sub_item = desc.split(' ')[1]
    sub_item = sub_item.lower()
    if sub_item == 'm':
        code = [
            DECLARE_PTR_FROM_HIGH_LOW,
            'val = self.a - self.ram[ptr]',
            'self._update_arith_flag(val, All_FLAG)',
            'self.CY = val < 0',
        ]
    else:
        sub_item = h_l2high_low(sub_item)
        code = [
            f'val = self.a - self.{sub_item}',
            'self._update_arith_flag(val, All_FLAG)',
            'self.CY = val < 0',
        ]
    return code


def pop(desc):
    item = desc.split(' ')[1]
    item = item.lower()
    if item == 'h':
        code = [
            'self.low = self.ram[self.sp]',
            'self.high = self.ram[self.sp + 1]',
        ]
    elif item == 'psw':
        code = [
            'val = self.ram[self.sp]',
            'self.S = (val & S_FLAG) == S_FLAG',
            'self.Z = (val & Z_FLAG) == Z_FLAG',
            'self.AC = (val & AC_FLAG) == AC_FLAG',
            'self.P = (val & P_FLAG) == P_FLAG',
            'self.CY = (val & CY_FLAG) == CY_FLAG',
            'self.a = self.ram[self.sp + 1]',
        ]
    else:
        next = operation_on_str(item, 1)
        code = [
            f'self.{next} = self.ram[self.sp]',
            f'self.{item} = self.ram[self.sp + 1]',
        ]
    post_common = [
        'self.sp += 2',
    ]
    return code + post_common


def push(desc):
    item = desc.split(' ')[1]
    item = item.lower()
    if item == 'h':
        code = [
            'self.ram[self.sp - 2] = self.low',
            'self.ram[self.sp - 1] = self.high',
        ]
    elif item == 'psw':
        code = [
            'val = 0',
            'if self.S:',
            f'{INDENT}val |= S_FLAG',
            'if self.Z:',
            f'{INDENT}val |= Z_FLAG',
            'if self.AC:',
            f'{INDENT}val |= AC_FLAG',
            'if self.P:',
            f'{INDENT}val |= P_FLAG',
            'if self.CY:',
            f'{INDENT}val |= CY_FLAG',
            'self.ram[self.sp - 2] = val',
            'self.ram[self.sp - 1] = self.a',
        ]
    else:
        next = operation_on_str(item, 1)
        code = [
            f'self.ram[self.sp - 2] = self.{next}',
            f'self.ram[self.sp - 1] = self.{item}',
        ]
    post_common = [
        'self.sp -= 2',
    ]
    return code + post_common


def rst(desc):
    index = desc.split(' ')[1]
    mapping = {
        '0': '0x00',
        '1': '0x08',
        '2': '0x10',
        '3': '0x18',
        '4': '0x20',
        '5': '0x28',
        '6': '0x30',
        '7': '0x38',
    }
    if index in mapping:
        address = mapping[index]
        return [f'self._call({address})']
    raise Exception('Not expected in rst')


output_buffer = ''
to_implement = ''
with open('opcode_gen//opcode_data.txt', 'r') as f:
    for line in f:
        if line.startswith('//'):
            continue
        sep = line.split('\t')
        if (sep[1] == '-'):
            continue
        result, code = to_function_str(sep)
        if result:
            output_buffer += code
        else:
            to_implement += code

with open('opcode_gen//output.py', 'w') as f:
    f.write(output_buffer)
with open('opcode_gen//to_implement.py', 'w') as f:
    f.write(to_implement)
