"""Movies Web Scraper

This script allows users to extract information about a movie's ratings and details from IMDb. 
The data is organized and returned in a comma-separated values file (results.csv). 
Users should list movie titles, with each movie on a new line, in the text file (movies.txt).  

This file contains the following functions:

    * getUrl - returns the URL of the movie page
    * getInfo - returns the details of the movie

"""

from bs4 import BeautifulSoup
import requests
import csv

def getUrl(movieName):
  """Return the URL of the movie page given movie name.
  
  Args: 
      movieName: the movie to get the URL of
  Returns:
      The URL of the movie
  """
  search = 'http://www.imdb.com/find?q=' + movieName
  response = requests.get(search)
  soup = BeautifulSoup(response.text, 'html.parser')
  result = soup.find('table', class_ = 'findList')
  url = 'http://www.imdb.com' + result.find('a').get('href')
  return url

def getInfo(movieName):
  """Return details of the movie given its name.
  
  Args: 
      movieName: the movie to get the details of
  Returns:
      The details of the movie
  """
  url = getUrl(movieName)
  response = requests.get(url)
  soup = BeautifulSoup(response.text, 'html.parser')
  
  title = soup.find('h1', attrs = {'data-testid': 'hero-title-block__title'})
  score = soup.find(class_ = 'AggregateRatingButton__RatingScore-sc-1ll29m0-1 iTLWoV')
  blurb = soup.find('span', class_ = 'GenresAndPlot__TextContainerBreakpointXS_TO_M-cum89p-0 dcFkRD')
  genreList = soup.find('div', attrs = {'data-testid': 'genres'})
  genres = genreList.find_all('span', class_ = 'ipc-chip__text')

  info = [title.text if title else movieName,score.text if score else 'N/A', ', '.join(genre.text for genre in genres), blurb.text, url]

  return info

header = ['Title', 'Score', 'Genre', 'Description', 'Link']

# read in movies from txt file, get movie info, and write to csv file
with open('results.csv', 'w') as log:
  writer = csv.writer(log)
  writer.writerow(header)

  with open('movies.txt', 'r') as file:
    for line in file:
      row = getInfo(line)
      writer.writerow(row)
