# src/main.py

from utils import text_to_state, state_to_text
from aes_core import sub_nibbles, shift_rows, mix_columns, add_round_key
from key_expansion import key_expansion

def encrypt(plaintext, key):
    state = text_to_state(plaintext)
    round_keys = key_expansion(key)

    print("Initial State:", state)

    # Round 0
    state = add_round_key(state, round_keys[0])
    print("After AddRoundKey (Round 0):", state)

    # Round 1
    state = sub_nibbles(state)
    state = shift_rows(state)
    state = mix_columns(state)
    state = add_round_key(state, round_keys[1])
    print("After Round 1:", state)

    # Round 2
    state = sub_nibbles(state)
    state = shift_rows(state)
    state = add_round_key(state, round_keys[2])
    print("After Round 2 (Final):", state)

    return state_to_text(state)

def ascii_to_16bit(text):
    if len(text) != 2:
        raise ValueError("Input harus 2 karakter ASCII (16-bit total).")
    return (ord(text[0]) << 8) | ord(text[1])

def bit16_to_ascii(val):
    return chr((val >> 8) & 0xFF) + chr(val & 0xFF)

if __name__ == "__main__":
    plaintext_ascii = input("Masukkan plaintext (2 karakter ASCII): ")
    key_ascii = input("Masukkan key (2 karakter ASCII): ")

    try:
        plaintext = ascii_to_16bit(plaintext_ascii)
        key = ascii_to_16bit(key_ascii)

        ciphertext = encrypt(plaintext, key)

        print(f"\nPlaintext (hex): {plaintext:04X}")
        print(f"Key       (hex): {key:04X}")
        print(f"Ciphertext (hex): {ciphertext:04X}")
        print(f"Ciphertext (ASCII): {bit16_to_ascii(ciphertext)}")
        
    except ValueError as e:
        print("Error:", e)

