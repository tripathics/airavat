/**
 *  Airavat
 *  Created: 11/2/2022
**/

#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>
#include <ESP8266HTTPClient.h>

void update_location(), register_network();

ESP8266WiFiMulti wifi_multi;
#define BUS_ID "1"
#define API_KEY "qazsevaqpoi123,azxcv42afpiweqf~faefalkj123"
#define DOMAIN "http://192.168.137.58:5000"

int network_id = -1;
const int n_places = 3;

const char *AP[][2] = {
    {"Hostel", "1234567890"},
    {"Acad", "1234567890"},
    {"Library", "1234567890"},
};

uint16_t connectTimeOutPerAP = 5000;

void setup()
{
    Serial.begin(115200);
    delay(100);
    Serial.println();

    for (int i = 0; i < n_places; i++)
        wifi_multi.addAP(AP[i][0], AP[i][1]);

    register_network();
}

void loop()
{
    if (wifi_multi.run() == WL_CONNECTED)
    {
        Serial.print("Current network: ");
        Serial.println(WiFi.SSID());
        // set network id
        for (int i = 0; i < n_places; i++)
        {
            if (WiFi.SSID() == AP[i][0])
            {
                network_id = i;
                break;
            }
        }
        // update location
        update_location();
    }
    else
        register_network();

    delay(10000);
}

void update_location()
{
    WiFiClient client;
    HTTPClient http;

    String get_url = DOMAIN;
    get_url += "/tracker_update?api_key=";
    get_url += API_KEY;
    get_url += "&id=";
    get_url += BUS_ID;
    get_url += "&location=";
    get_url += network_id;

    Serial.print("[HTTP] begin...\n");
    Serial.print(get_url);

    if (http.begin(client, get_url))
    {
        // HTTP
        Serial.print("[HTTP] GET...\n");
        // start connection and send HTTP header
        int httpCode = http.GET();

        // httpCode will be negative on error
        if (httpCode > 0)
        {
            // HTTP header has been send and Server response header has been handled
            Serial.print("[HTTP] GET... code: ");
            Serial.println(httpCode);

            // file found at server
            if (httpCode == HTTP_CODE_OK || httpCode == HTTP_CODE_MOVED_PERMANENTLY)
            {
                String payload = http.getString();
                Serial.println(payload);
            }
        }
        else
        {
            Serial.print("[HTTP] GET... failed, error: ");
            Serial.println(http.errorToString(httpCode).c_str());
        }
        http.end();
    }
    else
        Serial.println("[HTTP} Unable to connect");
    Serial.println();
}

void register_network()
{
    Serial.print("Connecting to Wi-Fi...");
    while (wifi_multi.run(connectTimeOutPerAP) != WL_CONNECTED)
    {
        Serial.print(".");
        delay(1000);
    }
    Serial.println();
    Serial.print("Connected to ");
    Serial.println(WiFi.SSID());
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());
}
