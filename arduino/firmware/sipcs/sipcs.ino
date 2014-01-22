int pins[] = {0,1,2,3,4,5,6,7,8,9,10,11,12};

void setup()
{
 Serial.begin(9600);
 for (int i=0;i<(sizeof(pins)/sizeof(pins[0]));i++)
 {
   pinMode(pins[i], OUTPUT);
 } 
 
 digitalWrite (13, HIGH);
 Serial.println ("SIPCS READY");
}

void loop()
{
  if (Serial.available())
  {
      char pin = Serial.read();
      
      if (pin>100)
      {
        digitalWrite (pin-101, HIGH);
      }
      
      if (pin<100)
      {
        digitalWrite (pin-51, LOW);
      }
      
      for (int i=0;i<(sizeof(pins)/sizeof(pins[0]));i++)
      {
       int mode = digitalRead (pins[i]);
       
       if (mode == HIGH){ Serial.write (i+101);}
       if (mode == LOW){ Serial.write (i+51);}
      }
      
      Serial.write ('\n');
  }
  delay (20);
}
