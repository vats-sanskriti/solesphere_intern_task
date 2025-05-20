# solesphere_intern_task
# 🛡️ System Security Utility (Cross-Platform)

A lightweight Python-based system utility that runs in the background on **Windows**, **Linux**, and **macOS**, checking for basic system security settings and reporting any changes to a remote API.

---

## ✅ Features

- Cross-platform support: **Windows, Linux, macOS**
- Checks and monitors:
  - 🔐 Disk encryption status
  - ⚙️ OS update status (current vs. latest)
  - 🛡️ Antivirus presence and status
  - 💤 Inactivity sleep timeout (should be ≤10 minutes)
- Background daemon:
  - Runs every 30 minutes (configurable)
  - Sends updates **only when a change is detected**
- Sends reports to a **remote API endpoint**
- Consumes minimal system resources (headless)

---

## 🧩 Requirements

- Python 3.7+
- pip packages: `requests`

Install dependencies:
```bash
pip install -r requirements.txt




Clone the repo:
git clone https://github.com/yourname/system-security-utility.git
cd system-security-utility


Edit API endpoint in system_utility.py:
API_ENDPOINT = "https://your-api-url.com/api/report"


Run the script:
python system_utility.py


# 🛡️ System Security Utility – Backend Server (API + Storage)

This is the **backend component** for the System Security Utility tool. It provides APIs for receiving, storing, and retrieving system security status reports sent by the client-side system utility script.

---

## ✅ Features

- Accepts system check data from the utility (via secure HTTP)
- Stores:
  - `machine_id`
  - `timestamp`
  - `OS type`
  - System check results (disk encryption, antivirus, sleep settings, update status)
- Provides APIs for:
  - Listing all machines and their **latest** security status
  - Filtering machines by **OS** or systems with **issues**
  - Exporting all report data as a **CSV file**

---

## 🧩 Tech Stack

- ⚙️ FastAPI – Python web framework
- 📦 MongoDB – For storing reports
- 🔗 Motor – Async MongoDB driver
- 📊 Pandas – For CSV export
- 🔐 dotenv – For secure config handling

---

## 🚀 Getting Started

### 1️⃣ Clone the repository

```bash
git clone https://github.com/yourusername/system-utility-backend.git
cd system-utility-backend

Install dependencies
pip install -r requirements.txt

3️ Setup MongoDB
Ensure MongoDB is installed and running locally, or use a cloud MongoDB URI.

Create a .env file in the project root:
MONGO_URI=mongodb://localhost:27017

Running the Server
uvicorn main:app --reload
Server runs at: http://localhost:8000
