import sqlite3
import sys
import os
import time

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "olist_oltp.db")

BANNER = r"""
   ____                                           ___ ___  
  / ___|___  _ __ ___  _ __ ___   ___ _ __ ___   |_ _/ _ \ 
 | |   / _ \| '_ ` _ \| '_ ` _ \ / _ \ '__/ __|   | | | | |
 | |__| (_) | | | | | | | | | | |  __/ | | (__    | | |_| |
  \____\___/|_| |_| |_|_| |_| |_|\___|_|  \___|  |___\__\_\
   Enterprise Data Engineering & Customer Analytics Platform
"""

def format_table(headers, rows):
    if not rows:
        return "(0 rows returned)"
    
    str_rows = [[str(val) if val is not None else "NULL" for val in row] for row in rows]
    col_widths = [len(h) for h in headers]
    for row in str_rows:
        for idx, val in enumerate(row):
            col_widths[idx] = max(col_widths[idx], len(val))
    
    col_widths = [min(w, 40) for w in col_widths]
    
    header_line = " | ".join(h.ljust(col_widths[i])[:col_widths[i]] for i, h in enumerate(headers))
    sep_line = "-+-".join("-" * col_widths[i] for i in range(len(headers)))
    
    lines = [header_line, sep_line]
    for row in str_rows:
        line = " | ".join(row[i].ljust(col_widths[i])[:col_widths[i]] for i, h in enumerate(headers))
        lines.append(line)
    
    return "\n".join(lines)

def execute_query(query: str):
    if not os.path.exists(DB_PATH):
        print(f"\n[ERROR] Database not found at: {DB_PATH}")
        print("Run `python3 python/database_loader.py` to initialize and populate the database.\n")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    start_time = time.perf_counter()
    try:
        statements = [s.strip() for s in query.split(";") if s.strip()]
        for stmt in statements:
            lines = [l for l in stmt.splitlines() if not l.strip().startswith("--")]
            clean_stmt = "\n".join(lines).strip()
            if not clean_stmt:
                continue
                
            upper_stmt = clean_stmt.upper()
            if upper_stmt.startswith("SELECT") or upper_stmt.startswith("WITH") or upper_stmt.startswith("EXPLAIN"):
                t0 = time.perf_counter()
                cur.execute(clean_stmt)
                elapsed_ms = (time.perf_counter() - t0) * 1000
                if cur.description:
                    headers = [desc[0] for desc in cur.description]
                    rows = cur.fetchall()
                    print("\n" + format_table(headers, rows))
                    print(f"\n⚡ ({len(rows):,} row{'s' if len(rows) != 1 else ''} in {elapsed_ms:.2f} ms)\n")
            else:
                t0 = time.perf_counter()
                cur.execute(clean_stmt)
                conn.commit()
                elapsed_ms = (time.perf_counter() - t0) * 1000
                print(f"Statement executed successfully in {elapsed_ms:.2f} ms.")
    except Exception as e:
        print(f"\n[SQL ERROR] {e}\n")
    finally:
        conn.close()

def interactive_shell():
    print(BANNER)
    print("Connected to:", DB_PATH)
    print("Type your SQL query and press Enter. End with ';' or type 'exit' to quit.\n")
    
    buffer = []
    while True:
        try:
            prompt = "commerceiq> " if not buffer else "      ...> "
            line = input(prompt)
            if line.strip().lower() in ("exit", "quit", "\\q"):
                print("Exiting CommerceIQ interactive shell. Goodbye!")
                break
            if line.strip().lower() in (".tables", "\\dt"):
                execute_query("SELECT name FROM sqlite_master WHERE type IN ('table', 'view') ORDER BY name;")
                continue
            
            buffer.append(line)
            if ";" in line:
                full_query = " ".join(buffer)
                execute_query(full_query)
                buffer = []
        except (KeyboardInterrupt, EOFError):
            print("\nExiting CommerceIQ shell.")
            break

if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if os.path.exists(arg):
            with open(arg, "r") as f:
                execute_query(f.read())
        else:
            execute_query(arg)
    else:
        interactive_shell()
