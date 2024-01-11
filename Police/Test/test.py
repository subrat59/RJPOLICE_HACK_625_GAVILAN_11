def auto_Scraper(request_client):
    # if request_client.method=='POST':
        # keywords = ["Credit Cards","Drugs","Guns","Weapons","Bombs","Cocaine","Heroine","Passports","Visa","Debit Cards"]
        keywords = ["Credit Cards","Guns","Drugs"]
        reachable_sites = initial_result(keywords)
        for keys in reachable_sites:
            user_input = keys
            if " " in user_input:
                user_input = user_input.replace(" ", "+")

            search_url = "https://ahmia.fi/search/?q={}".format(user_input)
            print(search_url)
            useragents = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19577", "Mozilla/5.0 (X11) AppleWebKit/62.41 (KHTML, like Gecko) Edge/17.10859 Safari/452.6", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2656.18 Safari/537.36", "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36",
                  "Mozilla/5.0 (Linux; U; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13", "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27", "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_8; zh-cn) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27"]
            u_a = random.choice(useragents)
            headers = {'User-Agent': u_a}
            request = requests.get(search_url, headers=headers)
            fetched_content = request.text

            def links_search(content):
                Q_regex = "\w+\.onion"

                data_scraped = re.findall(Q_regex, fetched_content)
                data_scraped = list(dict.fromkeys(data_scraped))

                session = get_tor_session()

            #for onion_sites in data_scraped:
                for onion_sites in range(2):  #To Limit the number of results
                # url = "http://" + onion_sites
                    url = "http://" + data_scraped[onion_sites]
                    print(url)
                    try:
                        response_url = session.get(url)
                        if (response_url.ok):
                            print(200)
                        # reachable_sites.append(onion_sites)
                            reachable_sites[keys].append(data_scraped[onion_sites])
                        
                    except:
                        print("Unreachable")
                        continue
            if request.status_code == 200:
                print("Request code 200 \n")
                links_search(fetched_content)
            # progress=int((i+1)/5 * 100)
            # responsedata = {'progress':progress}
            # return JsonResponse(responsedata)
        return render(request_client,'result_sites1.html',{'reached_sites':reachable_sites,'user_input':"Auto Scan"})


