import asyncio
import sys

from src.controllers.construct_tg_bot.app import main

if __name__ == '__main__':
    asyncio.run(
        main(
            bot_config_json_file_path=sys.argv[1],
            bot_api_token=sys.argv[2]
        )
    )
