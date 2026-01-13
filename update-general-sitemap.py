#!/usr/bin/env python3

import os
from datetime import datetime
import xml.etree.ElementTree as ET

# --- CONFIGURATION ---
SITE_URL = "https://societalnews.com/"
BASE_DIR = "/home/societal/public_html/" 
OUTPUT_FILE = os.path.join(BASE_DIR, "sitemap.xml")

def generate_general_sitemap():
    try:
        root = ET.Element("urlset")
        root.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")
        root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        root.set("xsi:schemaLocation", "http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd")

        files_added = 0

        for root_path, dirs, files in os.walk(BASE_DIR):
            for filename in files:
                if filename.endswith(".html"):
                    filepath = os.path.join(root_path, filename)
                    mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
                    
                    # Clean the URL
                    relative_path = os.path.relpath(filepath, BASE_DIR).replace("\\", "/")
                    if relative_path == "index.html":
                        clean_url_path = ""
                        priority_val = "1.00"
                    elif relative_path.endswith("index.html"):
                        clean_url_path = relative_path[:-10]
                        priority_val = "0.80"
                    else:
                        clean_url_path = relative_path
                        priority_val = "0.80" if "news/" in relative_path else "0.64"

                    # Create Entry
                    url_entry = ET.SubElement(root, "url")
                    ET.SubElement(url_entry, "loc").text = f"{SITE_URL}{clean_url_path}"
                    
                    # MATCHING YOUR FORMAT: Full ISO timestamp
                    ET.SubElement(url_entry, "lastmod").text = mtime.strftime('%Y-%m-%dT%H:%M:%S+00:00')
                    
                    # ADDING PRIORITY:
                    ET.SubElement(url_entry, "priority").text = priority_val

                    files_added += 1

        tree = ET.ElementTree(root)
        timestamp_log = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(OUTPUT_FILE, "wb") as f:
            f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
            tree.write(f, encoding="utf-8", xml_declaration=False)

        print(f"[{timestamp_log}] ✅ General Sitemap Created! Added {files_added} links.")

    except Exception as e:
        print(f"❌ Python Error: {str(e)}")

if __name__ == "__main__":
    generate_general_sitemap()
    