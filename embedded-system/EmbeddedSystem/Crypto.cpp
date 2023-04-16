#include "Crypto.h"

Crypto::Crypto(byte *key, byte *iv)
{
    memcpy(this->key, key, KEY_SIZE);
    memcpy(this->iv, iv, BLOCK_SIZE);

    aes.set_paddingmode((paddingMode)0);
}

uint16_t Crypto::encrypt(char *plain_text, uint16_t plain_text_size, char *cipher_text)
{
    memcpy(iv_, iv, BLOCK_SIZE);
    return aes.encrypt((byte *)plain_text, plain_text_size, cipher_text, key, KEY_SIZE, iv_);
}

uint16_t Crypto::decrypt(char *cipher_text, uint16_t cipher_text_size, char *plain_text)
{
    char base64_decoded[2 * DATA_SIZE] = {0};
    int size = base64_decode(base64_decoded, cipher_text, cipher_text_size);

    memcpy(iv_, iv, BLOCK_SIZE);
    return aes.decrypt((byte *)base64_decoded, size, plain_text, key, KEY_SIZE, iv_);
}
