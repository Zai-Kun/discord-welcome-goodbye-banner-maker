import asyncio
import time

from dc_banner_maker import BackgroundImage, DiscordBannerMaker

bg_image = BackgroundImage("./backgrounds/5.jpg")
banner_maker = DiscordBannerMaker(bg_image)


async def main():
    img = await banner_maker.make_banner(
        "https://cdn.discordapp.com/avatars/1100460955390988410/a03d2ff8d56a7f1212ff0aa0c9a736e0.png",
        "Welcome, Zai",
        "Hope you enjoy your stay",
    )

    img.show()


asyncio.run(main())
