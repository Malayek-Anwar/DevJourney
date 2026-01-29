----
# Time Zone API 🌍

A high-performance REST API built with **FastAPI** that calculates time differences between local time and GMT, instantly returning the correct Time zone Code (e.g., EST, IST, PST).

## 🚀 Features

- **Instant Lookup:** Converts User Time + GMT Time into a standardized Time zone Code.

- **Error Handling:** Validates 24-hour format inputs automatically.

- **Lightweight:** Built on FastAPI for high speed and low latency.

## 🛠️ Tech Stack

- **Language:** Python 3.10+

- **Framework:** FastAPI

- **Server:** Uvicorn

---
## 📦 How to Run

1. **Clone the repository**

   ```bash
   git clone [https://github.com/Malayek-Anwar/DevJourney.git] (https://github.com/Malayek-Anwar/DevJourney.git)
   ```

2. **Install Dependencies**

    ```bash
    pip install fastapi uvicorn
    ```
    
3. **Run the Server**

    ```bash
    uvicorn main:app --reload
    ```

4. **Test the API**

    ```bash
    Open your browser to: http://127.0.0.1:8000/docs
    ```

  
---
## 📝 Example Usage

Request: GET /find-timezone?user_hour=14&user_minute=30

Response:

```JSON
{

  "input_time": "14:30",

  "calculated_offset": "GMT+5:30",

  "location": "IST (Indian Standard Time)"

}
```

  

---