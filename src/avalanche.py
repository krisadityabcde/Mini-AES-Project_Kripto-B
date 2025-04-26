from utils import text_to_state, state_to_text, chars_to_16bit, bit16_to_chars, bit16_to_hex, bit16_to_binary
from main import encrypt

def count_bit_differences(a, b):
    """Count how many bits differ between two 16-bit values."""
    xor_result = a ^ b
    binary = bin(xor_result)[2:].zfill(16)
    return binary.count('1')

def analyze_plaintext_avalanche(plaintext, key, bit_position):
    """Analyze avalanche effect by flipping a single bit in plaintext."""
    # Original encryption
    plaintext_16bit = chars_to_16bit(plaintext)
    key_16bit = chars_to_16bit(key)
    original_cipher, _ = encrypt(plaintext_16bit, key_16bit)
    
    # Flip the specified bit
    modified_16bit = plaintext_16bit ^ (1 << bit_position)
    modified_plaintext = bit16_to_chars(modified_16bit)
    modified_cipher, _ = encrypt(modified_16bit, key_16bit)
    
    # Calculate bit differences
    bits_changed = count_bit_differences(original_cipher, modified_cipher)
    percentage = (bits_changed / 16) * 100
    
    # Analysis results
    results = {
        "original_plaintext": plaintext,
        "original_plaintext_binary": bit16_to_binary(plaintext_16bit),
        "modified_plaintext": modified_plaintext,
        "modified_plaintext_binary": bit16_to_binary(modified_16bit),
        "original_cipher_hex": bit16_to_hex(original_cipher),
        "modified_cipher_hex": bit16_to_hex(modified_cipher),
        "original_cipher_binary": bit16_to_binary(original_cipher),
        "modified_cipher_binary": bit16_to_binary(modified_cipher),
        "bits_changed": bits_changed,
        "total_bits": 16,
        "change_percentage": percentage,
        "bit_position_flipped": bit_position
    }
    
    return results

def analyze_key_avalanche(plaintext, key, bit_position):
    """Analyze avalanche effect by flipping a single bit in key."""
    # Original encryption
    plaintext_16bit = chars_to_16bit(plaintext)
    key_16bit = chars_to_16bit(key)
    original_cipher, _ = encrypt(plaintext_16bit, key_16bit)
    
    # Flip the specified bit
    modified_key_16bit = key_16bit ^ (1 << bit_position)
    modified_key = bit16_to_chars(modified_key_16bit)
    modified_cipher, _ = encrypt(plaintext_16bit, modified_key_16bit)
    
    # Calculate bit differences
    bits_changed = count_bit_differences(original_cipher, modified_cipher)
    percentage = (bits_changed / 16) * 100
    
    # Analysis results
    results = {
        "plaintext": plaintext,
        "original_key": key,
        "original_key_binary": bit16_to_binary(key_16bit),
        "modified_key": modified_key,
        "modified_key_binary": bit16_to_binary(modified_key_16bit),
        "original_cipher_hex": bit16_to_hex(original_cipher),
        "modified_cipher_hex": bit16_to_hex(modified_cipher),
        "original_cipher_binary": bit16_to_binary(original_cipher),
        "modified_cipher_binary": bit16_to_binary(modified_cipher),
        "bits_changed": bits_changed,
        "total_bits": 16,
        "change_percentage": percentage,
        "bit_position_flipped": bit_position
    }
    
    return results

def full_avalanche_analysis(plaintext, key):
    """Perform a full avalanche analysis for all bits in plaintext and key."""
    pt_results = []
    key_results = []
    
    # Test flipping each bit in plaintext
    for bit in range(16):
        pt_results.append(analyze_plaintext_avalanche(plaintext, key, bit))
    
    # Test flipping each bit in key
    for bit in range(16):
        key_results.append(analyze_key_avalanche(plaintext, key, bit))
    
    # Calculate averages
    pt_avg_bits = sum(r["bits_changed"] for r in pt_results) / len(pt_results)
    pt_avg_percentage = sum(r["change_percentage"] for r in pt_results) / len(pt_results)
    
    key_avg_bits = sum(r["bits_changed"] for r in key_results) / len(key_results)
    key_avg_percentage = sum(r["change_percentage"] for r in key_results) / len(key_results)
    
    summary = {
        "plaintext_avg_bits_changed": pt_avg_bits,
        "plaintext_avg_percentage": pt_avg_percentage,
        "key_avg_bits_changed": key_avg_bits,
        "key_avg_percentage": key_avg_percentage,
        "plaintext_results": pt_results,
        "key_results": key_results
    }
    
    return summary