from utils import s_box, gf_mul

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
