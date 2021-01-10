import random
import argparse
from argparse import ArgumentParser, SUPPRESS
from pathlib import Path
from random import randint, choice
from requests import get
from shutil import which
from subprocess import Popen
from sys import exit
from urllib import request


def default_command():
    if which("wpg") is not None:
        return "wpg -s &>/dev/null"
    elif which("wal") is not None:
        return "wal -q -i"
    elif which("feh") is not None:
        return "feh --bg-fill"
    elif which("xsetbg") is not None:
        return ("xsetbg")
    elif which("gsettings") is not None:
        return "gsettings set org.gnome.desktop.background picture-uri"
    else:
        return False


def get_random_board():
    boardnums = list()
    boards = get('https://a.4cdn.org/boards.json').json()
    # gotta catch em all
    for board in boards["boards"]:
        # nsfw filter
        if board['ws_board'] == 0 and "nsfw" in args.random:
            boardnums.append(board['board'])
        if board['ws_board'] == 1 and "sfw" in args.random:
            boardnums.append(board['board'])
    args.board = random.choice(boardnums)


def get_random_thread():
    catalog = f"https://a.4cdn.org/{args.board.strip().replace('/', '')}/catalog.json"
    res = get(catalog).json()
    page = randint(0, len(res) - 1)
    return choice(res[page]["threads"])["no"]


def get_random_post(thread_post_num):
    thread = f"https://a.4cdn.org/{args.board}/thread/{thread_post_num}.json"
    res = get(thread).json()
    title = res["posts"][0].get("sub")

    post = choice(res["posts"])
    while not post.get("ext") or (post["w"] < int(args.min_res.split("x")[0]) or post["h"] < int(args.min_res.split("x")[1])) or post['ext'] not in args.extension:
        post = choice(res["posts"])

    filename = (post["filename"] if args.filename == "user" else str(post["tim"])) + post["ext"]

    request.urlretrieve(f"https://i.4cdn.org/{args.board}/{str(post['tim']) + post['ext']}", "".join((str(args.path).rstrip("/"), "/")) + filename)

    if args.command:
        Popen(args.command + " " + f"'{''.join((str(args.path).rstrip('/'), '/')) + filename}'", shell=True).wait()

    if not args.quiet:
        if title: print("   \33[1m" + title + "\33[0m")
        print("   https://boards.4chan.org/{}/thread/{}\n" .format(args.board, thread_post_num))
        print(">> {} No.{}" .format(str(post["now"]), post["no"]))
        print("   {} ({}x{})".format(filename, str(post["w"]), str(post["h"])))
        print("   saved to {}" .format(str(args.path)))
        print("  \33[90m ██ \33[0m\33[91m ██ \33[0m\33[92m ██ \33[0m\33[93m ██ \33[0m"
              "\33[94m ██ \33[0m\33[95m ██ \33[0m\33[96m ██ \33[0m\33[97m ██  \33[0m")


if __name__ == "__main__":
    parser = ArgumentParser(description="Set a random wallpaper from 4chan!", add_help=False, formatter_class=lambda prog: argparse.HelpFormatter(prog,max_help_position=70))
    arg_filt = parser.add_argument_group(title='filter arguments', description='')
    arg_info = parser.add_argument_group(title='information arguments', description='')
    arg_info.add_argument("-h", "--help", action="help", default=SUPPRESS, help="show this help message and exit")
    arg_info.add_argument("-v", "--version", action="version", version="2.0", help="show program version and exit")
    arg_filt.add_argument("-b", "--board", metavar="<board>", default="wg", help="board to scrape for wallpaper (default: /wg/)")
    arg_filt.add_argument("-c", "--command", metavar="<cmd>", default=default_command(), help=f"command to set wallpaper (default: {default_command()})")
    arg_filt.add_argument("-m", "--min-res", metavar="<res>", default="0x0", help="specify minimum resolution (ex. 1920x1080)")
    parser.add_argument("-f", "--filename", metavar="user/server", choices=["user", "server"], default="user", help="save file with \33[1muser\33[0m or \33[1mserver\33[0m filename")
    arg_filt.add_argument("-e", "--extension", metavar="<ext>", default=[".jpg", ".jpeg", ".png"], nargs="+", help="specify file extension(s) (default: .jpg .jpeg .png)")
    arg_filt.add_argument("-r", "--random", metavar="nsfw/sfw", action="store", const=["nsfw", "sfw"], nargs="?", help="choose board at random, filter by \33[1mnsfw\33[0m or \33[1msfw\33[0m")
    parser.add_argument("-p", "--path", metavar="<path>", default=Path.cwd(), help=f"where to save wallpaper files (default: {Path.cwd()})")
    parser.add_argument("-q", "--quiet", default=False, action="store_true", help="silence all output")
    args = parser.parse_args()

    if not args.command:
        if input("No program for setting wallpapers found. Please specify one with '-c'.\nDownload anyway? (y/n)") != "y":
            exit(1)

    try:
        print("\nFetching...", end="\r")
        if args.random:
            get_random_board()
        random_thread = get_random_thread()
        get_random_post(random_thread)
    except KeyboardInterrupt:
        if not args.quiet:
            print("\nProgram killed by user ;_;")
        exit(1)
