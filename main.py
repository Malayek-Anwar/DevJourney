from fastapi import FastAPI, HTTPException
from datetime import datetime, timezone

app = FastAPI()

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
def find_timezone(user_hour: int, user_minute: int):
    # 1. Validation (Replacing your 'Invalid time format' print)
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

    # Normalize logic
    if th > 14:
        th -= 24
    elif th < -12:
        th += 24

    # 4. Format the key
    sign = "+" if th >= 0 else "" 
    # Use :02 to ensure single digits get a leading zero (e.g., 5 -> 05)
    key = f"GMT{sign}{th}:{tm:02}" 

    # 5. Result
    found_zone = time_zones.get(key, "Unknown Time Zone")
    
    return {
        "input_time": f"{user_hour}:{user_minute:02}",
        "calculated_offset": key,
        "location": found_zone
    }