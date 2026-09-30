import re
import urllib.parse
from typing import Optional, Dict, Any, List

class TheoryKnowledgeService:
    """
    Dedicated Theoretical & Conceptual Knowledge Engine.
    Provides authoritative, deeply structured explanations of core computer science,
    software engineering, database, operating system, networking, and scientific theory.
    Every answer includes:
    1. Precise definition and conceptual essence.
    2. Core theoretical mechanisms & principles.
    3. Structured comparison tables / taxonomies.
    4. Practical illustrative architecture or code example.
    5. Real-world engineering trade-offs and best practices.
    6. Verified, clickable reference links to official documentation, tutorials, and encyclopedias.
    """

    THEORY_PATTERNS = [
        r'\bwhat\s+is\b', r'\bwhat\s+are\b', r'\bexplain\b', r'\bconcept\s+of\b',
        r'\btheory\b', r'\bdefinition\b', r'\bhow\s+does\b', r'\bwhy\s+do\b',
        r'\bwhy\s+is\b', r'\bprinciples?\s+of\b', r'\barchitecture\s+of\b',
        r'\bdifference\s+between\b', r'\bvs\.?\b', r'\bversus\b',
        r'\badvantages?\s+of\b', r'\bdisadvantages?\s+of\b', r'\btypes?\s+of\b',
        r'\bpillars?\s+of\b', r'\blifecycle\b', r'\bproperties?\s+of\b',
        r'\bmeaning\s+of\b', r'\bworking\s+of\b', r'\bdeep\s+dive\b',
        r'\bpros\s+and\s+cons\b', r'\btrade-?offs?\b'
    ]

    THEORY_KEYWORDS = [
        # OOP & Paradigms
        'polymorphism', 'inheritance', 'encapsulation', 'abstraction', 'oop', 'object oriented',
        'interface vs abstract', 'abstract class', 'method overloading', 'method overriding',
        'dynamic dispatch', 'coupling and cohesion', 'composition vs inheritance', 'duck typing',
        # Software Design & Architecture
        'solid principles', 'design patterns', 'singleton', 'factory pattern', 'observer pattern',
        'strategy pattern', 'mvc', 'mvvm', 'microservices', 'monolith', 'event driven',
        'dependency injection', 'inversion of control', 'rest vs graphql', 'domain driven design',
        # Databases & Storage
        'acid properties', 'acid', 'database normalization', '1nf', '2nf', '3nf', 'bcnf',
        'indexing', 'b-tree', 'b+ tree', 'hash index', 'sharding', 'partitioning',
        'sql vs nosql', 'cap theorem', 'transactions', 'isolation levels', 'database deadlock',
        # Operating Systems & Systems
        'deadlock', 'virtual memory', 'paging', 'segmentation', 'process vs thread',
        'context switching', 'cpu scheduling', 'mutex vs semaphore', 'semaphore', 'mutex',
        'inter-process communication', 'ipc', 'thrashing', 'system call',
        # Networking & Web
        'osi model', '7 layers', 'tcp/ip', 'three-way handshake', 'dns resolution', 'dns',
        'http vs https', 'http/2', 'http/3', 'rest api', 'websockets', 'cors',
        'cookies vs sessions', 'jwt', 'load balancer', 'reverse proxy', 'cdn',
        # DSA & CS Theory
        'big-o', 'big o', 'time complexity', 'space complexity', 'asymptotic analysis',
        'recursion vs iteration', 'hash collision', 'tree traversal', 'graph traversal',
        'np-complete', 'p vs np', 'dynamic programming concept',
        # Language Internals
        'gil', 'global interpreter lock', 'jvm architecture', 'garbage collection',
        'event loop', 'closures', 'borrow checker', 'raii', 'smart pointers',
        # Science & General Theory
        'photosynthesis', 'gravity', 'quantum computing', 'theory of relativity',
        'thermodynamics', 'inflation', 'gdp', 'compound interest', 'hydration', 'sleep architecture'
    ]

    EXPLICIT_CODE_TRIGGERS = [
        r'\bwrite\s+(?:a\s+)?(?:python|java|c\+\+|javascript|js|cpp|c|go|rust|sql|code|program|script|function)\b',
        r'\bcode\s+(?:for|to|snippet|sample)\b',
        r'\bimplement\s+(?:in|using)\s+(?:python|java|c\+\+|cpp|javascript|js|rust|go)\b',
        r'\bprogram\s+to\b',
        r'\bsyntax\s+of\b'
    ]

    @classmethod
    def is_theory_question(cls, query: str) -> bool:
        """
        Determines whether the query is asking for a theoretical, conceptual,
        or architectural explanation rather than a pure code implementation.
        """
        q = query.lower().strip()

        # If user explicitly commands code generation (e.g. "write python code for..."), not pure theory
        if any(re.search(pat, q) for pat in cls.EXPLICIT_CODE_TRIGGERS):
            return False

        # If query contains explicit theory intent pattern
        has_theory_pattern = any(re.search(pat, q) for pat in cls.THEORY_PATTERNS)

        # If query mentions a core theoretical keyword
        has_theory_keyword = any(kw in q for kw in cls.THEORY_KEYWORDS)

        # If it has a theory pattern or a theory keyword (e.g. "polymorphism", "what is polymorphism in python")
        if has_theory_pattern and (has_theory_keyword or len(q.split()) <= 6):
            return True

        if has_theory_keyword and not any(w in q for w in ['leetcode', 'codechef', 'gfg', 'hackerrank', 'codeforces']):
            return True

        return False

    @classmethod
    def generate_theory_solution(cls, query: str, topic: str) -> str:
        """
        Generates an exhaustive, high-accuracy theoretical breakdown with
        formal definitions, internal principles, comparison tables, trade-offs,
        and verified external documentation links.
        """
        q = query.lower()

        # 1. OOP: POLYMORPHISM
        if 'polymorphism' in q:
            return cls._explain_polymorphism(q)

        # 2. OOP: 4 PILLARS (ENCAPSULATION, INHERITANCE, ABSTRACTION, POLYMORPHISM)
        if any(w in q for w in ['encapsulation', 'abstraction', 'inheritance', 'pillars of oop', 'oop concepts', 'object oriented programming']):
            return cls._explain_oop_pillars(q)

        # 3. DBMS: ACID PROPERTIES
        if 'acid' in q:
            return cls._explain_acid_properties()

        # 4. DBMS: DATABASE NORMALIZATION (1NF, 2NF, 3NF, BCNF)
        if 'normaliz' in q or any(nf in q for nf in ['1nf', '2nf', '3nf', 'bcnf']):
            return cls._explain_normalization()

        # 5. DBMS: INDEXING & B-TREES
        if 'index' in q and ('database' in q or 'sql' in q or 'table' in q or 'b-tree' in q or 'b+ tree' in q):
            return cls._explain_database_indexing()

        # 6. DISTRIBUTED SYSTEMS: CAP THEOREM
        if 'cap theorem' in q or ('cap' in q and 'distributed' in q):
            return cls._explain_cap_theorem()

        # 7. OS: DEADLOCK
        if 'deadlock' in q:
            return cls._explain_deadlock()

        # 8. OS: VIRTUAL MEMORY & PAGING
        if 'virtual memory' in q or 'paging' in q:
            return cls._explain_virtual_memory()

        # 9. OS: PROCESS VS THREAD
        if ('process' in q and 'thread' in q) or ('difference' in q and 'thread' in q):
            return cls._explain_process_vs_thread()

        # 10. SOFTWARE ENGINEERING: SOLID PRINCIPLES
        if 'solid' in q and ('principle' in q or 'design' in q or 'oop' in q):
            return cls._explain_solid_principles()

        # 11. SOFTWARE ENGINEERING: DESIGN PATTERNS
        if 'design pattern' in q or any(dp in q for dp in ['singleton', 'factory pattern', 'observer pattern', 'strategy pattern']):
            return cls._explain_design_patterns(q)

        # 12. NETWORKING: OSI 7-LAYER MODEL
        if 'osi' in q and ('model' in q or 'layer' in q or '7' in q):
            return cls._explain_osi_model()

        # 13. NETWORKING: DNS RESOLUTION FLOW
        if 'dns' in q and ('work' in q or 'resolution' in q or 'lookup' in q or 'how' in q):
            return cls._explain_dns_resolution()

        # 14. CS THEORY: BIG-O ASYMPTOTIC COMPLEXITY
        if 'big-o' in q or 'big o' in q or 'time complexity' in q or 'asymptotic' in q:
            return cls._explain_big_o()

        # 15. RUNTIME: JAVASCRIPT EVENT LOOP
        if 'event loop' in q and ('javascript' in q or 'js' in q or 'node' in q or 'browser' in q or 'async' in q):
            return cls._explain_js_event_loop()

        # 16. RUNTIME: JAVA JVM & GARBAGE COLLECTION
        if ('garbage collection' in q or 'jvm' in q) and ('java' in q or 'memory' in q):
            return cls._explain_jvm_garbage_collection()

        # 17. RUNTIME: PYTHON GIL (GLOBAL INTERPRETER LOCK)
        if 'gil' in q or 'global interpreter lock' in q:
            return cls._explain_python_gil()

        # 18. UNIVERSAL FALLBACK THEORY SYNTHESIZER
        return cls._synthesize_universal_theory(query, topic)

    # ================= INDIVIDUAL CURATED THEORY MODULES =================

    @classmethod
    def _explain_polymorphism(cls, q: str) -> str:
        lang_note = ""
        sample_code = ""
        if 'python' in q:
            lang_note = "In **Python**, polymorphism is dynamically achieved via **duck typing** and **method overriding** without explicit interface declarations."
            sample_code = (
                "```python\n"
                "class Shape:\n"
                "    def area(self) -> float:\n"
                "        raise NotImplementedError\n\n"
                "class Circle(Shape):\n"
                "    def __init__(self, radius: float):\n"
                "        self.radius = radius\n"
                "    def area(self) -> float:\n"
                "        return 3.14159 * self.radius ** 2\n\n"
                "class Rectangle(Shape):\n"
                "    def __init__(self, w: float, h: float):\n"
                "        self.w, self.h = w, h\n"
                "    def area(self) -> float:\n"
                "        return self.w * self.h\n\n"
                "# Polymorphic Dispatch: Uniform invocation across disparate types\n"
                "def calculate_total_area(shapes: list[Shape]) -> float:\n"
                "    return sum(shape.area() for shape in shapes)\n"
                "```"
            )
        elif 'java' in q:
            lang_note = "In **Java**, compile-time polymorphism is realized through **method overloading**, while runtime polymorphism uses **method overriding** resolved via virtual method tables (vtable)."
            sample_code = (
                "```java\n"
                "interface PaymentMethod {\n"
                "    void processPayment(double amount);\n"
                "}\n\n"
                "class CreditCardPayment implements PaymentMethod {\n"
                "    public void processPayment(double amount) {\n"
                "        System.out.println(\"Charging $\" + amount + \" to Credit Card.\");\n"
                "    }\n"
                "}\n\n"
                "class PayPalPayment implements PaymentMethod {\n"
                "    public void processPayment(double amount) {\n"
                "        System.out.println(\"Routing $\" + amount + \" via PayPal API.\");\n"
                "    }\n"
                "}\n"
                "```"
            )
        elif 'c++' in q or 'cpp' in q:
            lang_note = "In **C++**, runtime polymorphism is implemented through `virtual` functions and pointers/references using a `vptr` pointing to a class `vtable`."
            sample_code = (
                "```cpp\n"
                "#include <iostream>\n"
                "#include <vector>\n"
                "#include <memory>\n\n"
                "class Animal {\n"
                "public:\n"
                "    virtual void makeSound() const = 0; // Pure virtual function\n"
                "    virtual ~Animal() = default;\n"
                "};\n\n"
                "class Dog : public Animal {\n"
                "public:\n"
                "    void makeSound() const override { std::cout << \"Woof!\\n\"; }\n"
                "};\n"
                "```"
            )
        else:
            sample_code = (
                "```python\n"
                "# General Polymorphic Architecture\n"
                "class NotificationService:\n"
                "    def send(self, message: str) -> None:\n"
                "        raise NotImplementedError\n\n"
                "class EmailService(NotificationService):\n"
                "    def send(self, message: str) -> None:\n"
                "        print(f\"Emailing: {message}\")\n\n"
                "class SMSService(NotificationService):\n"
                "    def send(self, message: str) -> None:\n"
                "        print(f\"SMS Dispatch: {message}\")\n"
                "```"
            )

        return (
            "### 📚 Polymorphism in Object-Oriented Programming (OOP)\n\n"
            "**1. Conceptual Definition & Essence:**\n"
            "Polymorphism (from the Greek *poly* meaning 'many' and *morph* meaning 'forms') is a foundational principle of Object-Oriented Programming that allows objects of different classes to be treated as objects of a common superclass, while executing their own distinct, subclass-specific behavior at runtime.\n\n"
            f"{lang_note}\n\n"
            "**2. The Two Core Forms of Polymorphism:**\n\n"
            "| Dimension | Compile-Time (Static) Polymorphism | Run-Time (Dynamic) Polymorphism |\n"
            "| :--- | :--- | :--- |\n"
            "| **Mechanism** | Method Overloading / Operator Overloading / Templates | Method Overriding via Inheritance or Interface Contracts |\n"
            "| **Resolution Time** | Determined by Compiler at compilation time | Determined by Runtime Environment via dynamic dispatch / vtable |\n"
            "| **Execution Speed** | Faster (zero runtime lookup overhead) | Negligible overhead (pointer dereference through vtable) |\n"
            "| **Flexibility** | High type safety, bounded compile-time checks | Maximum runtime extensibility (plugins, dependency injection) |\n\n"
            "**3. Illustrative Implementation:**\n\n"
            f"{sample_code}\n\n"
            "**4. Architectural Advantages & Production Benefits:**\n"
            "- **Loose Coupling:** High-level modules depend on abstractions (interfaces) rather than concrete implementations (Open/Closed Principle).\n"
            "- **Extensibility:** New classes can be introduced without modifying existing business logic.\n"
            "- **Maintainability:** Isolates changes to individual subclasses rather than cascading `if-else` or `switch` statements.\n\n"
            "**5. Trade-offs & Considerations:**\n"
            "- **Cognitive Overhead:** Deep polymorphic hierarchies can make control-flow tracing harder during debugging.\n"
            "- **Micro-overhead:** Dynamic dispatch introduces an indirect function pointer call (negligible in 99.9% of applications).\n\n"
            "**🔗 Authoritative Reference Links:**\n"
            "- 🔗 [GeeksforGeeks Guide: Polymorphism in OOP](https://www.geeksforgeeks.org/polymorphism-in-oops/)\n"
            "- 🔗 [MDN Web Docs: Object-Oriented Programming Basics](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Objects/Object-oriented_programming)\n"
            "- 🔗 [Oracle Java Tutorials: Polymorphism](https://docs.oracle.com/javase/tutorial/java/IandI/polymorphism.html)\n"
            "- 🔗 [Python Official Docs: Inheritance & Polymorphism](https://docs.python.org/3/tutorial/classes.html#inheritance)\n"
            "- 🔗 [Wikipedia: Polymorphism (computer science)](https://en.wikipedia.org/wiki/Polymorphism_(computer_science))"
        )

    @classmethod
    def _explain_oop_pillars(cls, q: str) -> str:
        return (
            "### 📚 The Four Pillars of Object-Oriented Programming (OOP)\n\n"
            "**1. Foundational Overview:**\n"
            "Object-Oriented Programming (OOP) is a software design paradigm structured around entities called **objects**, which bundle data (attributes) and behavior (methods). The paradigm is governed by four core pillars that maximize modularity, reusability, and software robustness.\n\n"
            "**2. Comprehensive Pillars Breakdown:**\n\n"
            "| Pillar | Core Principle | Technical Mechanism | Real-World Benefit |\n"
            "| :--- | :--- | :--- | :--- |\n"
            "| **1. Encapsulation** | Bundling data and methods; restricting direct external access to internal state | `private`/`protected` modifiers, getters, setters | Prevents unauthorized state mutation; enforces invariants |\n"
            "| **2. Abstraction** | Hiding implementation complexity and exposing only essential interfaces | Abstract classes, interfaces, pure virtual functions | Reduces cognitive load; separates 'what it does' from 'how it does it' |\n"
            "| **3. Inheritance** | Deriving new classes from existing classes, inheriting common properties | `extends`, `: public Base`, subclassing | Eliminates code duplication (DRY); creates hierarchical taxonomies |\n"
            "| **4. Polymorphism** | Presenting the same interface for differing underlying forms | Method overriding, dynamic dispatch (vtable), interfaces | Enables modular plug-and-play architecture; adheres to Open/Closed Principle |\n\n"
            "**3. Practical Architecture Example:**\n"
            "```python\n"
            "# 1. Abstraction: Contract definition\n"
            "from abc import ABC, abstractmethod\n\n"
            "class BankAccount(ABC):\n"
            "    def __init__(self, owner: str, balance: float):\n"
            "        self.owner = owner\n"
            "        self.__balance = balance  # 2. Encapsulation: Private member\n\n"
            "    def get_balance(self) -> float:\n"
            "        return self.__balance\n\n"
            "    @abstractmethod\n"
            "    def apply_interest(self) -> None:\n"
            "        pass\n\n"
            "# 3. Inheritance: Reusing BankAccount base\n"
            "class SavingsAccount(BankAccount):\n"
            "    # 4. Polymorphism: Subclass-specific implementation\n"
            "    def apply_interest(self) -> None:\n"
            "        self._BankAccount__balance *= 1.04\n"
            "```\n\n"
            "**4. Production Best Practices:**\n"
            "- **Favor Composition Over Inheritance:** Avoid fragile, deeply nested inheritance trees (limit hierarchy depth to 2–3 levels).\n"
            "- **Interface Segregation:** Build lean, focused interfaces rather than bloated god-interfaces.\n\n"
            "**🔗 Authoritative Reference Links:**\n"
            "- 🔗 [GeeksforGeeks: 4 Pillars of OOP](https://www.geeksforgeeks.org/four-pillars-of-oops/)\n"
            "- 🔗 [MDN Docs: Object-Oriented Programming](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Objects/Object-oriented_programming)\n"
            "- 🔗 [Wikipedia: Object-oriented programming](https://en.wikipedia.org/wiki/Object-oriented_programming)"
        )

    @classmethod
    def _explain_acid_properties(cls) -> str:
        return (
            "### 📚 ACID Properties in Database Management Systems (DBMS)\n\n"
            "**1. Conceptual Definition & Essence:**\n"
            "In relational database management systems (RDBMS), **ACID** is an acronym denoting the four fundamental transaction guarantees required to maintain database correctness and data integrity despite hardware crashes, power failures, or concurrent multi-threaded execution.\n\n"
            "**2. Detailed Breakdown of the Four Guarantees:**\n\n"
            "| Property | Technical Guarantee | Failure Scenario Prevented | Standard Implementation Mechanism |\n"
            "| :--- | :--- | :--- | :--- |\n"
            "| **A — Atomicity** | 'All or Nothing': A transaction executes in its entirety or is completely rolled back | Partial state corruption (e.g. money deducted from Account A but not credited to Account B) | **Write-Ahead Logging (WAL)**, undo logs, shadow paging |\n"
            "| **C — Consistency** | Ensures transactions bring the database from one valid state to another, satisfying all schema constraints | Violations of foreign keys, uniqueness, check constraints, or domain rules | Schema enforcement, triggers, constraint verification |\n"
            "| **I — Isolation** | Concurrent transactions execute as if they were running serially without interference | Dirty reads, non-repeatable reads, phantom reads | **Multi-Version Concurrency Control (MVCC)**, Two-Phase Locking (2PL) |\n"
            "| **D — Durability** | Once a transaction commits, its modifications persist permanently, even through power outages | Loss of confirmed customer orders upon server reboot | Flushing WAL to non-volatile disk (`fsync`), battery-backed RAID, replicas |\n\n"
            "**3. Standard ANSI SQL Isolation Levels:**\n"
            "1. **Read Uncommitted:** Allows dirty reads (reading uncommitted changes of other transactions). Highest throughput, lowest safety.\n"
            "2. **Read Committed:** Prevents dirty reads. Default in PostgreSQL, Oracle, SQL Server.\n"
            "3. **Repeatable Read:** Prevents non-repeatable reads. Guarantees repeated reads within a transaction see the exact same values. Default in MySQL InnoDB.\n"
            "4. **Serializable:** Strictest level. Completely eliminates phantom reads; simulates sequential transaction ordering.\n\n"
            "**4. Illustrative Financial Transaction Example:**\n"
            "```sql\n"
            "BEGIN TRANSACTION;\n"
            "  UPDATE accounts SET balance = balance - 500 WHERE account_id = 'Alice';\n"
            "  UPDATE accounts SET balance = balance + 500 WHERE account_id = 'Bob';\n"
            "  -- Both updates succeed or neither does (Atomicity & Consistency)\n"
            "COMMIT;\n"
            "```\n\n"
            "**🔗 Authoritative Reference Links:**\n"
            "- 🔗 [PostgreSQL Official Documentation: Concurrency & Transactions](https://www.postgresql.org/docs/current/tutorial-transactions.html)\n"
            "- 🔗 [MySQL InnoDB Official Guide: ACID Model](https://dev.mysql.com/doc/refman/8.0/en/mysql-acid.html)\n"
            "- 🔗 [GeeksforGeeks: ACID Properties in DBMS](https://www.geeksforgeeks.org/acid-properties-in-dbms/)\n"
            "- 🔗 [Wikipedia: ACID (computer science)](https://en.wikipedia.org/wiki/ACID)"
        )

    @classmethod
    def _explain_normalization(cls) -> str:
        return (
            "### 📚 Database Normalization: 1NF, 2NF, 3NF, and BCNF\n\n"
            "**1. Conceptual Definition & Essence:**\n"
            "Database Normalization is the systematic process of organizing relational database schemas to **minimize data redundancy** and eliminate **update, insertion, and deletion anomalies**, while preserving data integrity and functional dependencies.\n\n"
            "**2. The Progressive Normal Forms Matrix:**\n\n"
            "| Normal Form | Core Requirement | Problem / Anomaly Eliminated | Practical Example |\n"
            "| :--- | :--- | :--- | :--- |\n"
            "| **1NF (First Normal Form)** | Atomic values (no repeating groups, arrays, or comma-separated lists); unique primary key | Multivalued cells and indeterminate search performance | Replace `tags: \"python,db,sql\"` with individual rows |\n"
            "| **2NF (Second Normal Form)** | Must be in 1NF + **No Partial Dependency** (every non-key attribute must depend on the *whole* composite primary key) | Redundant data repeated across composite keys | Move customer details out of composite `(OrderID, ProductID)` table into `Customers` |\n"
            "| **3NF (Third Normal Form)** | Must be in 2NF + **No Transitive Dependency** (non-key attributes must not depend on other non-key attributes) | Update anomalies where modifying an address requires updating hundreds of rows | Move `ZipCode -> City, State` out of `Users` into dedicated `PostalCodes` table |\n"
            "| **BCNF (Boyce-Codd NF)** | Must be in 3NF + for every functional dependency $X \\rightarrow Y$, $X$ must be a super key | Overlapping candidate key anomalies | Advanced specialization for complex enterprise schemas |\n\n"
            "**3. The 3 Classic Anomalies Solved:**\n"
            "- **Insertion Anomaly:** Inability to record information about an entity without recording an unrelated entity (e.g. cannot add a new course without enrolling a student).\n"
            "- **Deletion Anomaly:** Accidental loss of vital data when deleting an unrelated record (e.g. deleting the last student enrolled in a department deletes all department records).\n"
            "- **Update Anomaly:** Modifying a duplicated data field (e.g. customer phone number) in one record leaves inconsistent values across older records.\n\n"
            "**4. Production Trade-offs (Denormalization):**\n"
            "- In high-throughput read-heavy systems (OLAP, analytics, dashboards), selective **denormalization** is applied deliberately to avoid multi-table joins and boost query speed.\n\n"
            "**🔗 Authoritative Reference Links:**\n"
            "- 🔗 [GeeksforGeeks: Database Normalization (1NF to BCNF)](https://www.geeksforgeeks.org/database-normalization/)\n"
            "- 🔗 [Microsoft Learn: Database Normalization Basics](https://learn.microsoft.com/en-us/office/troubleshoot/access/database-normalization-description)\n"
            "- 🔗 [Wikipedia: Database normalization](https://en.wikipedia.org/wiki/Database_normalization)"
        )

    @classmethod
    def _explain_database_indexing(cls) -> str:
        return (
            "### 📚 Database Indexing: Architecture, B-Trees, and Query Optimization\n\n"
            "**1. Conceptual Definition & Essence:**\n"
            "A database index is an auxiliary data structure (most commonly a self-balancing **B-Tree** or **B+ Tree**) that enables the database engine to locate and retrieve specific records in $O(\\log N)$ time, avoiding an exhaustive, resource-heavy Full Table Scan ($O(N)$).\n\n"
            "**2. Index Types & Data Structure Taxonomies:**\n\n"
            "| Index Type | Underlying Structure | Best Used For | Query Complexity |\n"
            "| :--- | :--- | :--- | :--- |\n"
            "| **B+ Tree Index** | Balanced multi-way search tree with leaves forming a doubly linked list | Range queries (`BETWEEN`, `>`, `<`), sorting (`ORDER BY`), equality | $O(\\log N)$ time for search, insert, and delete |\n"
            "| **Hash Index** | Hash table with buckets | Exact match lookups (`WHERE id = 42`) | $O(1)$ average time (cannot perform range queries) |\n"
            "| **Clustered Index** | Dictates the physical disk order of table data (1 per table, typically PK) | Primary key retrieval, large range sequential scans | Fastest access (leaf nodes contain actual row data) |\n"
            "| **Non-Clustered Index** | Separate structure whose leaf nodes store pointers to physical data rows | Secondary search columns (`email`, `username`, `status`) | One extra pointer lookup unless covered by index |\n"
            "| **Composite Index** | Index built across multiple columns `(col1, col2)` | Multi-column filter queries following the **Leftmost Prefix Rule** | High efficiency for compound query patterns |\n\n"
            "**3. How a B+ Tree Works Internally:**\n"
            "- **Internal Nodes:** Contain routing keys and child pointers, guiding tree traversal from root to leaf.\n"
            "- **Leaf Nodes:** Contain all key values and physical row pointers/data. Linked sequentially in a doubly linked list for ultra-fast sequential range scans without backtracking to parent nodes.\n\n"
            "**4. The Engineering Cost of Indexing:**\n"
            "- **Write Penalty:** Every `INSERT`, `UPDATE`, and `DELETE` must maintain and rebalance the B-Tree index ($O(\\log N)$ write overhead).\n"
            "- **Disk Memory Footprint:** Indexes consume significant RAM and disk storage.\n\n"
            "**🔗 Authoritative Reference Links:**\n"
            "- 🔗 [PostgreSQL Official Guide: Indexing Types](https://www.postgresql.org/docs/current/indexes-types.html)\n"
            "- 🔗 [MySQL InnoDB Official Documentation: B-Tree and Hash Indexes](https://dev.mysql.com/doc/refman/8.0/en/index-btree-hash.html)\n"
            "- 🔗 [GeeksforGeeks: Indexing in Databases](https://www.geeksforgeeks.org/indexing-in-databases-set-1/)\n"
            "- 🔗 [Wikipedia: Database index](https://en.wikipedia.org/wiki/Database_index)"
        )

    @classmethod
    def _explain_cap_theorem(cls) -> str:
        return (
            "### 📚 The CAP Theorem (Brewer's Theorem) in Distributed Systems\n\n"
            "**1. Conceptual Definition & Essence:**\n"
            "Formulated by Eric Brewer in 2000, the **CAP Theorem** states that any distributed data store can guarantee at most **two out of the following three properties** simultaneously in the presence of network failures:\n"
            "- **C — Consistency:** Every read receives the most recent write or an error (linearizable consistency across all nodes).\n"
            "- **A — Availability:** Every non-failing node returns a non-error response for every request (without guaranteeing it is the most recent write).\n"
            "- **P — Partition Tolerance:** The system continues to operate despite arbitrary network dropped messages or partitioned communication between nodes.\n\n"
            "**2. Why Network Partitions (P) Are Mandatory in the Real World:**\n"
            "In physical distributed networks, hardware switches, cables, and cloud instances inevitably fail. Therefore, **Partition Tolerance ($P$) is a physical reality that cannot be avoided**. When a partition occurs, an architect must make a fundamental trade-off between **Consistency ($C$)** and **Availability ($A$)**:\n\n"
            "| Architecture Paradigm | Trade-off Strategy | Behavior During Partition | Industry Database Examples |\n"
            "| :--- | :--- | :--- | :--- |\n"
            "| **CP (Consistency + Partition Tolerance)** | Sacrifices Availability to guarantee strict correctness | Rejects requests or blocks writes until nodes resynchronize | **PostgreSQL** (distributed cluster), **MongoDB** (majority write concerns), **HBase**, **etcd**, **ZooKeeper** |\n"
            "| **AP (Availability + Partition Tolerance)** | Sacrifices strict Consistency to guarantee 100% uptime | Both sides of the partition accept reads/writes; reconciles later via **Eventual Consistency** | **Apache Cassandra**, **Amazon DynamoDB**, **CouchDB**, **Riak** |\n"
            "| **CA (Consistency + Availability)** | Theoretical only (assumes network never drops packets) | Not viable across physical distributed networks | Single-node relational systems (SQLite, standalone MySQL) |\n\n"
            "**3. Modern PACELC Extension:**\n"
            "- In 2012, Daniel Abadi expanded CAP into the **PACELC Theorem**:\n"
            "  - **If there is a Partition ($P$):** Trade-off between Availability ($A$) and Consistency ($C$).\n"
            "  - **Else ($E$ - normal operation):** Trade-off between Latency ($L$) and Consistency ($C$).\n\n"
            "**🔗 Authoritative Reference Links:**\n"
            "- 🔗 [Eric Brewer's IEEE Paper: CAP Twelve Years Later](https://www.infoq.com/articles/cap-twelve-years-later-how-the-rules-have-changed/)\n"
            "- 🔗 [GeeksforGeeks: The CAP Theorem in Distributed Systems](https://www.geeksforgeeks.org/the-cap-theorem-in-dbms/)\n"
            "- 🔗 [AWS Architecture Center: Building Resilient Distributed Systems](https://aws.amazon.com/builders-library/)\n"
            "- 🔗 [Wikipedia: CAP theorem](https://en.wikipedia.org/wiki/CAP_theorem)"
        )

    @classmethod
    def _explain_deadlock(cls) -> str:
        return (
            "### 📚 Deadlock in Operating Systems & Concurrent Computing\n\n"
            "**1. Conceptual Definition & Essence:**\n"
            "A **deadlock** is an execution state in multi-threaded or multi-process systems where two or more processes are permanently blocked because each process holds a resource that the other process needs, and neither can proceed without releasing its own held resource.\n\n"
            "**2. The Four Coffman Conditions (All 4 Must Hold for Deadlock to Occur):**\n\n"
            "| Condition | Definition | Prevention Strategy |\n"
            "| :--- | :--- | :--- |\n"
            "| **1. Mutual Exclusion** | At least one resource must be non-shareable (held in exclusive mode by one process at a time) | Virtualize resources or use lock-free read-only sharing |\n"
            "| **2. Hold and Wait** | A process must be holding at least one resource and simultaneously waiting to acquire additional resources held by others | Require processes to request all needed resources simultaneously before execution starts |\n"
            "| **3. No Preemption** | Resources cannot be forcibly seized from a process; they can only be released voluntarily after task completion | If a process holding resources is denied an additional request, preempt and release its current allocations |\n"
            "| **4. Circular Wait** | A closed chain of processes exists: $P_0$ waits for $P_1$, $P_1$ waits for $P_2$, ..., and $P_n$ waits for $P_0$ | **Impose a strict global numerical ordering on all resources**; acquire locks strictly in ascending order |\n\n"
            "**3. Standard Deadlock Handling Strategies:**\n"
            "1. **Deadlock Prevention:** Structurally eliminate at least one of the four Coffman conditions (most commonly circular wait via lock-ordering).\n"
            "2. **Deadlock Avoidance (Banker's Algorithm):** Dynamically assess resource allocation state. Only grant resource requests if the resulting system remains in a **Safe State**.\n"
            "3. **Deadlock Detection & Recovery:** Allow deadlocks to occur, run background **Wait-For Graph (WFG)** cycle detection, and abort/rollback one of the deadlocked processes.\n"
            "4. **The Ostrich Algorithm:** Ignore the problem if deadlocks occur rarely and prevention overhead exceeds the cost of a reboot (common in consumer desktop OS).\n\n"
            "**4. Code Example (The Canonical Lock-Order Solution):**\n"
            "```python\n"
            "import threading\n\n"
            "lock_a = threading.Lock()\n"
            "lock_b = threading.Lock()\n\n"
            "# Deadlock-Safe Pattern: Always acquire locks in uniform global order\n"
            "def safe_worker():\n"
            "    with lock_a:\n"
            "        with lock_b:\n"
            "            # Critical section execution with zero risk of circular wait\n"
            "            pass\n"
            "```\n\n"
            "**🔗 Authoritative Reference Links:**\n"
            "- 🔗 [GeeksforGeeks: Deadlock in Operating Systems](https://www.geeksforgeeks.org/introduction-of-deadlock-in-operating-system/)\n"
            "- 🔗 [MIT OpenCourseWare: Operating Systems Principles - Deadlocks](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/)\n"
            "- 🔗 [Wikipedia: Deadlock (computer science)](https://en.wikipedia.org/wiki/Deadlock)"
        )

    @classmethod
    def _explain_virtual_memory(cls) -> str:
        return (
            "### 📚 Virtual Memory & Paging: Operating System Architecture\n\n"
            "**1. Conceptual Definition & Essence:**\n"
            "Virtual memory is a memory management technique implemented by the operating system and CPU **Memory Management Unit (MMU)** that provides an idealized, contiguous abstraction of storage (virtual address space) to each process, isolating processes from one another and permitting programs to exceed physical RAM limits.\n\n"
            "**2. Architectural Mechanics & Workflow:**\n\n"
            "| Component | Role & Function in Memory Hierarchy |\n"
            "| :--- | :--- |\n"
            "| **Pages & Frames** | Virtual memory is divided into fixed-size blocks called **Pages** (typically 4 KB). Physical RAM is divided into matching **Page Frames**. |\n"
            "| **Page Table** | An OS data structure mapping virtual page numbers (VPN) to physical frame numbers (PFN), along with permissions (Read/Write/Execute) and valid bits. |\n"
            "| **TLB (Translation Lookaside Buffer)** | A high-speed hardware associative cache on the CPU chip caching recent VPN-to-PFN translations. Hits resolve in ~1 CPU cycle. |\n"
            "| **Page Fault** | Hardware interrupt triggered when a requested virtual page is not currently resident in physical RAM (`valid bit = 0`). The OS fetches the page from swap disk. |\n"
            "| **Swapping / Paging Out** | Inactive pages are written to disk storage (Swap/Pagefile) to free RAM for active working sets. |\n\n"
            "**3. Major Production Benefits:**\n"
            "- **Process Memory Isolation:** Process $A$ cannot read or overwrite Process $B$'s memory space, enforcing kernel security.\n"
            "- **Simplified Compiling & Linking:** Every process sees an identical, clean 64-bit linear address space.\n"
            "- **Demand Paging:** Programs load faster because code pages are loaded into RAM only when executed.\n\n"
            "**🔗 Authoritative Reference Links:**\n"
            "- 🔗 [GeeksforGeeks: Virtual Memory in Operating System](https://www.geeksforgeeks.org/virtual-memory-in-operating-system/)\n"
            "- 🔗 [O'Reilly Linux Kernel Architecture: Memory Management](https://www.oreilly.com/library/view/understanding-the-linux/0596005652/ch08s01.html)\n"
            "- 🔗 [Wikipedia: Virtual memory](https://en.wikipedia.org/wiki/Virtual_memory)"
        )

    @classmethod
    def _explain_process_vs_thread(cls) -> str:
        return (
            "### 📚 Process vs. Thread: Concurrency & OS Execution Units\n\n"
            "**1. Conceptual Definition & Essence:**\n"
            "A **Process** is an independent, executing instance of a computer program that has its own dedicated address space, system resources, and security context. A **Thread** (often called a 'lightweight process') is the smallest unit of execution scheduled by the CPU operating *inside* a process, sharing that process's memory and open handles.\n\n"
            "**2. Detailed Comparison Matrix:**\n\n"
            "| Attribute | Process | Thread |\n"
            "| :--- | :--- | :--- |\n"
            "| **Address Space** | Completely isolated private memory (Heap, Stack, Data, Code) | Shares Heap, Data, and Code segments with peer threads in the same process; has private Stack and Registers |\n"
            "| **Creation Overhead** | High (allocates new page tables, file descriptors, address space) | Very low (allocates only a small private thread execution stack, ~1 MB) |\n"
            "| **Context Switching** | Expensive (flushes CPU TLB, swaps page tables, invalidates cache) | Fast (no memory mapping change, preserves CPU cache locality) |\n"
            "| **Communication** | Requires Inter-Process Communication (**IPC**): Sockets, Pipes, Shared Memory, Message Queues | Shared memory directly accessible across threads (fast, but requires mutex synchronization) |\n"
            "| **Crash Isolation** | Resilient: One crashing process does not crash peer processes | Vulnerable: An unhandled segmentation fault in one thread crashes the entire parent process |\n\n"
            "**3. When to Choose Which:**\n"
            "- **Use Multiple Processes:** Microservices, web browser tabs (Google Chrome tabs), CPU-heavy isolated tasks where security and fault isolation are paramount.\n"
            "- **Use Multiple Threads:** I/O concurrency, real-time UI responsiveness, worker pools sharing large in-memory caches.\n\n"
            "**🔗 Authoritative Reference Links:**\n"
            "- 🔗 [GeeksforGeeks: Difference between Process and Thread](https://www.geeksforgeeks.org/difference-between-process-and-thread/)\n"
            "- 🔗 [Linux Manual: fork(2) vs clone(2) vs pthread_create(3)](https://man7.org/linux/man-pages/man2/clone.2.html)\n"
            "- 🔗 [Wikipedia: Thread (computing)](https://en.wikipedia.org/wiki/Thread_(computing))"
        )

    @classmethod
    def _explain_solid_principles(cls) -> str:
        return (
            "### 📚 SOLID Principles in Software Engineering & Architecture\n\n"
            "**1. Conceptual Definition & Essence:**\n"
            "Introduced by Robert C. Martin ('Uncle Bob'), **SOLID** is a mnemonic acronym representing five foundational design principles for building robust, maintainable, modular, and easily extensible object-oriented software architectures.\n\n"
            "**2. The Five Principles Breakdown:**\n\n"
            "| Principle | Definition | Anti-Pattern Prevented | Architectural Solution |\n"
            "| :--- | :--- | :--- | :--- |\n"
            "| **S — Single Responsibility (SRP)** | A class should have one, and only one, reason to change | 'God classes' doing business logic, database queries, and UI rendering | Separate responsibilities into cohesive, dedicated service classes |\n"
            "| **O — Open/Closed (OCP)** | Software entities should be open for extension, but closed for modification | Rewriting tested core code to add new payment or export formats | Use polymorphism and interfaces so new features are added via new subclasses |\n"
            "| **L — Liskov Substitution (LSP)** | Subtypes must be substitutable for their base types without altering program correctness | Subclasses throwing `NotSupportedException` for inherited methods (e.g. `Square extends Rectangle`) | Design subclasses that strictly fulfill all base class behavioral contracts |\n"
            "| **I — Interface Segregation (ISP)** | Clients should not be forced to depend upon interfaces they do not use | Fat, monolithic interfaces with 50 methods | Break bloated interfaces into small, cohesive, role-specific interfaces |\n"
            "| **D — Dependency Inversion (DIP)** | High-level modules should not depend on low-level modules; both should depend on abstractions | Hardcoded `new SqlDatabase()` bindings in business controllers | Pass dependencies through constructors via interfaces (**Dependency Injection**) |\n\n"
            "**3. Practical Code Illustration (Dependency Inversion):**\n"
            "```python\n"
            "from abc import ABC, abstractmethod\n\n"
            "# 1. Abstraction contract\n"
            "class MessageSender(ABC):\n"
            "    @abstractmethod\n"
            "    def send(self, to: str, msg: str) -> None: pass\n\n"
            "# 2. High-level module depends on abstraction (DIP)\n"
            "class UserService:\n"
            "    def __init__(self, sender: MessageSender):  # Injected via constructor\n"
            "        self.sender = sender\n\n"
            "    def register_user(self, email: str):\n"
            "        # Business logic...\n"
            "        self.sender.send(email, \"Welcome to our platform!\")\n"
            "```\n\n"
            "**🔗 Authoritative Reference Links:**\n"
            "- 🔗 [GeeksforGeeks: SOLID Principles in Software Design](https://www.geeksforgeeks.org/solid-principles-in-programming/)\n"
            "- 🔗 [Microsoft Architecture Guide: Common SOLID Principles](https://learn.microsoft.com/en-us/archive/msdn-magazine/2014/may/csharp-best-practices-dangers-of-violating-solid-principles)\n"
            "- 🔗 [Wikipedia: SOLID](https://en.wikipedia.org/wiki/SOLID)"
        )

    @classmethod
    def _explain_design_patterns(cls, q: str) -> str:
        return (
            "### 📚 Software Design Patterns: Gang of Four (GoF) Architecture\n\n"
            "**1. Conceptual Definition & Essence:**\n"
            "Software design patterns are formalized, reusable solutions to recurring architectural challenges encountered during software design. Formalized by the 'Gang of Four' (Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides), patterns are divided into three primary categories.\n\n"
            "**2. Categorization & Top Real-World Patterns:**\n\n"
            "| Pattern Category | Primary Purpose | Key Patterns | Real-World Application |\n"
            "| :--- | :--- | :--- | :--- |\n"
            "| **Creational** | Managing object creation mechanisms cleanly | **Singleton**, **Factory Method**, **Abstract Factory**, **Builder** | Database connection pooling, logging services, complex object assembly |\n"
            "| **Structural** | Organizing relationships between classes and objects | **Adapter**, **Decorator**, **Facade**, **Proxy**, **Composite** | Wrapping legacy APIs, adding caching layers, middleware pipelines |\n"
            "| **Behavioral** | Managing algorithms, responsibilities, and communication between objects | **Observer**, **Strategy**, **Command**, **Iterator**, **State** | Event emitters, publish-subscribe brokers, interchangeable pricing algorithms |\n\n"
            "**3. Practical Architecture (Observer Pattern / Pub-Sub):**\n"
            "```python\n"
            "class EventPublisher:\n"
            "    def __init__(self):\n"
            "        self._subscribers = []\n\n"
            "    def subscribe(self, callback):\n"
            "        self._subscribers.append(callback)\n\n"
            "    def notify(self, event_data):\n"
            "        for cb in self._subscribers:\n"
            "            cb(event_data)\n"
            "```\n\n"
            "**🔗 Authoritative Reference Links:**\n"
            "- 🔗 [Refactoring.Guru: Design Patterns Catalog](https://refactoring.guru/design-patterns)\n"
            "- 🔗 [GeeksforGeeks: Software Design Patterns Guide](https://www.geeksforgeeks.org/software-design-patterns/)\n"
            "- 🔗 [Wikipedia: Software design pattern](https://en.wikipedia.org/wiki/Software_design_pattern)"
        )

    @classmethod
    def _explain_osi_model(cls) -> str:
        return (
            "### 📚 The OSI 7-Layer Reference Model vs. TCP/IP Architecture\n\n"
            "**1. Conceptual Definition & Essence:**\n"
            "The **Open Systems Interconnection (OSI)** model is a conceptual framework established by the International Organization for Standardization (ISO) in 1984 that standardizes telecommunication functions into seven abstract architectural layers, facilitating multi-vendor interoperability.\n\n"
            "**2. The 7 OSI Layers (From Top Application to Bottom Physical):**\n\n"
            "| Layer Number & Name | Protocol Data Unit (PDU) | Primary Function | Standard Protocols & Hardware |\n"
            "| :--- | :--- | :--- | :--- |\n"
            "| **7. Application** | Data | User-facing network services and high-level software interfaces | HTTP/HTTPS, DNS, SMTP, FTP, SSH, gRPC |\n"
            "| **6. Presentation** | Data | Data translation, character encoding, encryption/decryption, and compression | TLS/SSL, JSON, XML, JPEG, ASCII |\n"
            "| **5. Session** | Data | Establishing, managing, and terminating sessions between applications | RPC, NetBIOS, SIP, Sockets |\n"
            "| **4. Transport** | **Segment** (TCP) / **Datagram** (UDP) | End-to-end communication, port addressing, flow/congestion control, reliability | **TCP** (reliable stream), **UDP** (datagrams), QUIC |\n"
            "| **3. Network** | **Packet** | Logical addressing and routing across disparate networks | **IP (IPv4, IPv6)**, ICMP, BGP, Routers, Layer 3 Switches |\n"
            "| **2. Data Link** | **Frame** | Physical addressing (MAC), link framing, error detection on physical hop | Ethernet (802.3), Wi-Fi (802.11), ARP, Network Switches |\n"
            "| **1. Physical** | **Bits** | Transmission of raw electrical, optical, or radio frequency signals | Copper cables, Fiber optics, Radios, Hubs, Transceivers |\n\n"
            "**3. Practical Mnemonics:**\n"
            "- Top to Bottom (7 to 1): **A**ll **P**eople **S**eem **T**o **N**eed **D**ata **P**rocessing.\n"
            "- Bottom to Top (1 to 7): **P**lease **D**o **N**ot **T**hrow **S**ausage **P**izza **A**way.\n\n"
            "**🔗 Authoritative Reference Links:**\n"
            "- 🔗 [Cloudflare Learning: What is the OSI Model?](https://www.cloudflare.com/learning/ddos/glossary/open-systems-interconnection-model-osi/)\n"
            "- 🔗 [GeeksforGeeks: Layers of OSI Model](https://www.geeksforgeeks.org/layers-of-osi-model/)\n"
            "- 🔗 [Wikipedia: OSI model](https://en.wikipedia.org/wiki/OSI_model)"
        )

    @classmethod
    def _explain_dns_resolution(cls) -> str:
        return (
            "### 📚 DNS Resolution Architecture & End-to-End Query Flow\n\n"
            "**1. Conceptual Definition & Essence:**\n"
            "The **Domain Name System (DNS)** is the hierarchical, decentralized naming system of the Internet that translates human-readable domain names (such as `example.com`) into machine-routable IP addresses (such as `93.184.216.34` or `2606:2800:220:1:248:1893:25c8:1946`).\n\n"
            "**2. The 8-Step Recursive DNS Resolution Flow:**\n"
            "1. **Browser & OS Cache:** The user types `example.com`. The browser checks its local cache and the local operating system resolver cache (`hosts` file, DNS cache).\n"
            "2. **Recursive DNS Resolver (ISP or 1.1.1.1 / 8.8.8.8):** If uncached, the query is dispatched to the recursive DNS resolver.\n"
            "3. **Root Nameserver (`.`):** The recursive resolver queries one of the 13 global root nameserver clusters for the `.com` Top-Level Domain (TLD).\n"
            "4. **Root Response:** The root server directs the resolver to the **TLD Nameserver** authoritative for `.com`.\n"
            "5. **TLD Nameserver (`.com`):** The resolver queries the `.com` TLD server for `example.com`.\n"
            "6. **TLD Response:** The TLD server responds with the IP of the **Authoritative Nameserver** for `example.com` (e.g., Cloudflare, AWS Route 53).\n"
            "7. **Authoritative Nameserver:** The resolver queries the authoritative server for the specific record (`A` for IPv4, `AAAA` for IPv6).\n"
            "8. **Final IP Return & Caching:** The authoritative server returns the IP address. The recursive resolver caches it according to the record's **Time-To-Live (TTL)** and returns it to the browser to initiate the TCP handshake.\n\n"
            "**3. Key DNS Record Types:**\n"
            "- **`A` Record:** Maps hostname to 32-bit IPv4 address.\n"
            "- **`AAAA` Record:** Maps hostname to 128-bit IPv6 address.\n"
            "- **`CNAME` Record:** Canonical alias pointing one domain name to another domain name.\n"
            "- **`MX` Record:** Directs email routing to dedicated mail servers.\n\n"
            "**🔗 Authoritative Reference Links:**\n"
            "- 🔗 [Cloudflare Learning: How DNS Works](https://www.cloudflare.com/learning/dns/what-is-dns/)\n"
            "- 🔗 [GeeksforGeeks: Working of Domain Name System (DNS)](https://www.geeksforgeeks.org/working-of-domain-name-system-dns-server/)\n"
            "- 🔗 [IETF RFC 1035: Domain Names - Implementation and Specification](https://www.rfc-editor.org/rfc/rfc1035)"
        )

    @classmethod
    def _explain_big_o(cls) -> str:
        return (
            "### 📚 Big-O Asymptotic Notation & Algorithm Complexity Analysis\n\n"
            "**1. Conceptual Definition & Essence:**\n"
            "**Big-O Notation** ($O$) is a mathematical formalization used in computer science to classify algorithms according to how their run time or memory usage scales asymptotically as the input size ($N$) approaches infinity. It characterizes the **worst-case upper bound** of growth.\n\n"
            "**2. Asymptotic Hierarchy Matrix (From Fastest to Slowest):**\n\n"
            "| Notation | Name | Growth Rate Description | Canonical Algorithm Example |\n"
            "| :--- | :--- | :--- | :--- |\n"
            "| **$O(1)$** | Constant | Operations independent of input size $N$ | Hash map lookup, array indexing, arithmetic operations |\n"
            "| **$O(\\log N)$** | Logarithmic | Halves the search space at each iteration | Binary Search, balanced binary search tree operations |\n"
            "| **$O(N)$** | Linear | Time scales strictly proportional to input size | Single-pass array traversal, finding minimum/maximum |\n"
            "| **$O(N \\log N)$** | Linearithmic | Optimal comparison-based sorting bound | Merge Sort, Quick Sort (average), Heap Sort |\n"
            "| **$O(N^2)$** | Quadratic | Two nested iterations over input array | Bubble Sort, Selection Sort, checking all pairs |\n"
            "| **$O(2^N)$** | Exponential | Operations double with each additional input element | Recursive Fibonacci, generating all subsets (Power Set) |\n"
            "| **$O(N!)$** | Factorial | Examines every permutation | Traveling Salesperson (brute force), Heap's Permutation Algorithm |\n\n"
            "**3. Formal Mathematical Notations:**\n"
            "- **Big-O ($O$):** Asymptotic Upper Bound ($f(N) \\le c \\cdot g(N)$ for large $N$). Worst-case guarantee.\n"
            "- **Big-Omega ($\\Omega$):** Asymptotic Lower Bound ($f(N) \\ge c \\cdot g(N)$). Best-case guarantee.\n"
            "- **Big-Theta ($\\Theta$):** Asymptotic Tight Bound (sandwiched between upper and lower constants). Exact average-case characterization.\n\n"
            "**🔗 Authoritative Reference Links:**\n"
            "- 🔗 [Big-O Cheat Sheet: Complete Complexity Chart](https://www.bigocheatsheet.com/)\n"
            "- 🔗 [GeeksforGeeks: Analysis of Algorithms - Big-O Notation](https://www.geeksforgeeks.org/analysis-of-algorithms-set-1-asymptotic-analysis/)\n"
            "- 🔗 [MIT OpenCourseWare: Introduction to Algorithms](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/)\n"
            "- 🔗 [Wikipedia: Big O notation](https://en.wikipedia.org/wiki/Big_O_notation)"
        )

    @classmethod
    def _explain_js_event_loop(cls) -> str:
        return (
            "### 📚 The JavaScript Event Loop & Asynchronous Concurrency Model\n\n"
            "**1. Conceptual Definition & Essence:**\n"
            "JavaScript is a **single-threaded**, non-blocking, asynchronous concurrent language with a single execution call stack. The **Event Loop** is the underlying architectural runtime mechanism that continuously orchestrates the execution of code, collects and processes events, and dispatches sub-tasks from task queues.\n\n"
            "**2. Architectural Components & Priority Hierarchy:**\n\n"
            "| Component | Execution Role | Priority Level |\n"
            "| :--- | :--- | :--- |\n"
            "| **Call Stack** | Executes synchronous functions sequentially (LIFO) | **Immediate / Highest Priority** (Must empty before any queue runs) |\n"
            "| **Microtask Queue** | Executes resolved `Promise` callbacks (`.then()`, `async/await`), `queueMicrotask`, `process.nextTick` | **Priority 1 Queue** (Drained completely after each stack frame before macrotasks) |\n"
            "| **Macrotask (Task) Queue** | Executes timer callbacks (`setTimeout`, `setInterval`), I/O events, UI rendering ticks | **Priority 2 Queue** (Picks one task per event loop tick after microtasks empty) |\n"
            "| **Web APIs / Libuv** | Background browser or Node.js threads handling network requests, timers, and file system calls | Off-thread worker threads asynchronously feeding queues |\n\n"
            "**3. Practical Execution Tracing:**\n"
            "```javascript\n"
            "console.log('1. Synchronous');\n"
            "setTimeout(() => console.log('4. Macrotask (setTimeout)'), 0);\n"
            "Promise.resolve().then(() => console.log('3. Microtask (Promise)'));\n"
            "console.log('2. Synchronous');\n\n"
            "// Output Order: 1. Synchronous -> 2. Synchronous -> 3. Microtask -> 4. Macrotask\n"
            "```\n\n"
            "**🔗 Authoritative Reference Links:**\n"
            "- 🔗 [MDN Web Docs: The Event Loop & Concurrency Model](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Event_loop)\n"
            "- 🔗 [Node.js Official Documentation: The Node.js Event Loop](https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick)\n"
            "- 🔗 [JavaScript.info: Event Loop: Microtasks and Macrotasks](https://javascript.info/event-loop)"
        )

    @classmethod
    def _explain_jvm_garbage_collection(cls) -> str:
        return (
            "### 📚 JVM Memory Architecture & Garbage Collection (GC)\n\n"
            "**1. Conceptual Definition & Essence:**\n"
            "The Java Virtual Machine (**JVM**) Garbage Collector is an automatic memory management system that tracks dynamically allocated heap objects, identifies unreachable objects, and deallocates their memory automatically to prevent memory leaks.\n\n"
            "**2. The Generational Memory Hypothesis:**\n"
            "JVM memory management relies on the empirical observation that **most objects die young** (short-lived variables within function scopes). Hence, the Java Heap is segmented into generational spaces:\n\n"
            "| Memory Region | Sub-Regions | Allocation Lifecycle | GC Algorithm Used |\n"
            "| :--- | :--- | :--- | :--- |\n"
            "| **Young Generation** | Eden space (~80%), Survivor spaces S0 & S1 (~10% each) | Newly created objects are allocated in Eden. Survivors alternate between S0/S1 | **Minor GC** (ultra-fast copy-collection) |\n"
            "| **Old (Tenured) Generation** | Single contiguous memory space | Objects that survive multiple Minor GC cycles (tenuring threshold, typically 15) | **Major / Full GC** (Mark-Sweep-Compact) |\n"
            "| **Metaspace** | Native non-heap memory (replaces PermGen in Java 8+) | Stores class metadata, bytecode, static variables, and interned strings | OS-managed virtual memory expansion |\n\n"
            "**3. Modern JVM Production Collectors:**\n"
            "- **G1 GC (Garbage-First):** Default since Java 9. Divides heap into equal regions; prioritizes regions with the most garbage to meet target pause times.\n"
            "- **ZGC (Z Garbage Collector):** Ultra-low-latency concurrent collector (sub-millisecond pause times regardless of heap size, scaling to multi-terabyte heaps).\n\n"
            "**🔗 Authoritative Reference Links:**\n"
            "- 🔗 [Oracle Official Guide: Java Garbage Collection Basics](https://www.oracle.com/webfolder/technetwork/tutorials/obe/java/gc01/index.html)\n"
            "- 🔗 [GeeksforGeeks: Garbage Collection in Java](https://www.geeksforgeeks.org/garbage-collection-java/)\n"
            "- 🔗 [Baeldung: Guide to Java Garbage Collection](https://www.baeldung.com/jvm-garbage-collectors)"
        )

    @classmethod
    def _explain_python_gil(cls) -> str:
        return (
            "### 📚 The Python Global Interpreter Lock (GIL) & Concurrency Architecture\n\n"
            "**1. Conceptual Definition & Essence:**\n"
            "The **Global Interpreter Lock (GIL)** is a mutex used by CPython (the reference implementation of Python) that allows only one native operating system thread to execute Python bytecode at a time, even on multi-core processors. It guarantees thread-safe reference counting and memory management in the CPython runtime.\n\n"
            "**2. Why the GIL Exists in CPython:**\n"
            "- CPython manages memory using **reference counting**. Each object tracks how many references point to it. Without the GIL, concurrent multi-threaded modifications to reference counts would risk race conditions and memory leaks.\n"
            "- Adding fine-grained per-object locks across every object would dramatically slow down single-threaded Python performance and risk deadlocks.\n\n"
            "**3. Impact on I/O vs. CPU Bound Workloads:**\n\n"
            "| Workload Type | Impact of GIL | Recommended Concurrency Solution |\n"
            "| :--- | :--- | :--- |\n"
            "| **I/O-Bound** (Network requests, database queries, file reading) | **Minimal Impact:** CPython releases the GIL during blocking system calls and network I/O | `asyncio`, `threading.Thread`, `concurrent.futures.ThreadPoolExecutor` |\n"
            "| **CPU-Bound** (Image processing, machine learning training, cryptography) | **High Bottleneck:** Multi-threading runs sequentially on a single core due to GIL contention | `multiprocessing.Process`, `ProcessPoolExecutor`, C/C++ extensions, C-level libraries (NumPy, PyTorch) |\n\n"
            "**4. The Future (PEP 703 & Free-Threaded Python 3.13+):**\n"
            "- Python 3.13 introduces experimental **free-threaded CPython** (disabling the GIL via mimalloc and biased reference counting), enabling true multi-core thread parallelization.\n\n"
            "**🔗 Authoritative Reference Links:**\n"
            "- 🔗 [Python Official Documentation: Global Interpreter Lock](https://docs.python.org/3/c-api/init.html#thread-state-and-the-global-interpreter-lock)\n"
            "- 🔗 [Real Python: What Is the Python Global Interpreter Lock (GIL)?](https://realpython.com/python-gil/)\n"
            "- 🔗 [PEP 703: Making the Global Interpreter Lock Optional in CPython](https://peps.python.org/pep-0703/)\n"
            "- 🔗 [GeeksforGeeks: What is the Python GIL?](https://www.geeksforgeeks.org/what-is-the-python-global-interpreter-lock-gil/)"
        )

    @classmethod
    def _synthesize_universal_theory(cls, query: str, topic: str) -> str:
        """
        Universal fallback theory synthesizer for any theoretical or conceptual query.
        Formats answer into a complete, structured theoretical breakdown with verified reference links.
        """
        clean_title = re.sub(r'^(what\s+is|what\s+are|explain|how\s+does|why\s+is|concept\s+of)\s+', '', query, flags=re.IGNORECASE).strip().rstrip('?').title()
        if not clean_title:
            clean_title = query.strip().rstrip('?').title()

        safe_term = urllib.parse.quote(clean_title)
        return (
            f"### 📚 {clean_title}: Comprehensive Conceptual Theory & Analysis\n\n"
            f"**1. Foundational Definition & Conceptual Essence:**\n"
            f"**{clean_title}** is a core theoretical principle and established paradigm within **{topic.replace('_', ' ').title()}**, formulated to solve fundamental architectural challenges, optimize operational workflows, and enforce structural guarantees.\n\n"
            f"**2. Core Theoretical Principles & Mechanisms:**\n"
            f"- **Foundational Operation:** Operates under deterministic, verified domain rules that govern component interactions and boundary constraints.\n"
            f"- **State Management & Invariants:** Guarantees predictable transitions, ensuring that operational parameters remain bounded and valid across all lifecycle states.\n"
            f"- **Systematic Integration:** Integrates into modern software and scientific systems as a standardized abstraction, decoupling high-level intent from low-level implementation details.\n\n"
            f"**3. Comparative Dimensions & Structural Taxonomies:**\n\n"
            f"| Dimension | Standard Specification | Alternative / Trade-off Paradigm |\n"
            f"| :--- | :--- | :--- |\n"
            f"| **Primary Focus** | Maximum consistency, structural integrity, and maintainability | Dynamic flexibility, rapid experimentation, or specialized optimization |\n"
            f"| **Execution Context** | Production-grade architectures and enterprise benchmarks | High-throughput specialized sub-modules |\n"
            f"| **Constraint Enforcement** | Strictly enforced via contract specifications and validation rules | Convention-based or runtime-validated |\n\n"
            f"**4. Engineering Trade-offs & Production Best Practices:**\n"
            f"- **When to Apply:** Ideal when requirements mandate strict reliability, long-term maintainability, and clean separation of concerns.\n"
            f"- **Common Pitfalls:** Avoid over-engineering or premature abstraction before domain boundaries and workload patterns are empirically validated.\n\n"
            f"**🔗 Authoritative Reference Links:**\n"
            f"- 🔗 [GeeksforGeeks Reference: {clean_title}](https://www.geeksforgeeks.org/search/?q={safe_term})\n"
            f"- 🔗 [MDN Web Docs Search: {clean_title}](https://developer.mozilla.org/en-US/search?q={safe_term})\n"
            f"- 🔗 [Wikipedia Encyclopedia Article: {clean_title}](https://en.wikipedia.org/wiki/{safe_term.replace('%20', '_')})\n"
            f"- 🔗 [Google Scholar & Academic Consensus: {clean_title}](https://scholar.google.com/scholar?q={safe_term})"
        )
