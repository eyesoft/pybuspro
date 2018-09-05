import asyncio

# ip, port = gateway_address
# subnet_id, device_id, channel = device_address


# Wrapper class
class buspro:


            
    class Buspro():

        def __init__(self, gateway_address):
            self._telegram_received_cbs = []
            self._gateway_address = gateway_address
            
        def register_telegram_received_cb(self, telegram_received_cb, device_address):
            self._telegram_received_cbs.append({'callback':telegram_received_cb, 'device_address':device_address})

        async def connect(self):
            print(f"...Connected to {self._gateway_address}...")
            
        async def _send_message(self, telegram):
            await asyncio.sleep(0.1)
            print(f"send telegram: {telegram}...")

        async def start(self, callback=None):
            iterations = 15
            i = 0
            
            while True:
                i += 1
                
                telegram = buspro.Telegram(source_address=(1,120,10))
                telegram.payload = f"[{i}]"
                #print(telegram.payload)
                #print(telegram.source_address)
                #print(str(telegram))
                
                if callback is not None:
                    await callback(telegram)
                
                for telegram_received_cb in self._telegram_received_cbs:
                    device_address = telegram_received_cb['device_address']
                    
                    # Sender callback kun for oppgitt kanal
                    if device_address[2] == i:
                        ret = await telegram_received_cb['callback'](f"{device_address} ==> {str(telegram)}")
               
                if i == iterations:
                    break;
                await asyncio.sleep(1)
                

        
                
                
                

    class Device(object):
        def __init__(self, buspro, device_address):
            self._device_address = device_address
            self._buspro = buspro
        
        @property
        def name(self):
            adr = f"{self._device_address}"
            return adr

        def register_telegram_received_cb(self, telegram_received_cb):
            self._buspro.register_telegram_received_cb(telegram_received_cb, self._device_address)
            
            
            

    class Light(Device):
        def __init__(self,  buspro, device_address):
            super().__init__(buspro, device_address)
            self._device_address = device_address
            self._buspro = buspro
            
        async def turn_on(self):
            telegram = buspro.Telegram(target_address=self._device_address, payload=100)
            await self._buspro._send_message(telegram)
            
        async def turn_off(self):
            telegram = buspro.Telegram(target_address=self._device_address, payload=0)
            await self._buspro._send_message(telegram)
            
        async def dim(self, intensity):
            telegram = buspro.Telegram(target_address=self._device_address, payload=intensity)
            await self._buspro._send_message(telegram)
        
       
   
   
   
       
        
    # DTO class
    class Telegram:
        def __init__(self, source_address=None, source_device_type=None, target_address=None, operate_code=None, payload=None):
            self.source_address = source_address
            self.source_device_type = source_device_type
            self.target_address = target_address
            self.operate_code = operate_code
            self.payload = payload
        
        def __str__(self):
            """Return object as readable string."""
            return '<Telegram source_address="{0}", source_device_type="{1}" ' \
                'target_address="{2}" operate_code="{3}" ' \
                'payload="{4}" />'.format(
                    self.source_address,
                    self.source_device_type,
                    self.target_address,
                    self.operate_code,
                    self.payload)

        def __eq__(self, other):
            """Equal operator."""
            return self.__dict__ == other.__dict__
        
        
   
   
   
   
   
   
   
   
   
   
   
   
async def callback_all_messages(telegram):
    print(telegram)
    
async def first_callback(message):
    print(f"callback 1 received: {message}")

async def second_callback(message):
    print(f"callback 2 received: {message}")

    
    
    
    
async def main():

    # Now you want to start long_operation, but you don't want to wait it finised:
    # long_operation should be started, but second msg should be printed immediately.
    # Create task to do so:
    
    GATEWAY_ADDRESS = ('192.168.1.15', 6000)
        
    hdl = buspro.Buspro(GATEWAY_ADDRESS)
    await hdl.connect()
    
    light = buspro.Light(hdl, device_address=(1, 123, 11))
    light.register_telegram_received_cb(first_callback)
    #print(light.name)
    
    task = asyncio.ensure_future(hdl.start(callback_all_messages))
    #task = asyncio.ensure_future(hdl.start())

    await light.turn_on()
    await asyncio.sleep(2)
    await light.turn_off()
    await asyncio.sleep(4)
    await light.dim(75)

    # Now, when you want, you can await task finised:
    await task


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())