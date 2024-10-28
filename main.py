
import chrome
import firefox
from colorama import Fore, Style, init
import os

# Initialize colorama for Windows support
init(autoreset=True)

def clear_screen():
    # Clear screen for Windows and Unix-like systems
    os.system("cls" if os.name == "nt" else "clear")

def display_banner():
    banner = r"""

███╗   ██╗ ██████╗     ███╗   ███╗ ██████╗ ██████╗ ███████╗    ███████╗███████╗ ██████╗██████╗ ███████╗████████╗███████╗
████╗  ██║██╔═══██╗    ████╗ ████║██╔═══██╗██╔══██╗██╔════╝    ██╔════╝██╔════╝██╔════╝██╔══██╗██╔════╝╚══██╔══╝██╔════╝
██╔██╗ ██║██║   ██║    ██╔████╔██║██║   ██║██████╔╝█████╗      ███████╗█████╗  ██║     ██████╔╝█████╗     ██║   ███████╗
██║╚██╗██║██║   ██║    ██║╚██╔╝██║██║   ██║██╔══██╗██╔══╝      ╚════██║██╔══╝  ██║     ██╔══██╗██╔══╝     ██║   ╚════██║
██║ ╚████║╚██████╔╝    ██║ ╚═╝ ██║╚██████╔╝██║  ██║███████╗    ███████║███████╗╚██████╗██║  ██║███████╗   ██║   ███████║
╚═╝  ╚═══╝ ╚═════╝     ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝    ╚══════╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝
                                                                    
                                                By 3ls3if (Rohan Das)                                       
                                                                
    """
    print(Fore.MAGENTA + Style.BRIGHT + banner + Style.RESET_ALL)
    print(Fore.YELLOW + "[i] Extract saved passwords from Chrome and Firefox browsers" + Style.RESET_ALL)
    print(Fore.CYAN + "=" * 60 + Style.RESET_ALL)

def display_passwords(browser_name, passwords):
    if passwords:
        print(f"{Fore.YELLOW}{Style.BRIGHT}[i] Passwords from {browser_name}:{Style.RESET_ALL}")
        for entry in passwords:
            print(f"{Fore.GREEN}[+] URL: {Fore.WHITE}{entry['url']}")
            print(f"{Fore.GREEN}[+] Username: {Fore.WHITE}{entry['username']}")
            print(f"{Fore.GREEN}[+] Password: {Fore.WHITE}{entry['password']}")
            print(f"{Fore.CYAN}{'-' * 40}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}[!] No passwords found for {browser_name}.{Style.RESET_ALL}")

def main():

    
    while True:
        clear_screen()
        display_banner()
        print(Fore.MAGENTA + Style.BRIGHT + "\n[+] Select an option:" + Style.RESET_ALL)
        print(f"{Fore.YELLOW}[1] Extract Chrome passwords")
        print(f"{Fore.YELLOW}[2] Extract Firefox passwords")
        print(f"{Fore.YELLOW}[3] Exit{Style.RESET_ALL}")
        
        choice = input(Fore.CYAN + "\n[+] Enter your choice (1, 2, or 3): " + Style.RESET_ALL)
        
        if choice == "1":
            try:
                print(f"\n{Fore.MAGENTA}{Style.BRIGHT}Extracting Chrome passwords...{Style.RESET_ALL}\n")
                chrome_passwords = chrome.extract_and_save_passwords()
                display_passwords("Chrome", chrome_passwords)
                input("\n\n[+] Please press enter to continue...")
            except Exception as e:
                print(f"{Fore.RED}[ERROR] Chrome password extraction failed: {e}{Style.RESET_ALL}")
                input("\n\n[+] Please press enter to continue...")

        elif choice == "2":
            try:
                print(f"\n{Fore.MAGENTA}{Style.BRIGHT}Extracting Firefox passwords...{Style.RESET_ALL}\n")
                firefox_passwords = firefox.firefox_decrypt()
                display_passwords("Firefox", firefox_passwords)
                input("\n\n[+] Please press enter to continue...")
            except Exception as e:
                print(f"{Fore.RED}[ERROR] Firefox password extraction failed: {e}{Style.RESET_ALL}")
                input("\n\n[+] Please press enter to continue...")

        elif choice == "3":
            print(Fore.GREEN + "\n[+] Exiting..." + Style.RESET_ALL)
            break

        else:
            print(Fore.RED + "[!] Invalid choice! Please enter 1, 2, or 3." + Style.RESET_ALL)

if __name__ == "__main__":
    main()



