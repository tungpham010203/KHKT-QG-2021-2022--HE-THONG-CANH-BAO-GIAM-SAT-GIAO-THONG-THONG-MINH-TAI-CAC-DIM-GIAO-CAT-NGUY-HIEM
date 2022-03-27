float ham_coxe();
float nhayvang();
#define vang  13
#define coxe 12
#define den_do  11
#define coi 10
#define xin_duong 8
float time_den_do_bat;
float time_den_vang_bat=-48000;
bool den_vang_bat = !true;
bool dung =!true;
float velocity,timetatden,timetatden2;
float s = 0.13;  ///m
float a=1;
float one_giay=1;
int dem_xe=1;
void setup()
{  
    Serial.begin(115200);
    Serial.setTimeout(1);
    pinMode(vang, OUTPUT);
    pinMode(coxe, OUTPUT);
    pinMode(den_do, OUTPUT);
    pinMode(coi, OUTPUT);
    pinMode(xin_duong, INPUT);
    digitalWrite(coi,1);
    digitalWrite(vang,1);
    digitalWrite(coxe,1);
    digitalWrite(den_do,1);
}


float ham_coxe()
{   float timexedi;
    digitalWrite(coxe,0);
    timexedi=s/velocity;
    timetatden=(timexedi*60*60*1000)+millis();     
    //return timetatden;
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

void loop()
{ 
     if(Serial.available())  
              {
              velocity = Serial.readString().toInt();//Until('\n');
              if (velocity>0)
                 {
                 digitalWrite(vang,1);
                 dem_xe=dem_xe+1;
                 if(velocity>50){digitalWrite(coi,0);}
                 ham_coxe();
                 
                 //cộng 1 xe nếu có giá trị vận tốc xe đi đến
                 }
              }
     //khi ko có xe
     else if (den_vang_bat==!true)
              {
              nhayvang();
              
              }
     //thời gian tắt đèn báo "có xe"
     if(digitalRead(xin_duong)==HIGH)
              {
                while (digitalRead(xin_duong)==HIGH)
                      {
                        nhayvang();
                        digitalWrite(den_do,1);
                        //Serial.print
                      }
              }
    
     if (millis()-timetatden>0)
              {
              digitalWrite(coxe,1);
              digitalWrite(coi,1);
              }
     // 1s sẽ trừ 1 chiếc xe. Trung bình 1s là 1 xe đi đến.
     if(millis()-one_giay>3000 && dem_xe>0)
              {
              dem_xe=dem_xe-1;
              one_giay=millis();
              }
     // nếu quá số lượng xe trung bình trong 1s thì đèn đỏ bật. đèn vàng tắt.
     // "có xe" vẫn bật
     if(digitalRead(vang)==LOW && den_vang_bat==true && millis()-time_den_vang_bat>=3000)
              {
                dung=true;
               }
     if(dem_xe>2 )
              {
              dung=!true;
              den_vang_bat=!true;
              digitalWrite(vang,1);
              digitalWrite(den_do,0);
              time_den_do_bat=millis();
              }
     if(/*dem_xe<2*/ millis()-time_den_do_bat>=15000)
              {
              digitalWrite(den_do,1);
              
              }
    /* if((digitalRead(xin_duong)==HIGH and digitalRead(den_do)==HIGH) && millis()-time_den_vang_bat>=48000)
              {
              den_vang_bat = true;
              digitalWrite(vang,LOW);
              time_den_vang_bat=millis();  
              }
*/}