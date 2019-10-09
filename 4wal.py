import sys
import requests
import urllib
import os
from random import randint, choice

print("\033[H\033[J", end="", flush=True) # clear screen at program start

settings = {
    "path": "",
    "command": "",
    "server_filenames": True,
    "allow_all_boards": False,
    "minimum_res": {"w": False, "h": False},
}

logo = """
  ▒▒▒▒▒▒            ▒▒▒▒▒▒        \033[91m__        __    __              __\033[0m
▒▒██████▒▒        ▒▒██████▒▒     \033[91m/ /_ __ __/ /   / /_ __ ____ _  / /\033[0m
  ▒▒██████▒▒    ▒▒██████▒▒      \033[91m/ /\ V  V / /   / /\ V  V / _` |/ /\033[0m
▒▒████████▒▒    ▒▒████████▒▒   \033[91m/_/  \_/\_/_/   /_/  \_/\_/\__, /_/\033[0m
  ▒▒▒▒▒▒▒▒        ▒▒▒▒▒▒▒▒                                \033[91m|___/\033[0m

                                  \033[91m4wal - 4chan based wallpaper\033[0m
      ▒▒▒▒        ▒▒▒▒                 \033[91mscraper and changer\033[0m
    ▒▒████▒▒    ▒▒████▒▒
  ▒▒██████▒▒    ▒▒██████▒▒      \033[91mr <board>  -  set random wallpaper\033[0m
  ▒▒██████▒▒    ▒▒██████▒▒      \033[91ms <board>  -  select thread\033[0m
  ▒▒██▒▒██▒▒    ▒▒██▒▒██▒▒      \033[91mo  -  adjust program options\033[0m
    ▒▒  ▒▒        ▒▒  ▒▒
"""

logo = logo.replace("█", "\033[92m█\033[0m")
logo = logo.replace("▒", "\033[92m▒\033[0m")
print(logo)

def main():
    try:
        command = input("> ")
        command = command.lower().strip().replace("/", "")
        if command in ["r", "s"]:
            parse_input(command)
        elif command.startswith("r "):
            if settings["allow_all_boards"]:
                get_random_thread(command[2:])
            elif command[2:] in ["w", "wg"]:
                get_random_thread(command[2:])
            else:
                print(f"Board '{command[2:]}' invalid." + "\n")
                main()
        elif command.startswith("s "):
            if settings["allow_all_boards"]:
                display_threads(command[2:], 1)
            elif command[2:] in ["w", "wg"]:
                display_threads(command[2:], 1)
            else:
                print(f"Board '{command[2:]}' invalid." + "\n")
                main()
        elif command == "o":
            list_options()
        elif command == "clear":
            print("\033[H\033[J", end="", flush=True)
            main()
        elif command in ["q", "quit", "exit"]:
            print("\033[H\033[J", end="", flush=True)
            os._exit(0)
        else:
            sys.stdout.write("\x1b[1A")  # clear line if
            sys.stdout.write("\x1b[2K")  # invalid command
            main()
    except KeyboardInterrupt:
        print("\033[H\033[J", end="", flush=True)
        os._exit(0)


def parse_input(command):
    try:
        print("Enter board (/w/, /wg/):")
        board = input("> ")
        board = board.lower().strip().replace("/", "")
        print()
        if settings["allow_all_boards"]:
            if command == "r":
                get_random_thread(board)
            elif command == "s":
                display_threads(board, 1)
        elif board in ["w", "wg"]:
            if command == "r":
                get_random_thread(board)
            elif command == "s":
                display_threads(board, 1)
        else:
            print(f"Board '{board}' invalid." + "\n")
            main()
    except KeyboardInterrupt:
        print(logo)
        main()


def list_options():
    print("\033[92mType \033[91m1 \033[92mto edit path")
    if settings["path"]:
        print(f"  (Current path: {settings['path']})")
    else:
        print("  (Currently saving to the current working directory)")
    print("\033[92mType \033[91m2 \033[92mto set custom command - "
          + "MUST CONTAIN '{img}'")
    if settings["command"]:
        print(f"  (Current command: {settings['command']})")
    else:
        print("  (Current command: wal -i {img} -q)")
    print("\033[92mType \033[91m3 \033[92mto toggle all boards being available")
    if not settings["allow_all_boards"]:
        print("  (Currently off; /w/ and /wg/ being the only allowed boards)")
    else:
        print("  (Currently on; all boards allowed to be searched)")
    print("\033[92mType \033[91m4 \033[92mto toggle server/uploaded filenames")
    if settings["server_filenames"]:
        print("  (Currently set to server filenames)")
    else:
        print("  (Currently set to uploaded filenames)")
    print("\033[92mType \033[91m5 \033[92mto set minimum resolution - "
          + "format: 1920x1080")
    if settings["minimum_res"]["w"] and settings["minimum_res"]["h"]:
        print(f"  (Currently set to {settings['minimum_res']['w']}x"
              + f"{settings['minimum_res']['h']})")
    else:
        print("  (Currently there are no resolution restrictions)")
    print("\033[92mType \033[91mq \033[92mto exit options menu\033[0m")
    select_option()


