import msoffcrypto
import io
import threading
from queue import Queue
import time
import sys
import os

def print_logo():
    logo = r"""
         "   '|'˜¨¯¨'˜¯\/'˜¨¯¨'˜˜¨¯'\‚        |\˜¨¯¨˜'\ '                       '|\˜¨¯¨˜\‚   |˜¨¯¨˜'|°               '|\˜¨¯¨˜'\‚   \˜¨¯¨˜'\      /˜¨¯¨˜'/'
   /             '/|\       \'‚ |˜¨¯¨˜'|\      '\'‚               '/˜¨¯¨˜'/\      \  |      |    '       |˜¨¯¨˜'|\      \'   '\      '\   /      /
  '|      '|\    '/ / |       |  |      | |      '|                |      '| '|      '|°|      '|           |      |/¸_¸_¸/|'    \¸_¸_¸\/¸_¸_¸/
 '/      '/\ \_/ / /       /|  |      |/¸_¸_¸/'                |      '|_|      '| |      '|'|˜¨¯¨˜°|  |      |\˜¨¯\_|/'    /˜¨¯¨˜'/\˜¨¯¨˜'\  '
'|       |  \|_|/ /       / '|  |      |\˜¨¯¨˜'\‚                |      '|¯|      '| |      '|'|       |  |      |/¸_¸/|°    /       /  \      '\'
|\¸_¸_¸\       |¸_¸_¸'|  /‘  |      | |      | '               |      '| '|      '|°|¸_¸_¸|/¸_¸_¸/|‘ |      |\˜¨¯¨˜'\'  /¸_¸_¸/ /\ '\¸_¸_¸\'
| |˜¨¯¨˜'|      '|˜¨¯¨˜˜'| /‘   |¸_¸_'| |¸_¸_¸|                |¸_¸_¸| '|¸_¸_¸|°|˜¨¯¨˜'||˜¨¯¨˜'| |‘ |¸_¸_'|/      /|  |˜¨¯¨˜| '/  '\ '|˜¨¯¨˜|
 \|¸_¸_¸|      '|¸_¸_¸'|/'    |˜¨¯¨˜'| |˜¨¯¨˜'|                |˜¨¯¨˜'|  |˜¨¯¨˜'|°|¸_¸_¸||¸_¸_¸|/  |˜¨¯¨/¸_¸_¸/ '|  |¸_¸_'|/     \|¸_¸_'|
   ¯\(¯         '¯)/¯'  '    |¸_¸_¸| |¸_¸_¸|'               |¸_¸_¸| '|¸_¸_¸|°  ¯\(¯  ¯)/¯    |¸_¸¸|˜¨¯¨˜'| '/'   ¯\(¯         ¯)/¯
      '                         '¯\(¯   ¯)/¯                  ¯\(¯    ¯)/¯  ‘                   '¯\(¯|¸_¸_'|/‘
                   '                      '                                 ‘                                ¯)/¯‘
    ╔════════════════════════════════════════════════════════╗
    ║              Mr. Al3X - brutcell v1.1                  ║
    ╠════════════════════════════════════════════════════════╣
    ║ Author     : Muhammad Lutfi Alfian                     ║
    ║ GitHub     : github.com/Alfiasnyah78                   ║
    ║ Instagram  : @alex                                     ║
    ║ Telegram   : @alex                                     ║
    ║ Donate     : Chat with me on Telegram!                 ║
    ╚════════════════════════════════════════════════════════╝
    """

    print(logo)

def loading_animation(stop_event):
    animation = "|/-\\"
    idx = 0
    while not stop_event.is_set():
        print(f"\r[•] Cracking... {animation[idx % len(animation)]}", end="", flush=True)
        idx += 1
        time.sleep(0.1)
    print("\r", end="")

def try_password(excel_file, password):
    try:
        decrypted = io.BytesIO()
        file = msoffcrypto.OfficeFile(open(excel_file, "rb"))
        file.load_key(password=password)
        file.decrypt(decrypted)
        return True
    except Exception:
        return False

def worker(queue, found_flag, excel_file, verbosity, lock):
    while not found_flag.is_set():
        try:
            password = queue.get(timeout=1)
        except:
            break
        if verbosity >= 2:
            with lock:
                print(f"[•] Trying password: '{password}'")
        if try_password(excel_file, password):
            found_flag.set()
            with lock:
                print(f"\n[✓] Password found: '{password}'")
                os.makedirs("logs", exist_ok=True)
                with open("logs/success.log", "a") as f:
                    f.write(f"{excel_file} | {password}\n")
            break
        queue.task_done()

def main():
    print_logo()
    excel_file = input("📁 Enter Excel file path: ").strip()
    wordlist_path = input("📖 Enter path to wordlist: ").strip()
    threads = int(input("⚙️ Threads to use [e.g., 4]: ").strip())
    verbosity = int(input("🔊 Verbosity [1=Silent, 2=Verbose]: ").strip())

    if not os.path.isfile(excel_file):
        print("[!] Excel file not found.")
        return
    if not os.path.isfile(wordlist_path):
        print("[!] Wordlist not found.")
        return

    queue = Queue()
    found_flag = threading.Event()
    lock = threading.Lock()

    with open(wordlist_path, "r", encoding="latin1", errors="ignore") as f:
        for line in f:
            pwd = line.strip()
            if pwd:
                queue.put(pwd)

    print(f"\n[•] Starting brute force with {threads} threads...")
    time.sleep(1)

    stop_event = threading.Event()
    animation_thread = threading.Thread(target=loading_animation, args=(stop_event,))
    animation_thread.start()

    thread_list = []
    for _ in range(threads):
        t = threading.Thread(target=worker, args=(queue, found_flag, excel_file, verbosity, lock))
        t.start()
        thread_list.append(t)

    try:
        for t in thread_list:
            t.join()
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user. Exiting...")
        found_flag.set()

    stop_event.set()
    animation_thread.join()

    if not found_flag.is_set():
        print("\n[-] Password not found.")
    else:
        print("\n[✓] Attack complete. Check logs/success.log")

if __name__ == "__main__":
    main()

