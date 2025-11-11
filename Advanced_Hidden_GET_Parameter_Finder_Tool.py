import re
import sys
import requests
import threading
import time
import os
import json
import argparse
from urllib.parse import urljoin, urlparse, quote
from concurrent.futures import ThreadPoolExecutor, as_completed
import random
from datetime import datetime

class AdvancedHiddenParamFinder:
    def __init__(self):
        self.found_params = []
        self.scanned_urls = set()
        self.scanned_js_files = set()
        self.session = requests.Session()
        self.total_js_files = 0
        self.scanned_js_count = 0
        self.start_time = None
        
        # Advanced headers to avoid detection
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        })
        
    def print_banner(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
        banner = r"""
        
 ██████╗██╗  ██╗ ██████╗ ██╗    ██╗██████╗ ██╗   ██╗██████╗ ██╗   ██╗██╗   ██╗ █████╗ ██╗
██╔════╝██║  ██║██╔═══██╗██║    ██║██╔══██╗██║   ██║██╔══██╗╚██╗ ██╔╝██║   ██║██╔══██╗██║
██║     ███████║██║   ██║██║ █╗ ██║██║  ██║██║   ██║██████╔╝ ╚████╔╝ ██║   ██║███████║██║
██║     ██╔══██║██║   ██║██║███╗██║██║  ██║██║   ██║██╔══██╗  ╚██╔╝  ██║   ██║██╔══██║██║
╚██████╗██║  ██║╚██████╔╝╚███╔███╔╝██████╔╝╚██████╔╝██║  ██║   ██║   ╚██████╔╝██║  ██║███████╗
 ╚═════╝╚═╝  ╚═╝ ╚═════╝  ╚══╝╚══╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝
                                                                                            
        """
        colors = ['\033[92m', '\033[93m', '\033[94m', '\033[95m', '\033[96m']
        colored_banner = random.choice(colors) + banner + '\033[0m'
        
        print(colored_banner)
        print("\033[92m" + "═" * 80 + "\033[0m")
        print("\033[93m" + "🚀 ADVANCED HIDDEN GET PARAMETER FINDER TOOL" + "\033[0m")
        print("\033[92m" + "═" * 80 + "\033[0m")
        print("\033[96m" + "👨‍💻 Developed by: chowdhuryvai" + "\033[0m")
        print("\033[95m" + "📱 Telegram: https://t.me/darkvaiadmin" + "\033[0m")
        print("\033[95m" + "📢 Channel: https://t.me/windowspremiumkey" + "\033[0m")
        print("\033[95m" + "🌐 Website: https://crackyworld.com/" + "\033[0m")
        print("\033[94m" + "📅 " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\033[0m")
        print("\033[92m" + "═" * 80 + "\033[0m")
        print()
    
    def animate_loading(self, text):
        animation = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
        for i in range(len(animation)):
            time.sleep(0.1)
            sys.stdout.write(f"\r\033[93m{text} {animation[i % len(animation)]}\033[0m")
            sys.stdout.flush()
    
    def print_status(self, message, msg_type="info"):
        icons = {
            "info": "🔍",
            "success": "✅",
            "warning": "⚠️",
            "error": "❌",
            "found": "🎯"
        }
        colors = {
            "info": "\033[96m",
            "success": "\033[92m",
            "warning": "\033[93m",
            "error": "\033[91m",
            "found": "\033[95m"
        }
        
        icon = icons.get(msg_type, "🔍")
        color = colors.get(msg_type, "\033[96m")
        print(f"{color}{icon} {message}\033[0m")
    
    def extract_js_urls(self, html_content, base_url):
        js_urls = []
        
        # Comprehensive patterns for JavaScript files
        patterns = [
            r'src\s*=\s*["\'](.*?\.js(?:\?[^"\']*)?)["\']',
            r'script[^>]*src\s*=\s*["\'](.*?\.js(?:\?[^"\']*)?)["\']',
            r'<script[^>]*src\s*=\s*["\'](.*?\.js(?:\?[^"\']*)?)["\']',
            r'import\s+.*?from\s+["\'](.*?\.js)["\']',
            r'require\s*\(\s*["\'](.*?\.js)["\']',
            r'loadScript\s*\(\s*["\'](.*?\.js)["\']',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, html_content, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                full_url = urljoin(base_url, match.split('?')[0])  # Remove query parameters for scanning
                if full_url not in js_urls:
                    js_urls.append(full_url)
        
        return js_urls
    
    def advanced_param_patterns(self):
        return [
            # URL parameter patterns
            r'[\?&]([a-zA-Z0-9_\-]{3,50})=',
            r'location\.search.*?[\?&]([a-zA-Z0-9_\-]{3,50})=',
            r'URLSearchParams.*?get\(["\']([a-zA-Z0-9_\-]{3,50})["\']\)',
            r'window\.location.*?[\?&]([a-zA-Z0-9_\-]{3,50})=',
            r'[\?&]([a-zA-Z0-9_\-]{3,50})\s*:\s*',
            
            # Object parameter patterns
            r'params\[["\']([a-zA-Z0-9_\-]{3,50})["\']\]',
            r'query\[["\']([a-zA-Z0-9_\-]{3,50})["\']\]',
            r'data\[["\']([a-zA-Z0-9_\-]{3,50})["\']\]',
            r'options\[["\']([a-zA-Z0-9_\-]{3,50})["\']\]',
            
            # Function parameter patterns
            r'\.get\(["\']([a-zA-Z0-9_\-]{3,50})["\']\)',
            r'\.post\(["\']([a-zA-Z0-9_\-]{3,50})["\']\)',
            r'fetch\([^)]*[\?&]([a-zA-Z0-9_\-]{3,50})=',
            r'axios\.(?:get|post)\([^)]*[\?&]([a-zA-Z0-9_\-]{3,50})=',
            
            # Common parameter names
            r'(api_key|token|auth|key|secret|id|user|password|hash|signature)',
            r'(callback|cb|jsonp|callback_func)',
            r'(redirect|return|next|continue|url)',
            r'(debug|test|dev|stage|production)',
            
            # Template literals
            r'`[^`]*\?([a-zA-Z0-9_\-]{3,50})=`',
            
            # Concatenation patterns
            r'\?[^"\']*\+([a-zA-Z0-9_\-]{3,50})\+',
        ]
    
    def find_parameters_in_js(self, js_content, js_url):
        found_params = []
        
        for pattern in self.advanced_param_patterns():
            matches = re.findall(pattern, js_content, re.IGNORECASE)
            for param in matches:
                if self.is_valid_parameter(param):
                    # Create different test payloads
                    test_payloads = [
                        f"{param}=test",
                        f"{param}=true",
                        f"{param}=1",
                        f"{param}=admin",
                        f"{param}[]=test"
                    ]
                    
                    for payload in test_payloads:
                        result = {
                            'js_url': js_url,
                            'parameter': param,
                            'test_url': self.create_test_url(js_url, payload),
                            'payload': payload,
                            'pattern_type': pattern[:50] + '...' if len(pattern) > 50 else pattern,
                            'confidence': self.calculate_confidence(param, pattern)
                        }
                        found_params.append(result)
        
        return found_params
    
    def is_valid_parameter(self, param):
        # Filter out common false positives
        false_positives = ['http', 'https', 'www', 'com', 'org', 'net', 'io', 'js', 'css', 'html']
        return (len(param) >= 3 and 
                len(param) <= 50 and 
                param not in false_positives and
                not param.isdigit())
    
    def calculate_confidence(self, param, pattern):
        confidence = 50
        
        # Increase confidence for common parameter names
        common_params = ['id', 'key', 'token', 'auth', 'secret', 'api_key', 'user', 'password']
        if param.lower() in common_params:
            confidence += 30
        
        # Increase confidence for specific patterns
        if 'URLSearchParams' in pattern or 'location.search' in pattern:
            confidence += 20
        
        return min(confidence, 100)
    
    def create_test_url(self, js_url, payload):
        base_url = js_url.split('?')[0]
        separator = '?' if '?' not in base_url else '&'
        return f"{base_url}{separator}{payload}"
    
    def get_js_content(self, url):
        try:
            # Random delay to avoid rate limiting
            time.sleep(random.uniform(0.1, 0.5))
            
            response = self.session.get(url, timeout=15, verify=False)
            if response.status_code == 200:
                return response.text
            else:
                self.print_status(f"HTTP {response.status_code} for {url}", "warning")
        except requests.exceptions.Timeout:
            self.print_status(f"Timeout while fetching {url}", "warning")
        except requests.exceptions.ConnectionError:
            self.print_status(f"Connection error for {url}", "warning")
        except Exception as e:
            self.print_status(f"Error fetching {url}: {str(e)}", "error")
        
        return None
    
    def scan_js_file(self, js_url):
        if js_url in self.scanned_js_files:
            return []
        
        self.scanned_js_files.add(js_url)
        self.scanned_js_count += 1
        
        # Update progress
        progress = (self.scanned_js_count / self.total_js_files) * 100
        sys.stdout.write(f"\r\033[94m📊 Progress: {self.scanned_js_count}/{self.total_js_files} ({progress:.1f}%)\033[0m")
        sys.stdout.flush()
        
        self.print_status(f"Scanning: {js_url}", "info")
        
        js_content = self.get_js_content(js_url)
        if not js_content:
            return []
        
        params = self.find_parameters_in_js(js_content, js_url)
        
        for result in params:
            self.found_params.append(result)
            self.print_status(f"Found parameter: {result['parameter']} (Confidence: {result['confidence']}%)", "found")
        
        return params
    
    def scan_website(self, url):
        self.start_time = time.time()
        self.print_status(f"Starting scan for: {url}", "info")
        
        try:
            response = self.session.get(url, timeout=15, verify=False)
            if response.status_code != 200:
                self.print_status(f"Failed to access website (HTTP {response.status_code})", "error")
                return
            
            # Extract JavaScript URLs
            js_urls = self.extract_js_urls(response.text, url)
            self.total_js_files = len(js_urls)
            
            self.print_status(f"Found {self.total_js_files} JavaScript files to scan", "success")
            
            if not js_urls:
                self.print_status("No JavaScript files found to scan", "warning")
                return
            
            # Scan JS files with threading
            with ThreadPoolExecutor(max_workers=10) as executor:
                futures = [executor.submit(self.scan_js_file, js_url) for js_url in js_urls]
                
                for future in as_completed(futures):
                    try:
                        future.result()
                    except Exception as e:
                        self.print_status(f"Thread error: {str(e)}", "error")
            
            print()  # New line after progress
            self.display_results()
            
        except Exception as e:
            self.print_status(f"Scan error: {str(e)}", "error")
    
    def display_results(self):
        execution_time = time.time() - self.start_time
        
        print("\n" + "═" * 100)
        print("\033[92m" + "🎉 SCAN COMPLETED SUCCESSFULLY!" + "\033[0m")
        print("═" * 100)
        print(f"\033[96m📊 Scan Summary:\033[0m")
        print(f"   🕒 Execution Time: {execution_time:.2f} seconds")
        print(f"   📁 JavaScript Files Scanned: {self.scanned_js_count}")
        print(f"   🎯 Parameters Found: {len(self.found_params)}")
        print("═" * 100)
        
        if not self.found_params:
            self.print_status("No hidden GET parameters found!", "warning")
            return
        
        # Group by confidence level
        high_confidence = [p for p in self.found_params if p['confidence'] >= 80]
        medium_confidence = [p for p in self.found_params if 50 <= p['confidence'] < 80]
        low_confidence = [p for p in self.found_params if p['confidence'] < 50]
        
        print(f"\n\033[92m🔴 High Confidence ({len(high_confidence)}):\033[0m")
        for i, result in enumerate(high_confidence, 1):
            print(f"   {i}. \033[91m{result['parameter']}\033[0m")
            print(f"      📍 File: {result['js_url']}")
            print(f"      🔗 Test: {result['test_url']}")
            print(f"      🎯 Confidence: {result['confidence']}%")
            print()
        
        if medium_confidence:
            print(f"\033[93m🟡 Medium Confidence ({len(medium_confidence)}):\033[0m")
            for i, result in enumerate(medium_confidence, 1):
                print(f"   {i}. \033[93m{result['parameter']}\033[0m")
                print(f"      📍 File: {result['js_url']}")
                print(f"      🔗 Test: {result['test_url']}")
                print(f"      🎯 Confidence: {result['confidence']}%")
                print()
        
        if low_confidence:
            print(f"\033[96m🔵 Low Confidence ({len(low_confidence)}):\033[0m")
            for i, result in enumerate(low_confidence, 1):
                print(f"   {i}. \033[96m{result['parameter']}\033[0m")
                print(f"      📍 File: {result['js_url']}")
                print(f"      🔗 Test: {result['test_url']}")
                print(f"      🎯 Confidence: {result['confidence']}%")
                print()
    
    def save_results(self, filename=None):
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"hidden_params_scan_{timestamp}"
        
        # Save as JSON
        json_filename = f"{filename}.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump({
                'scan_info': {
                    'tool': 'chowdhuryvai Advanced Hidden Param Finder',
                    'website': 'https://crackyworld.com/',
                    'telegram': 'https://t.me/darkvaiadmin',
                    'timestamp': datetime.now().isoformat(),
                    'total_parameters_found': len(self.found_params)
                },
                'results': self.found_params
            }, f, indent=2, ensure_ascii=False)
        
        # Save as TXT
        txt_filename = f"{filename}.txt"
        with open(txt_filename, 'w', encoding='utf-8') as f:
            f.write("ADVANCED HIDDEN GET PARAMETER SCAN RESULTS\n")
            f.write("=" * 60 + "\n")
            f.write(f"Tool: chowdhuryvai Advanced Hidden Param Finder\n")
            f.write(f"Website: https://crackyworld.com/\n")
            f.write(f"Telegram: https://t.me/darkvaiadmin\n")
            f.write(f"Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Parameters Found: {len(self.found_params)}\n")
            f.write("=" * 60 + "\n\n")
            
            for result in self.found_params:
                f.write(f"Parameter: {result['parameter']}\n")
                f.write(f"JavaScript File: {result['js_url']}\n")
                f.write(f"Test URL: {result['test_url']}\n")
                f.write(f"Confidence: {result['confidence']}%\n")
                f.write(f"Payload: {result['payload']}\n")
                f.write("-" * 60 + "\n")
        
        self.print_status(f"Results saved to: {json_filename} and {txt_filename}", "success")

def main():
    finder = AdvancedHiddenParamFinder()
    finder.print_banner()
    
    while True:
        print("\033[92m" + "🚀 SCANNING OPTIONS:" + "\033[0m")
        print("\033[96m[1] 🔍 Scan single website")
        print("[2] 📁 Scan multiple websites from file")
        print("[3] ⚙️  Advanced options")
        print("[4] 📊 View previous results")
        print("[5] ❌ Exit\033[0m")
        
        choice = input("\n\033[93m🎯 Enter your choice (1-5): \033[0m").strip()
        
        if choice == '1':
            url = input("\n\033[96m🌐 Enter website URL: \033[0m").strip()
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            finder.scan_website(url)
            
            if finder.found_params:
                save_choice = input("\n\033[93m💾 Save results to file? (y/n): \033[0m").strip().lower()
                if save_choice == 'y':
                    finder.save_results()
        
        elif choice == '2':
            filename = input("\n\033[96m📂 Enter filename with URLs: \033[0m").strip()
            try:
                with open(filename, 'r') as f:
                    urls = [line.strip() for line in f if line.strip()]
                
                for i, url in enumerate(urls, 1):
                    if not url.startswith(('http://', 'https://')):
                        url = 'https://' + url
                    
                    print(f"\n\033[92m📍 Scanning {i}/{len(urls)}: {url}\033[0m")
                    finder.scan_website(url)
                    print("\n" + "═" * 80 + "\n")
                
                if finder.found_params:
                    finder.save_results("batch_scan_results")
            
            except FileNotFoundError:
                finder.print_status("File not found!", "error")
        
        elif choice == '3':
            print("\n\033[93m⚙️  Advanced features coming soon...\033[0m")
            # Additional advanced features can be added here
        
        elif choice == '4':
            print("\n\033[93m📊 Previous results feature coming soon...\033[0m")
            # Feature to view previous scan results
        
        elif choice == '5':
            print("\n\033[92m" + "🎉 Thank you for using chowdhuryvai Advanced Hidden Param Finder!" + "\033[0m")
            print("\033[95m" + "📱 Telegram: https://t.me/darkvaiadmin" + "\033[0m")
            print("\033[95m" + "🌐 Website: https://crackyworld.com/" + "\033[0m")
            break
        
        else:
            finder.print_status("Invalid choice!", "error")
        
        input("\n\033[93m⏎ Press Enter to continue...\033[0m")
        finder.print_banner()

if __name__ == "__main__":
    try:
        # Disable SSL warnings for better user experience
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        main()
    except KeyboardInterrupt:
        print("\n\n\033[91m❌ Scan interrupted by user. Exiting...\033[0m")
    except Exception as e:
        print(f"\n\033[91m💥 Unexpected error: {str(e)}\033[0m")
