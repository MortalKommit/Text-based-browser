# Text-based Browser
A simple web page scraper for non-javascript dependent sites demonstrating tag and content parsing with BeautifulSoup.  
Downloads tag contents into text files (saved pages). Uses a stack to navigate to previous 'saved pages'.  
No web crawling is involved in this program.

## Installation & Run
1. pip per the requirements file.
2. Provide a folder name to save pages.
3. Provide a site as input URL, e.g news.ycombinator.com.
4. Program parses tag content if it is of the type 'p', 'h1', 'h2', 'a', 'ul', 'ol' or 'li'.

