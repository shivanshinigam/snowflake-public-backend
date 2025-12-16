
# What We Tried & What We Learned — Simple Summary

1️⃣ Original Goal

We wanted to:

Build a PUBLIC API for our app users

The API should:

Run analytics on Snowflake data  
Use Semantic View / Snowpark logic  
NOT expose Snowflake credentials to users  

2️⃣ First Approach — Snowpark Containers (SPCS)

What we did:

Created database, tables, semantic view, and agent in Snowflake  
Built a FastAPI backend  
Dockerized it  
Pushed Docker image to Snowflake Image Repository  
Created a Snowpark Container Service  
Got an ingress URL like:  
eaza6r-wbauoba-qf14503.snowflakecomputing.app  

<img width="1440" height="900" alt="Screenshot 2025-12-16 at 8 15 55 PM" src="https://github.com/user-attachments/assets/84e0ab53-d16e-40af-a1dd-6662434c236a" />

What happened:

Opening the URL always redirected to Snowflake login  

Why this happened:

Snowpark Container ingress is NOT a public API gateway  
It is protected by Snowflake authentication  
Public users cannot access it without Snowflake login  
Snowflake does not support anonymous or public access  

Conclusion:

Snowpark Containers are for internal Snowflake apps, not public APIs  

3️⃣ Tried Fixing Snowflake Ingress (Why it didn’t work)

What we tried:

Tried disabling auth (auth NONE, ingress configs, etc.)  
Tried updating service spec  
Tried GitHub Actions redeploy  
Tried altering service image  

Result:

SQL errors  
Unsupported configs  
Still redirected to login  

Key learning:

Snowflake does not allow public unauthenticated ingress  
This is by design for enterprise security  

4️⃣ Decision Point

Option A (Rejected):

Give Snowflake credentials to users  
This is a major security risk  

Option B (Chosen):

Create a public backend outside Snowflake  
Backend securely talks to Snowflake  
Users talk only to backend  

5️⃣ Final Architecture Chosen

What we built:

FastAPI backend  
Hosted publicly on Render  

Backend behavior:

Uses Snowflake credentials internally  
Calls Snowflake tables and semantic view  
Exposes REST APIs  

Endpoints:

/health  
/analytics  
/ask  

Flow:

App → Public API → Snowflake  

6️⃣ Why Render Works but Snowflake Ingress Didn’t

Snowflake Containers:

Requires Snowflake login  
Internal only  
Not an API gateway  

Render:

Public HTTPS access  
Internet facing  
Designed for APIs  

7️⃣ Current Status

Snowflake:

Tables ready  
Semantic View ready  

Backend:

FastAPI working  
Public URL live  
Docs working  
Analytics endpoint implemented  

Final fix needed:

Correct Snowflake environment variables in Render


