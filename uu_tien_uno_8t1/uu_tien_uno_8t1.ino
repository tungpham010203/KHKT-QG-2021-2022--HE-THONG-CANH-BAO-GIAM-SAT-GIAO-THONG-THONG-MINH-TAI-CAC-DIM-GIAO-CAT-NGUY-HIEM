float ham_coxe();
float nhayvang();
float sang_vang_3s();
#define vang  13
#define coxe 12
#define den_do  11
#define coi 10
#define xin_duong 8
#define tin_hieu_mega 7
float time_den_do_bat;
float time_den_vang_bat=-48000;
bool den_vang_bat;
float velocity,timetatden,timetatden2;
float s = 0.067;  ///m
float a=1;
void setup()
{  
    Serial.begin(115200);
    Serial.setTimeout(1);
    pinMode(vang, OUTPUT);
    pinMode(coxe, OUTPUT);
    pinMode(den_do, OUTPUT);
    pinMode(tin_hieu_mega, OUTPUT);
    pinMode(coi, OUTPUT);
    pinMode(xin_duong, INPUT);
    
    digitalWrite(coi,1);
    digitalWrite(vang,1);
    digitalWrite(coxe,1);
    digitalWrite(den_do,1);
    //digitalWrite(den_do,0);
    den_vang_bat = !true;
}
float ham_coxe()
{   float timexedi;
    digitalWrite(coxe,0);
    timexedi=s/velocity;
    timetatden=(timexedi*60*60*1000)+millis();
    if(timetatden>=timetatden2)
        {
            timetatden2=timetatden;
        }
    else
        {
            timetatden=timetatden2;
        }
}
float nhayvang()
{
        if (millis()-a>600)
      {
       if (digitalRead(vang)==LOW)
          {
              digitalWrite(vang,HIGH);
          }
       else if (digitalRead(vang)==HIGH && digitalRead(coxe)==HIGH&& digitalRead(den_do)==HIGH )
          {
              digitalWrite(vang,LOW);  
          }
       a = millis();
       } 
}
float sang_vang_3s()
{
        den_vang_bat = true;
        digitalWrite(vang,LOW);
        time_den_vang_bat=millis(); 
}
void loop()
{ 
     if(Serial.available())  
              {
              velocity = Serial.readString().toInt();
              if (velocity>0)
                 {
                 digitalWrite(vang,1);
                 if(velocity>50){digitalWrite(coi,0);}
                 ham_coxe();
                 }
              }
     //khi ko có xe
     else if (den_vang_bat==!true) // nháy vàng
              {
              nhayvang();
              }
     
     if (millis()-timetatden>0) //tắt đèn báo "có xe"
              {
              digitalWrite(coxe,1);
              digitalWrite(coi,1);
              }


     if(digitalRead(vang)==LOW && den_vang_bat==true && millis()-time_den_vang_bat>3000) // bật đèn đỏ ( xin đường )
              {
              time_den_do_bat=millis();// tính time đèn đỏ bắt đầu được bật
              digitalWrite(vang,1);//off vàng
              digitalWrite(den_do,0);//on đỏ
              digitalWrite(tin_hieu_mega,1);
              den_vang_bat=!true; 
              }

     if( millis()-time_den_do_bat>=15000)
              {
              digitalWrite(den_do,1);
              digitalWrite(tin_hieu_mega,0);
              
              }
     if(digitalRead(xin_duong)==HIGH && digitalRead(den_do)==HIGH && millis()-time_den_vang_bat>=33000)
              {
               sang_vang_3s();
              }
}
 
        
