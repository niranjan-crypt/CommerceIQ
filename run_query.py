import sqlite3
import sys
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "olist_oltp.db")

def format_table(headers, rows):
    if not rows:
        return "(0 rows returned)"
    
    # Calculate column widths
    str_rows = [[str(val) if val is not None else "NULL" for val in row] for row in rows]
    col_widths = [len(h) for h in headers]
    for row in str_rows:
        for idx, val in enumerate(row):
            col_widths[idx] = max(col_widths[idx], len(val))
    
    # Cap column width at 40 chars for readability
    col_widths = [min(w, 40) for w in col_widths]
    
    # Build separator and row templates
    header_line = " | ".join(h.ljust(col_widths[i])[:col_widths[i]] for i, h in enumerate(headers))
    sep_line = "-+-".join("-" * col_widths[i] for i in range(len(headers)))
    
    lines = [header_line, sep_line]
    for row in str_rows:
        line = " | ".join(row[i].ljust(col_widths[i])[:col_widths[i]] for i in range(len(headers)))
        lines.append(line)
    
    return "\n".join(lines)

def execute_query(query: str):
    if not os.path.exists(DB_PATH):
        print(f"Error: Database not found at {DB_PATH}")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        # Split queries by semicolon, preserving comments
        statements = [s.strip() for s in query.split(";") if s.strip()]
        for stmt in statements:
            # Check if this statement is a query
            lines = [l for l in stmt.splitlines() if not l.strip().startswith("--")]
            clean_stmt = "\n".join(lines).strip()
            if not clean_stmt:
                continue
                
            if clean_stmt.upper().startswith("SELECT") or clean_stmt.upper().startswith("WITH") or clean_stmt.upper().startswith("EXPLAIN"):
                cur.execute(clean_stmt)
                if cur.description:
                    headers = [desc[0] for desc in cur.description]
                    rows = cur.fetchall()
                    print("\n" + format_table(headers, rows))
                    print(f"({len(rows)} row{'s' if len(rows) != 1 else ''})\n")
            else:
                cur.execute(clean_stmt)
                conn.commit()
                print("Statement executed successfully.")
    except Exception as e:
        print(f"\nSQL Error: {e}\n")
    finally:
        conn.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if os.path.exists(arg):
            with open(arg, "r") as f:
                execute_query(f.read())
        else:
            execute_query(arg)
    else:
        print("Usage:")
        print("  python3 run_query.py \"SELECT * FROM orders LIMIT 5;\"")
        print("  python3 run_query.py sql/day1_exercises.sql")
