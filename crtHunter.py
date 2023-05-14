#!/usr/bin/env python3
# Import required libraries
import re
import requests
from bs4 import BeautifulSoup
import argparse
import sys
from colorama import init, Fore, Style

# Initialize colorama for colored terminal output
init(autoreset=True)

# Define the banner to be displayed when the script is run
BANNER = r'''

                  _     _                             
             _   | |   | |            _               
  ____  ____| |_ | |__ | |_   _ ____ | |_  ____  ____ 
 / ___)/ ___|  _)|  __)| | | | |  _ \|  _)/ _  )/ ___)
( (___| |   | |__| |   | | |_| | | | | |_( (/ /| |    
 \____|_|    \___|_|   |_|\____|_| |_|\___\____|_|    
                                                      

               Coded by Hazem Elsayed
               @Zoma0x00
'''

# Function to extract subdomains using RegEx
def extract_subdomains(text, domain):
    subdomains = set()
    regex = re.compile(r'\b(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+' + re.escape(domain) + r'\b')
    matches = regex.findall(text)
    for match in matches:
        subdomains.add(match)
    return subdomains

# Function to get subdomains from crt.sh
def get_subdomains_crtsh(domain):
    subdomains = set()
    url = f"https://crt.sh/?q=%.{domain}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Error: {str(e)}")
        return subdomains

    subdomains.update(extract_subdomains(response.text, domain))
    return subdomains

# Function to save subdomains to a file
def save_subdomains(subdomains, output_file):
    with open(output_file, "w") as f:
        for subdomain in subdomains:
            f.write(subdomain + "\n")

# Main function that runs the script
def main(domain, output_file):
    print(Fore.CYAN + "Extracting subdomains from crt.sh now...")
    subdomains = get_subdomains_crtsh(domain)

    subdomain_count = len(subdomains)

    if subdomain_count > 0:
        print(Fore.GREEN + f"[§]Found {subdomain_count} unique subdomains for {domain}")

        if output_file:
            save_subdomains(subdomains, output_file)
            print(Fore.GREEN + f"[§]Subdomains saved to {output_file}")
        else:
            print(Fore.RED + "Subdomains:")
            for subdomain in subdomains:
                print(Fore.GREEN + subdomain)
    else:
        print(Fore.RED + f"No subdomains found for {domain}")

    print(Fore.CYAN + f"Total number of subdomains: {subdomain_count}")

# The entry point of the script
if __name__ == "__main__":
    print(Fore.CYAN + BANNER)

    # Define command-line argument parser
    parser = argparse.ArgumentParser(description=Fore.YELLOW + Style.BRIGHT + "Find subdomains of a domain.")
    parser.add_argument("-d", "--domain", required=True, help=Fore.YELLOW + "The target domain.")
    parser.add_argument("-o", "--output_file", required=False, help=Fore.RED + "The file to store subdomains into (optional).")

    # Check if there are any arguments provided
    if len(sys.argv) == 1:
        print(Fore.YELLOW + parser.description)
        print(Fore.CYAN + "Usage: python crt.py -d DOMAIN [-o OUTPUT_FILE]")
        sys.exit(1)

    # Parse the command-line arguments and run the main function
    args = parser.parse_args()
    main(args.domain, args.output_file)