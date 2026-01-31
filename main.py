from fastapi import FastAPI, HTTPException, Depends
from datetime import datetime, timezone
from sqlalchemy.orm import Session
import models, database

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

# --- DATABASE DEPENDENCY ---
def get_db():
    db = database.SessionLocal()
    try:
        yield db # Hand over the session to the function that needs it
    finally:
        db.close() # Clean up / close the session after the function is done

time_zones = {
    "GMT-12:00": "AoE (Anywhere on Earth)",
    "GMT-11:00": "SST (Samoa Standard Time)",
    "GMT-10:00": "HST (Hawaii Standard Time)",
    "GMT-9:30": "MART (Marquesas Islands Time)",
    "GMT-9:00": "AKST (Alaska Standard Time)",
    "GMT-8:00": "PST (Pacific Standard Time)",
    "GMT-7:00": "MST (Mountain Standard Time)",
    "GMT-6:00": "CST (Central Standard Time)",
    "GMT-5:00": "EST (Eastern Standard Time)",
    "GMT-4:00": "AST (Atlantic Standard Time)",
    "GMT-3:30": "NST (Newfoundland Standard Time)",
    "GMT-3:00": "BRT (Brasilia Time)",
    "GMT-2:00": "GST (South Georgia Time)",
    "GMT-1:00": "CVT (Cape Verde Time)",
    "GMT+0:00": "UTC (Coordinated Universal Time)",
    "GMT+1:00": "CET (Central European Time)",
    "GMT+2:00": "EET (Eastern European Time)",
    "GMT+3:00": "MSK (Moscow Time)",
    "GMT+3:30": "IST (Iran Standard Time)",
    "GMT+4:00": "GST (Gulf Standard Time)",
    "GMT+4:30": "AFT (Afghanistan Time)",
    "GMT+5:00": "PKT (Pakistan Standard Time)",
    "GMT+5:30": "IST (Indian Standard Time)",
    "GMT+5:45": "NPT (Nepal Time)",
    "GMT+6:00": "BST (Bangladesh Standard Time)",
    "GMT+6:30": "CCT (Cocos Islands Time)",
    "GMT+7:00": "ICT (Indochina Time)",
    "GMT+8:00": "CST (China Standard Time)",
    "GMT+8:45": "CWST (Central Western Standard Time)",
    "GMT+9:00": "JST (Japan Standard Time)",
    "GMT+9:30": "ACST (Australian Central Standard Time)",
    "GMT+10:00": "AEST (Australian Eastern Standard Time)",
    "GMT+10:30": "LHST (Lord Howe Standard Time)",
    "GMT+11:00": "SBT (Solomon Islands Time)",
    "GMT+12:00": "NZST (New Zealand Standard Time)",
    "GMT+12:45": "CHAST (Chatham Standard Time)",
    "GMT+13:00": "TOT (Tonga Time)",
    "GMT+14:00": "LINT (Line Islands Time)"
}

# --- HELPER FUNCTIONS ---
def get_gmt_time():
    """Gets current GMT time."""
    gmt_time = datetime.now(timezone.utc)
    return gmt_time.hour, gmt_time.minute

# --- THE API ENDPOINTS ---
@app.get("/")
def home():
    return {"message": "Welcome to the Timezone API. Go to /docs to test it."}

@app.get("/find-timezone")
def find_timezone(user_hour: int, user_minute: int, db: Session = Depends(get_db)):

    # 1. Validation
    if not (0 <= user_hour <= 23) or not (0 <= user_minute <= 59):
        raise HTTPException(status_code=400, detail="Time must be HH:MM in 24hr format")

    # 2. Get GMT
    gmth, gmtm = get_gmt_time()

    # 3. Logic
    th = user_hour - gmth
    tm = user_minute - gmtm
    
    if tm < 0:
        tm += 60
        th -= 1
    elif tm >= 60:
        tm -= 60
        th += 1

    if th > 14:
        th -= 24
    elif th < -12:
        th += 24

    # 4. Format the key
    sign = "+" if th >= 0 else "" 
    key = f"GMT{sign}{th}:{tm:02}" 

    # 5. Result
    found_zone = time_zones.get(key, "Unknown Time Zone")
    
    # --- DATABASE SAVING LOGIC ---
    # Create the Python Object (The row)
    new_log = models.Log(
        input_time=f"{user_hour}:{user_minute:02}",
        location=found_zone
    )
    
    # Add to the "staging area"
    db.add(new_log)
    
    # Commit (Save firmly to the file)
    db.commit()
    
    # Refresh (Update the object with the ID the DB assigned it)
    db.refresh(new_log)
    
    return {
        "id": new_log.id, # We can now return the DB ID!
        "input_time": new_log.input_time,
        "calculated_offset": key,
        "location": new_log.location
    }

@app.get("/logs")
def get_logs(db: Session = Depends(get_db)):
    # 1. Query the database
    logs = db.query(models.Log).all()
    
    # 2. Return the list of logs
    return logs