import json
import os
import random
import string

SESSIONS_FILE = os.path.expanduser("~/auth/sessions.json")

def load_sessions():
    if os.path.exists(SESSIONS_FILE) and os.path.getsize(SESSIONS_FILE) > 0:
        with open(SESSIONS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_sessions(sessions):
    with open(SESSIONS_FILE, "w") as f:
        json.dump(sessions, f, indent=4)

def generate_code():
    chars = string.ascii_uppercase + string.digits
    return "AUDIT-" + "".join(random.choices(chars, k=4)) + "-2026"

def main():
    print("=========================================")
    print("   NODE 4 ADMIN | SESSION CONTROL TOOL")
    print("=========================================")
    print("1. Create New Audit Session")
    print("2. View All Sessions")
    print("3. Revoke an Audit Code")
    print("4. Exit")
    
    choice = input("\nSelect an action (1-4): ").strip()
    sessions = load_sessions()

    if choice == '1':
        code = generate_code()
        runs = int(input("Enter maximum allowed runs (e.g., 50): "))
        session_id = "GN-AUDIT-" + "".join(random.choices(string.digits, k=4))
        
        sessions[code] = {
            "session_id": session_id,
            "status": "active",
            "remaining_runs": runs,
            "max_runs": runs
        }
        save_sessions(sessions)
        print(f"\n[+] SUCCESS! Give this exact code to your auditor: {code}")

    elif choice == '2':
        print("\n--- CURRENT SESSIONS ---")
        for code, data in sessions.items():
            print(f"Code: {code} | Status: {data['status']} | Runs Left: {data['remaining_runs']}")
            
    elif choice == '3':
        code = input("Enter the Audit Code to terminate: ").strip()
        if code in sessions:
            sessions[code]['status'] = "revoked"
            save_sessions(sessions)
            print(f"\n[+] SECURITY LOCK: Code {code} has been permanently disabled.")
        else:
            print("\n[!] Code not found in database.")

if __name__ == "__main__":
    main()
