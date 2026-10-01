# CommerceIQ: DBMS Fundamentals, Relational Architecture & Normalization

## 1. Relational Database Management Systems (RDBMS) & ACID Properties

In a production transactional system (OLTP), data reliability is guaranteed through the **ACID** properties:
- **Atomicity (All or Nothing)**: A transaction is an indivisible unit. If an order insertion succeeds but payment deduction fails, the entire transaction is rolled back.
- **Consistency (Rules Enforcement)**: Every transaction brings the database from one valid state to another according to all defined schema constraints (foreign keys, check constraints, unique constraints).
- **Isolation (Concurrency Control)**: Concurrent transactions execute without interfering with one another. (Standard SQL Isolation levels: `Read Uncommitted`, `Read Committed`, `Repeatable Read`, `Serializable`).
- **Durability (Persistence)**: Once a transaction commits, its effects survive system crashes via the Write-Ahead Log (WAL).

---

## 2. Primary Keys, Foreign Keys, and Cardinality

### Primary Key (PK)
A minimal set of attributes that uniquely identifies each tuple (row) in a relation (table).
- **Surrogate Key**: A system-generated unique identifier with no intrinsic business meaning (e.g., auto-incrementing integer `BIGSERIAL` or `UUID`). Best for immutability.
- **Natural Key**: An attribute that already exists in the real world (e.g., `tax_id`, `email`, `VIN`). Dangerous if business definitions change.

### Foreign Key (FK) & Referential Integrity
An attribute or collection of attributes in one table that refers to the Primary Key of another table.
- **Referential Action Rules**:
  - `ON DELETE RESTRICT`: Blocks parent deletion if child records exist (standard for financial audit trails).
  - `ON DELETE CASCADE`: Deletes child rows when the parent is deleted (e.g., deleting an order deletes its line items).
  - `ON DELETE SET NULL`: Sets foreign key columns to NULL in child records when the parent is deleted.

### Cardinality & Relationships
1. **One-to-One (1:1)**: e.g., An order has exactly one review record (`order_id` in reviews is UNIQUE).
2. **One-to-Many (1:N)**: e.g., One customer places many orders; one seller lists many items.
3. **Many-to-Many (M:N)**: e.g., Orders and Products. Resolved via an associative junction table (`order_items`).

---

## 3. Normalization (1NF, 2NF, 3NF) vs. Denormalization

### Why Normalize?
To eliminate **redundancy** and avoid three critical data anomalies:
1. **Insertion Anomaly**: Inability to record certain facts without adding unrelated attributes (e.g., unable to add a new product category without adding a product).
2. **Update Anomaly**: Changing an attribute in one place requires updating dozens of redundant rows (risk of inconsistency).
3. **Deletion Anomaly**: Deleting one piece of data inadvertently destroys other independent information (e.g., deleting a customer's only order deletes customer details).

### Normal Forms Breakdown:
* **1NF (First Normal Form)**:
  - Each column contains atomic (indivisible) values.
  - No repeating groups or arrays stored as comma-separated strings.
  - A unique primary key exists.
* **2NF (Second Normal Form)**:
  - Must be in 1NF.
  - **No partial functional dependencies**: All non-key attributes must be fully functionally dependent on the entire primary key (relevant when a table has a composite primary key).
* **3NF (Third Normal Form)**:
  - Must be in 2NF.
  - **No transitive functional dependencies**: Non-key attributes must depend *only* on the primary key, not on other non-key attributes ($X \to Y \to Z$).
  - *"Each attribute must depend on the key, the whole key, and nothing but the key, so help me Codd."*

---

## 4. OLTP vs. OLAP Architecture

| Dimension | OLTP (Online Transaction Processing) | OLAP (Online Analytical Processing) |
| :--- | :--- | :--- |
| **Primary Goal** | High-throughput, low-latency transaction processing | High-speed analytical aggregations, reporting, and BI |
| **Database Design** | Normalized (3NF) to minimize write amplification and lock contention | Denormalized (Star Schema / Snowflake Schema) |
| **Workload Type** | High volume of simple, targeted `INSERT`, `UPDATE`, `DELETE` | Batch `SELECT` queries scanning millions of historical rows |
| **Query Pattern** | `SELECT * FROM orders WHERE order_id = ?` (single-row lookup) | `SELECT date_trunc('month', date), SUM(price) GROUP BY 1` |
| **Latency Expectation** | Milliseconds (< 50ms) | Seconds to minutes |
| **Indexing Strategy** | Focused B-trees on primary and foreign keys | Bitmap indexes, columnar storage, composite indexes |
| **Schema in CommerceIQ** | PostgreSQL Normalized 3NF Schema | Analytical Fact & Dimension Star Schema |
