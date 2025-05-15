import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import getpass
import re

def parse_percentage(mark_text):
    match = re.search(r'(\d+(?:\.\d+)?)\s*%', mark_text)
    if match:
        return float(match.group(1))
    return None

def fetch_assignments(session_req, course_link):
    response = session_req.get(course_link)
    if response.status_code != 200:
        print("❌ Failed to fetch advanced report.")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    main_table = soup.find("table", attrs={
        "border": "1",
        "cellpadding": "3",
        "cellspacing": "0",
        "width": "100%"
    })

    if not main_table:
        print("⚠️ No assignment table found.")
        return

    all_rows = main_table.find_all("tr")
    assignments = []
    i = 1

    while i < len(all_rows):
        row = all_rows[i]
        name_cell = row.find("td", attrs={"rowspan": "2"})
        if not name_cell:
            i += 1
            continue

        assignment_name = name_cell.get_text(strip=True)
        assignment_data = {
            "name": assignment_name,
            "knowledge": "No Mark",
            "thinking": "No Mark",
            "communication": "No Mark",
            "application": "No Mark",
            "culminating": "No Mark",
            "overall": None
        }

        cells = row.find_all("td", attrs={"rowspan": None}, recursive=False)

        for cell in cells:
            bg = cell.get("bgcolor", "").lower().replace("#", "")
            mark_text = cell.get_text(strip=True)

            if bg == "ffffaa":
                assignment_data["knowledge"] = mark_text
            elif bg == "c0fea4":
                assignment_data["thinking"] = mark_text
            elif bg == "afafff":
                assignment_data["communication"] = mark_text
            elif bg == "ffd490":
                assignment_data["application"] = mark_text
            elif bg == "dedede":
                assignment_data["culminating"] = mark_text

        category_marks = []
        for cat in ["knowledge", "thinking", "communication", "application", "culminating"]:
            p = parse_percentage(assignment_data[cat])
            if p is not None:
                category_marks.append(p)

        if category_marks:
            avg_val = sum(category_marks) / len(category_marks)
            assignment_data["overall"] = round(avg_val, 1)

        assignments.append(assignment_data)
        i += 2

    for a in assignments:
        print(f"\n📌 {a['name']}")
        print(f"   - Knowledge: {a['knowledge']}")
        print(f"   - Thinking: {a['thinking']}")
        print(f"   - Communication: {a['communication']}")
        print(f"   - Application: {a['application']}")
        print(f"   - Culminating: {a['culminating']}")
        if a['overall'] is not None:
            print(f"   - Overall: {a['overall']}%")

def fetch_marks_console():
    base_url = "https://ta.yrdsb.ca/"
    login_url = base_url + "yrdsb/"

    username = input("Enter your YRDSB username: ")
    password = getpass.getpass("Enter your password (input hidden): ")

    session_req = requests.Session()
    login_payload = {"username": username, "password": password}
    response = session_req.post(login_url, data=login_payload)

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find('table', width="85%")
    
    if not table:
        print("\n❌ Failed to retrieve marks. Please check your credentials.")
        input("\nPress Enter to exit...")
        return

    rows = table.find_all('tr')[1:]
    courses = []

    print(f"\n✅ Course Marks for {username}:\n")
    for i, row in enumerate(rows):
        cols = row.find_all('td')
        course_name = cols[0].get_text(strip=True)
        mark_info = cols[2]

        current_mark = mark_info.find('a')
        current_text = current_mark.get_text(strip=True) if current_mark else "No current mark"
        current_link = None

        if current_mark and current_mark.get('href'):
            href = current_mark['href']
            if not href.startswith("live/students/"):
                href = "live/students/" + href
            current_link = urljoin(base_url, href)

        courses.append({
            "name": course_name,
            "mark": current_text,
            "link": current_link
        })

        print(f"{i + 1}. {course_name}: {current_text}")

    # Ask if user wants a detailed view
    view_detail = input("\nWould you like to view detailed assignments? (yes/no): ").strip().lower()
    if view_detail in ["yes", "y"]:
        try:
            choice = int(input("Enter the course number to view: "))
            if 1 <= choice <= len(courses):
                selected = courses[choice - 1]
                if selected["link"]:
                    print(f"\n🔍 Fetching detailed assignments for {selected['name']}...\n")
                    fetch_assignments(session_req, selected["link"])
                else:
                    print("⚠️ No detailed link found for this course.")
            else:
                print("❌ Invalid selection.")
        except ValueError:
            print("❌ Please enter a valid number.")

    input("\nPress Enter to exit...")

if __name__ == "__main__":
    fetch_marks_console()
