import sys
import sqlite3
import tarfile
import zlib
import json

# Create SQLite database connection (or connect to an existing one)
conn = sqlite3.connect('pmc.db')
cur = conn.cursor()

# Ensure the table exists (you can skip this if you've already created the table)
cur.execute('''
CREATE TABLE IF NOT EXISTS records (
    id VARCHAR(32) PRIMARY KEY,
    pmid VARCHAR(32),
    content BLOB
);
''')

cur.execute('CREATE INDEX IF NOT EXISTS idx_pmid ON records (pmid)')

conn.commit()

batch_data = []

# Set batch size (adjust based on available memory and desired performance)
BATCH_SIZE = 1024

# Path to your .tar.gz file
tar_file_path = 'PMC000XXXXX_json_unicode.tar.gz'
if len(sys.argv) > 1:
    tar_file_path = sys.argv[1]

print("open",tar_file_path)
# Open the .tar.gz file
with tarfile.open(tar_file_path, 'r:gz') as tar:
    # Iterate through each member in the archive
    for member in tar.getmembers():
        # Ensure it's a regular file (skip directories, etc.)
        if member.isfile():
            # Get the filename (use it as the primary key)
            filename = member.name.split('/')[-1]  # Only take the filename part (without directory path)
            filename = filename.removesuffix(".xml")
#            print(filename)
#            exit(0)
            
            # Extract the file content in memory
            file_content = tar.extractfile(member).read() # Decoding as UTF-8, adjust if necessary

            pmid = ""
            try:
              content_text = file_content.decode('utf-8')
              content = json.loads(content_text)
              first = content
              doc = first['documents']
              fd = doc[0]
              p = fd['passages']
              p0 = p[0]
              inf = p0['infons']
              pmid = inf['article-id_pmid']

            except:
              pass

            compressed_content = zlib.compress(file_content)
            
            # Append the entry to batch data
            batch_data.append((filename, pmid, compressed_content))

            if len(batch_data) >= BATCH_SIZE:
                print(".",end="")
                cur.executemany('''
                    INSERT OR IGNORE INTO records (id, pmid, content)
                    VALUES (?, ?, ?)
                ''', batch_data)
                conn.commit()  # Commit the transaction
                batch_data.clear()  # Clear the batch data
            
if batch_data:
    cur.executemany('''
        INSERT OR IGNORE INTO records (id, pmid, content)
        VALUES (?, ?, ?)
    ''', batch_data)
    conn.commit()  
# Commit the final transaction

# Close the database connection
conn.close()

print("End")

