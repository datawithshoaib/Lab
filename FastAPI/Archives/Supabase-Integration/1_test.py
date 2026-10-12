import os
from supabase import create_client, Client
from dotenv import load_dotenv
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# create client to connect to supabase project
client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Assuming you have a table "students" in supabase project you are connecting to
response = client.table("students").select("*").execute()

# check if you are getting the data present in the students table
print(response.data)

