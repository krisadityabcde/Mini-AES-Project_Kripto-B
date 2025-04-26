from utils import text_to_state, state_to_text, chars_to_16bit, bit16_to_chars, bit16_to_hex
from aes_core import sub_nibbles, shift_rows, mix_columns, add_round_key, inv_sub_nibbles, inv_shift_rows, inv_mix_columns
from key_expansion import key_expansion

def encrypt(plaintext_16bit, key_16bit):
    state = text_to_state(plaintext_16bit)
    round_keys = key_expansion(key_16bit)

    logs = []
    logs.append(f"Initial State: {state}")

    # Round 0
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

    ciphertext_16bit = state_to_text(state)
    logs.append(f"Ciphertext (16-bit): {ciphertext_16bit} (0x{bit16_to_hex(ciphertext_16bit)})")

    return ciphertext_16bit, logs

def decrypt(ciphertext_16bit, key_16bit):
    state = text_to_state(ciphertext_16bit)
    round_keys = key_expansion(key_16bit)

    logs = []
    logs.append(f"Ciphertext Input: {state}")

    # Round 2
    state = add_round_key(state, round_keys[2])
    logs.append(f"After AddRoundKey (Round 2): {state}")

    state = inv_shift_rows(state)
    logs.append(f"After InvShiftRows (Round 2): {state}")

    state = inv_sub_nibbles(state)
    logs.append(f"After InvSubNibbles (Round 2): {state}")

    # Round 1
    state = add_round_key(state, round_keys[1])
    logs.append(f"After AddRoundKey (Round 1): {state}")

    state = inv_mix_columns(state)
    logs.append(f"After InvMixColumns (Round 1): {state}")

    state = inv_shift_rows(state)
    logs.append(f"After InvShiftRows (Round 1): {state}")

    state = inv_sub_nibbles(state)
    logs.append(f"After InvSubNibbles (Round 1): {state}")

    # Round 0
    state = add_round_key(state, round_keys[0])
    logs.append(f"After AddRoundKey (Round 0): {state}")

    plaintext_16bit = state_to_text(state)
    logs.append(f"Plaintext (16-bit): {plaintext_16bit} (0x{bit16_to_hex(plaintext_16bit)})")
    logs.append(f"Plaintext (ASCII): {bit16_to_chars(plaintext_16bit)}")

    return plaintext_16bit, logs

if __name__ == "__main__":
    print("=== Mini-AES 16-bit CLI ===\n")
    input_mode = input("Pilih Mode (e = Encrypt, d = Decrypt): ").lower()

    if input_mode not in ['e', 'd']:
        print("Mode tidak valid! Harus 'e' untuk Encrypt atau 'd' untuk Decrypt.")
        exit()

    input_text = input("Masukkan teks (2 karakter): ")
    key_text = input("Masukkan key (2 karakter): ")

    try:
        input_16bit = chars_to_16bit(input_text)
        key_16bit = chars_to_16bit(key_text)

        if input_mode == 'e':
            # Encrypt
            ciphertext, encrypt_logs = encrypt(input_16bit, key_16bit)
            print("\n=== HASIL ENKRIPSI ===")
            print(f"Plaintext: '{input_text}' (0x{bit16_to_hex(input_16bit)})")
            print(f"Key: '{key_text}' (0x{bit16_to_hex(key_16bit)})")
            print(f"Ciphertext: '{bit16_to_chars(ciphertext)}' (0x{bit16_to_hex(ciphertext)})")

            print("\n--- Detail Proses Enkripsi ---")
            for log in encrypt_logs:
                print(log)

        else:
            # Decrypt
            plaintext, decrypt_logs = decrypt(input_16bit, key_16bit)
            print("\n=== HASIL DEKRIPSI ===")
            print(f"Ciphertext: '{input_text}' (0x{bit16_to_hex(input_16bit)})")
            print(f"Key: '{key_text}' (0x{bit16_to_hex(key_16bit)})")
            print(f"Plaintext: '{bit16_to_chars(plaintext)}' (0x{bit16_to_hex(plaintext)})")

            print("\n--- Detail Proses Dekripsi ---")
            for log in decrypt_logs:
                print(log)

    except ValueError as e:
        print("Error:", e)