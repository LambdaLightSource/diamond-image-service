import asyncio

import aiohttp

IMAGE_SERVICE_URL = "https://image-service.diamond.ac.uk/unsafe/random_image_{:06d}.jpg"
TOTAL_IMAGES = 1000


async def fetch_url(session, url, count_success, count_fail):
    async with session.get(url) as response:
        if response.status == 200:
            print(f"Pre-warmed cache for: {url}")
            await count_success.put(1)
        else:
            print(
                f"Failed to pre-warm cache for: {url}, Status code: {response.status}"
            )
            await count_fail.put(1)


async def pre_warm_cache():
    count_success = asyncio.Queue()
    count_fail = asyncio.Queue()

    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(TOTAL_IMAGES):
            image_url = IMAGE_SERVICE_URL.format(i)
            task = asyncio.create_task(
                fetch_url(session, image_url, count_success, count_fail)
            )
            tasks.append(task)
            await asyncio.sleep(0.1)
        await asyncio.gather(*tasks)

        total_success = 0
        total_fail = 0
        while not count_success.empty():
            total_success += await count_success.get()
        while not count_fail.empty():
            total_fail += await count_fail.get()
        print(total_success, total_fail)


if __name__ == "__main__":
    asyncio.run(pre_warm_cache())
