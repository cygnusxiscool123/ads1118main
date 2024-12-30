import asyncio
import busio
import microcontroller
import time
import digitalio
import pin_manager
from drivers.ads1118 import ADS1118, ADS1118_MUX_SELECT, ADS1118_FSR, ADS1118_SAMPLE_RATE
 
cs_pins = [microcontroller.pin.PA18, microcontroller.pin.PA23, microcontroller.pin.PA22, microcontroller.pin.PB23, microcontroller.pin.PB22, microcontroller.pin.PA27] 

adcs = []
 
for cs_pin_number in cs_pins:
    adc = ADS1118(clock=microcontroller.pin.PA17, MOSI=microcontroller.pin.PA16, MISO=microcontroller.pin.PA19, ss=cs_pin_number)
    adcs.append(adc)
    
async def main():
    while True:
        tasks = []
        channels = []
        for adc in adcs:
            for channel in range(4, 8):  
                tasks.append(adc.take_sample(channel))
                channels.append(channel)
                
            for channel in range(0, 4):  
                tasks.append(adc.take_sample(channel))
                channels.append(channel)
                
            tasks.append(adc.take_sample(ADS1118_MUX_SELECT.TEMPERATURE))
            channels.append(ADS1118_MUX_SELECT.TEMPERATURE)
 
        results = await asyncio.gather(*tasks)

        for i, (result, channel) in enumerate(zip(results, channels)):
            if channel == ADS1118_MUX_SELECT.TEMPERATURE:   
                print(f"Temperature {i}: {result:.2f} °C")
            else:
                print(f"Sample Value {i}: {result:.4f} V")
 
        await asyncio.sleep(1)   
    
if __name__ == "__main__":
    asyncio.run(main())
