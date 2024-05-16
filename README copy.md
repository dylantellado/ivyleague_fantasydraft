# Ivy League Fantasy Draft Website

## Link to Video Demonstration
https://youtu.be/WuBXXSHmV_c

## Introduction
This project is a web-based implementation of FIFA's FUT Draft game mode with an Ivy League twist. Users can create an account, draft their own team, and compete in a leaderboard ranking.

## Features
- **User Accounts**: Secure sign-up and authentication system to manage user sessions.
- **Team Drafting**: Users can draft their team from a roster of Ivy League players from the 2023 season.
- **Player Ratings**: Players are rated using an algorithm that evaluates their real life performance data from the 2023 season.
- **Dynamic Player Cards**: Player information is displayed on cards created by scraping Ivy League school websites.
- **Player Search**: Users can search for Ivy League players by name to view their cards and stats.
- **Save Drafted Team**: Users can save their drafted teams for future reference.
- **Leaderboard**: Features a leaderboard displaying the teams with the highest ratings, including usernames and team ratings, sorted from highest to lowest.
- **Season Standings**: Users can view the standings from the 2023 Ivy League season through an embeded site

## Setup and Installation
1. Unzip the file.
2. Install the required Python packages with `pip install pycountry'.
3. Start the Flask server using `flask run`.
4. Access the website by navigating to the link displayed after 'Running on' in your terminal.

## Usage
- Sign up for an account and log in.
- Use the search feature to find and view player cards.
- Navigate to the draft page to draft your team and save it to your profile.
- Check the leaderboard to see how your team compares to others.

## Technologies Used
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python with Flask
- **Database**: SQLite3
- **Web Scraping**: Python libraries such as BeautifulSoup and Requests
- **Deployment**: TBD



