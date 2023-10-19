# PackageHunter

The PackageHunter is a Python script that connects to a remote server via SSH and retrieves the distribution name and package information from the server. It provides the option to either print the information to the console or write it to a text file.

## Table of Contents

- [PackageHunter](#packagehunter)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Requirements](#requirements)
  - [Usage](#usage)
  - [Configuration](#configuration)
  - [License](#license)

## Features

- Retrieves the distribution name and package information from a remote server.
- Provides options to print the information to the console or write it to a text file.
- Checks server availability before attempting an SSH connection.
- Supports customizable output filenames.

## Requirements

- Python 3.x
- Paramiko (SSH library for Python)
- `distributions.json` configuration file (see Configuration section)

To install the required dependencies, you can use pip:

```shell
pip install paramiko
```
## Usage

To use the script, follow these steps:

1. Clone the repository:

```shell
git clone https://github.com/trojkry/Get-packages-from-server.git
```

2. Navigate to the script's directory.
3. Run the script with desired options:
    -To print informations to the console

```shell
python3 packages.py <ip_address>
```

-To write the information to a text file (customizable filename):

```shell
python3 packages.py <ip_address> -o w -f <custom_filename>

```
Replace <ip_address> with the IP address of the remote server.
4. The script will prompt you for your SSH username and password, and then it will connect to the server and retrieve the requested information.

## Configuration
The script uses a distributions.json configuration file to map Linux distribution names to the corresponding package retrieval commands. You can customize this file to add or modify distribution-specific commands.

Example distributions.json file:
```shell
{
  "distributions": {
    "ubuntu": "dpkg -l",
    "centos": "rpm -qa"
  }
}

```

## License

This script is open-source and available under the MIT License.
