import asyncio
import aiohttp
import bs4


async def main():
    base_url = "https://nfgymuc.eltern-portal.org"
    username = "michael@ullrich.bayern"
    password = "chHs8QjMA&#tTMN5$HI0"

    async with aiohttp.ClientSession(base_url=base_url) as session:
        url = "/"
        print(f"url={url}")
        async with session.get(url) as response:

            print(f"response.url={response.url}")
            print(f"response.method={response.method}")
            print(f"response.status={response.status}")
            print(f"cookies={session.cookie_jar.filter_cookies(base_url)}")

            html = await response.text()
            soup = bs4.BeautifulSoup(html, "html5lib")
            tag = soup.find("input", {"name": "csrf"})
            csrf = tag["value"]
            print(f"csrf={csrf}")

        url = "/includes/project/auth/login.php"
        print(f"url={url}")
        login_data = {
            "csrf": csrf,
            "username": username,
            "password": password,
            "go_to": "",
        }
        print(f"login_data={login_data}")
        async with session.post(url, data=login_data) as response:

            print(f"len(history)={len(response.history)}")
            for h in response.history:
                print(f"h.url={h.url}")
                print(f"h.method={h.method}")
                print(f"h.status={h.status}")

            print(f"response.url={response.url}")
            print(f"response.method={response.method}")
            print(f"response.status={response.status}")
            print(f"cookies={session.cookie_jar.filter_cookies(base_url)}")

            html = await response.text()
            print("pupil-selector" in html)
            soup = bs4.BeautifulSoup(html, "html5lib")
            tag = soup.select_one(".pupil-selector")
            print(f"tag={tag}")

loop = asyncio.get_event_loop()
loop.run_until_complete(main())