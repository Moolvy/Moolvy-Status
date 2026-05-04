import requests
import sys
from colorama import init, Fore, Style
from concurrent.futures import ThreadPoolExecutor, as_completed

init(autoreset=True)


def check_domain(domain: str):
    url = f"https://{domain}"
    try:
        response = requests.get(url, timeout=4, allow_redirects=True)
        if response.status_code == 200:
            print(f"{domain:<25} {Fore.GREEN}[OK] ONLINE{Style.RESET_ALL}")
            return True
        else:
            print(f"{domain:<25} {Fore.YELLOW}[!] HTTP {response.status_code}{Style.RESET_ALL}")
            return False
    except requests.exceptions.RequestException:
        print(f"{domain:<25} {Fore.RED}[-] OFFLINE{Style.RESET_ALL}")
        return False


def main():
    if len(sys.argv) > 1:
        target = sys.argv[1].strip().lower()
    else:
        target = input("Enter domain or name (e.g. google): ").strip().lower()

    if not target:
        print(f"{Fore.RED}[!] Error: No target provided.{Style.RESET_ALL}")
        return

    extensions = [".com", ".me", ".org", ".net", ".io", ".ru", ".tv", ".app", ".store", ".info"]

    if "." in target:
        to_check = [target]
    else:
        to_check = [target + ext for ext in extensions]

    print(f"\n{Fore.CYAN}[!] Analyzing: {target}{Style.RESET_ALL}")
    print("-" * 50)

    success_count = 0
    with ThreadPoolExecutor(max_workers=len(to_check)) as executor:
        futures = {executor.submit(check_domain, domain): domain for domain in to_check}
        for future in as_completed(futures):
            if future.result():
                success_count += 1

    print("-" * 50)
    print(f"{Fore.GREEN}[+] Scan complete. Active hosts found: {success_count}{Style.RESET_ALL}")


if __name__ == "__main__":
    main()

