#### Changes specific to this fork:
```
1. get random board with '-r', filter by worksafe status with '-r [nsfw/sfw]'
2. specify file extension(s) with '-e ext [ext..]'
3. ask user if they want to download anyway if no software to set wp exists
4. small changes in printout (formatting, print thread url, more verbose help)
5. wpgtk support
```
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
  -e, --extension <ext> [ext ...]    specify file extension(s) (default: .jpg .jpeg .png)
  -r, --random [nsfw/sfw]            choose board at random, filter by nsfw or sfw

information arguments:
  -h, --help                         show this help message and exit
  -v, --version                      show program version and exit

```
