#include <stdlib.h>
#include <SoftwareSerial.h> 
SoftwareSerial monitor(4, 5);       // 定义软串口RX, TX   用于数据监测 便于调试

#include <LiquidCrystal.h>             //LCD1602液晶显示器
LiquidCrystal lcd(12, 11, 10, 9, 8, 7); //LiquidCrystal(rs, enable, d4, d5, d6, d7)  

#include <dht11.h>                                               //引用dht11库文件，使得下面可以调用相关参数
#define DHT11PIN 6                                             //定义温湿度针脚号为6号引脚
dht11 DHT11;                                                       //实例化一个对象
int  val=analogRead(0);   //读取传感器的模拟值并赋值给val   A0   MQ-135

char StrDipId[10];                  //节点ID   拨码开关获取    1.2.3.4-----A1.A2.A3.A4   下面接地 上面输入检测   最大支持到16
char StrMQ135[10];                  //MQ135 字符串值
char LCDstrMQ135[10];               //在lcd1602上显示的字符串

String ssid= "iphone";           //wifi名 
String pass= "123456789";        //wifi密码 
String ip = "172.20.10.3";       //虚拟服务器的IP
String port= "8080";             //端口
String temph;
String tempt;
int  sendtime=10;

String  ResetWIFI= ""; //要分离的字符串      //输入接收判断
int commaPosition;//存储还没有分离出来的字符串     , 索引

//初始化----------------------------------------- 
void setup() 
{ 
  GetDipId();       //获取拨码开关  节点号
  DHT11.read(DHT11PIN); // 读取 DHT11 传感器    初始化  避免第一条空数据
  float tempH = DHT11.humidity; 
  float tempT = DHT11.temperature; 

  lcd.begin(16,2);  //初始化
  lcd.clear();      //清屏
  pinMode(DHT11PIN,OUTPUT);                       //初始化DHT11引脚

  monitor.begin(115200); 
  Serial.begin(115200); 

 for (int i=50;i>0;i--)
 {
  while(monitor.read()>= 0){}        //清空接收数据缓存
  delay(100);
  if(monitor.available()>0){  
      delay(100);  
      ResetWIFI = monitor.readString();  
    }  
  if (ResetWIFI.length()>10)                   //有效接收数量
  {
      commaPosition = ResetWIFI.indexOf(',');//检测字符串中的逗号
      if(commaPosition != -1)//如果有逗号存在就向下执行
      {
         ssid=ResetWIFI.substring(0,commaPosition);
         ResetWIFI = ResetWIFI.substring(commaPosition+1, ResetWIFI.length());//从当前位置+1开始
      }
      commaPosition = ResetWIFI.indexOf(',');//检测字符串中的逗号
      if(commaPosition != -1)//如果有逗号存在就向下执行
      {
         pass= ResetWIFI.substring(0,commaPosition);
         ResetWIFI = ResetWIFI.substring(commaPosition+1, ResetWIFI.length());//从当前位置+1开始
      }
     commaPosition = ResetWIFI.indexOf(',');//检测字符串中的逗号
      if(commaPosition != -1)//如果有逗号存在就向下执行
      {
          ip =ResetWIFI.substring(0,commaPosition);
         ResetWIFI = ResetWIFI.substring(commaPosition+1, ResetWIFI.length());//从当前位置+1开始
      }
     commaPosition = ResetWIFI.indexOf(',');//检测字符串中的逗号
      if(commaPosition != -1)//如果有逗号存在就向下执行
      {
          port =ResetWIFI.substring(0,commaPosition);
         ResetWIFI = ResetWIFI.substring(commaPosition+1, ResetWIFI.length());//从当前位置+1开始
      }
      if(ResetWIFI.length() > 0)
      sendtime=ResetWIFI[0]-'0';  
  }
 }

  sendDebug("AT+RESTORE"); //恢复出厂设置
  delay(2000);      //延时2s
  while(1)
  {
     sendDebug("AT"); //指令测试 
     delay(300);      //延时0.3s
     if(Serial.find("OK"))      //接收指令正常则返回OK 
     { 
        monitor.println("RECEIVED: OK"); 
        connectWiFi();        //连接wifi
        break;
      }
     else                      //esp8266收不到指令返回ESP8266 Error
     {
        monitor.println("ESP8266 Error"); 
     }
  } 
  delay(500);     //延时1s
} 
void loop() 
{ 
  Serial.println(StrDipId); 

  
  GetSensorValue();        //获取传感器数据
  showlcd1602();           //刷新显示屏
  
  ConServer();                                  //连接服务器

  GetSensorValue();        //获取传感器数据
  showlcd1602();           //刷新显示屏
  
  SendSensorData();                            //发送数据给服务器端

  for(int i=sendtime;i>0;i--)                 //1s更新一次lcd1602数据
  {
  GetSensorValue();        //获取传感器数据
  showlcd1602();           //刷新显示屏
  delay(950);    //延时发送一次数据给服务器
  }
} 

