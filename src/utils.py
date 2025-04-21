s_box = [0x9, 0x4, 0xA, 0xB,
         0xD, 0x1, 0x8, 0x5,
         0x6, 0x2, 0x0, 0x3,
         0xC, 0xE, 0xF, 0x7]

def text_to_state(text):
    return [[(text >> 12) & 0xF, (text >> 4) & 0xF],
            [(text >> 8) & 0xF, (text >> 0) & 0xF]]

def state_to_text(state):
    return (state[0][0] << 12) | (state[1][0] << 8) | (state[0][1] << 4) | (state[1][1])

def gf_mul(a, b):
    p = 0
    for _ in range(4):
        if b & 1:
            p ^= a
        carry = a & 0x8
        a <<= 1
        if carry:
            a ^= 0b10011
        b >>= 1
    return p & 0xF
