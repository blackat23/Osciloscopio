int pot = 0;

void setup() {
  pinMode(2, OUTPUT); //Bit0
  pinMode(3, OUTPUT); //Bit1
  pinMode(4, OUTPUT); //Bit2
  pinMode(5, OUTPUT); //Bit3
  pinMode(6, OUTPUT); //Bit4
  pinMode(7, OUTPUT); //Bit5
  pinMode(8, OUTPUT); //Bit6
  pinMode(9, OUTPUT); //Bit7
  Serial.begin(115200);
  Serial.setTimeout(100);  // Establece un timeout de 100 ms para la lectura de datos serial
}

void loop() {
  if (Serial.available() > 0) {
    String dato = Serial.readStringUntil('\n'); // Leer hasta el salto de línea
    pot = dato.toInt();  // Convertir el dato leído a un entero
    
    if(pot < 0) {
      pot = 0;
    }

    // Imprimir el valor recibido para verificar
    Serial.print("Valor recibido: ");
    Serial.println(pot);
    
    // Procesar el valor 'pot'
    for (int i = 0; i < 8; i++) {
      digitalWrite(i + 2, pot % 2);
      pot = pot / 2;
    }

    delay(5);  // Agregar un pequeño delay de 5 ms para asegurar el procesamiento
  }
}