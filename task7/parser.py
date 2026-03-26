import time

from playwright.sync_api import sync_playwright
import random as rn


def scroll_to_new_games(page):
    try:
        cards = page.query_selector_all('.title')
        if cards:
            last_card = cards[-2] if len(cards) > 1 else cards[-1]
            
            last_card.scroll_into_view_if_needed(timeout=5000)
            time.sleep(rn.uniform(2, 5))
    except:
        page.evaluate('window.scrollBy(0, 500)')
        time.sleep(rn.uniform(2, 5))

def run_steam_parser(url):
    max_scrolls = 2
    all_games_data = []

    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        page = browser.new_page()
        page.set_extra_http_headers({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ...'})
        
        page.goto(url)
        page.wait_for_selector('.title')

        num_scrolls, idx_main = 0, 0
        while num_scrolls < max_scrolls:
            selectors = ['.title', '.search_released', '.discount_pct', '.discount_original_price', '.discount_final_price']
            
            results = []
            for sel in selectors:
                elements = page.query_selector_all(sel)
                results.append([el.inner_text().strip() for el in elements])

            if results and all(results):
                for i in range(len(results[0])):
                    if i >= idx_main:
                        all_games_data.append({
                            "name": results[0][i],
                            "release_date": results[1][i],
                            "discount": results[2][i],
                            "original_price": results[3][i],
                            "discount_price": results[4][i]
                        })
            
            idx_main = len(results[0])
            scroll_to_new_games(page)
            num_scrolls += 1

    return all_games_data