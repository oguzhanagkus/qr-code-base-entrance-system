#include <HardwareSerial.h>

#ifndef AUTH_DATA_H
#define AUTH_DATA_H

#define AUTH_DATA_SIZE 256 + 4

class AuthData
{
public:
    AuthData();

    void read();
    bool write();
    bool reset();
    bool is_saved();

    char *get_ssid();
    char *get_password();
    char *get_token();
    char *get_url();

    void set(char *new_data);
    void set(char *ssid, char *password, char *token, char *url);

private:
    struct data_struct
    {
        char ssid[32 + 1];
        char password[64 + 1];
        char token[96 + 1];
        char url[64 + 1];
    };

    struct data_struct data;
};

#endif // AUTH_DATA_H
