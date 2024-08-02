def get_player_details():
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    driver.get("https://www.prokabaddi.com/stats/0-102-player-total-points-statistics")
    element = driver.find_element(By.CLASS_NAME, "loadmore")
    for i in range(16):
        driver.execute_script("arguments[0].click();", element)
    soup = BeautifulSoup(driver.page_source)

    for info in soup.find_all("div", class_="info-name"):
        first_name_elem = info.find("p", class_="name first-name")
        last_name_elem = info.find("p", class_="name last-name")

        if first_name_elem and last_name_elem:
            first_name = first_name_elem.text.strip()
            last_name = last_name_elem.text.strip()
            full_name = f"{first_name} {last_name}"
            with open("parsed.txt", "a") as f:
                f.write(full_name + "\n")
    playerDetails = pd.read_csv(
        "parsed.txt", encoding="ISO-8859-1", names=["playerName"]
    )
    if os.path.exists("parsed.txt"):
        os.remove("parsed.txt")
    dfObj = pd.DataFrame(data=[])
    dfObj["PlayerName"] = playerDetails[playerDetails.columns[0]]

    soup = BeautifulSoup(driver.page_source)
    for item in soup.find_all("div", class_="table-data matches-played"):
        [elem.extract() for elem in soup.find("div")]
        file = open("parsed.txt", "a")
        file.write(item.text)
        file.write("\n")
        # print(item.text)

        file.close()
    playerDetails = pd.read_csv(
        "parsed.txt", encoding="ISO-8859-1", sep="\t", names=["MatchesPlayed"]
    )
    dfObj["MatchesPlayed"] = playerDetails[playerDetails.columns[0]]
    if os.path.exists("parsed.txt"):
        os.remove("parsed.txt")

    soup = BeautifulSoup(driver.page_source)
    for item in soup.find_all("div", class_="table-data rank"):
        [elem.extract() for elem in soup.find("div")]
        file = open("parsed.txt", "a")
        file.write(item.text)
        file.write("\n")

        file.close()
    playerDetails = pd.read_csv(
        "parsed.txt", encoding="ISO-8859-1", sep="\t", names=["Rank"]
    )
    dfObj["Rank"] = playerDetails[playerDetails.columns[0]]
    if os.path.exists("parsed.txt"):
        os.remove("parsed.txt")

    soup = BeautifulSoup(driver.page_source)
    for item in soup.find_all("div", class_="category"):
        [elem.extract() for elem in soup.find("div")]
        file = open("parsed.txt", "a")
        file.write(item.text)
        file.write("\n")

        file.close()
    playerDetails = pd.read_csv(
        "parsed.txt", encoding="ISO-8859-1", sep="\t", names=["PlayerProfile"]
    )

    if os.path.exists("parsed.txt"):
        os.remove("parsed.txt")
    dfObj["PlayerProfile"] = playerDetails[playerDetails.columns[0]]

    soup = BeautifulSoup(driver.page_source)
    for item in soup.find_all("div", class_="table-data total-points"):
        [elem.extract() for elem in soup.find("div")]
        file = open("parsed.txt", "a")
        file.write(item.text)
        file.write("\n")

        file.close()
    playerDetails = pd.read_csv(
        "parsed.txt", encoding="ISO-8859-1", sep="\t", names=["TotalPoints"]
    )

    if os.path.exists("parsed.txt"):
        os.remove("parsed.txt")
    dfObj["TotalPoints"] = playerDetails[playerDetails.columns[0]]
    driver.get("https://www.prokabaddi.com/stats/0-21-successful-raids-statistics")
    soup = BeautifulSoup(driver.page_source)

    for item in soup.find_all("div", class_="table-data total-points"):
        [elem.extract() for elem in soup.find("div")]
        file = open("parsed.txt", "a")
        file.write(item.text)
        file.write("\n")

        file.close()
    playerDetails = pd.read_csv(
        "parsed.txt", encoding="ISO-8859-1", sep="\t", names=["Successful raids"]
    )
    if os.path.exists("parsed.txt"):
        os.remove("parsed.txt")
    dfObj["SuccessfulRaidPoints"] = playerDetails[playerDetails.columns[0]]
    driver.get("https://www.prokabaddi.com/stats/0-22-raid-points-statistics")
    soup = BeautifulSoup(driver.page_source)

    for item in soup.find_all("div", class_="table-data total-points"):
        [elem.extract() for elem in soup.find("div")]
        file = open("parsed.txt", "a")
        file.write(item.text)
        file.write("\n")

        file.close()
    playerDetails = pd.read_csv(
        "parsed.txt", encoding="ISO-8859-1", sep="\t", names=["raid points"]
    )

    if os.path.exists("parsed.txt"):
        os.remove("parsed.txt")
    dfObj["RaidPoints"] = playerDetails[playerDetails.columns[0]]
    driver.get("https://www.prokabaddi.com/stats/0-23-successful-tackles-statistics")
    soup = BeautifulSoup(driver.page_source)

    for item in soup.find_all("div", class_="table-data total-points"):
        [elem.extract() for elem in soup.find("div")]
        file = open("parsed.txt", "a")
        file.write(item.text)
        file.write("\n")

        file.close()
    playerDetails = pd.read_csv(
        "parsed.txt", encoding="ISO-8859-1", sep="\t", names=["successful tackles"]
    )

    if os.path.exists("parsed.txt"):
        os.remove("parsed.txt")
    dfObj["SuccessfulTackles"] = playerDetails[playerDetails.columns[0]]
    driver.get("https://www.prokabaddi.com/stats/0-103-tackle-points-statistics")
    soup = BeautifulSoup(driver.page_source)

    for item in soup.find_all("div", class_="table-data total-points"):
        [elem.extract() for elem in soup.find("div")]
        file = open("parsed.txt", "a")
        file.write(item.text)
        file.write("\n")

        file.close()
    playerDetails = pd.read_csv(
        "parsed.txt", encoding="ISO-8859-1", sep="\t", names=["tackle points"]
    )
    if os.path.exists("parsed.txt"):
        os.remove("parsed.txt")
    dfObj["TacklePoints"] = playerDetails[playerDetails.columns[0]]
    driver.get("https://www.prokabaddi.com/stats/0-22-avg-raid-points-statistics")
    soup = BeautifulSoup(driver.page_source)

    for item in soup.find_all("div", class_="table-data total-points"):
        [elem.extract() for elem in soup.find("div")]
        file = open("parsed.txt", "a")
        file.write(item.text)
        file.write("\n")

        file.close()
    playerDetails = pd.read_csv(
        "parsed.txt", encoding="ISO-8859-1", sep="\t", names=["avg. raid points"]
    )

    if os.path.exists("parsed.txt"):
        os.remove("parsed.txt")
    dfObj["AverageRaidPoints"] = playerDetails[playerDetails.columns[0]]
    driver.get("https://www.prokabaddi.com/stats/0-139-avg-tackle-points-statistics")
    soup = BeautifulSoup(driver.page_source)

    for item in soup.find_all("div", class_="table-data total-points"):
        [elem.extract() for elem in soup.find("div")]
        file = open("parsed.txt", "a")
        file.write(item.text)
        file.write("\n")

        file.close()
    playerDetails = pd.read_csv(
        "parsed.txt", encoding="ISO-8859-1", sep="\t", names=["avg. tackle points"]
    )

    if os.path.exists("parsed.txt"):
        os.remove("parsed.txt")
    dfObj["AverageTacklePoints"] = playerDetails[playerDetails.columns[0]]
    driver.get(
        "https://www.prokabaddi.com/stats/0-132-do-or-die-raid-points-statistics"
    )
    soup = BeautifulSoup(driver.page_source)

    for item in soup.find_all("div", class_="table-data total-points"):
        [elem.extract() for elem in soup.find("div")]
        file = open("parsed.txt", "a")
        file.write(item.text)
        file.write("\n")

        file.close()
    playerDetails = pd.read_csv(
        "parsed.txt", encoding="ISO-8859-1", sep="\t", names=["do or die points"]
    )
    if os.path.exists("parsed.txt"):
        os.remove("parsed.txt")
    dfObj["DODRaidPoints"] = playerDetails[playerDetails.columns[0]]
    driver.get("https://www.prokabaddi.com/stats/0-104-super-raids-statistics")
    soup = BeautifulSoup(driver.page_source)

    for item in soup.find_all("div", class_="table-data total-points"):
        [elem.extract() for elem in soup.find("div")]
        file = open("parsed.txt", "a")
        file.write(item.text)
        file.write("\n")

        file.close()
    playerDetails = pd.read_csv(
        "parsed.txt", encoding="ISO-8859-1", sep="\t", names=["super raids"]
    )
    if os.path.exists("parsed.txt"):
        os.remove("parsed.txt")
    dfObj["SuperRaids"] = playerDetails[playerDetails.columns[0]]
    driver.get("https://www.prokabaddi.com/stats/0-28-super-tackles-statistics")
    soup = BeautifulSoup(driver.page_source)

    for item in soup.find_all("div", class_="table-data total-points"):
        [elem.extract() for elem in soup.find("div")]
        file = open("parsed.txt", "a")
        file.write(item.text)
        file.write("\n")

        file.close()
    playerDetails = pd.read_csv(
        "parsed.txt", encoding="ISO-8859-1", sep="\t", names=["super tackles"]
    )
    if os.path.exists("parsed.txt"):
        os.remove("parsed.txt")
    dfObj["SuperTackles"] = playerDetails[playerDetails.columns[0]]
    driver.get("https://www.prokabaddi.com/stats/0-100-super-10s-statistics")
    soup = BeautifulSoup(driver.page_source)

    for item in soup.find_all("div", class_="table-data total-points"):
        [elem.extract() for elem in soup.find("div")]
        file = open("parsed.txt", "a")
        file.write(item.text)
        file.write("\n")

        file.close()
    playerDetails = pd.read_csv(
        "parsed.txt", encoding="ISO-8859-1", sep="\t", names=["super 10s"]
    )
    if os.path.exists("parsed.txt"):
        os.remove("parsed.txt")
    dfObj["Super10s"] = playerDetails[playerDetails.columns[0]]
    driver.get("https://www.prokabaddi.com/stats/0-101-high-5s-statistics")
    soup = BeautifulSoup(driver.page_source)

    for item in soup.find_all("div", class_="table-data total-points"):
        [elem.extract() for elem in soup.find("div")]
        file = open("parsed.txt", "a")
        file.write(item.text)
        file.write("\n")

        file.close()
    playerDetails = pd.read_csv(
        "parsed.txt", encoding="ISO-8859-1", sep="\t", names=["high 5s"]
    )
    if os.path.exists("parsed.txt"):
        os.remove("parsed.txt")
    dfObj["High5s"] = playerDetails[playerDetails.columns[0]]

    return dfObj
