
# Prism Console — YRDSB Mark Viewer

**Made With ❤️ By sariyan-0**

Prism Console is a command-line Python tool that allows students in the **York Region District School Board (YRDSB)** to securely log in and view their course marks, including optional detailed assignment breakdowns.

> 🔐 This project is intended for educational and non-commercial use only. It is not affiliated with or endorsed by the YRDSB.

---

## ✨ Features

- 📋 View current marks for all your courses.
- 🔍 Get breakdowns of each assignment by category:
  - Knowledge
  - Thinking
  - Communication
  - Application
  - Culminating
- 💻 Terminal-only — no browser needed.
- 🔑 Login securely using your student credentials (password is hidden).

---

## 🚀 Getting Started

### 📦 Prerequisites

- Python 3.7+
- Packages:
  - `requests`
  - `beautifulsoup4`

Install packages using your windows terminal:

```bash
pip install requests beautifulsoup4
````

---

## 🧠 How It Works

This script simulates a login to the [YRDSB TeachAssist portal](https://ta.yrdsb.ca/), fetches your course data, and (optionally) digs into each assignment using HTML parsing via `BeautifulSoup`.

---

## ▶️ Usage

1. Clone the repo or copy the script to your local machine.
2. Run it using Python:

```bash
python TA_Console.py
```

3. Enter your YRDSB **username** and **password** when prompted.
4. View your course marks instantly.
5. Optionally, choose a course to see detailed assignment breakdowns.

---

## 📌 Example Output

```
Enter your YRDSB username: johndoe123
Enter your password (input hidden):

✅ Course Marks for johndoe123:

1. ENG3U1: 84%
2. MCR3U1: 91%
3. SCH3U1: 77%

Would you like to view detailed assignments? (yes/no): yes
Enter the course number to view: 2

🔍 Fetching detailed assignments for MCR3U1...

📌 Quadratic Functions Assignment
   - Knowledge: 85%
   - Thinking: 90%
   - Communication: 80%
   - Application: 92%
   - Culminating: No Mark
   - Overall: 86.8%
```

---

## ⚠️ Disclaimer

* This is a **personal educational tool**.
* Do not misuse or share your YRDSB credentials.

---

## 🧊 Stay Frosty

If you enjoyed this project or want to contribute, feel free to open a pull request or drop a star ⭐ on the repo.

---

## 📁 License
non-commercial use only
