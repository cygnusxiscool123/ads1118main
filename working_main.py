# Write your code here :-)
import asyncio
import busio
import microcontroller
import time
import digitalio
import pin_manager
from ads1118 import ADS1118, ADS1118_MUX_SELECT, ADS1118_FSR, ADS1118_SAMPLE_RATE

cs_pins = [microcontroller.pin.PA18, microcontroller.pin.PA23, microcontroller.pin.PA22, microcontroller.pin.PB23, microcontroller.pin.PB22] # microcontroller.pin.PA27

adcs = []

for cs_pin_number in cs_pins:
    adc = ADS1118(sck=microcontroller.pin.PA17, mosi=microcontroller.pin.PA16, miso=microcontroller.pin.PA19, ss=cs_pin_number)
    adcs.append(adc)
 
async def main():
    while True:
        tasks = []
        channels = []
        for adc in adcs:
            for channel in range(8):
                tasks.append(adc.take_sample(channel))
                channels.append(channel)
                
        results = await asyncio.gather(*tasks)

        for i, (result, channel) in enumerate(zip(results, channels)):
            if channel == ADS1118_MUX_SELECT.TEMPERATURE:
                print(f"Temperature {i}: {result:.2f} °C")
            else:
                print(f"Sample Value {i}: {result:.4f} V")

        await asyncio.sleep(1)
        
if __name__ == "__main__":
    asyncio.run(main())