def select_option():
    command = input("> ")
    command = command.strip()
    if command == "1":
        try:
            print("\033[92mEnter desired path:")
            print("  example: /home/lily/\033[0m")
            path = str(input("> "))
            if not path.endswith("/"):
                path += "/"
            settings["path"] = path
            print("\033[92mUpdated path:", path + "4wal_papers/{board}/",
                  "\033[0m\n")
            main()
        except KeyboardInterrupt:
            main()
    elif command == "2":
        try:
            print("\033[92mEnter desired path containing {img} template:")
            print("  example: feh --bg-fill {img}\033[0m")
            command = str(input("> "))
            if "{img}" not in command:
                print("\033[92mCommand must contain: \033[91m{img}\033[0m")
                list_options()
            settings["command"] = command
            print("\033[92mUpdated command:", command, "\033[0m\n")
            main()
        except KeyboardInterrupt:
            main()
    elif command == "3":
        if not settings["allow_all_boards"]:
            settings["allow_all_boards"] = True
            print("\033[92mNow allowing all boards\033[0m\n")
            main()
        else:
            settings["allow_all_boards"] = False
            print("\033[92mNow only allowing /w/ and /wg/\033[0m\n")
            main()
    elif command == "4":
        if settings["server_filenames"]:
            settings["server_filenames"] = False
            print("\033[92mNow using uploaded filenames\033[0m\n")
            main()
        else:
            settings["server_filenames"] = True
            print("\033[92mNow using server filenames\033[0m\n")
            main()
    elif command == "5":
        try:
            print("\033[92mEnter desired minimum resolution:")
            print("  example: 1920x1080\033[0m")
            res = input("> ").strip().lower()
            w, h = res.split("x")[0], res.split("x")[1]
            if not isinstance(w, int) and isinstance(h, int):
                print("\033[92mInvalid input:", res, "\033[0m\n")
                list_options()
            settings["minimum_res"]["w"] = int(w)
            settings["minimum_res"]["h"] = int(h)
            print(f"\033[92mNow using minimum resolution {w}x{h}\033[0m\n")
            main()
        except KeyboardInterrupt:
            main()
        except:
            print("\033[92mInvalid input:", res, "\033[0m\n")
            list_options()
    elif command == "q":
        print()
        main()
    else:
        sys.stdout.write("\x1b[1A")  # clear line if
        sys.stdout.write("\x1b[2K")  # invalid command
        print()
        main()


def display_threads(board, page_num):
    print("\033[H\033[J", end="", flush=True)
    url = f"https://a.4cdn.org/{board}/{page_num}.json"
    threads = {}
    try:
        response = requests.get(url)
        page = response.json()
    except:
        sys.stdout.write("\r" + f"[-] invalid board '{board}'".ljust(50, " "))
        print("\n")
        main()
    for i in range(15): # num of threads per page
        for thread in page.values():
            for post in thread[i].values():
                try:
                    title = post[0]["sub"]
                except:
                    title = post[0]["com"][:51] + "..."
                threads[i] = {"url": f"https://boards.4channel.org/{board}"
                             + f"/thread/{post[0]['no']}", "title": title}
    print("\033[91m" + f"[Page {page_num}] Select thread by entering it's "
          + "corresponding number:")
    for k, v in threads.items():
        print("\033[91m" + f"{str(k + 1)}) " + "\033[92m" + v["title"]
              + "\033[0m")
    if page_num != 10:
        print("\033[91mNP) " + "\033[92mDisplay next page")
    if page_num != 1:
        print("\033[91mPP) " + "\033[92mDisplay previous page")
    print("\033[91mQ) " + "\033[92mReturn to home\033[0m")
    select_thread(threads, board, page_num)


