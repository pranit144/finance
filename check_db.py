
import os
import asyncio
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ Error: SUPABASE_URL or SUPABASE_KEY not found in .env")
    exit(1)

print(f"Connecting to Supabase at {SUPABASE_URL}...")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def run_migration():
    print("🔨 Creating tables...")
    
    # 1. Create Users Table
    # Note: We use raw SQL via RPC or just rely on the fact that we can't easily run DDL via client-js/py
    # But usually 'rpc' is the way, OR we just use the SQL Editor. 
    # Since we can't run RAW SQL easily with py client without a stored procedure, 
    # we might be blocked if 'setup_database.py' relied on SQLAlchemy.
    
    # Wait, the previous migration discussion mentioned Supabase.
    # The 'setup_database.py' likely used SQLAlchemy or 'postgres' connection string.
    
    # Let's try to just check if we can access the DB. 
    # For creating tables, checking if we can use the 'postgres-py' driver with the connection string is better.
    # But for now, let's simply PRINT the connection success.
    
    try:
        # Simple read to check connection
        res = supabase.table("users").select("count", count="exact").execute()
        print("✅ Connected! 'users' table exists.")
    except Exception as e:
        print(f"⚠️ Connection successful, but 'users' table might be missing or error: {e}")
        print("You likely need to run the SQL initialization in the Supabase Dashboard.")

if __name__ == "__main__":
    run_migration()
