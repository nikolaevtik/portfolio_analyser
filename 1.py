import asyncio

counter=0

async def increment():
    global counter
    value = counter
    await asyncio.sleep(0.05)
    counter =value + 1
    
async def main():
    tasks = [increment() for _ in range(100)]
    await asyncio.gather(*tasks)
    print(counter)
    
    
asyncio.run(main())