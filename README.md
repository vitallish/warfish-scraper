# warfish-scraper

## Introduction

This repository contains the code to scrape data off of warfish.net.

## Getting Started

This projects uses `poetry` to manage dependencies. 

1. Install poetry as described [in their instructions](https://python-poetry.org/docs/)
2. Switch to the working directory for this project and run the following in your terminal:
```bash
poetry install
```
3. See `warfish_example.py` for an example.

## Features

### Current

- Login to warfish automatically through a script
- Get a list of all games played
- Download game summaries

### Planned

- Download all turns taken in a game (both finished and active)
- Summarise data into flat files 
- Calculate expected and actual outcomes from an attack
