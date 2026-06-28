#!/usr/bin/python3
import ctypes
import glob
import importlib.util
import math
import os
import pathlib
import platform
import readline
import shutil
import signal
import subprocess
import sys
from itertools import zip_longest
from pathlib import Path

# DO NOT MODIFY ANYTHING BELOW THIS LINE UNLESS YOU KNOW WHAT YOU ARE DOING!
# Colourwgfues
COLOR_RE = "\033[0m"
COLOR_USER = "\033[92m"
COLOR_HOST = "\033[94m"
COLOR_CWD = "\033[96m"
COLOR_ERR = "\033[91m"

ROSEWATER = "\033[38;2;245;224;220m"
FLAMINGO = "\033[38;2;242;205;205m"
PINK = "\033[38;2;245;194;231m"
MAUVE = "\033[38;2;203;166;247m"
RED = "\033[38;2;243;139;168m"
MAROON = "\033[38;2;235;160;172m"
PEACH = "\033[38;2;250;179;135m"
YELLOW = "\033[38;2;249;226;175m"
GREEN = "\033[38;2;166;227;161m"
TEAL = "\033[38;2;148;226;213m"
SKY = "\033[38;2;137;220;235m"
SAPPHIRE = "\033[38;2;116;199;236m"
BLUE = "\033[38;2;137;180;250m"
LAVENDER = "\033[38;2;180;190;254m"

TEXT = "\033[38;2;205;214;244m"
SUBTEXT = "\033[38;2;186;194;222m"
OVERLAY = "\033[38;2;127;132;156m"

RESET = "\033[0m"
BOLD = "\033[1m"


