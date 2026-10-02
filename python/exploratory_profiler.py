import os
import csv
import glob

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
DOCS_DIR = os.path.join(os.path.dirname(__file__), "..", "docs")

def profile_dataset(file_path):
    table_name = os.path.basename(file_path).replace(".csv", "")
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f)
        headers = next(reader)
        row_count = 0
        null_counts = [0] * len(headers)
        sample_values = [None] * len(headers)
        
        for row in reader:
            row_count += 1
            for i, val in enumerate(row):
                val_clean = val.strip()
                if val_clean == "" or val_clean.lower() == "null":
                    null_counts[i] += 1
                elif sample_values[i] is None and val_clean:
                    sample_values[i] = val_clean[:30]
                    
    return {
        "table": table_name,
        "rows": row_count,
        "cols": len(headers),
        "headers": headers,
        "null_counts": null_counts,
        "sample_values": sample_values
    }

def generate_report():
    files = sorted(glob.glob(os.path.join(RAW_DIR, "*.csv")))
    out_lines = [
        "# CommerceIQ: Comprehensive Dataset Dictionary & Profile",
        "",
        "This data dictionary profiles the raw Olist Brazilian E-Commerce dataset.",
        "It details schema structures, cardinality, null counts, and candidate keys for our relational modeling.",
        "",
        "## Summary of Raw Datasets",
        "",
        "| Table Name | Total Records | Column Count | Potential Primary Key |",
        "| :--- | :--- | :--- | :--- |"
    ]
    
    profiles = []
    for fp in files:
        prof = profile_dataset(fp)
        profiles.append(prof)
        pk_cand = prof["headers"][0] if prof["headers"] else "N/A"
        out_lines.append(f"| `{prof['table']}` | {prof['rows']:,} | {prof['cols']} | `{pk_cand}` |")
        
    out_lines.append("\n---\n")
    out_lines.append("## Detailed Table Specifications\n")
    
    for prof in profiles:
        out_lines.append(f"### Table: `{prof['table']}`")
        out_lines.append(f"- **Row Count**: {prof['rows']:,}")
        out_lines.append(f"- **Column Count**: {prof['cols']}\n")
        out_lines.append("| Column Name | Null Count | Null % | Sample Value | Suggested Postgres Type |")
        out_lines.append("| :--- | :--- | :--- | :--- | :--- |")
        
        for idx, col in enumerate(prof["headers"]):
            nulls = prof["null_counts"][idx]
            null_pct = (nulls / prof["rows"] * 100) if prof["rows"] > 0 else 0
            sample = prof["sample_values"][idx] if prof["sample_values"][idx] else "N/A"
            
            # Precise heuristic for suggested types
            col_l = col.lower()
            if col_l.endswith("_date") or col_l.endswith("_timestamp") or col_l in ("order_approved_at",):
                sug_type = "TIMESTAMP"
            elif col_l in ("price", "freight_value", "payment_value"):
                sug_type = "NUMERIC(10, 2)"
            elif col_l in ("order_item_id", "payment_sequential", "payment_installments", "review_score", "product_photos_qty"):
                sug_type = "INTEGER"
            elif col_l.endswith("_g") or col_l.endswith("_cm"):
                sug_type = "INTEGER"
            elif col_l in ("geolocation_lat", "geolocation_lng"):
                sug_type = "NUMERIC(10, 6)"
            elif col_l.endswith("_state"):
                sug_type = "VARCHAR(2)"
            elif col_l.endswith("_zip_code_prefix"):
                sug_type = "VARCHAR(5)"
            elif col_l.endswith("_id") or col_l == "customer_unique_id":
                sug_type = "VARCHAR(32)"
            else:
                sug_type = "VARCHAR(255)"
                
            out_lines.append(f"| `{col}` | {nulls:,} | {null_pct:.1f}% | `{sample}` | `{sug_type}` |")
            
        out_lines.append("\n---\n")
        
    dict_path = os.path.join(DOCS_DIR, "data_dictionary.md")
    with open(dict_path, "w", encoding="utf-8") as f:
        f.write("\n".join(out_lines))
    print(f"Data dictionary successfully written to: {dict_path}")

if __name__ == "__main__":
    generate_report()
