import sqlite3
import os

# Number of shards
NUM_SHARDS = 10

# Directory to store shard databases
SHARD_DIR = '.db'
os.makedirs(SHARD_DIR, exist_ok=True)

# Create shard databases
for i in range(NUM_SHARDS):
    conn = sqlite3.connect(os.path.join(SHARD_DIR, f'shard_{i}.db'))
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS data (
            id INTEGER PRIMARY KEY,
            key INTEGER,
            value TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS metadata (
            id TEXT PRIMARY KEY,
            value INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def insert_data(key, value):
    shard_id = get_shard(key)
    conn = sqlite3.connect(os.path.join(SHARD_DIR, f'shard_{shard_id}.db'))
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO data (key, value) VALUES (?, ?)
    ''', (key, value))
    conn.commit()
    conn.close()

def query_data(key):
    shard_id = get_shard(key)
    conn = sqlite3.connect(os.path.join(SHARD_DIR, f'shard_{shard_id}.db'))
    cursor = conn.cursor()
    cursor.execute('''
        SELECT value FROM data WHERE key = ?
    ''', (key,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def check_if_data_exists(key): 
    shard_id = get_shard(key) 
    conn = sqlite3.connect(os.path.join(SHARD_DIR, f'shard_{shard_id}.db')) 
    cursor = conn.cursor() 
    cursor.execute(''' SELECT 1 FROM data WHERE key = ? ''', (key,)) 
    result = cursor.fetchone() 
    conn.close() 
    return result is not None
    
def check_if_file_exists(file_path): 
    return os.path.exists(file_path)

def insert_metadata(id, value):
    shard_id = 0  # Use a consistent shard for metadata
    conn = sqlite3.connect(os.path.join(SHARD_DIR, f'shard_{shard_id}.db'))
    cursor = conn.cursor()
    cursor.execute('''
        REPLACE INTO metadata (id, value) VALUES (?, ?)
    ''', (id, value))
    conn.commit()
    conn.close()

def query_metadata(id):
    shard_id = 0  # Use a consistent shard for metadata
    conn = sqlite3.connect(os.path.join(SHARD_DIR, f'shard_{shard_id}.db'))
    cursor = conn.cursor()
    cursor.execute('''
        SELECT value FROM metadata WHERE id = ?
    ''', (id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


def get_shard(key):
    # Determine shard based on the key (e.g., modulus operation)
    return key % NUM_SHARDS







if __name__ == "__main__":
    # Example: Insert data
    NUM_ENTRIES = 250 #999_000_000_000  # 999 billion entries
    for i in range(NUM_ENTRIES):
        insert_data(i, f'value_{i}')

    print('Data insertion completed.')

    # Example: Query data
    key_to_query = 59 
    result = query_data(key_to_query)
    print(f'Result for key {key_to_query}: {result}')

    # Example: Check if data exists
    key_to_check = 59
    exists = check_if_data_exists(key_to_check)
    print(f'Data exists for key {key_to_check}: {exists}')
