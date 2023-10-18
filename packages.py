import argparse
import json
import paramiko
import getpass

def load_distribution_commands():
    try:
        with open('distributions.json', 'r') as file:
            data = json.load(file)
            return data.get('distributions', {})
    except FileNotFoundError:
        print("File 'distributions.json' not found.")
        return {}

def get_distribution_name_ssh(hostname, username, password):
    try:
        # Create an SSH client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Connect to the server
        client.connect(hostname, username=username, password=password)
        
        # Try to get the distribution name from /etc/os-release
        stdin, stdout, stderr = client.exec_command("cat /etc/os-release")
        os_release_info = stdout.read().decode('utf-8')
        
        # Try to extract the distribution name from /etc/os-release
        distribution_name = None
        for line in os_release_info.split('\n'):
            if line.startswith('PRETTY_NAME='):
                pretty_name = line.split('=')[1].strip('"\n')
                distribution_name = pretty_name.split()[0]
                break
        
        # If /etc/os-release does not contain information, try /etc/issue
        if not distribution_name:
            stdin, stdout, stderr = client.exec_command("cat /etc/issue")
            distribution_name = stdout.read().strip().decode('utf-8').split()[0]
        
        # Get the corresponding package command for the distribution
        package_commands = load_distribution_commands()
        package_command = package_commands.get(distribution_name.lower(), "N/A")
        
        # Get the package information
        if package_command != "N/A":
            stdin, stdout, stderr = client.exec_command(package_command)
            package_info = stdout.read().decode('utf-8')
        else:
            package_info = "Failed to retrieve package information for this distribution."
        
        # Close the connection
        client.close()
        
        return distribution_name, package_info
    except paramiko.AuthenticationException:
        return "Failed to authenticate. Invalid credentials.", ""
    except paramiko.SSHException:
        return "Failed to establish SSH connection.", ""
    except Exception as e:
        return "An error occurred: " + str(e), ""

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Retrieve distribution and package information from a remote server.")
    parser.add_argument("ip_address", type=str, help="IP address of the remote server")
    parser.add_argument("-o", "--output", choices=['p', 'w'], default='p', help="Output mode: 'p' for print, 'w' for write to file (default: print)")
    parser.add_argument("-f", "--filename", type=str, help="Output filename (without extension)")
    
    # Parse the arguments and show help if needed
    args, unknown = parser.parse_known_args()
    
    # Show help if there are unknown arguments or no IP address provided
    if unknown or not args.ip_address:
        parser.print_help()
        exit(1)
    
    # Prompt for username and password
    username = input("Enter your SSH username: ")
    password = getpass.getpass("Enter your SSH password: ")
    
    # Set SSH connection details
    hostname = args.ip_address
    
    # Determine the filename
    filename = args.filename if args.filename else "package_info"
    filename += ".txt"
    
    # Get distribution name and package information
    distribution_name, package_info = get_distribution_name_ssh(hostname, username, password)
    
    # Process output based on the chosen mode
    if args.output == 'p':
        # Print the results
        if distribution_name:
            print("Distribution: {}".format(distribution_name))
        else:
            print("Failed to retrieve the distribution name.")
        
        if package_info:
            print("\nInstalled Packages Information:")
            print(package_info)
        else:
            print("Failed to retrieve installed package information.")
    elif args.output == 'w':
        # Write to a file
        with open(filename, 'w') as file:
            file.write("Distribution: {}\n".format(distribution_name))
            file.write("\nInstalled Packages Information:\n")
            file.write(package_info)
        print("Information written to '{}'.".format(filename))


