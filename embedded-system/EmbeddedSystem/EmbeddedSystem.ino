#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <SoftwareSerial.h>
#include <ArduinoJson.h>

#include "AuthData.h"
#include "Crypto.h"

#define RESET_BUTTON D1
#define QR_RX D2
#define QR_TX D3
#define POWER_LED D5
#define WIFI_LED D6
#define SUCCESS_LED D7
#define FAIL_LED D8

/* ************************************************************************** */

// TODO: Change this keys
byte key[] = {"3EYFIc48AKz7GzlK"};
byte iv[] = {"GZTUlYH1Kcmcsopg"};
String qr_code_data = "";
String post_data = "";
char decrypted_data[DATA_SIZE] = {0};
char encrypted_data[2 * DATA_SIZE] = {0};
bool reset_button_status = false;
unsigned int reset_button_push_time = 0;

AuthData auth_data;
Crypto crypto(key, iv);
SoftwareSerial qr_code_reader(QR_RX, QR_TX);
StaticJsonDocument<256> request_json;
StaticJsonDocument<1024> response_json;

/* ************************************************************************** */

void reset_handler();

/* ************************************************************************** */

void setup()
{
    // For debugging
    Serial.begin(115200);
    Serial.println();
    Serial.println("Starting...");

    // Initialize the UART for the QR code reader
    qr_code_reader.begin(9600);

    // Initialize the GPIO pins
    pinMode(RESET_BUTTON, INPUT_PULLUP);
    pinMode(POWER_LED, OUTPUT);
    pinMode(WIFI_LED, OUTPUT);
    pinMode(SUCCESS_LED, OUTPUT);
    pinMode(FAIL_LED, OUTPUT);
    digitalWrite(POWER_LED, HIGH);
    digitalWrite(WIFI_LED, LOW);
    digitalWrite(SERVER_LED, LOW);
    digitalWrite(RELAY, LOW);

    // Set hardware interrupt for reset button
    attachInterrupt(digitalPinToInterrupt(RESET_BUTTON), reset_handler, CHANGE);

    // Auth data operations
    Serial.print("Saved: ");
    Serial.println(auth_data.is_saved());
    Serial.print("SSID: ");
    Serial.println(auth_data.get_ssid());
    Serial.print("Password: ");
    Serial.println(auth_data.get_password());
    Serial.print("Token: ");
    Serial.println(auth_data.get_token());
    Serial.print("URL: ");
    Serial.println(auth_data.get_url());

    if (auth_data.is_saved())
    {
        // Connect to WiFi
        WiFi.begin(auth_data.get_ssid(), auth_data.get_password());
        Serial.println("Connecting to WiFi...");
        while (WiFi.status() != WL_CONNECTED)
        {
            // Blink the WiFi LED
            digitalWrite(WIFI_LED, HIGH);
            delay(250);
            digitalWrite(WIFI_LED, LOW);
            delay(250);
        }
        digitalWrite(WIFI_LED, HIGH);
        Serial.println("WiFi connected!");
    }
    else
    {
        unsigned int timeout = 0;

        Serial.println("No saved data found. Please scan the QR code!");
        while (true)
        {
            if (qr_code_reader.available())
            {
                qr_code_data = qr_code_reader.readStringUntil('#');
                Serial.println(qr_code_data);

                strcpy(encrypted_data, qr_code_data.c_str());
                crypto.decrypt(encrypted_data, sizeof(encrypted_data), decrypted_data);

                auth_data.set(decrypted_data);
                Serial.print("Saved: ");
                Serial.println(auth_data.is_saved());
                Serial.print("SSID: ");
                Serial.println(auth_data.get_ssid());
                Serial.print("Password: ");
                Serial.println(auth_data.get_password());
                Serial.print("Token: ");
                Serial.println(auth_data.get_token());
                Serial.print("URL: ");
                Serial.println(auth_data.get_url());

                // Connect to WiFi
                WiFi.begin(auth_data.get_ssid(), auth_data.get_password());
                Serial.println("Connecting to WiFi...");
                while (timeout <= 10000 && WiFi.status() != WL_CONNECTED)
                {
                    digitalWrite(WIFI_LED, HIGH);
                    delay(250);
                    digitalWrite(WIFI_LED, LOW);
                    delay(250);
                    timeout += 500;
                }

                if (WiFi.status() == WL_CONNECTED)
                {
                    digitalWrite(WIFI_LED, HIGH);
                    Serial.println("WiFi connected!");
                    auth_data.write();
                    break;
                }
                else
                {
                    Serial.println("WiFi connection failed!");
                }
            }
        }
    }

    request_json["api_token"] = auth_data.get_token();
}

/* ************************************************************************** */

void loop()
{
    if (qr_code_reader.available())
    {
        qr_code_data = qr_code_reader.readStringUntil('#');
        qr_code_data.trim();
        if (qr_code_data.length() >= 8)
        {
            request_json["qr_code_data"] = qr_code_data;
        }
        else
        {
            return;
        }

        post_data = "";
        serializeJson(request_json, post_data);
        Serial.println(post_data);
        Serial.println();

        WiFiClient wifi_client;
        HTTPClient http_client;
        http_client.begin(wifi_client, auth_data.get_url());
        http_client.addHeader("Content-Type", "application/json");
        int http_code = http_client.POST(post_data);

        if (http_code > 0)
        {
            String response = http_client.getString();
            Serial.print("Response: ");
            Serial.println(response);

            DeserializationError error = deserializeJson(response_json, response);
            if (error)
            {
                Serial.print("Deserialization failed: ");
                Serial.println(error.f_str());
                http_client.end();
                return;
            }

            bool result = response_json["result"];
            if (result)
            {
                Serial.println("Entrance allowed!");
                digitalWrite(SUCCESS_LED, HIGH);
                delay(5000);
                digitalWrite(RELAY, LOW);
            }
            else
            {
                Serial.println("Entrance allowed!");
                digitalWrite(FAIL_LED, HIGH);
                delay(5000);
                digitalWrite(RELAY, LOW);
            }
        }
        http_client.end();
    }
}

/* ************************************************************************** */

void IRAM_ATTR reset_handler()
{
    unsigned int time_diff;

    Serial.println("Reset button pressed!");
    if (!reset_button_status)
    {
        if (digitalRead(RESET_BUTTON) == HIGH)
        {
            reset_button_status = true;
            reset_button_push_time = millis();
        }
    }
    else
    {
        if (digitalRead(RESET_BUTTON) == LOW)
        {
            time_diff = millis() - reset_button_push_time;
            reset_button_status = false;
            reset_button_push_time = 0;

            if (time_diff > 1000)
            {
                Serial.println("Disconnecting from WiFi...");
                WiFi.disconnect(true);
                digitalWrite(WIFI_LED, LOW);
                delay(2000);

                if (time_diff > 5000)
                {
                    Serial.println("Resetting auth data...");
                    auth_data.reset();
                    delay(1000);
                }

                Serial.println("Powering off...");
                digitalWrite(POWER_LED, LOW);
                delay(2000);
                ESP.reset();
            }
        }
    }
}
