from utils import s_box, inv_s_box, gf_mul

def sub_nibbles(state):
    return [[s_box[nibble] for nibble in row] for row in state]

def shift_rows(state):
    state[1][0], state[1][1] = state[1][1], state[1][0]
    return state

def mix_columns(state):
    a, b = state[0][0], state[1][0]
    c, d = state[0][1], state[1][1]
    return [
        [a ^ gf_mul(4, b), c ^ gf_mul(4, d)],
        [gf_mul(4, a) ^ b, gf_mul(4, c) ^ d]
    ]

def add_round_key(state, key):
    return [[state[i][j] ^ key[i][j] for j in range(2)] for i in range(2)]

def inv_sub_nibbles(state):
    return [[inv_s_box[nibble] for nibble in row] for row in state]

def inv_shift_rows(state):
    # Tukar posisi baris ke-2 (kembalikan pertukaran)
    state[1][0], state[1][1] = state[1][1], state[1][0]
    return state

def inv_mix_columns(state):
    a, b = state[0][0], state[1][0]
    c, d = state[0][1], state[1][1]
    return [
        [gf_mul(9, a) ^ gf_mul(2, b), gf_mul(9, c) ^ gf_mul(2, d)],
        [gf_mul(2, a) ^ gf_mul(9, b), gf_mul(2, c) ^ gf_mul(9, d)]
    ]