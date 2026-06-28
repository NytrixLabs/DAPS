# DAPS

DAPS is a shell written in pure Python. No other language is used—even your configuration file is pure Python code!

[![PyPI Version](https://img.shields.io/pypi/v/daps-pip?style=for-the-badge&color=blue)](https://pypi.org/project/daps-pip/)
[![PyPI Downloads](https://img.shields.io/pypi/dm/daps-pip?style=for-the-badge&color=green)](https://pypi.org/project/daps-pip/)

---

DAPS is available on PyPI!

```bash
pip install daps-pip
```

## Usage

Basic shell commands work seamlessly, like `cd` or `ls`.  

Built-in commands include:

- `clear` – Clears everything on screen.  
- `clearhist` – Clears shell history. After running this, the shell cannot record history until restarted. This prevents bugs.  
- `exit` – Exits the shell.  
- `update` – Updates DAPS to the latest version.

---

### `clear`

The `clear` command clears the screen.  
See **Configuration** below for behavior options.

### `clearhist`

Clears shell history.  
The shell cannot record history if this command has been run until the shell is restarted. This is a safety feature.

### `exit`

Exits the shell.

### `update`

Updates DAPS by cloning the repository into a temporary folder and copying the new version into `/usr/bin`.

---

## Configuration

The shell automatically creates a configuration file named `config.py` in your `~/.config/daps/` directory. 

Because the configuration file is actual Python code, you modify settings by changing properties on the `daps` object. By default, the file initializes with:

```python
daps = Config()
daps.aliases = {}
daps.devicename = False
daps.cleargreet = False
daps.greeter = None
```

---

### `daps.greeter`

The `greeter` option runs a command as a string every time the shell starts:

```python
daps.greeter = "fastfetch"
```

---

### `daps.aliases`

The `aliases` option uses a Python dictionary to define your shell aliases:

```python
daps.aliases = {
    "ll": "ls -l",
    "gcm": "git commit -m"
}
```

**Note:** Built-in shell commands cannot be used in aliases. Built-in commands are listed in the usage section above.

---

### `daps.cleargreet`

The `cleargreet` option expects a boolean value (`True` or `False`). It specifies whether your greeter command should run again when you type `clear`:

```python
daps.cleargreet = True
```

---

### `daps.devicename`

The `devicename` option expects a boolean value (`True` or `False`). It specifies if your literal **device name** (e.g., `ASUS E410MA`) should be displayed in the prompt instead of the standard network hostname (e.g., `fedora`):

```python
daps.devicename = True
```

---

### Example of a full `config.py`

```python
daps = Config()

# Custom Shell Customization
daps.greeter = "fastfetch"
daps.cleargreet = True
daps.devicename = False

# Quick Aliases
daps.aliases = {
    "ll": "ls -lh",
    "la": "ls -A"
}
```

---

## More Information

- More features are coming soon!  
- DAPS is protected by the **GNU license**, meaning any contributions or derivatives of the program **must be fully open source**.  

---

**© 2026, Nytrix Labs**