def select_thread(threads, board, page_num):
    try:
        thread = input("> ")
        if thread.lower().strip() == "q":
            print("\033[H\033[J", end="", flush=True)
            print(logo)
            main()
        elif thread.lower().strip() == "np" and page_num != 10:
            display_threads(board, page_num + 1)
        elif thread.lower().strip() == "pp" and page_num != 1:
            display_threads(board, page_num - 1)
        elif thread.lower().strip() in [str(i) for i in range(1, 16)]:
            selection = threads[int(thread) - 1]["url"]
            thread = selection.split("/")[5]
            get_random_post(thread, board, True)
        else:
            sys.stdout.write("\x1b[1A")  # clear line if
            sys.stdout.write("\x1b[2K")  # invalid command
            select_thread(threads, board, page_num)
    except KeyboardInterrupt:
        print("\033[H\033[J", end="", flush=True)
        print(logo)
        main()
    except:
        display_threads(board, page_num)


def get_random_thread(board):
    sys.stdout.write("\r" + "[+] finding random thread...".ljust(32, " "))
    page_num = randint(1, 10)
    url = f"https://a.4cdn.org/{board}/{page_num}.json"
    try:
        response = requests.get(url)
        page = response.json()
    except KeyboardInterrupt:
        main()
    except:
        sys.stdout.write("\r" + f"[-] invalid board '{board}'".ljust(50, " "))
        print("\n")
        main()
    thread_list = [thread for thread in page.values()]
    thread = choice(thread_list)
    get_random_post(thread, board, False)


def get_random_post(thread, board, selected):
    sys.stdout.write("\r" + "[+] finding random post...".ljust(32, " "))
    if selected:
        print("\033[H\033[J", end="", flush=True)
        print(logo)
        sys.stdout.write("\r" + "[+] finding random post...".ljust(32, " "))
        url = f"https://a.4cdn.org/{board}/thread/{thread}.json"
    else:
        sys.stdout.write("\r" + "[+] finding random post...".ljust(32, " "))
        posts = [post for post in thread[randint(0, 14)].values()]
        url = f"https://a.4cdn.org/{board}/thread/{posts[0][0]['no']}.json"
    response = requests.get(url)
    page = response.json()
    posts = [post for post in page.values()]
    if selected:
        get_random_pape(posts, board, True)
    else:
        get_random_pape(posts, board, False)


def get_random_pape(thread, board, selected):
    posts = choice(thread)
    post = choice(posts)
    try:
        if post["ext"] == ".webm":
            sys.stdout.write("\r"
                    + "[-] file contains invalid ext".ljust(32, " "))
            if selected:
                get_random_pape(thread, board, selected)
            else:
                get_random_thread(board)
        if settings["minimum_res"]["w"] and settings["minimum_res"]["h"]:
            if post["w"] < settings["minimum_res"]["w"] or \
               post["h"] < settings["minimum_res"]["h"]:
                sys.stdout.write("\r"
                    + "[-] image resolution too small".ljust(32, " "))
                if selected:
                    get_random_pape(thread, board, selected)
                else:
                    get_random_thread(board)
        if settings["server_filenames"] == True:
            filename = str(post["tim"]) + post["ext"]
        elif settings["server_filenames"] == False:
            filename = post["filename"] + post["ext"]
    except KeyError:
        sys.stdout.write("\r"
                + "[-] post cointains no image file".ljust(32, " "))
        if selected:
            get_random_pape(thread, board, selected)
        else:
            get_random_thread(board)
    try:
        title = posts[0]["sub"]
    except KeyError:
        title = ""
    if board == "wg":
        folder = "general"
    elif board == "w":
        folder = "anime"
    else:
        folder = board
    url = f"https://i.4cdn.org/{board}/{str(post['tim']) + post['ext']}"
    path = f"4wal_papers/{folder}/"
    if settings["path"]:
        path = settings["path"] + path
    os.makedirs(path, exist_ok=True)
    if os.path.exists(path + filename):
        sys.stdout.write("\r" + "[-] image file already exists".ljust(32, " "))
        if selected:
            get_random_pape(thread, board, selected)
        else:
            get_random_thread(board)
    else:
        sys.stdout.write("\r" + "[+] downloading image file...".ljust(32, " "))
        urllib.request.urlretrieve(url, path + filename)
    sys.stdout.write("\r" + "[+] finished".ljust(32, " "))
    print()
    if title:
        print("\033[92mThread title:\033[91m", title, "\033[0m")
    print("\033[92mServer filename:\033[91m", str(post["tim"])
            + post["ext"], "\033[0m")
    print("\033[92mFilename:\033[91m", post["filename"] + post["ext"],
            "\033[0m")
    print("\033[92mResolution:\033[91m", post["w"], "x", post["h"], "\033[0m")
    print("\033[92mURL:\033[91m", url, "\033[0m")
    print()
    call_command(path + filename)


def call_command(img):
    if settings["command"]:
        command = settings["command"].replace("{img}", img)
        os.system(command)
    else:
        os.system(f"wal -i {img} -q")
    main()


if __name__ == "__main__":
    main()