def sysfetch():
    total, used, free = shutil.disk_usage("/")
    os_name = None
    device_id = None
    gpu_name = None
    gpu_pci_path = None
    hostname = open("/etc/hostname").read().strip()
    username = os.getenv("USER", "unknown")
    wm = os.getenv("XDG_CURRENT_DESKTOP", "Unknown")
    productname = open("/sys/devices/virtual/dmi/id/product_name").read().strip()
    term = (
        os.environ.get("TERM_PROGRAM") or os.environ.get("TERM") or "/dev/tty"
    ).capitalize()
    uptime = open("/proc/uptime").read().strip().split()
    uptime_seconds = int(math.trunc(float(uptime[0])))
    hours = int(uptime_seconds // 3600)
    minutes = int((uptime_seconds % 3600) // 60)
    seconds = int(uptime_seconds % 60)
    cpu = None
    pacman_dir = "/var/lib/pacman/local/"
    if os.path.exists(pacman_dir):
        packages = sum(1 for entry in os.scandir(pacman_dir) if entry.is_dir())
    else:
        packages = 0

    # Memory formatting
    TotalGB = None
    AvailableGB = None

    def kb_to_gb(kb):
        return kb / (1024**2)

    def to_gb(bytes):
        return bytes / (1024**3)

    def color_blocks():
        blocks = []

        for i in range(8):
            blocks.append(f"\033[38;5;{i}m● ")

        return "".join(blocks) + RESET

    with open("/proc/meminfo") as mem:
        for line in mem:
            if line.startswith("MemTotal:"):
                TotalGB = kb_to_gb(
                    int(line.replace("MemTotal:", "").replace("kB", "").strip())
                )
            if line.startswith("MemAvailable:"):
                AvailableGB = kb_to_gb(
                    int(line.replace("MemAvailable:", "").replace("kB", "").strip())
                )

    with open("/proc/cpuinfo") as f:
        for line in f:
            if line.startswith("model name"):
                cpu = line.split(":", 1)[1].strip()
                break

    with open("/etc/os-release") as os_file:
        for line in os_file:
            if line.startswith("ID="):
                os_name = line.strip("ID=").replace('"', "").strip().lower()

    def parse_pci_ids():
        db = {}
        current_vendor = None

        try:
            with open("/usr/share/hwdata/pci.ids") as f:
                for line in f:
                    if not line.strip() or line.startswith("#"):
                        continue

                    if not line.startswith("\t"):
                        parts = line.strip().split(maxsplit=1)
                        if len(parts) == 2:
                            current_vendor = parts[0].lower()
                    else:
                        parts = line.strip().split(maxsplit=1)
                        if len(parts) == 2 and current_vendor:
                            device_id = parts[0].lower()
                            db[(current_vendor, device_id)] = parts[1]
        except OSError:
            pass

        return db

    def get_gpus():
        db = parse_pci_ids()
        gpus = []

        for path in glob.glob("/sys/bus/pci/devices/*/class"):
            try:
                with open(path) as f:
                    if not f.read().strip().startswith("0x03"):
                        continue

                base = path.rsplit("/", 1)[0]

                with open(f"{base}/vendor") as v, open(f"{base}/device") as d:
                    vendor_id = v.read().strip().replace("0x", "").lower()
                    device_id = d.read().strip().replace("0x", "").lower()

                name = db.get((vendor_id, device_id), f"{vendor_id}:{device_id}")

                gpus.append(name)

            except OSError:
                continue

        return gpus

    def get_resolution():
        drm_path = Path("/sys/class/drm")
        try:
            for entry in drm_path.iterdir():
                modes_path = entry / "modes"

                try:
                    content = modes_path.read_text()
                    first_line = content.splitlines()[0] if content else ""

                    if first_line:
                        return first_line
                except (FileNotFoundError, PermissionError, IsADirectoryError):
                    continue

        except FileNotFoundError:
            pass

        return "Unknown"

    gpus = get_gpus()
    active_ascii = None
    info_lines = [
        f"{LAVENDER}{username}{RESET}@{LAVENDER}{hostname}{RESET}",
        f"{SUBTEXT}----------------{RESET}",
        f"{LAVENDER}OS ❯{RESET} {TEXT}{os_name}{RESET}",
        f"{LAVENDER}Host ❯{RESET} {TEXT}{productname}{RESET}",
        f"{LAVENDER}Kernel ❯{RESET} {TEXT}{platform.system()} {platform.release()}{RESET}",
        f"{LAVENDER}Uptime ❯{RESET} {TEXT}{hours} hours, {minutes} mins, {seconds} secs{RESET}",
        f"{LAVENDER}Packages ❯{RESET} {TEXT}{packages}{RESET}",
        f"{LAVENDER}Shell ❯{RESET} {TEXT}DAPS - Definitely a Python Shell{RESET}",
        f"{LAVENDER}Terminal ❯{RESET} {TEXT}{term}{RESET}",
        f"{LAVENDER}Resolution ❯{RESET} {TEXT}{get_resolution()}{RESET}",
        f"{LAVENDER}WM ❯{RESET} {TEXT}{wm}{RESET}",
        *[f"{LAVENDER}GPU ❯{RESET} {TEXT}{gpu}{RESET}" for gpu in gpus],
        f"{LAVENDER}CPU ❯{RESET} {TEXT}{cpu}{RESET}",
        f"{LAVENDER}Memory ❯{RESET} {TEXT}{AvailableGB:.2f} GiB / {TotalGB:.2f} GiB{RESET}",
        f"{LAVENDER}Disk ❯{RESET} {TEXT}{to_gb(used):.2f} GiB / {to_gb(total):.2f} GiB{RESET}",
        f"{SUBTEXT}----------------{RESET}",
        f"{color_blocks()} ",
    ]

    if "arch" in os_name.split():
        active_ascii = [
            "                   -`                   ",
            "                  .o+`                  ",
            "                 `ooo/                  ",
            "                `+oooo:                 ",
            "               `+oooooo:                ",
            "               -+oooooo+:               ",
            "             `/:-:++oooo+:              ",
            "            `/++++/+++++++:             ",
            "           `/++++++++++++++:            ",
            "          `/+++ooooooooooooo/`          ",
            "         ./ooosssso++osssssso+`         ",
            "        .oossssso-````/ossssss+`        ",
            "       -osssssso.      :ssssssso.       ",
            "      :osssssss/        osssso+++.      ",
            "     /ossssssss/        +ssssooo/-      ",
            "   `/ossssso+/:-        -:/+osssso+-    ",
            "  `+sso+:-`                 `.-/+oso:   ",
            " `++:.                           `-/+/  ",
            " .`                                 `/  ",
        ]
    elif "nyarch" in os_name.split():
        active_ascii = [
            "                     +*                     ",
            "                    =**+                    ",
            "                   -****+                   ",
            "                  :#*****=                  ",
            "          :=-:.  .#*******-        .        ",
            "           +=++++--+*******=:=++==+:        ",
            "           -+=+***+=+********#*==+:         ",
            "           :**#**##*******##***++=          ",
            "             =#+++***####**+++*:.           ",
            "            :***+-+#*=+=*#+-=**-            ",
            "           -*##+*#%%*::-#%%#*+##=           ",
            "          -#*##%%%%=    .#%%%##**+:::::::.  ",
            "      .::+#**#%%%%=  ..:.=%%%%#**#*:   ..-=-",
            "   .--:.+###*###**-:-::.. *%%%%*+==+..::::. ",
            "  :=:  =*++++***##:      .+****++++*=..     ",
            "   ::-+*******+=-:   :---:..-=***###*+.     ",
            "    .*#*+=:.       :-:.         .:-+***:    ",
            "   :+=:           :-                 :-+-   ",
            "   :                                    .   ",
        ]
    elif "fedora" in os_name.split():
        active_ascii = [
            "           .',;::::;,'.                ",
            "       .';:cccccccccccc:;,.            ",
            "    .;cccccccccccccccccccccc;.         ",
            "  .:cccccccccccccccccccccccccc:.       ",
            ".;ccccccccccccc;.:dddl:.;ccccccc;.     ",
            ".:ccccccccccccc;OWMKOOXMWd;ccccccc:.   ",
            ".:ccccccccccccc;KMMc;cc;xMMc;ccccccc:. ",
            ",cccccccccccccc;MMM.;cc;;WW:;cccccccc, ",
            ":cccccccccccccc;MMM.;cccccccccccccccc: ",
            ":ccccccc;oxOOOo;MMM000k.;cccccccccccc: ",
            "cccccc;0MMKxdd:;MMMkddc.;cccccccccccc; ",
            "ccccc;XMO';cccc;MMM.;cccccccccccccccc' ",
            "ccccc;MMo;ccccc;MMW.;ccccccccccccccc;  ",
            "ccccc;0MNc.ccc.xMMd;ccccccccccccccc;   ",
            "cccccc;dNMWXXXWM0:;cccccccccccccc:,    ",
            "cccccccc;.:odl:.;cccccccccccccc:,.     ",
            "ccccccccccccccccccccccccccccc:'.       ",
            ":ccccccccccccccccccccccc:;,..          ",
            " ':cccccccccccccccc::;,.               ",
        ]

    assert active_ascii is not None

    print("\033[?7l", end="")  # disable line wrap
    for art, text in zip_longest(active_ascii, info_lines, fillvalue=""):
        # the extra spaces are for padding
        print(f"{LAVENDER}{art}{RESET}   {text}")
    print("\033[?7h", end="")  # enable line wrap
    print()


class Config:
    def __init__(self):
        self.aliases = {}
        self.devicename = False
        self.cleargreet = False
        self.greeter = None


def loadconf():
    config_dir = os.path.expanduser("~/.config/daps")
    modules_dir = os.path.join(config_dir, "modules")
    config_file = os.path.join(config_dir, "config.py")
    if not os.path.exists(modules_dir):
        os.makedirs(modules_dir)
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)

    if not os.path.exists(config_file):
        with open(config_file, "w") as f:
            f.write("""
daps = Config()
daps.aliases = {}
daps.devicename = False
daps.cleargreet = False
daps.greeter = None
""")

    config_parent = os.path.dirname(config_dir)
    if config_parent not in sys.path:
        sys.path.insert(0, config_parent)

    spec = importlib.util.spec_from_file_location("daps.config", config_file)
    assert spec is not None
    config_module = importlib.util.module_from_spec(spec)

    setattr(config_module, "Config", Config)
    assert spec.loader
    spec.loader.exec_module(config_module)

    # Return the daps object as a dict
    return config_module.daps.__dict__


loadconf()


def load_modules():
    """Load all command modules"""
    modules_dir = os.path.expanduser("~/.config/daps/modules")
    module_manager = os.path.expanduser("~/.config/daps/modules/plugin.py")
    if modules_dir not in sys.path:
        sys.path.insert(0, os.path.dirname(modules_dir))
    modules = {}
    for file in os.listdir(modules_dir):
        if file.endswith(".py") and file != "__init__.py":
            module_name = file[:-3]
            spec = importlib.util.spec_from_file_location(
                module_name, os.path.join(modules_dir, file)
            )
            assert spec is not None
            module = importlib.util.module_from_spec(spec)
            assert spec.loader
            spec.loader.exec_module(module)
            modules[module_name] = module

    return modules


modules = load_modules()

# Shenanigans taht make it go brrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr
config = loadconf()
greeter = config.get("greeter")
alias = config.get("aliases", {})
devicename = bool(config.get("devicename", False))
cleargreet = bool(config.get("cleargreet", False))
git = bool(config.get("git", True))
signal.signal(signal.SIGINT, signal.SIG_IGN)
readline.parse_and_bind("tab: complete")
readline.parse_and_bind("set show-all-if-ambiguous-on")
historyfile = os.path.expanduser("~/.daps.history")
if os.path.exists(historyfile):
    readline.read_history_file(historyfile)
user = subprocess.run(["whoami"], capture_output=True, text=True).stdout.strip()
if devicename:
    hostn = subprocess.run(
        "cat /sys/devices/virtual/dmi/id/product_name",
        shell=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
else:
    hostn = subprocess.run(
        ["cat", "/etc/hostname"], capture_output=True, text=True
    ).stdout.strip()
cwd = os.getcwd()
iden = "$"
if cwd == f"/home/{user}":
    cwd = "~"
elif cwd == "/root":
    if user == "root":
        cwd = "~"
        iden = "#"
    else:
        pass


def update():
    print("Updating.. A sudo prompt may appear soon.")
    os.system("rm -rf /tmp/daps/")
    os.system("git clone https://github.com/NytrixLabs/DAPS /tmp/daps")
    os.system("sudo cp /tmp/daps/daps /usr/bin/daps")
    os.system("rm -rf /tmp/daps/")
    print("Done!")


def clear():
    os.system("clear")


def runfc(confsec: str):
    torun = config.get(confsec)
    if not torun:
        return
    os.system(torun)


def getgit():
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            capture_output=True,
            text=True,
            stderr=subprocess.DEVNULL,
            cwd=os.getcwd(),
        )
        if result.returncode != 0:
            return ""

        branch_result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            cwd=os.getcwd(),
        )
        branch = branch_result.stdout.strip()

        status_result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            cwd=os.getcwd(),
        )

        if status_result.stdout.strip():
            return f" ({branch}*)"
        else:
            return f" ({branch})"
    except:
        return ""


