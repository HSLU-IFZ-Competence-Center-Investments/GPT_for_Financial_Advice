import os
import pandas as pd
import requests
from requests.exceptions import InvalidSchema
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from pywebcopy import save_webpage
from pywebcopy import save_website
# import SSLCertVerificationError
from ssl import SSLError
from ssl import SSLCertVerificationError
from urllib3.exceptions import MaxRetryError


def crawler(websites):

    # Download all the pages: https://github.com/rajatomar788/pywebcopy 

    # base path for saving the websites 
    base_path = r'C:\Users\levin\Documents\IFZ\GitHub\AI-and-Impact-Investing\CRAWLER' # REPLACE WITH YOUR OWN PATH
    general_error_dict = {}


    for website in websites['Website']:
        # get name of the website
        name = websites['Carbon Fund Companies'][websites['Website'] == website].values[0]
        # replace whitespace with underscore
        name = name.replace(' ', '_')
        # get website trunk without domain
        trunk = urlparse(website).netloc
        # strip www.
        trunk = trunk.replace('www.', '')
        # strip .com / .ch ; everthing after a dot
        trunk = trunk.split('.')[0]
        # print(trunk)

        general_error = 0

        # Check website
        response = requests.get(website)
        if response.status_code == 200:
            # create folder for website
            folder = os.path.join(base_path, name)
            if not os.path.exists(folder):
                os.makedirs(folder)
            # save webpage
            soup = BeautifulSoup(response.content, 'html.parser')
            links = soup.find_all('a', href=True)
            # print('Name, length of links: ', len(links))
            # # print links 1 - 10
            # for link in links[:10]:
            #     print(link['href'])    

            # save webpage
            for link in links:
                href = link['href']
                try:
                    if href.startswith('http'):
                        # download full website
                        save_webpage(
                            url=href,
                            project_folder=folder,
                            project_name=name,
                            bypass_robots=True,
                            debug=True,
                            open_in_browser=False,
                            delay=None,
                            threaded=False,
                        )
                    # if trunk in href download full website
                    if trunk in href:
                        print('Subpage:', href)
                        save_webpage(
                            url=href,
                            project_folder=folder,
                            project_name=name,
                            bypass_robots=True,
                            debug=True,
                            open_in_browser=False,
                            delay=None,
                            threaded=False,
                        )
                    if href.startswith('/'):
                        # download full website
                        print(website + href)
                        save_webpage(
                            url=website + href,
                            project_folder=folder,
                            project_name=name,
                            bypass_robots=True,
                            debug=True,
                            open_in_browser=False,
                            delay=None,
                            threaded=False,
                        )
                    else:
                        continue
                except TypeError as e:
                    print(f'Error: {e} for {href} of {website}')

                except InvalidSchema as e:
                    print(f'Error: {e} for {href} of {website}')

                except MaxRetryError as e:
                    print(f'Error: {e} for {href} of {website}')

                except SSLCertVerificationError as e:
                    print(f'Error: {e} for {href} of {website}')

                except SSLError as e:
                    print(f'Error: {e} for {href} of {website}')

                except Exception as e:
                    general_error += 1
                    print(f'Error: {e} for {href} of {website}')

            general_error_dict[website] = general_error

        else:
            print(f'Failed to download {website}')

    return general_error_dict


if __name__ == '__main__':
    # read websites.csv
    websites = pd.read_csv(r'C:\Users\levin\Documents\IFZ\GitHub\AI-and-Impact-Investing\CRAWLER\Carbon_Fund_websites.csv', sep=';') # REPLACE WITH YOUR OWN PATH
    # drop rows with NaN values
    websites = websites.dropna()
    general_error_dict = crawler(websites)
    print(general_error_dict)