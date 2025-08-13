import psycopg2

# Database connection details
DB_HOST = "localhost"         # Docker maps 5432 to host
DB_PORT = 5432
DB_NAME = "postgres-1"          # or your custom DB
DB_USER = "tamilnilavan"
DB_PASS = "Msme232005"

try:
    # Connect to PostgreSQL
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    cur = conn.cursor()

    # Test query
    cur.execute("SELECT version();")
    version = cur.fetchone()
    print("✅ Connected successfully!")
    print("PostgreSQL version:", version[0])

    # Clean up
    cur.close()
    conn.close()

except Exception as e:
    print("❌ Connection failed!")
    print("Error:", e)
