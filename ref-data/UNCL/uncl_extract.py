import requests
from bs4 import BeautifulSoup
import csv
import re
import os
import sys

def extract_and_save_tsv(url):
    """
    Fetches the HTML content from the given URL, extracts the code values,
    and saves them into a Tab-Separated Values (.tsv) file.

    The script targets the 'Code Values:' section commonly found on UNECE
    code list pages, where data is often presented as:
    CODE   Description text that spans multiple lines (sometimes).
    """
    
    filename = url.split('/')[-1].replace('.htm', '') + '_code_values.tsv'
    
    print(f"Fetching data from: {url}", file=sys.stderr)

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        html_content = response.content
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}", file=sys.stderr)
        return

    soup = BeautifulSoup(html_content, 'html.parser') # Keep this line to parse HTML

    # Title Extraction and Filename Construction
    
    # Fallback filename base
    clean_title = url.split('/')[-1].replace('.htm', '')
    
    # Search for the specific title pattern (text ending with [A-Z]) in key header elements
    title_pattern = re.compile(r'^(.*)\s+\[[A-Z]\]$', re.IGNORECASE)
    
    # Check H1, H2, and the <title> tag text for the pattern
    potential_titles = [soup.find('title').get_text(strip=True)] if soup.find('title') else []
    potential_titles.extend([tag.get_text(strip=True) for tag in soup.find_all(['h1', 'h2', 'h3'])])
    
    found_title = None
    for raw_text in potential_titles:
        match = title_pattern.search(raw_text)
        if match:
            found_title = match.group(1).strip()
            break
    
    if found_title:
        clean_title = re.sub(r'[^\w\s-]', '', found_title).strip().replace(' ', '_').replace('__', '_')
        clean_title = clean_title.strip('_')
        print(f"Processing: {clean_title}", file=sys.stderr)
    
    #
    # filename = clean_title + '.tsv'

    # Locate the "Code Values:" section and the following data block
    # The code values are preceded by the text "Code Values:"
    target_heading = soup.find(string=re.compile(r"Code Values:"))

    if not target_heading:
        print("Could not find the 'Code Values:' heading on the page.")
        return

    text_content = ""
    target_heading = target_heading.parent
    sibling = target_heading.next_sibling

    while sibling:
        # Check if the sibling is an HTML tag (element)
        if sibling.name:
            break
        elif isinstance(sibling, str) and sibling.strip():
            text_content = sibling
            break
        sibling = sibling.next_sibling

    extracted_data = []
    lines_to_parse = []

    if text_content:
        lines_to_parse = text_content.split('\n')
    else:
        print("Could not find the data block immediately following 'Code Values:'.", file=sys.stderr)
        return

    code = ""
    value = ""
    newItem = True
    description = ""
    
    code_pattern = re.compile(r'^\s*([A-Z0-9]{1,4})\s+(.*)$')
    
    for line in lines_to_parse:
        # Change indicators
        # a plus sign (+)    for an addition
        # an asterisk (*)    for an amendment to structure
        # a hash sign (#)    for changes to names
        # a vertical bar (|) for changes to text for descriptions and notes
        # a minus sign (-)   for marked for deletion (within either batch and interactive messages)
        # a X sign (X)       for marked for deletion (within both batch and interactive messages)
        if newItem:
            if line.startswith(('+','*','#','|','-','X')):
                line = line[1:]
            match = code_pattern.match(line)
            if match:
                code = match.group(1).strip()
                value = line.replace(code,'').strip()
                description = ""
                newItem = False
        else:
            if line == "" and len(code)>0 and len(value)>0:
                extracted_data.append([code, value, description])
                code = ""
                value = ""
                newItem = True
            else:
                if len(description) == 0:
                    description = line.strip()
                else:
                    description = description + " " + line.strip()

    if not extracted_data:
        print("No structured code values were extracted. The page structure might have changed.", file=sys.stderr)
        return
    print(f"Successfully extracted {len(extracted_data)} code values.", file=sys.stderr)

    header = ['Code Tag', 'Code Value', 'Description']

    # Write to stdout
    writer = csv.writer(sys.stdout, delimiter='\t')
    writer.writerow(header)
    writer.writerows(extracted_data)

    print("Data written to stdout.", file=sys.stderr)

if __name__ == "__main__":
    print(sys.argv[2], file=sys.stderr)
    # URL (UN/EDIFACT Code Lists)
    #uncl_url = 'https://service.unece.org/trade/untdid/d22a/tred/tred3055.htm'
    
    # Other examples:
    #uncl_url = 'https://service.unece.org/trade/untdid/d22a/tred/tred4499.htm'
    #uncl_url = 'https://service.unece.org/trade/untdid/d22a/tred/tred1229.htm'
    #uncl_url = 'https://service.unece.org/trade/untdid/d22a/tred/tred3139.htm'
    extract_and_save_tsv(sys.argv[2])