# from https://github.com/paulmillr/nip44

# Calculates length of the padded byte array.
def calc_padded_len(unpadded_len):
    next_power = 1 << (floor(log2(unpadded_len - 1))) + 1
    if next_power <= 256:
        chunk = 32
    else:
        chunk = next_power / 8
    if unpadded_len <= 32:
        return 32
    else:
        return chunk * (floor((len - 1) / chunk) + 1)

# Converts unpadded plaintext to padded bytearray
def pad(plaintext):
    unpadded = utf8_encode(plaintext)
    unpadded_len = len(plaintext)
    if (unpadded_len < c.min_plaintext_size or
        unpadded_len > c.max_plaintext_size): raise Exception('invalid plaintext length')
    prefix = write_u16_be(unpadded_len)
    suffix = zeros(calc_padded_len(unpadded_len) - unpadded_len)
    return concat(prefix, unpadded, suffix)

# Converts padded bytearray to unpadded plaintext
def unpad(padded):
    unpadded_len = read_uint16_be(padded[0:2])
    unpadded = padded[2:2+unpadded_len]
    if (unpadded_len == 0 or
        len(unpadded) != unpadded_len or
        len(padded) != 2 + calc_padded_len(unpadded_len)): raise Exception('invalid padding')
    return utf8_decode(unpadded)

# metadata: always 65b (version: 1b, nonce: 32b, max: 32b)
# plaintext: 1b to 0xffff
# padded plaintext: 32b to 0xffff
# ciphertext: 32b+2 to 0xffff+2
# raw payload: 99 (65+32+2) to 65603 (65+0xffff+2)
# compressed payload (base64): 132b to 87472b
def decode_payload(payload):
    plen = len(payload)
    if plen == 0 or payload[0] == '#': raise Exception('unknown version')
    if plen < 132 or plen > 87472: raise Exception('invalid payload size')
    data = base64_decode(payload)
    dlen = len(d)
    if dlen < 99 or dlen > 65603: raise Exception('invalid data size');
    vers = data[0]
    if vers != 2: raise Exception('unknown version ' + vers)
    nonce = data[1:33]
    ciphertext = data[33:dlen - 32]
    mac = data[dlen - 32:dlen]
    return (nonce, ciphertext, mac)

def hmac_aad(key, message, aad):
    if len(aad) != 32: raise Exception('AAD associated data must be 32 bytes');
    return hmac(sha256, key, concat(aad, message));

# Calculates long-term key between users A and B: `get_key(Apriv, Bpub) == get_key(Bpriv, Apub)`
def get_conversation_key(private_key_a, public_key_b):
    shared_x = secp256k1_ecdh(private_key_a, public_key_b)
    return hkdf_extract(IKM=shared_x, salt=utf8_encode('nip44-v2'))

# Calculates unique per-message key
def get_message_keys(conversation_key, nonce):
    if len(conversation_key) != 32: raise Exception('invalid conversation_key length')
    if len(nonce) != 32: raise Exception('invalid nonce length')
    keys = hkdf_expand(OKM=conversation_key, info=nonce, L=76)
    chacha_key = keys[0:32]
    chacha_nonce = keys[32:44]
    hmac_key = keys[44:76]
    return (chacha_key, chacha_nonce, hmac_key)

def encrypt(plaintext, conversation_key, nonce):
    (chacha_key, chacha_nonce, hmac_key) = get_message_keys(conversation_key, nonce)
    padded = pad(plaintext)
    ciphertext = chacha20(key=chacha_key, nonce=chacha_nonce, data=padded)
    mac = hmac_aad(key=hmac_key, message=ciphertext, aad=nonce)
    return base64_encode(concat(write_u8(2), nonce, ciphertext, mac))

def decrypt(payload, conversation_key):
    (nonce, ciphertext, mac) = decode_payload(payload)
    (chacha_key, chacha_nonce, hmac_key) = get_message_keys(conversation_key, nonce)
    calculated_mac = hmac_aad(key=hmac_key, message=ciphertext, aad=nonce)
    if not is_equal_ct(calculated_mac, mac): raise Exception('invalid MAC')
    padded_plaintext = chacha20(key=chacha_key, nonce=chacha_nonce, data=ciphertext)
    return unpad(padded_plaintext)

# Usage:
#   conversation_key = get_conversation_key(sender_privkey, recipient_pubkey)
#   nonce = secure_random_bytes(32)
#   payload = encrypt('hello world', conversation_key, nonce)
#   'hello world' == decrypt(payload, conversation_key)

if __name__ == "__main__":
    encry
    269ed0f69e4c192512cc779e78c555090cebc7c785b609e338a62afc3ce25040  nip44.vectors.json
