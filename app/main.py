from fastapi import FastAPI, Header
from audit_access import read_users, log_access

app = FastAPI()

@app.get("/usuarios")
def list_users(x_user: str = Header(None)):
    user = x_user or "anon"
    rows = read_users(requesting_user=user)
    return {"rows": rows}
