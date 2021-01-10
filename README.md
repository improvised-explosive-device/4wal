## 4wal 2.0

Set a random wallpaper from 4chan!

Uses 4chan's read only API to find a random post in a random thread on a random page number

I completely rewrote the program in one sitting to be more simple because of how bad it was was before

## usage
```
4wal.py [options]

optional arguments:
  -f, --filename user/server         save file with user or server filename
  -p, --path <path>                  where to save wallpaper files (default: current directory)
  -q, --quiet                        silence all output

filter arguments:

  -b, --board <board>                board to scrape for wallpaper (default: /wg/)
  -c  --command <cmd>                command to set wallpaper
  -m, --min-res <res>                specify minimum resolution (ex. 1920x1080)
  -e, --extension <ext> [<ext> ...]  specify file extension(s) (default: .jpg .jpeg .png)
  -r, --random [nsfw/sfw]            choose board at random, filter by nsfw or sfw

information arguments:

  -h, --help                         show this help message and exit
  -v, --version                      show program version and exit

```
