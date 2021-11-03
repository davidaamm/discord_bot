async def check_rocket_league_news():
  chanel = client.get_channel(864631358383194123)

  if not chanel:
    return

  with open("links.json") as links_file:
    links_saved = json.load(links_file)

  existing_links= links_saved['links']
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')

  driver = webdriver.Chrome(options=chrome_options)
  driver.get("https://www.rocketleague.com/es-mx/news/")
  myElem = driver.find_elements_by_class_name("news-tile-wrap")
  list_links = []
  for a in myElem:
      link = a.get_attribute('href')
      list_links.append(link)

  if list_links[0] in existing_links:
    pass
  else:
    await chanel.send("Shabos, hay una nueva noticia de Rokelij, acá el link: " + list_links[0])
    existing_links.insert(0,list_links[0])
    total_links = len(existing_links)
    my_dict = {'links': existing_links, 'cant': total_links}
    with open("links.json", "w") as links_file:
        json.dump(my_dict, links_file, indent=4)

  #check_rocket_league_news.start()