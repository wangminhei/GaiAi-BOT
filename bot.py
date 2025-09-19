from aiohttp import (
    ClientResponseError,
    ClientSession,
    ClientTimeout,
    BasicAuth
)
from aiohttp_socks import ProxyConnector
from fake_useragent import FakeUserAgent
from eth_account import Account
from eth_account.messages import encode_defunct
from eth_utils import to_hex
from datetime import datetime, timezone
from colorama import *
import asyncio, random, time, json, re, os, pytz

wib = pytz.timezone('Asia/Jakarta')

class GaiAI:
    def __init__(self) -> None:
        self.BASE_API = "https://api.metagaia.io/api"
        self.REF_CODE = "63R39E" # U can change it with yours.
        self.HEADERS = {}
        self.proxies = []
        self.proxy_index = 0
        self.account_proxies = {}
        self.tona_tokens = {}

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def welcome(self):
        print(
            f"""
        {Fore.GREEN + Style.BRIGHT}Gai AI {Fore.BLUE + Style.BRIGHT}Auto BOT
            """
            f"""
        {Fore.GREEN + Style.BRIGHT}Rey? {Fore.YELLOW + Style.BRIGHT}<INI WATERMARK>
            """
        )

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    
    async def load_proxies(self):
        filename = "proxy.txt"
        try:
            if not os.path.exists(filename):
                self.log(f"{Fore.RED + Style.BRIGHT}File {filename} Not Found.{Style.RESET_ALL}")
                return
            with open(filename, 'r') as f:
                self.proxies = [line.strip() for line in f.read().splitlines() if line.strip()]
            
            if not self.proxies:
                self.log(f"{Fore.RED + Style.BRIGHT}No Proxies Found.{Style.RESET_ALL}")
                return

            self.log(
                f"{Fore.GREEN + Style.BRIGHT}Proxies Total  : {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{len(self.proxies)}{Style.RESET_ALL}"
            )
        
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}Failed To Load Proxies: {e}{Style.RESET_ALL}")
            self.proxies = []

    def check_proxy_schemes(self, proxies):
        schemes = ["http://", "https://", "socks4://", "socks5://"]
        if any(proxies.startswith(scheme) for scheme in schemes):
            return proxies
        return f"http://{proxies}"

    def get_next_proxy_for_account(self, account):
        if account not in self.account_proxies:
            if not self.proxies:
                return None
            proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
            self.account_proxies[account] = proxy
            self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return self.account_proxies[account]

    def rotate_proxy_for_account(self, account):
        if not self.proxies:
            return None
        proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
        self.account_proxies[account] = proxy
        self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return proxy
    
    def build_proxy_config(self, proxy=None):
        if not proxy:
            return None, None, None

        if proxy.startswith("socks"):
            connector = ProxyConnector.from_url(proxy)
            return connector, None, None

        elif proxy.startswith("http"):
            match = re.match(r"http://(.*?):(.*?)@(.*)", proxy)
            if match:
                username, password, host_port = match.groups()
                clean_url = f"http://{host_port}"
                auth = BasicAuth(username, password)
                return None, clean_url, auth
            else:
                return None, proxy, None

        raise Exception("Unsupported Proxy Type.")
        
    def generate_address(self, account: str):
        try:
            account = Account.from_key(account)
            address = account.address

            return address
        except Exception as e:
            return None
    
    def generate_payload(self, account: str, address: str, nonce: str):
        try:
            encoded_message = encode_defunct(text=nonce)
            signed_message = Account.sign_message(encoded_message, private_key=account)
            signature = to_hex(signed_message.signature)

            timestamp = datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")

            return {
                "address": address,
                "signature": signature,
                "message": f"GaiAI Login\nAddress: {address}\nNonce: {nonce}\nTime: {timestamp}",
                "name": "walletConnect",
                "inviteCode": self.REF_CODE
            }
        except Exception as e:
            raise Exception(f"Generate Req Payload Failed: {str(e)}")

    def generate_prompt(self):
        subjects = [
            "a cyberpunk girl", "a medieval knight", "a futuristic robot", "a space explorer",
            "a wise old wizard", "a young samurai", "a brave firefighter", "a skilled archer",
            "a superhero flying", "a pirate captain", "a wandering monk", "a mysterious assassin",
            "a friendly alien", "a futuristic soldier", "a desert nomad", "a time traveler",
            "a steampunk engineer", "a martial artist", "a gothic vampire", "a powerful sorceress",
            "a jungle explorer", "a modern hacker", "a fantasy dwarf warrior", "a cosmic entity",
            "a giant dragon", "a mystical elf", "a cyborg mercenary", "a cybernetic animal",
            "a wise shaman", "a futuristic bounty hunter", "a skydiver", "a futuristic pilot",
            "a ghostly figure", "a glowing angel", "a demon overlord", "a ninja warrior",
            "a gladiator fighter", "a wandering bard", "a desert warrior", "a futuristic scientist",
            "a monstrous creature", "a superhero duo", "a wild werewolf", "a robotic animal",
            "a powerful witch", "a cyberpunk detective", "a war general", "a dark sorcerer",
            "a cosmic traveler", "a legendary hero"
        ]
        
        objects = [
            "in a neon-lit city", "inside a spaceship cockpit", "on a snowy mountain peak", 
            "at a futuristic laboratory", "in a burning battlefield", "under the full moon", 
            "in a mystical forest", "at the edge of a volcano", "underwater in the deep sea", 
            "in a ruined castle", "inside a cyberpunk alley", "on top of a skyscraper", 
            "in a post-apocalyptic desert", "at a magical academy", "in an alien marketplace", 
            "in a glowing cave", "inside a dark dungeon", "at a medieval battlefield", 
            "in an enchanted garden", "on a stormy ocean", "inside a digital matrix", 
            "in a haunted mansion", "in a giant arena", "on a floating island", 
            "in the middle of a lightning storm", "at the edge of the universe", 
            "in a futuristic subway", "inside a warship", "in a cybernetic jungle", 
            "at a forgotten temple", "in a parallel dimension", "on a desolate moon", 
            "in an ancient ruin", "in a magical desert", "inside a robotic factory", 
            "on an icy tundra", "in a crystal cave", "at the bottom of the ocean", 
            "in a futuristic city square", "on a fiery battlefield", "inside a hidden bunker", 
            "in a cosmic nebula", "inside a mystical library", "on a floating castle", 
            "in a gigantic clock tower", "inside a magical portal", "at a sacred shrine", 
            "in a chaotic marketplace", "inside a spaceship hangar", "in a futuristic arena"
        ]
        
        subject = random.choice(subjects)
        obj = random.choice(objects)
    
        prompt = f"{subject} {obj}, ultra-detailed, cinematic, highly realistic, 8k"
        return prompt

    def mask_account(self, account):
        try:
            mask_account = account[:6] + '*' * 6 + account[-6:]
            return mask_account
        except Exception as e:
            return None

    def print_question(self):
        while True:
            try:
                print(f"{Fore.WHITE + Style.BRIGHT}1. Run With Proxy{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}2. Run Without Proxy{Style.RESET_ALL}")
                proxy_choice = int(input(f"{Fore.BLUE + Style.BRIGHT}Choose [1/2] -> {Style.RESET_ALL}").strip())

                if proxy_choice in [1, 2]:
                    proxy_type = (
                        "With" if proxy_choice == 1 else 
                        "Without"
                    )
                    print(f"{Fore.GREEN + Style.BRIGHT}Run {proxy_type} Proxy Selected.{Style.RESET_ALL}")
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Please enter either 1 or 2.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number (1 or 2).{Style.RESET_ALL}")

        rotate_proxy = False
        if proxy_choice == 1:
            while True:
                rotate_proxy = input(f"{Fore.BLUE + Style.BRIGHT}Rotate Invalid Proxy? [y/n] -> {Style.RESET_ALL}").strip()

                if rotate_proxy in ["y", "n"]:
                    rotate_proxy = rotate_proxy == "y"
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter 'y' or 'n'.{Style.RESET_ALL}")

        return proxy_choice, rotate_proxy
    
    async def check_connection(self, proxy_url=None):
        connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
        try:
            async with ClientSession(connector=connector, timeout=ClientTimeout(total=30)) as session:
                async with session.get(url="https://api.ipify.org?format=json", proxy=proxy, proxy_auth=proxy_auth) as response:
                    response.raise_for_status()
                    return True
        except (Exception, ClientResponseError) as e:
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}Status  :{Style.RESET_ALL}"
                f"{Fore.RED+Style.BRIGHT} Connection Not 200 OK {Style.RESET_ALL}"
                f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                f"{Fore.YELLOW+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
            )
        
        return None
    
    async def wallet_nonce(self, address: str, proxy_url=None, retries=5):
        url = f"{self.BASE_API}/v2/gaiai-login/wallet-nonce?address={address}"
        headers = {
            **self.HEADERS[address],
            "Signature": str(int(time.time()) * 1000),
            "Token": ""
        }
        for attempt in range(retries):
            connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.get(url=url, headers=headers, proxy=proxy, proxy_auth=proxy_auth) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}Status  :{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} Fetch Nonce Failed {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
                )

        return None
    
    async def wallet_login(self, account: str, address: str, nonce: str, proxy_url=None, retries=5):
        url = f"{self.BASE_API}/v2/gaiai-login/wallet"
        data = json.dumps(self.generate_payload(account, address, nonce))
        headers = {
            **self.HEADERS[address],
            "Content-Length": str(len(data)),
            "Content-Type": "application/json",
            "Signature": str(int(time.time()) * 1000),
            "Token": ""
        }
        for attempt in range(retries):
            connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, data=data, proxy=proxy, proxy_auth=proxy_auth) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}Status  :{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} Login Failed {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
                )

        return None
    
    async def user_profile(self, address: str, proxy_url=None, retries=5):
        url = f"{self.BASE_API}/v2/gaiai-user/profile"
        headers = {
            **self.HEADERS[address],
            "Signature": str(int(time.time()) * 1000),
            "Token": self.tona_tokens[address]
        }
        for attempt in range(retries):
            connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.get(url=url, headers=headers, proxy=proxy, proxy_auth=proxy_auth) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}Balanc  :{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} Fetch aGai Points Failed {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
                )

        return None
    
    async def daily_checkin(self, address: str, proxy_url=None, retries=5):
        url = f"{self.BASE_API}/v1/gaiai-sign"
        headers = {
            **self.HEADERS[address],
            "Content-Length": "2",
            "Content-Type": "application/json",
            "Signature": str(int(time.time()) * 1000),
            "Token": self.tona_tokens[address]
        }
        for attempt in range(retries):
            connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, json={}, proxy=proxy, proxy_auth=proxy_auth) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}Check-In:{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} Not Claimed {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
                )

        return None
    
    async def create_task(self, address: str, prompt: str, proxy_url=None, retries=5):
        url = f"{self.BASE_API}/v2/gaiai-ai/create-task"
        data = json.dumps({"type":"1", "prompt":prompt, "width":"1024", "height":"1024", "aspectRatio":"1"})
        headers = {
            **self.HEADERS[address],
            "Content-Length": str(len(data)),
            "Content-Type": "application/json",
            "Signature": str(int(time.time()) * 1000),
            "Token": self.tona_tokens[address]
        }
        for attempt in range(retries):
            connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, data=data, proxy=proxy, proxy_auth=proxy_auth) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}     Status    :{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} Failed {Style.RESET_ALL}"
                )
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}     Message   :{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
                )

        return None
    
    async def process_check_connection(self, address: str, use_proxy: bool, rotate_proxy: bool):
        while True:
            proxy = self.get_next_proxy_for_account(address) if use_proxy else None
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}Proxy   :{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {proxy} {Style.RESET_ALL}"
            )

            is_valid = await self.check_connection(proxy)
            if not is_valid:
                if rotate_proxy:
                    proxy = self.rotate_proxy_for_account(address)
                    await asyncio.sleep(1)
                    continue

                return False

            return True
    
    async def process_user_login(self, account: str, address: str, use_proxy: bool, rotate_proxy: bool):
        is_valid = await self.process_check_connection(address, use_proxy, rotate_proxy)
        if is_valid:
            proxy = self.get_next_proxy_for_account(address) if use_proxy else None

            wallet_nonce = await self.wallet_nonce(address, proxy)
            if not wallet_nonce: return

            err_msg = wallet_nonce.get("message")

            if err_msg != "Success": 
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}Status  :{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} Fetch Nonce Failed {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} {err_msg} {Style.RESET_ALL}"
                )
                return False

            nonce = wallet_nonce.get("data", {}).get("nonce")

            wallet_login = await self.wallet_login(account, address, nonce, proxy)
            if not wallet_login: return False

            err_msg = wallet_login.get("message")

            if err_msg != "Success": 
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}Status  :{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} Login Failed {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} {err_msg} {Style.RESET_ALL}"
                )
                return False

            self.tona_tokens[address] = wallet_login.get("data", {}).get("token")

            self.log(
                f"{Fore.CYAN + Style.BRIGHT}Status  :{Style.RESET_ALL}"
                f"{Fore.GREEN + Style.BRIGHT} Login Success {Style.RESET_ALL}"
            )

            return True

    async def process_accounts(self, account: str, address: str, use_proxy: bool, rotate_proxy: bool):
        logined = await self.process_user_login(account, address, use_proxy, rotate_proxy)
        if logined:
            proxy = self.get_next_proxy_for_account(address) if use_proxy else None

            profile = await self.user_profile(address, proxy)
            if profile:
                err_msg = profile.get("message")

                if err_msg != "Success": 
                    self.log(
                        f"{Fore.CYAN + Style.BRIGHT}Balance :{Style.RESET_ALL}"
                        f"{Fore.RED+Style.BRIGHT} Fetch aGai Points Failed {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                        f"{Fore.YELLOW+Style.BRIGHT} {err_msg} {Style.RESET_ALL}"
                    )
                else:
                    points = profile.get("data", {}).get("gPoints", 0)

                    self.log(
                        f"{Fore.CYAN + Style.BRIGHT}Balance :{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} {points} aGai {Style.RESET_ALL}"
                    )


            checkin = await self.daily_checkin(address, proxy)
            if checkin:
                err_msg = checkin.get("message")
                if err_msg != "Success": 
                    self.log(
                        f"{Fore.CYAN+Style.BRIGHT}Check-In:{Style.RESET_ALL}"
                        f"{Fore.RED+Style.BRIGHT} Not Claimed {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                        f"{Fore.YELLOW+Style.BRIGHT} {err_msg} {Style.RESET_ALL}"
                    )
                else:
                    points = checkin.get("data", {}).get("gPoints", 0)
                    self.log(
                        f"{Fore.CYAN+Style.BRIGHT}Check-In:{Style.RESET_ALL}"
                        f"{Fore.GREEN+Style.BRIGHT} Claimed {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                        f"{Fore.CYAN+Style.BRIGHT} Balance Now: {Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT}{points} aGai{Style.RESET_ALL}"
                    )

                self.log(f"{Fore.CYAN+Style.BRIGHT}Creation:{Style.RESET_ALL}")

                prompt = self.generate_prompt()
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}     Prompt    :{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {prompt} {Style.RESET_ALL}"
                )

                create = await self.create_task(address, prompt, proxy)
                if create:
                    err_msg = create.get("message")
                    if err_msg != "Success": 
                        self.log(
                            f"{Fore.CYAN+Style.BRIGHT}     Status    :{Style.RESET_ALL}"
                            f"{Fore.RED+Style.BRIGHT} Failed {Style.RESET_ALL}"
                        )
                        self.log(
                            f"{Fore.CYAN+Style.BRIGHT}     Message   :{Style.RESET_ALL}"
                            f"{Fore.YELLOW+Style.BRIGHT} {err_msg} {Style.RESET_ALL}"
                        )
                    else:
                        reward = create.get("data", {}).get("rewardVal", 0)
                        self.log(
                            f"{Fore.CYAN+Style.BRIGHT}     Status    :{Style.RESET_ALL}"
                            f"{Fore.GREEN+Style.BRIGHT} Success {Style.RESET_ALL}"
                        )
                        self.log(
                            f"{Fore.CYAN+Style.BRIGHT}     Reward    :{Style.RESET_ALL}"
                            f"{Fore.WHITE+Style.BRIGHT} {reward} aGai {Style.RESET_ALL}"
                        )

    async def main(self):
        try:
            with open('accounts.txt', 'r') as file:
                accounts = [line.strip() for line in file if line.strip()]

            proxy_choice, rotate_proxy = self.print_question()

            while True:
                use_proxy = True if proxy_choice == 1 else False

                self.clear_terminal()
                self.welcome()
                self.log(
                    f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{len(accounts)}{Style.RESET_ALL}"
                )

                if use_proxy:
                    await self.load_proxies()

                separator = "=" * 25
                for account in accounts:
                    if account:
                        address = self.generate_address(account)
                        self.log(
                            f"{Fore.CYAN + Style.BRIGHT}{separator}[{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} {self.mask_account(address)} {Style.RESET_ALL}"
                            f"{Fore.CYAN + Style.BRIGHT}]{separator}{Style.RESET_ALL}"
                        )

                        if not address:
                            self.log(
                                f"{Fore.CYAN + Style.BRIGHT}Status  :{Style.RESET_ALL}"
                                f"{Fore.RED + Style.BRIGHT} Invalid Private Key or Library Version Not Supported {Style.RESET_ALL}"
                            )
                            continue

                        self.HEADERS[address] = {
                            "Accept": "application/json, text/plain, */*",
                            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
                            "Connection": "keep-alive",
                            "Host": "api.metagaia.io",
                            "Lang": "en-US",
                            "Origin": "https://www.gaiai.io",
                            "Referer": "https://www.gaiai.io/",
                            "Sec-Fetch-Dest": "empty",
                            "Sec-Fetch-Mode": "cors",
                            "Sec-Fetch-Site": "cross-site",
                            "User-Agent": FakeUserAgent().random
                        }
                        
                        await self.process_accounts(account, address, use_proxy, rotate_proxy)

                self.log(f"{Fore.CYAN + Style.BRIGHT}={Style.RESET_ALL}"*72)
                
                delay = 12 * 60 * 60
                while delay > 0:
                    formatted_time = self.format_seconds(delay)
                    print(
                        f"{Fore.CYAN+Style.BRIGHT}[ Wait for{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {formatted_time} {Style.RESET_ALL}"
                        f"{Fore.CYAN+Style.BRIGHT}... ]{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.BLUE+Style.BRIGHT}All Accounts Have Been Processed...{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(1)
                    delay -= 1

        except FileNotFoundError:
            self.log(f"{Fore.RED}File 'accounts.txt' Not Found.{Style.RESET_ALL}")
            return
        except Exception as e:
            self.log(f"{Fore.RED+Style.BRIGHT}Error: {e}{Style.RESET_ALL}")
            raise e

if __name__ == "__main__":
    try:
        bot = GaiAI()
        asyncio.run(bot.main())
    except KeyboardInterrupt:
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{Fore.RED + Style.BRIGHT}[ EXIT ] Gai AI - BOT{Style.RESET_ALL}                                       "                              
        )