from scrapegraphai.graphs import SmartScraperGraph
from parser import csv_opener

def products_from_url_sga(url, prompt = "Find all product names on the website of online shop"):
    try:
        # Define the configuration for the scraping pipeline
        graph_config = {
            "llm": {
                "api_key": "AIzaSyCfwYRE76eXT6s2SRpAYqe6IcEW1bxiYW4",
                "model": "google_genai/gemini-pro",  # Use a correct and supported model
                "rate_limit": {
                "requests_per_second": 1
            }
            },
            "headless" : True
        }

        # Create the SmartScraperGraph instance
        smart_scraper_graph = SmartScraperGraph(
            prompt=prompt,
            source=url,
            config=graph_config
        )

        # Run the pipeline
        result = smart_scraper_graph.run()
        for key in result:
            return result[key]
    except:
        return 

with open('data/data_100.txt', 'w', encoding='utf-8') as file:
    urls = csv_opener('data/URL_list.csv')
    data = []
    for i, url in enumerate(urls):
        if i == 100:
            break
        names = products_from_url_sga(url)
        if names and names != 'NA':
            data += names
        else: print(url)
        print(names)
    try:
        file.write('\n'.join(data))
    except:
        file.write(data)

        

