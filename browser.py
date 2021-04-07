import argparse
import os
import logging
from collections import deque
import requests
from requests import exceptions
from bs4 import BeautifulSoup, SoupStrainer
from colorama import Fore, Style


def chk_url_validity(url):
    if '.' not in url:
        return False

    return True


def chk_page_saved(url, dirname):
    return os.access(os.path.join(dirname, url), os.F_OK)


def save_browser_pages(arguments):
    os.makedirs(arguments.directory, exist_ok=True)

    page_requested = input()
    page_stack = deque()
    schema = "https://"

    while page_requested and page_requested != 'exit':
        # if back is entered, and browser history has more than 1 page, show previous
        if 'back' in page_requested:
            if len(page_stack) > 1:
                page_stack.pop()
                with open(page_stack[-1], encoding='utf-8') as f:
                    print(*f.readlines())
            elif len(page_stack) == 1:
                with open(page_stack[0], encoding='utf-8') as f:
                    print(*f.readlines())
            else:
                print('error : no page saved')
        # If the page hasn't been saved yet, and is valid (.suffix), try request
        if not chk_page_saved(page_requested, arguments.directory):
            if chk_url_validity(page_requested):
                try:
                    if not page_requested.startswith('https://'):
                        response = requests.get(schema + page_requested.replace('www.', ''))
                    else:
                        response = requests.get(page_requested)
                        response.encoding = 'utf-8'
                    soup = BeautifulSoup(response.content, 'html.parser', parse_only=SoupStrainer(allowed_tags))

                    with open(os.path.join(arguments.directory, page_requested.replace('www.', '')[:
                    page_requested.rfind('.')]), mode='w', encoding='utf-8') as f:
                        for tag in soup.find_all(allowed_tags):
                            if tag.name == 'a':
                                f.write(tag.get_text().strip())
                                print(Fore.BLUE + tag.get_text())
                            else:
                                print(Style.RESET_ALL)
                                print(tag.get_text().strip())
                            f.write(tag.get_text().strip(" "))
                        page_stack.append(f.name)
                except exceptions.InvalidURL as e:
                    print('error:', str(e))
                    logging.error(str(e))
                except exceptions.ConnectionError as e:
                    print('Error : Incorrect URL, Page does not exist')
                    logging.error(str(e))
            else:
                print("error: Incorrect URL")
        else:
            with open(os.path.join(arguments.directory, page_requested), encoding='utf-8') as f:
                print(*f.readlines())

        page_requested = input()


allowed_tags = ['p', 'h1', 'h2', 'a', 'ul', 'ol', 'li']
parser = argparse.ArgumentParser(description='Save article pages in a directory')
parser.add_argument('directory', help='directory to store webpage')
args = parser.parse_args()

save_browser_pages(args)
