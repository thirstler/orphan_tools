ORPHAN TOOLS

This is a set of simple scripts for archiving and removing data via sproxyd.
Created for a Zimbra orphan hunt, it assumes that orphans have been identified
and we have a text file with the list. This set was tested on a orphan project
of almost 400 million keys so it scales fairly well.

1) Shard your keylist. If the complete list is in the millions of keys you'll
   need to separate the list into sections that can be operated on separately.
   This what the shard script is for.
   
   ./shard.py [key list]
   
   This script will (rapidly) split the keylist into 256 parts using the first
   two chars of the RING key. If your orphan list is so large that each shard
   would be tens of millions of keys you'll want to modify the script to split
   the list into 2048 parts (first 3 chard of the key) 
   
   Shards will need to be handled separately, this is to keep the resultant
   files (sqlite3 database) from getting too big.

2) Next step is to download the shards into sqlite databases. Each one will 
   need to be handled separately. Run archive.py with

   a. The input list of keys. List needs formatted with one key per line and no
      other data.
   b. Path to the database file to be created or used 
   c. The hostame or IP of the sproxyd host to be used to retrieve records
   
3) After you've archived a key-list (shard) you can delete it. The delete.py
   script takes two arguments.
   
   a. Database file containing the key list. Script will only delete files 
      which had a 200 HTTP status code on retrieval.
   b. The hostame or IP of the sproxyd host to be used to delete records
   
4) THINGS WENT BAD. Restore records with the restore.py script It takes two
   arguments.
   
   a. Database file containing the key list. Script will only delete files 
      which had a 200 HTTP status code on retrieval.
      
