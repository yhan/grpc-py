import asyncio


async def my_coroutine():
    print("Start")
    await asyncio.sleep(1)
    print("End")


async def main():
    await my_coroutine()

if __name__ == "__main__":
    asyncio.run(main())