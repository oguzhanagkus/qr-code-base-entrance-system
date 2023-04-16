#include <EEPROM.h>

#include "AuthData.h"

AuthData::AuthData()
{
    EEPROM.begin(AUTH_DATA_SIZE);
    read();
}

void AuthData::read()
{
    EEPROM.get(0, data);
}

bool AuthData::write()
{
    EEPROM.put(0, data);
    return EEPROM.commit();
}

bool AuthData::reset()
{
    char temp[AUTH_DATA_SIZE] = {0x00};

    EEPROM.put(0, temp);
    return EEPROM.commit();
}

bool AuthData::is_saved()
{
    return strlen(data.ssid) > 0;
}

char *AuthData::get_ssid()
{
    return data.ssid;
}

char *AuthData::get_password()
{
    return data.password;
}

char *AuthData::get_token()
{
    return data.token;
}

char *AuthData::get_url()
{
    return data.url;
}

void AuthData::set(char *data)
{
    if (strlen(data) > AUTH_DATA_SIZE)
    {
        return;
    }
    memcpy(&this->data, data, AUTH_DATA_SIZE);
}

void AuthData::set(char *ssid, char *password, char *token, char *url)
{
    strcpy(data.ssid, ssid);
    strcpy(data.password, password);
    strcpy(data.token, token);
    strcpy(data.url, url);
}
