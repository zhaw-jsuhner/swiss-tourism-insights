from playwright.sync_api import sync_playwright
import pandas as pd
import os
import time

def scroll_page(page, scroll_step=10000, max_scrolls=3, delay=2):
    for i in range(max_scrolls):
        print(f"Scroll {i + 1} von {max_scrolls}...")
        page.evaluate(f"window.scrollBy(0, {scroll_step});")
        time.sleep(delay)

def main():
    # Datenordner sicherstellen
    os.makedirs('data', exist_ok=True)

    with sync_playwright() as p:
        checkin_date = '2025-08-23'
        checkout_date = '2025-08-24'

        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            locale="de-DE"
        )
        page = context.new_page()

        all_hotels_list = []

        try:
            page_url = f'https://www.booking.com/searchresults.de.html?ss=Schweiz&ssne=Schweiz&ssne_untouched=Schweiz&label=gen173nr-1BCAEoggI46AdIM1gEaCyIAQGYAQe4ARfIAQzYAQHoAQGIAgGoAgO4ArfNy8EGwAIB0gIkNDcwMDlkZDMtMTJhOS00MTVhLThiOTQtMTlhMmM5NmVhNmRh2AIF4AIB&sid=557d3823a3e6b0674ada1cd455a39b2e&search_pageview_id=b15f58a56e0d0a94&aid=304142&lang=de&sb=1&src_elem=sb&src=index&dest_id=204&dest_type=country&checkin={checkin_date}&checkout={checkout_date}&group_adults=2&no_rooms=1&group_children=0'

            page.goto(page_url, timeout=60000)
            page.wait_for_load_state("networkidle", timeout=15000)

            # Rasteransicht aktivieren
            try:
                grid_button = page.locator('label[for="r8n-grid"]')
                if grid_button.is_visible():
                    grid_button.click()
                    page.wait_for_load_state("networkidle", timeout=5000)
                    print("Rasteransicht aktiviert.")
            except Exception as e:
                print(f"Fehler beim Aktivieren der Rasteransicht: {e}")

            # Loop: Scroll + Button-Klicks
            loop_count = 0
            total_hotels_loaded = 0

            while True:
                loop_count += 1
                range_start = total_hotels_loaded + 1
                print(f"\n=== Lade Hotels (Loop {loop_count}) ===")

                # Scrollen
                scroll_page(page, scroll_step=3000, max_scrolls=5, delay=2)

                # Button klicken
                try:
                    load_more_button = page.locator('button:has-text("Weitere Suchergebnisse laden")')
                    if load_more_button.is_visible():
                        print("Klicke auf 'Weitere Suchergebnisse laden'...")
                        load_more_button.click()
                        page.wait_for_load_state("networkidle", timeout=10000)
                        time.sleep(3)
                        

                        if loop_count >= 3:
                            print(f"\n Maximale Anzahl von {loop_count} Hotels erreicht. Beende den Loop.")
                            break
                    else:
                        print("Kein 'Weitere Suchergebnisse laden'-Button mehr sichtbar.")
                        break
                except Exception as e:
                    print(f"Fehler beim Klicken auf 'Weitere Suchergebnisse laden': {e}")
                    break

            # Warten für letzte Ladeprozesse
            time.sleep(5)

            # Hotels extrahieren
            hotels = page.locator('[data-testid="property-card"]').all()
            print(f'Gefundene Hotels insgesamt: {len(hotels)}')

            for hotel in hotels:
                hotel_dict = {}

                try:
                    hotel_dict['hotel'] = hotel.locator('[data-testid="title"]').inner_text()
                except:
                    hotel_dict['hotel'] = None

                try:
                    hotel_dict['place'] = hotel.locator('[data-testid="address"]').inner_text()
                except:
                    hotel_dict['place'] = None
                
                try:
                    hotel_dict['price_per_night'] = hotel.locator('[data-testid="price-and-discounted-price"]').inner_text()
                except:
                    hotel_dict['price_per_night'] = None
                
                try:
                    hotel_dict['rating'] = hotel.locator('[data-testid="review-score"] > div:nth-child(2)').inner_text()
                except:
                    hotel_dict['rating'] = None

                try:
                    hotel_dict['review_counter'] = hotel.locator('[data-testid="review-score"] > div:nth-child(3) > div:nth-child(2)').inner_text()
                except:
                    hotel_dict['review_counter'] = None

                all_hotels_list.append(hotel_dict)

            # Ergebnisse in CSV speichern
            df = pd.DataFrame(all_hotels_list)
            df.to_csv('data/hotels_list.csv', index=False)
            print(f"Alle Hotels gespeichert in data/hotels_list.csv")

        except Exception as e:
            print("Fehler aufgetreten:", e)

        finally:
            browser.close()

if __name__ == '__main__':
    main()
