# DAPS

DAPS is a shell written in pure Python. No other language is used, except JSON for the configuration file.

[![PyPI Version](https://img.shields.io/pypi/v/daps-pip?style=for-the-badge&color=blue)](https://pypi.org/project/daps-pip/)
[![PyPI Downloads](https://img.shields.io/pypi/dm/daps-pip?style=for-the-badge&color=green)](https://pypi.org/project/daps-pip/)

---

DAPS is available on PyPl!

```bash
pip install daps-pip
```

## Usage

Basic shell commands work, like `cd` or `ls`.  

Built-in commands include:

- `clear` – Clears everything on screen.  
- `clearhist` – Clears shell history. After running this, the shell cannot record history until restarted. This prevents bugs.  
- `exit` – Exits the shell.  

---

### `clear`

The `clear` command clears the screen.  
See **Configuration** below for options.

### `clearhist`

Clears shell history.  
The shell cannot record history if this command has been run, until the shell is restarted. This is a safety feature.

### `exit`

Exits the shell.

### `update`

Updates DAPS by cloning the repository into a temporary folder and copying the new version into `/usr/bin`.

---

## Configuration

The shell creates a file named `config.json` in the `~/.config/daps/` directory (where `~` is your current user's home folder).  

By default, the file contains:

```json
{}
```

To start editing, add options inside the braces:

```json
{
}
```

---

### `"greeter"`

The `"greeter"` option runs a command every time the shell starts:

```json
{
  "greeter": "fastfetch"
}
```

This will run `fastfetch` at shell start.

---

### `"aliases"`

The `"aliases"` option lets you create shell aliases:

```json
{
  "aliases": {
    "ll": "ls -l"
  }
}
```

**Note:** Built-in shell commands cannot be used in aliases. Built-in commands are listed above.

---

### `"cleargreet"`

The `"cleargreet"` option specifies whether the greeter should run when using `clear`:

```json
{
  "cleargreet": "yes"
}
```

---

### `"devicename"`

The `"devicename"` option specifies if the **device name** (e.g., `ASUS E410MA`) should be used instead of the hostname (e.g., `fedora`):

```json
{
  "devicename": true
}
```

---

### Example of a full config

```json
{
  "aliases": {
    "ll": "ls -l"
  },
  "greeter": "fastfetch",
  "cleargreet": "yes",
  "devicename": true
}
```

---

## More Information

- More features are coming soon!  
- DAPS is protected by the **GNU license**, meaning any contributions or derivatives of the program **must be fully open source**.  

---

**© 2026, Nytrix Labs**
