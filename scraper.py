import cloudscraper

scraper = cloudscraper.create_scraper()
print (scraper.get("https://api.tracker.gg/api/v2/rocket-league/standard/profile/epic/deividaam/").text)