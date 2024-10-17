// Definir el pin al que está conectado el potenciómetro
int potPin = 0; // Pin analógico A0

void setup() {
  // Iniciar la comunicación serial a 9600 bps
  Serial.begin(115200);
}

void loop() {
  // Leer el valor analógico del potenciómetro (0 a 1023)
  potPin = analogRead(A0);

  // Imprimir el valor en el monitor serial

  Serial.println(potPin);

  // Pausar un poco para no saturar el monitor serial
  delay(20); // 500 ms de pausa
}
