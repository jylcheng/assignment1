# Title: Assignment 1: Data Scraping

# Description: In this assignment this script will be scraping data from multiple of sites. The categories that it'll be scraping
# for are "First Name", "Last Name", "University", "Deparatment" and the person's "Highest Education" (mainly PhD). 

# Notes  
# 1. There are about 4 different sites used.
# 2. There are some special characters that are used, like french/spanish letterings that I have yet to figure out how to translate
# 3. If you run this program, it will scrape the data from all of the site and put it into a csv file named "cheng_jessalyn_assignment1".
#    Each category has their own columns if you were to open it up in excel!


# Author:  Jessalyn Cheng
# Date:  April 23, 2015

import requests

from bs4 import BeautifulSoup

import csv
with open('cheng_jessalyn_assignment1', 'w') as myfile:

    #creates the columns/row
    fieldnames = ['First Name', 'Last Name', 'University', 'Department', 'Highest Education']
    writer = csv.DictWriter(myfile, fieldnames=fieldnames, extrasaction='raise', dialect='excel', delimiter='\t') 

    writer.writeheader()

    #Data Scraping Script for the Princeton CS Department Website
    url="https://www.cs.princeton.edu/people/faculty?type=main"
    r=requests.get(url)
    soup = BeautifulSoup(r.content)

    #person info all
    person_data = soup.find_all("div", {"class":"person"})

    for item in person_data:
        first_name = item.contents[3].find_all("h2", {"class":"person-name"})[0].text.split()[0]
        last_name = item.contents[3].find_all("h2", {"class":"person-name"})[0].text.split()[1];

        #Print the department which in this case is engineering
        university = soup.find_all("title")
        uni_dep = university[0].text.split(" | ")

        #split to dep and uni
        uni_dep2 = uni_dep[1].split("at ")
        dep = uni_dep2[0]
        uni = uni_dep2[1]

        #check for highest degree
        try:
            degree = " ".join(item.contents[3].find_all("div",{"class":"person-degree"})[0].text.split())
   

        #if no person-degree, then it'll write "N/A" 
        except IndexError:
            degree = 'N/A'

        #Will write the data onto the csv file
        writer.writerow({'First Name': (first_name.encode("UTF-8")), 'Last Name': last_name.encode("UTF-8"),'University':uni.encode("UTF-8"), 'Department':dep.encode("UTF-8"), 'Highest Education':degree.encode("UTF-8")})

    #Data Scraping Script for the Cornell CS Department Website
    url="https://www.cs.cornell.edu/people/faculty"
    r =requests.get(url)
    soup = BeautifulSoup(r.content)

    person_data = soup.find_all("div", {"class":"person"})

    for item in person_data:
        lists = item.find_all("h2")[0].text.split()

        #Finds the first name and the last name of the faculty people. There are some special cases, where some people might
        #have an middle initial in theirs.
        if len(lists) == 3:
            first_name = lists[0] + " " + lists[1]
            last_name = lists[2]

        else:
            first_name = lists[0]
            last_name = lists[1]

        #Pulls information about the University/Department from the title of the website
        departmentpull = soup.find_all("title")
        department = departmentpull[0].text.split(" | ")
        
        info = item.find_all("p")
        meow = info[0].text.strip().split('\n')

        #looks for the degree of the faculty member
        for stuff in meow:
            if 'Ph.D.' in stuff:
                degree = stuff.strip()

        #Will write the data onto the csv file            
        writer.writerow({'First Name': first_name.encode("UTF-8"), 'Last Name': last_name.encode("UTF-8"),'University':'Cornell University'.encode("UTF-8"), 'Department':department[1].encode("UTF-8"), 'Highest Education':degree.encode("UTF-8")})

    #Princeton Economics
    url="http://www.princeton.edu/economics/faculty-members/"
    r=requests.get(url)
    soup = BeautifulSoup(r.content)

    #person info all
    person_data = soup.find_all("div",{"class":"body"})

    listing = person_data[0].find_all("tr")
    #print listing

    for person in listing:
        lists = person.find_all("strong")[0].text.split()

        #Finds the first name and the last name of the faculty people. There are some special cases, where some people might
        #have an middle initial in theirs.
        if len(lists) == 3:
            first_name = lists[0] + " " + lists[1]
            last_name = lists[2]
        elif len(lists)==2:
            first_name = lists[0]
            last_name = lists[1]
        
        #Looks for the degree
        people = person.find_all("em")

        if len(people) == 1:
            degree = people[0].text.strip()

        #Will write the data onto the csv file
        writer.writerow({'First Name': first_name.encode("UTF-8"), 'Last Name': last_name.encode("UTF-8"),'University':'Princeton University'.encode("UTF-8"), 'Department':'Department of Economics'.encode("UTF-8"), 'Highest Education':degree.encode("UTF-8")})

  
