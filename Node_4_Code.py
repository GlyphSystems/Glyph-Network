import json
import os
import time
import sys

SESSIONS_FILE = os.path.expanduser("~/auth/sessions.json")
REQUESTS_DIR = os.path.expanduser("~/drop_zone/requests/")
RESULTS_DIR = os.path.expanduser("~/drop_zone/results/")

def run_gateway():
    print("==================================================================")
    print("   GN AUDIT NODE | DATA-BUDGETED VERIFICATION GATEWAY")
    print("==================================================================")
    
    audit_code = input("\nENTER AUDIT CODE: ").strip()
    with open(SESSIONS_FILE, "r") as f:
        sessions = json.load(f)
    
    if audit_code not in sessions or sessions[audit_code]["status"] != "active":
        print("[!] ACCESS DENIED.")
        return

    session = sessions[audit_code]
    print(f"\nSESSION: {session['session_id']} | RUNS LEFT: {session['remaining_runs']}")
    
    print("\n[PASTE HIGH-DENSITY DATA. TYPE 'DONE' ON A NEW LINE AND HIT ENTER]")
    lines = []
    while True:
        line = sys.stdin.readline()
        if line.strip().upper() == "DONE":
            break
        lines.append(line)
    payload = "".join(lines)
    
    # MEASURE MEMORY/DATA SIZE
    payload_size_kb = len(payload.encode('utf-8')) / 1024
    
    # UPDATED LIMIT: 250 KB
    if payload_size_kb > 250:
        print(f"[!] REJECTED: PAYLOAD ({payload_size_kb:.2f} KB) EXCEEDS 250KB LIMIT.")
        return

    session["remaining_runs"] -= 1
    with open(SESSIONS_FILE, "w") as f:
        json.dump(sessions, f)

    now = time.time()
    session_id = f"{session['session_id']}_{int(now)}"
    with open(os.path.join(REQUESTS_DIR, f"{session_id}.json"), "w") as f:
        json.dump({"payload": payload, "size_kb": payload_size_kb, "timestamp": now}, f)

    print(f"\n[*] {payload_size_kb:.2f} KB TRANSFERRED TO VOLATILE RAM. WAITING...")

    start_wait = time.time()
    while time.time() - start_wait < 30:
        for file in os.listdir(RESULTS_DIR):
            if file.endswith(".json"):
                result_path = os.path.join(RESULTS_DIR, file)
                with open(result_path, "r") as f:
                    result = json.load(f)
                print("\n" + "="*30)
                print(f"AUDIT RESULT: {result.get('status')}")
                print(f"COHERENCE: {result.get('coherence')}")
                print("="*30)
                os.remove(result_path)
                return
        time.sleep(1)
    print("\n[!] TIMEOUT: CHECK NODE 3 CONNECTION.")

if __name__ == "__main__":
    run_gateway()