void GetDipId()
{
  int  DIPid=0;
  pinMode(15, INPUT_PULLUP);            //上拉输入  A1
  pinMode(16, INPUT_PULLUP);            //上拉输入  A2
  pinMode(17, INPUT_PULLUP);            //上拉输入  A3
  pinMode(18, INPUT_PULLUP);            //上拉输入  A4
  if(digitalRead(15)==0)  DIPid+=8;
  if(digitalRead(16)==0)  DIPid+=4;
  if(digitalRead(17)==0)  DIPid+=2;
  if(digitalRead(18)==0)  DIPid+=1;      //节点号
  itoa(DIPid, StrDipId, 10);             //int 转字符串
}

void sendDebug(String cmd) 
{ 
  monitor.print("SEND: "); 
  monitor.println(cmd); 
  Serial.println(cmd); 
 } 
 
void GetSensorValue()
{ 
  DHT11.read(DHT11PIN); // 读取 DHT11 传感器 
  int MQ135val=analogRead(0);   //读取传感器的模拟值并赋值给val   A0   MQ-135
  float tempH = DHT11.humidity; 
  float tempT = DHT11.temperature; 
  char buffer[10]; 
  temph = dtostrf(tempH, 2, 0, buffer);      //获取湿度数据  转字符串
  tempt = dtostrf(tempT, 2, 0, buffer);      //获取温度数据  转字符串
  itoa(MQ135val, StrMQ135, 10);             //int 转字符串

  LCDstrMQ135[0]=MQ135val/100%10+'0';               //取百位
  LCDstrMQ135[1]=MQ135val/10%10+'0';               //取十位
  LCDstrMQ135[2]='\0';
}
void showlcd1602()
{
  lcd.setCursor(0, 0);  
  lcd.print("T:");
  lcd.print(tempt);
  lcd.setCursor(4, 0);  
  lcd.print("'C");

  lcd.setCursor(9, 0);  
  lcd.print("Q:");
  lcd.print(LCDstrMQ135);
  lcd.setCursor(13, 0); 
  lcd.print("% ");
  
  lcd.setCursor(0, 1);  
  lcd.print("H:");
  lcd.print(temph);   
  lcd.setCursor(4, 1);  
  lcd.print("%RH");
}

void ConServer()
{
  String cmd = "AT+CIPSTART=\"TCP\",\""; 
  cmd += ip; 
  cmd += "\","; 
  cmd += port; 
  sendDebug(cmd);  //发送指令，连接服务器 
  delay(200);      //延时0.2s 
  if(Serial.find("Error")) 
  { 
      monitor.print("RECEIVED: Error"); 
      return; 
   } 
  else
  { 
      monitor.println("RECEIVED: OK"); 
   } 
  delay(500);      //延时0.5s 
}

void SendSensorData()       //发送湿度 温度值
{ 

   String cmd = StrDipId    ;
    cmd  =  cmd+",DHT11,"+ tempt+","+ temph+",MQ135,"+StrMQ135 ;     //温度、湿度 MQ135 的值   

   Serial.print("AT+CIPSEND="); 
   Serial.println(cmd.length());                     //发送长度
   delay(200);      //延时0.2s 
   if(Serial.find(">")) 
   { 
      monitor.print(">"); 
      sendDebug(cmd);                                 //发送温度湿度给服务器
   } 
   else 
   { 
        sendDebug("AT+CIPCLOSE"); 
   } 
   if(Serial.find("OK")) 
   { 
       monitor.println("RECEIVED: OK"); 
    } 
   else 
   { 
       monitor.println("RECEIVED: Error"); 
    } 
} 

void  connectWiFi()    
{ 
    Serial.println("AT+CWMODE=3"); 
    delay(500);       //延时0.5s     
    String cmd="AT+CWJAP=\""; 
    cmd+=ssid; 
    cmd+="\",\""; 
    cmd+=pass; 
    cmd+="\""; 
    sendDebug(cmd);         //发送wifi账号密码
    delay(5000);   
    if(Serial.find("OK")) 
    { 
      monitor.println("RECEIVED: OK"); 
    }
    else 
    { 
      monitor.println("RECEIVED: Error"); 
    } 
}


