#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "SESI ALUNOS";
const char* password = "SESI@21032024";

String servidor = "http://172.16.20.113:5000"; // IP do Flask

int ledPin = 13;       // LED
int sensorUmidade = 33; // Pino analógico do sensor de umidade

void setup() {
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT);
  pinMode(sensorUmidade, INPUT);

  Serial.println("🚀 Inicializando ESP32...");
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\n✅ Conectado ao Wi-Fi!");
  Serial.print("📡 IP da ESP32: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {

    // ----------- LÊ O SENSOR DE UMIDADE -----------
    int leituraBruta = analogRead(sensorUmidade);
    int umidadePercentual = map(leituraBruta, 0, 4095, 0, 100);
    Serial.printf("🌱 Umidade do solo: %d%%\n", umidadePercentual);

    // ----------- ENVIA UMIDADE AO SERVIDOR (GET) -----------
    String urlUmidade = servidor + "/umidade?valor=" + String(umidadePercentual);
    HTTPClient http1;
    http1.begin(urlUmidade);
    int httpCode1 = http1.GET();

    if (httpCode1 > 0) {
      Serial.printf("📤 Umidade enviada! Código HTTP: %d\n", httpCode1);
      Serial.println(http1.getString());
    } else {
      Serial.printf("⚠️ Erro ao enviar umidade: %d\n", httpCode1);
    }
    http1.end();

    // ----------- PEGA STATUS DO LED -----------
    String urlLed = servidor + "/led/status";
    HTTPClient http2;
    http2.begin(urlLed);
    int httpCode2 = http2.GET();

    if (httpCode2 > 0) {
      String resposta = http2.getString();
      bool ledStatus = false;

      // Verifica se servidor respondeu "true" ou "false"
      if (resposta.indexOf("true") >= 0) {
        ledStatus = true;
        digitalWrite(ledPin, HIGH);
      } else {
        digitalWrite(ledPin, LOW);
      }

      Serial.printf("💡 LED está %s\n", ledStatus ? "LIGADO" : "DESLIGADO");
    } else {
      Serial.printf("⚠️ Erro ao ler LED: %d\n", httpCode2);
    }
    http2.end();
  }

  delay(2000); // atualiza a cada 2s
}
