s_box = [0x9, 0x4, 0xA, 0xB,
         0xD, 0x1, 0x8, 0x5,
         0x6, 0x2, 0x0, 0x3,
         0xC, 0xE, 0xF, 0x7]

# Inverse S-Box
inv_s_box = [0xA, 0x5, 0x9, 0xB,
             0x1, 0x7, 0x8, 0xF,
             0x6, 0x0, 0x2, 0x3,
             0xC, 0x4, 0xD, 0xE]

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

def chars_to_16bit(text):
    """Convert a 2-character string to 16-bit value (8 bits per character)."""
    if len(text) != 2:
        raise ValueError("Input harus 2 karakter.")
    return (ord(text[0]) << 8) | ord(text[1])

def bit16_to_chars(val):
    """Convert a 16-bit value back to 2 characters."""
    return chr((val >> 8) & 0xFF) + chr(val & 0xFF)

# Format conversion functions for display purposes
def bit16_to_hex(val):
    """Convert 16-bit value to hex string."""
    return f"{val:04X}"

def bit16_to_decimal(val):
    """Convert 16-bit value to decimal string."""
    return str(val)

def bit16_to_binary(val):
    """Convert 16-bit value to binary string."""
    return f"{val:016b}"