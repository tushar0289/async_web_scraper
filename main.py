import asyncio, random, json, re, traceback
from curl_cffi.requests import AsyncSession
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd



async def fetch_with_retry(url, session, retries=3):
    for attempt in range(retries):
        try:
            await asyncio.sleep(random.uniform(0.5, 1.5))
            response = await session.get(url)

            if response.status_code == 200:
                return response

            elif response.status_code == 429:
                print("Too many tries! Wait a lil bit...")
                
                if attempt == (retries - 1):
                    print("Can't get the data!")
                    break

                wait_time = (2 ** attempt) + random.uniform(1, 3)
                await asyncio.sleep(wait_time)


        except Exception as e:
            print(f"Error: {e}.")

    return None



async def parse(response, url):
    if response == None:
        return []

    urls = []
    soup = BeautifulSoup(response.content, "lxml")
    product_list = soup.select("li.product-grid__item")

    for product in product_list:
        link = product.select_one("a.product-card")
        if link and link.get("href"):
            urls.append(urljoin(url, link["href"]))
            
    return urls 



async def page_links(session, i):
    current_page_link = f"https://www.thewhiskyexchange.com/c/35/japanese-whisky?pg={i}"
    response = await fetch_with_retry(current_page_link, session)
    return await parse(response, current_page_link)



async def get_product_data(url, session, sem):
    async with sem:
        await asyncio.sleep(random.uniform(0.5, 1.2))
        response = await fetch_with_retry(url, session)
        if response == None:
            return None

        soup = BeautifulSoup(response.content, "lxml")

        name_test = soup.select_one("h1.product-main__name")
        name = name_test.get_text(" ", strip=True) if name_test else None

        rating_test = soup.select_one("span.review-overview__rating span")
        rating = rating_test.text.strip() if rating_test else None

        price = soup.select_one("div.product-action__row")
        price_test = price.select_one(".product-action__price") if price else None
        product_price_raw = price_test.text.strip() if price_test else None
        match = re.search(r"\d+(\.\d+)?", product_price_raw) if product_price_raw else None
        product_price = float(match.group()) if match else None

        whiskey = {
            "Name": name,
            "Rating": rating,
            "Price": product_price
        }
        print(whiskey)

        return whiskey



async def main():
    home_url = "https://www.thewhiskyexchange.com/"
    end_point = "c/35/japanese-whisky"
    url = urljoin(home_url, end_point)

    try:
        async with AsyncSession(impersonate="chrome120") as session:
            await session.get(home_url)
            response = await fetch_with_retry(url, session)
            tasks = [parse(response, home_url)]

            for i in range(2, 8):
                tasks.append(page_links(session, i))

            result = await asyncio.gather(*tasks)
            all_urls = [url for sublist in result for url in sublist]

            sem = asyncio.Semaphore(5)
            product_data = [get_product_data(url, session, sem) for url in all_urls]

            results = await asyncio.gather(*product_data)
            whiskeys = [r for r in results if r is not None]

            with open("whiskeys.json", 'w') as wf:
                json.dump(whiskeys, wf, indent=4, ensure_ascii=False)

            
            df = pd.DataFrame(whiskeys)
            df.to_csv("whiskeys.csv", index=False)

            
            print("Scraping Successfully Finished!")

    
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()

   

if __name__ == "__main__":
    asyncio.run(main())