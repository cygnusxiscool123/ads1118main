import asyncio
import busio
import microcontroller
import time
import digitalio
from ADS1118 import ADS1118, ADS1118_MUX_SELECT, ADS1118_FSR, ADS1118_SAMPLE_RATE
from spi import spi_bus, spi_device

spi = spi_bus(clock=microcontroller.pin.PA17, MOSI=board.MOSI, MISO=board.MISO)
 
cs_pins = [board.ADC_CS1, board.ADC_CS3, board.ADC_CS2, board.ADC_CS4, board.ADC_CS5, board.ADC_CS6]
 
spi_devices = []
adcs = []
 
for cs_pin_number in cs_pins:
    cs_pin = digitalio.DigitalInOut(cs_pin_number)
    spi_dev = spi_device(spi, cs_pin)
    adc = ADS1118(spi_dev)
    spi_devices.append(spi_dev)
    adcs.append(adc)
    
async def main():
    while True:
        tasks = []
        channels = []
        for adc in adcs:
            for channel in range(4, 8):  
            # Read from single-ended channels 4 to 7 measuring voltage relative to ground
                tasks.append(adc.take_sample(channel))
                channels.append(channel)
            
            # Read from differential channels 0 to 3 measuring voltage difference between two input pins
            for channel in range(0, 4):  
                tasks.append(adc.take_sample(channel))
                channels.append(channel)
            
            # Read temperature
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
