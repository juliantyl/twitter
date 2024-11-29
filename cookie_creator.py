import asyncio
from configparser import ConfigParser
from twikit import Client


async def main():
    client = Client(language='en-US')

    config = ConfigParser()
    config.read('config.ini')
    username = config['X']['username']
    password = config['X']['password']
    email = config['X']['email']
    # Login and retrieve cookie
    await client.login(auth_info_1=username, auth_info_2=email, password=password)
    client.save_cookies('cookies.json')

if __name__ == '__main__':
    asyncio.run(main())