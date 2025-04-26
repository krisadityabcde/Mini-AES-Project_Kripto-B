from utils import text_to_state, state_to_text, chars_to_16bit, bit16_to_chars
from main import encrypt, decrypt
import random

def pad_text(text):
    """Pad the text to ensure it's a multiple of 2 characters (16-bit blocks)."""
    if len(text) % 2 == 0:
        return text
    else:
        return text + ' '  # Pad with a space

def split_to_blocks(text):
    """Split text into 16-bit (2 character) blocks."""
    blocks = []
    padded = pad_text(text)
    
    for i in range(0, len(padded), 2):
        block = padded[i:i+2]
        blocks.append(block)
    
    return blocks

def ecb_encrypt(plaintext, key):
    """ECB mode encryption: each block is encrypted independently."""
    blocks = split_to_blocks(plaintext)
    key_16bit = chars_to_16bit(key[:2])  # Use first 2 chars as key
    
    ciphertext_blocks = []
    logs = []
    
    for i, block in enumerate(blocks):
        logs.append(f"\n=== Processing Block {i+1}: '{block}' ===")
        block_16bit = chars_to_16bit(block)
        cipher_16bit, block_logs = encrypt(block_16bit, key_16bit)
        logs.extend(block_logs)
        ciphertext_blocks.append(bit16_to_chars(cipher_16bit))
    
    return ''.join(ciphertext_blocks), logs

def ecb_decrypt(ciphertext, key):
    """ECB mode decryption: each block is decrypted independently."""
    blocks = split_to_blocks(ciphertext)
    key_16bit = chars_to_16bit(key[:2])  # Use first 2 chars as key
    
    plaintext_blocks = []
    logs = []
    
    for i, block in enumerate(blocks):
        logs.append(f"\n=== Processing Block {i+1}: '{block}' ===")
        block_16bit = chars_to_16bit(block)
        plain_16bit, block_logs = decrypt(block_16bit, key_16bit)
        logs.extend(block_logs)
        plaintext_blocks.append(bit16_to_chars(plain_16bit))
    
    return ''.join(plaintext_blocks), logs

def generate_iv():
    """Generate a random 16-bit IV and return as 2 characters."""
    iv_value = random.randint(0, 65535)  # 0 to 2^16-1
    return bit16_to_chars(iv_value)

def cbc_encrypt(plaintext, key, iv=None):
    """CBC mode encryption: each block is XORed with previous ciphertext before encryption."""
    blocks = split_to_blocks(plaintext)
    key_16bit = chars_to_16bit(key[:2])  # Use first 2 chars as key
    
    # Generate IV if not provided
    if iv is None:
        iv = generate_iv()
    
    iv_16bit = chars_to_16bit(iv)
    previous_block = iv_16bit
    
    ciphertext_blocks = []
    logs = []
    logs.append(f"\n=== Using IV: '{iv}' (0x{iv_16bit:04X}) ===")
    
    for i, block in enumerate(blocks):
        logs.append(f"\n=== Processing Block {i+1}: '{block}' ===")
        block_16bit = chars_to_16bit(block)
        
        # XOR with previous ciphertext/IV
        xored_block = block_16bit ^ previous_block
        logs.append(f"XOR with previous: {block_16bit} ^ {previous_block} = {xored_block}")
        
        cipher_16bit, block_logs = encrypt(xored_block, key_16bit)
        logs.extend(block_logs)
        
        ciphertext_blocks.append(bit16_to_chars(cipher_16bit))
        previous_block = cipher_16bit
    
    # Return ciphertext with IV prepended
    return iv + ''.join(ciphertext_blocks), logs

def cbc_decrypt(ciphertext, key):
    """CBC mode decryption: each decrypted block is XORed with previous ciphertext."""
    if len(ciphertext) < 2:
        raise ValueError("CBC ciphertext must include IV (at least 2 characters)")
    
    # Extract IV and actual ciphertext
    iv = ciphertext[:2]
    actual_ciphertext = ciphertext[2:]
    
    blocks = split_to_blocks(actual_ciphertext)
    key_16bit = chars_to_16bit(key[:2])  # Use first 2 chars as key
    
    iv_16bit = chars_to_16bit(iv)
    previous_block = iv_16bit
    
    plaintext_blocks = []
    logs = []
    logs.append(f"\n=== Using IV: '{iv}' (0x{iv_16bit:04X}) ===")
    
    for i, block in enumerate(blocks):
        logs.append(f"\n=== Processing Block {i+1}: '{block}' ===")
        block_16bit = chars_to_16bit(block)
        
        # Decrypt block
        decrypted_16bit, block_logs = decrypt(block_16bit, key_16bit)
        logs.extend(block_logs)
        
        # XOR with previous ciphertext/IV
        plaintext_16bit = decrypted_16bit ^ previous_block
        logs.append(f"XOR with previous: {decrypted_16bit} ^ {previous_block} = {plaintext_16bit}")
        
        plaintext_blocks.append(bit16_to_chars(plaintext_16bit))
        previous_block = block_16bit
    
    return ''.join(plaintext_blocks), logs