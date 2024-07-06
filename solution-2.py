import time
import pandas as pd
import requests
from urllib.parse import urlparse
import json
import asyncio

CSV_FILE = 'contracts.csv'
GITHUB_TOKEN = 'use your github token here'



async def call_for_file_names(contract_address):
    ETHERSCAN_API_KEY ='use your etherscan token here'
    url = f"https://api.etherscan.io/api?module=contract&action=getsourcecode&address={contract_address}&apikey={ETHERSCAN_API_KEY}"

    print(f"Fetching contract : {contract_address}")
    try:
        response = await asyncio.get_event_loop().run_in_executor(None, lambda: requests.get(url))
        data = response.json()
        if data.get("status") != "1":
            raise ValueError("Smart Contract not verified on Etherscan")

        source_code = data["result"][0]["SourceCode"]
        try:
            source_code = source_code[1:-1]
            source_code = json.loads(source_code)
            json_verified_files = [filename.strip('/').split('/')[-1] for filename in source_code["sources"]]
        except json.JSONDecodeError:
            json_verified_files = [f"{data["result"][0]["ContractName"]}.sol"]


        return json_verified_files

    except Exception as e:
        print(f"Error fetching contract source code: {str(e)}")
        return []

def extract_org_and_repo_from_url(url):
    """
    Extracts organization name and repository name from a GitHub URL.
    Returns (org_name, repo_name) tuple or None if extraction fails.
    """
    parsed_url = urlparse(url)
    path_components = parsed_url.path.strip('/').split('/')
    if parsed_url.netloc == 'github.com':
        if len(path_components) >= 2:
            org_name = path_components[0]
            repo_name = path_components[1]
            return org_name, repo_name
    
    return None, None




def search_github_files_in_org(repolink, filename):
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }

    org_name, repo_name = extract_org_and_repo_from_url(repolink)

    url = f"https://api.github.com/search/code?q={filename}+org:{org_name}+in:path"

    print(f"Searching {filename} in organization {org_name}")
    try:
        while True:
            response = requests.get(url, headers=headers)
            
            # git hub rate limitation handling
            if response.status_code == 403:
                reset_time = int(response.headers['X-RateLimit-Reset'])
                wait_time = max(reset_time - time.time(), 5)  # Wait at least 5 seconds
                print(f"Rate limit exceeded. Waiting for {wait_time} seconds before retrying.")
                time.sleep(wait_time)
                continue
            
            response.raise_for_status()

            # Parse JSON response
            results = response.json()

            file = None
            for item in results.get('items', []):
                if filename.lower() in item['name'].lower():
                    file = item['html_url']
                    print(f"Got {filename} at {file}")
                    return file
            
            print(f"No match found for {filename} in organization {org_name}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from GitHub API: {e}")
        return None



def search_github_files( source_url,filename):
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }

    org_name, repo_name = extract_org_and_repo_from_url(source_url)

    url = f"https://api.github.com/search/code?q=filename:{filename}+org:{org_name}+repo:{org_name}/{repo_name}+in:path"


    print(f"Searching {filename}")
    try:
        while True:
            response = requests.get(url, headers=headers)
            
            # Handle rate limit exceeded
            if response.status_code == 403:
                reset_time = int(response.headers['X-RateLimit-Reset'])
                wait_time = max(reset_time - time.time(), 5)  
                print(f"Rate limit exceeded. Waiting for {wait_time} seconds before retrying.")
                time.sleep(wait_time)
                continue
            
            response.raise_for_status()

            # Parse JSON response
            results = response.json()

            file = None
            for item in results.get('items', []):
                if item['name'].lower() == filename.lower(): 
                    file = item['html_url']
            if not file is None:
                print(f"Got {filename} at {file}")
            return file

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from GitHub API: {e}")
        return None




async def process_addresses():
    file_data = pd.read_csv(CSV_FILE)

    for index, row in file_data.iterrows():
        contract_address = row['Smart Contract Address']
        repo_link = row['Repo Link']
        file_names = await call_for_file_names(contract_address)
        github_urls = []
        
        for file_name in file_names:
            file_found = search_github_files(repo_link, file_name)
            if file_found:
                github_urls.append(file_found)
            else:
                file_found_in_org   = search_github_files_in_org(repo_link, file_name)
                if file_found_in_org:
                    github_urls.append(file_found_in_org)
            
        if github_urls:
            file_data.at[index, 'Solidity_File_Names'] = ', '.join(file_names)
            file_data.at[index, 'GitHub_URLs'] = ', '.join(github_urls)

    file_data.to_csv(CSV_FILE, index=False)

if __name__ == '__main__':
    asyncio.run(process_addresses())
