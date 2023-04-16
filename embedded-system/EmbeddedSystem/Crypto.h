#include "AESLib.h"

#ifndef CRYPTO_H
#define CRYPTO_H

#define KEY_SIZE 16
#define BLOCK_SIZE 16
#define DATA_SIZE 256 + 4

class Crypto
{
public:
    Crypto(byte *key, byte *iv);

    uint16_t encrypt(char *plain_text, uint16_t plain_text_size, char *cipher_text);
    uint16_t decrypt(char *cipher_text, uint16_t cipher_text_size, char *plain_text);

private:
    AESLib aes;

    byte key[KEY_SIZE];
    byte iv[BLOCK_SIZE];
    byte iv_[BLOCK_SIZE];
};

#endif // CRYPTO_H
