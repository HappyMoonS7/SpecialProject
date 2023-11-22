#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEScan.h>
#include <BLEAdvertisedDevice.h>
#include <HardwareSerial.h>
int scanTime = 1;

BLEClient*  pClient;
BLEScan* pBLEScan = BLEDevice::getScan();
static BLEAddress *pServerAddress;

//String knownAddresses[] = {"a0:b7:65:58:59:46"};
//String knownAddresses[] = {"a0:b7:65:58:61:b6"};
//String knownAddresses[] = {"24:6f:28:2d:c2:92"};ของอาจาร
//String knownAddresses[] = {"a0:b7:65:58:ab:52"};
//String knownAddresses[] = {"24:6f:28:95:ae:12"};ของอาจาร
String knownAddresses[] = {"a0:b7:65:58:61:b6","a0:b7:65:58:59:46","a0:b7:65:58:ab:52","24:6f:28:2d:c2:92","24:6f:28:95:ae:12"};
int j = 0;
class MyAdvertisedDeviceCallbacks: public BLEAdvertisedDeviceCallbacks {
  float sum = 0,sum2 = 0,sum3 = 0,sum4 = 0;
    void onResult(BLEAdvertisedDevice Device) {
      pServerAddress = new BLEAddress(Device.getAddress());
      bool known = false;
      for (int i = 0; i < (sizeof(knownAddresses) / sizeof(knownAddresses[0])); i++) {
        if (strcmp(pServerAddress->toString().c_str(), knownAddresses[i].c_str()) == 0){
          known = true;
        } 
      }
      if(known){
        if (strcmp(pServerAddress->toString().c_str(), knownAddresses[0].c_str()) == 0){
          sum += Device.getRSSI();
          Serial.printf("RSSI: %d  Address:%s \n",Device.getRSSI(),pServerAddress->toString().c_str());
          Serial.printf("SumRSSI: %f \n",sum);
          Serial.printf("average: %f \n",sum/(j+1));
          Serial.printf("j: %d \n",j);
          Serial2.write(Device.getRSSI());
        }
        if (strcmp(pServerAddress->toString().c_str(), knownAddresses[1].c_str()) == 0){
          sum2 += Device.getRSSI();
          Serial.printf("RSSI: %d  Address:%s \n",Device.getRSSI(),pServerAddress->toString().c_str());
          Serial.printf("SumRSSI: %f \n",sum2);
          Serial.printf("average: %f \n",sum2/(j+1));
          Serial.printf("j: %d \n",j);
          Serial2.write(20);
        }
        if (strcmp(pServerAddress->toString().c_str(), knownAddresses[2].c_str()) == 0){
          sum3 += Device.getRSSI();
          Serial.printf("RSSI: %d  Address:%s \n",Device.getRSSI(),pServerAddress->toString().c_str());
          Serial.printf("SumRSSI: %f \n",sum3);
          Serial.printf("average: %f \n",sum3/(j+1));
          Serial.printf("j: %d \n",j);
          Serial2.write(Device.getRSSI());
        }
        if (strcmp(pServerAddress->toString().c_str(), knownAddresses[3].c_str()) == 0){
          sum4 += Device.getRSSI();
          Serial.printf("RSSI: %d  Address:%s \n",Device.getRSSI(),pServerAddress->toString().c_str());
          Serial.printf("SumRSSI: %f \n",sum4);
          Serial.printf("average: %f \n",sum4/(j+1));
          Serial.printf("j: %d \n",j);
        }
        // sum += Device.getRSSI();
        // Serial.printf("RSSI: %d  Address:%s \n",Device.getRSSI(),pServerAddress->toString().c_str());
        // Serial.printf("SumRSSI: %f \n",sum);
        // Serial.printf("average: %f \n",sum/(j+1));
        // Serial.printf("j: %d \n",j);
        // Serial.printf("Advertised Device: %s \n", Device.toString().c_str());
      }
  }
};
void setup() {
  Serial.begin(115200);
  Serial2.begin(9600, SERIAL_8N1, 16, 17);
  Serial.println("Scanning...");
  BLEDevice::init("");
  pClient  = BLEDevice::createClient();
  pBLEScan = BLEDevice::getScan();
  pBLEScan->setAdvertisedDeviceCallbacks(new MyAdvertisedDeviceCallbacks());
  pBLEScan->setActiveScan(true);
  for(j = 0 ; j<30 ;j++){
    BLEScanResults scanResults = pBLEScan->start(scanTime);
    delay(2000);
  }
}

void loop() {
  // BLEScanResults scanResults = pBLEScan->start(scanTime);
  // delay(2000);
}
