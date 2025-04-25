import csv
import re
import requests
from bs4 import BeautifulSoup

def extract_emails_from_url(url):
    try:
        if not url.startswith("http"):
            url = "http://" + url
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text()
            emails = set(re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text))
            return emails
    except Exception as e:
        print(f"[!] Error fetching {url}: {e}")
    return set()

def scrape_emails_from_csv(input_file, output_file):
    total_found = 0
    all_emails = set()
    updated_rows = []

    with open(input_file, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames + ['emails'] if 'emails' not in reader.fieldnames else reader.fieldnames

        for row in reader:
            website = row.get('website', '').strip()
            if website:
                print(f"[+] Scraping: {website}")
                emails = extract_emails_from_url(website)
                row['emails'] = ', '.join(emails)
                print(f"    ↳ Found {len(emails)} email(s)")
                all_emails.update(emails)
                total_found += len(emails)
            updated_rows.append(row)

    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)

    print(f"\n✅ Total emails found: {total_found}")
    if all_emails:
        print("\n📬 All Emails Found:")
        for email in sorted(all_emails):
            print(f" - {email}")
    else:
        print("⚠️ No emails found.")

if __name__ == '__main__':
    input_csv = 'consultancy.csv'                # Your original file
    output_csv = 'consultancy_with_emails.csv'  # New output file
    scrape_emails_from_csv(input_csv, output_csv)
