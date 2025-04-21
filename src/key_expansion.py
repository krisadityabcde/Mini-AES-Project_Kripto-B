from utils import s_box

def key_expansion(key):
    w = [0] * 6
    w[0] = (key >> 8) & 0xFF
    w[1] = key & 0xFF

    rcon1, rcon2 = 0x80, 0x30

    def sub_word(word):
        return ((s_box[(word >> 4) & 0xF] << 4) | s_box[word & 0xF])

    w[2] = w[0] ^ rcon1 ^ sub_word(w[1])
    w[3] = w[2] ^ w[1]
    w[4] = w[2] ^ rcon2 ^ sub_word(w[3])
    w[5] = w[4] ^ w[3]

    round_keys = [
        [[(w[0] >> 4) & 0xF, w[0] & 0xF], [(w[1] >> 4) & 0xF, w[1] & 0xF]],
        [[(w[2] >> 4) & 0xF, w[2] & 0xF], [(w[3] >> 4) & 0xF, w[3] & 0xF]],
        [[(w[4] >> 4) & 0xF, w[4] & 0xF], [(w[5] >> 4) & 0xF, w[5] & 0xF]],
    ]
    return round_keys
