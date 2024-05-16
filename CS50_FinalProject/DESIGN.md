# Design Document for Ivy League Draft Website

## Overview
The Ivy League FUT Draft Website is a platform that allows users to simulate the experience of building a team in a draft format using real players from the Ivy League universities. This document discusses the technical implementation of the project and the rationale behind key design decisions.

## Architecture
The website is built on a Flask framework, which is a Python-based web framework known for its simplicity and flexibility. Flask was chosen for its lightweight nature and because it allows for rapid development of web applications with the potential for scalability. The backend is powered by SQLite3, a serverless database engine, due to its ease of setup and sufficient capability to handle the expected load for this project.

## Database Design
The database schema consists of several SQL tables designed to store user information, player stats, and draft teams. We have tables for users, players, user team ratings, and player points, with relationships between them to allow for efficient queries. For example, player cards are generated from a combination of player information from the players table and a rating from the player points table. In addition, the users table keeps track of login information and the user ratings table keeps track of the leaderboard generated from the team ratings of saved teams.

## Web scraping
The player cards are dynamically created using data scraped from each Ivy League school's official athletics website. The decision to scrape this information was made to keep the data current and to automate the process of updating player statistics. Python libraries like BeautifulSoup and Requests are employed for web scraping because they are powerful yet user-friendly for parsing HTML documents. When scraping, we focused on
breaking down each college's roster into scrapeable segments by first realizing that each player’s information on the roster page is encapsulated in each row, so the find_all method was key in scraping player info. Unfortunately, this wasn’t the case for player stats, and we ended up having to scrape each column, and then integrating each individual player’s stats together with indexing to produce their rating.

## Player Rating Algorithm
HTML elements and then ca## Player Rating Algorithm
A custom algorithm was designed to assign ratings to players based on various statistics like goals scored, assists, games played, goals conceded, etc. The algorithm was also customized to fit the position of a given player. For example, the goals scored statistic was weighted more heavily for attackers compared to defenders and vice versa for the goals conceded statistic. The algorithm also took in to account potential special accolades from the season such as offensive player of the year, defensive player of the year, or being a part of an all Ivy team. Player rating boosts were assigned to players with such accolades. In the end, the algorithm calculates a base score from these stats, stat weights, and potential stat boosters and then provides a final rating in the range of 55 to 100. The decision to use a custom algorithm stems from the desire to have an accurate rating system that reflects the real life performances of players from the 2023 Ivy League season.

## Frontend Design
The frontend is built with HTML, CSS, and minimal boostrap. Each page within the site is an html page that extends a template called 'layout.html' so that each page includes a navigation bar and so the overall structure of each page is consistent. CSS was used extensively to organize elements within each page and make them look more visually appealing. For example, the "flex" feature allowed elements within a same class to appear side by side visually such as the player cards within the draft page while "color", "font-size", etc. were used to implement how text is displayed. CSS was also used to design each player card including where elements appear, how big they are, and how they are spaced.

## Security
User passwords are hashed before being stored in the database. Flask’s session management is used to handle user authentication and authorization. The decision to implement robust security measures is to protect user data and to ensure trust in the platform.

## Reflection
If we had more time or had thought it out more, we would have put the player ratings into the players table as another column. We didn’t scrape the stats at the same time as the player information, so we figured it was easier for us to create a new table named player ratings that just held the player’s name and his rating. However, it makes more sense to add the rating to the centralized player table to perhaps cross reference information.

Furthermore, web scraping for Princeton and Brown’s stats proved impossible and Yuta ended up manually typing up dictionaries for each college’s player stats. If we had more time, we would’ve tried harder to learn how to scrape websites that incorporated dynamic loading like Princeton and Brown (iframes).
