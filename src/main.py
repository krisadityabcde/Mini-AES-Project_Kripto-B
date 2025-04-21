from utils import text_to_state, state_to_text, chars_to_16bit, bit16_to_chars, bit16_to_hex
from aes_core import sub_nibbles, shift_rows, mix_columns, add_round_key
from key_expansion import key_expansion

def encrypt(plaintext, key):
    state = text_to_state(plaintext)
    round_keys = key_expansion(key)

    logs = []
    logs.append(f"Initial State: {state}")

    # Round 0 - AddRoundKey
    state = add_round_key(state, round_keys[0])
    logs.append(f"After AddRoundKey (Round 0): {state}")

    # Round 1
    state = sub_nibbles(state)
    logs.append(f"After SubNibbles (Round 1): {state}")

    state = shift_rows(state)
    logs.append(f"After ShiftRows (Round 1): {state}")

    state = mix_columns(state)
    logs.append(f"After MixColumns (Round 1): {state}")

    state = add_round_key(state, round_keys[1])
    logs.append(f"After AddRoundKey (Round 1): {state}")

    # Round 2 (Final Round)
    state = sub_nibbles(state)
    logs.append(f"After SubNibbles (Round 2): {state}")

    state = shift_rows(state)
    logs.append(f"After ShiftRows (Round 2): {state}")

    state = add_round_key(state, round_keys[2])
    logs.append(f"After AddRoundKey (Round 2): {state}")

    ciphertext = state_to_text(state)
    logs.append(f"Ciphertext (16-bit): {ciphertext} (0x{bit16_to_hex(ciphertext)})")

    return ciphertext, logs


if __name__ == "__main__":
    plaintext_chars = input("Masukkan plaintext (2 karakter): ")
    key_chars = input("Masukkan key (2 karakter): ")

    try:
        plaintext = chars_to_16bit(plaintext_chars)
        key = chars_to_16bit(key_chars)

        ciphertext, _ = encrypt(plaintext, key)

        print(f"\nPlaintext (chars): {plaintext_chars}")
        print(f"Plaintext (16-bit): {plaintext} (0x{plaintext:04X})")
        print(f"Key (chars): {key_chars}")
        print(f"Key (16-bit): {key} (0x{key:04X})")
        print(f"Ciphertext (16-bit): {ciphertext} (0x{ciphertext:04X})")
        print(f"Ciphertext (chars): {bit16_to_chars(ciphertext)}")
        
    except ValueError as e:
        print("Error:", e)