# out = subprocess.run([f"{torun}"], capture_output=True, text=True)
# print(out.stdout)
clear()
if greeter == "daps":
    sysfetch()
else:
    runfc("greeter")
if git:
    repo = getgit()
historycleared = 0
errcode = None
while True:
    try:
        cwd = os.getcwd()
        home = os.path.expanduser("~")
        if cwd.startswith(home):
            cwd = cwd.replace(home, "~", 1)
        if not errcode:
            print(
                f"{COLOR_USER}{user}{COLOR_RE}@{COLOR_HOST}{hostn}{COLOR_RE} {COLOR_USER}({iden}){COLOR_RE} - {COLOR_CWD}{cwd}{COLOR_RE} {repo}"
            )
        else:
            print(
                f"{COLOR_ERR}[{errcode}]{COLOR_RE} - {COLOR_USER}{user}{COLOR_RE}@{COLOR_HOST}{hostn}{COLOR_RE} {COLOR_USER}({iden}){COLOR_RE} - {COLOR_CWD}{cwd}"
            )
        try:
            cmd = input(f"{COLOR_USER}>{COLOR_HOST} ").strip()
        except EOFError:
            print("An exception occurred at ^D - EOFError.\n DAPS will now close.")
            sys.exit(123)
        if cmd in alias:
            cmd = alias[cmd]
        if not cmd:
            continue
        cmdsp = cmd.split()
        ccmd = cmdsp[0]
        ccmar = cmdsp[1:]
        all_cmds = [ccmd] + ccmar
        if ccmd == "cd":
            dir = pathlib.Path(ccmar[0] if ccmar else "~")
            if not dir.expanduser().exists():
                print("cd: No such file or directory")
                errcode = 2
            os.chdir(dir.expanduser())
        elif ccmd == "clear":
            clear()
            if cleargreet:
                runfc("greeter")
        elif ccmd == "clearhist":
            readline.clear_history()
            open(historyfile, "w").close()
            historycleared = 1
            print(
                f"{COLOR_ERR}ATTENTION! History will no longer be recorded until you restart the shell! (exit and then log back in/run daps)"
            )
        elif ccmd == "update":
            update()
        elif ccmd == "exit":
            sys.exit(255)
        elif "." in ccmd:
            module_name, func_name = ccmd.split(".", 1)
            if module_name in modules and hasattr(modules[module_name], func_name):
                try:
                    func = getattr(modules[module_name], func_name)
                    result = func(ccmar) if ccmar else func()
                    errcode = 0
                except Exception as e:
                    print(f"Error running {ccmd}: {e}")
                    errcode = 1
            else:
                print(f"Command not found: {ccmd}")
                errcode = 127
        elif shutil.which(ccmd):
            result = subprocess.run(
                [ccmd] + ccmar, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr
            )
            errcode = result.returncode
        else:
            result = subprocess.run(cmd, shell=True)
            errcode = result.returncode
    except Exception as e:
        print(f"An exception has occurred. {e}")
    finally:
        if errcode == "0":
            errcode = False
        if historycleared:
            readline.clear_history()
        else:
            readline.write_history_file(historyfile)
