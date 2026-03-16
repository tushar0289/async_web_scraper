# async_web_scraper

An asynchronous Python web scraper that collects **Japanese Whiskey** data from the **The Whiskey Exchange** website. This scraper extracts product information such as **name, rating and price** and saves them into **JSON and CSV formats.**

I've done this project while learning asynchronous python.


---


## Features

- Asynchronous scraping using `asyncio`
- HTTP request with `curl_cffi` which mimics browser's TLS Fingerprinting
- HTML parsing with `BeautifulSoup`
- Retry logic and Rate Limiting.
- Random delays to reduce the server load
- Exports data in both **JSON** and **CSV** format


---


## Example Output

### JSON

```JSON
[
    {
        "Name": "Hibiki Harmony",
        "Rating": "4",
        "Price": 75.5
    },
    {
        "Name": "Suntory Toki",
        "Rating": "4",
        "Price": 27.95
    }
]
```

### CSV

```CSV
Name,Rating,Price
Hibiki Harmony,4,75.5
Suntory Toki,4,27.95
```


---


## Notes

- Concurrecy is controlled by `asyncio.Semaphore`, which limits the number of tasks that can run simultaneously. In this project, the Semaphore ishave set the semaphore to 5, this is an ideal number, not too low or not too high and reduces the chances of getting banned and keeps a balance performance.


---


## Disclaimer

This project is intended for **educational purposes only**. This only scrapes publicly available data and respects the rate limit.
