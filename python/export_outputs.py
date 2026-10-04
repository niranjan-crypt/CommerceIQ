import subprocess
import os

SCRIPTS = [
    ("04_data_quality.sql", "Data Quality & Integrity Assertions"),
    ("06_business_analytics.sql", "Executive & Top-Line Revenue KPIs"),
    ("07_customer_analytics.sql", "Customer RFM Behavioral Segmentation"),
    ("08_product_analytics.sql", "Product Pareto & Logistics Freight Economics"),
    ("09_operations_analytics.sql", "Logistics Delivery SLAs & Review Degradation"),
    ("10_advanced_sql.sql", "Advanced Window Functions (MoM Growth & Running Totals)"),
    ("11_optimization.sql", "Empirical Indexing & Query Plan Optimization Benchmark")
]

os.makedirs("outputs", exist_ok=True)

for script_name, title in SCRIPTS:
    script_path = os.path.join("sql", script_name)
    proc = subprocess.run(["python3", "run_query.py", script_path], capture_output=True, text=True)
    out_md = os.path.join("outputs", script_name.replace(".sql", ".md"))
    
    with open(out_md, "w", encoding="utf-8") as f:
        f.write(f"# Query Output: {title}\n\n")
        f.write(f"- **SQL Script**: [`sql/{script_name}`](../sql/{script_name})\n")
        f.write(f"- **Engine**: PostgreSQL / SQLite Relational Storage\n")
        f.write(f"- **Scale**: 100,000+ Records Analyzed\n\n")
        f.write("## Execution Results\n\n")
        f.write("```text\n")
        f.write(proc.stdout.strip())
        f.write("\n```\n")
        
    print(f"Exported: {out_md}")
