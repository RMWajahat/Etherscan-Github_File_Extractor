# Smart Contract Source Code Finder

This Python script automates the process of fetching Solidity files associated with Ethereum smart contracts and finding them on GitHub. It utilizes Etherscan API to fetch the contract source code and GitHub API to search for corresponding files in specified repositories or organizations.

## Prerequisites

To run this script, you'll need:

- **Python**: Ensure Python 3.7 or higher is installed. You can download it from [python.org](https://www.python.org/downloads/).

## Installation

1. **Download the Script**: 
   - Download the `solution-2.py` script from the provided .zip file.

2. **Navigate to the Script Directory**: 
   - Extract the contents of the .zip file to a directory of your choice.

3. **Install Required Python Packages**: 
   - Open a terminal or command prompt.
   - Navigate to the directory where `solution-2.py` is located.
   - Run the following command to install necessary packages:

     ```
     pip install pandas requests
     ```

     - **pandas**: Library for data manipulation and analysis.
     - **requests**: HTTP library for making requests to APIs.

## Configuration

Before running the script, ensure you have set up the necessary configurations:

- **GitHub Token**: Obtain a personal access token from GitHub with appropriate permissions (e.g., read access to repositories).
- **Etherscan API Key**: Generate an API key from Etherscan for accessing Ethereum smart contract information.

Update the following variables in `solution-2.py`:

- `GITHUB_TOKEN`: Replace `'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'` with your GitHub token.
- `ETHERSCAN_API_KEY`: Replace `'ASFQBS9HQGTZUT1AQIIYA8QPZRHIY7AI1M'` with your Etherscan API key.

**You can use these for your testing or use your own (optional)**


## Running the Script

To execute the script:

1. Open a terminal or command prompt.
2. Navigate to the directory where `solution-2.py` is located.
3. Run the following command:

`python solution-2.py`


The script will read input from `contracts.csv` in same directory, fetch Solidity files associated with each contract address using Etherscan API, and search for these files on GitHub. It updates `contracts.csv` with the found GitHub URLs and Solidity file names.

## Notes

- If the GitHub API rate limit is exceeded, the script will wait and retry automatically.
- Errors encountered during API requests or data parsing will be logged, ensuring the process continues without interruption.
