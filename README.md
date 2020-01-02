# youtube-takeout-processor-
Two python scripts to take a bunch of html files containing youtube watch history and dump it into a sqlite3 database file

beware there may be some unfixed uncommented spaghetti code ahead, but feel free to have a cheeky look

## How to use
- Download your google takeout (you only need to select youtube history) and extract them
- Do this every few months just in case. I have found that they typically store the watch history for
about a year and a half 
- Store the entire takeout file in the folder takeouts, such that file hierachy will look like this.


- run the datacompiler.py
