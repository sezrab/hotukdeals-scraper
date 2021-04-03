from bs4 import BeautifulSoup
import requests
import webbrowser

def getDeals(cat,page):
    dealsList=[]

    url="https://www.hotukdeals.com/{}?page={}".format(cat,page)
    soup = BeautifulSoup(requests.get(url).content,"html5lib")
    
    deals = soup.find_all("article")
    for deal in deals:
        if "thread--expired" in deal["class"]:
            continue
        linkElement = deal.find("a",{"class":"thread-title--list"})
        title = linkElement["title"]
        try:
            href = deal.find("a",{"class":"cept-dealBtn"})["href"]
            price = deal.find("span",{"class":"thread-price"}).text
        except (AttributeError, TypeError):
            continue
        
        if price == "FREE":
            price = 0
        else:
            try:
                price = float(price[1:].replace(",",""))
            except ValueError:
                # print("ERROR: couldn't parse price",price)
                continue

        dealsList.append([title,price,href])
    return dealsList

def maxPrice(li,maxp):
    index = 0
    for item in li:
        index += 1
        if item[1] > maxp:
            break
    return li[:index-1]

def numSort(li):
    return sorted(li, key = lambda x: x[1]) # https://www.geeksforgeeks.org/python-sort-list-according-second-element-sublist/

def keyFilter(keywords,items):
    filteredList = []
    for item in items:
        if any(key.lower() in item[0].lower() for key in keywords):
            filteredList.append(item)
    return numSort(filteredList)

def getInputs(prompt):
    print("Ctrl+C to finish submitting keywords")
    inputs=[]
    while True:
        try:
            inputs.append(input(prompt))
        except KeyboardInterrupt:
            break
    return inputs

def printList(li):
    count = 0
    for item in li:
        count+=1
        print(str(count)+")","£"+str(item[1]),"-",item[0])

n = int(input("Scrape results from how many pages: "))
cat=input("Category [hot/new] (leave blank for default): ").lower()

print("Loading...")
deals = []
for i in range(1,n):
    deals.extend(getDeals(cat, i+1))
sortedDeals = numSort(deals)
print("Done")
while True:
    print()
    menuDict = {
        "K":"Keyword filter",
        "P":"Price filter",
        "D":"Display results",
        "G":"Go to number"
    }
    for key in menuDict:
        print(key,":",menuDict[key])
    print()
    option = input("Select option: ").lower()
    if option == "k":
        keywords = getInputs("Add a keyword: ")
        sortedDeals = keyFilter(keywords, deals)
    elif option == "p":
        sortedDeals = maxPrice(numSort(deals), float(input("Max price: ")))
    elif option == "d":
        printList(sortedDeals)
    elif option == "g":
        index = int(input("Number: "))
        webbrowser.open_new_tab(requests.get(sortedDeals[index-1][2]).url)
