#!/usr/bin/env python3

import os
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET

# --- CONFIGURATION ---
SITE_URL = "https://societalnews.com/"
PUBLICATION_NAME = "Societal News"
LANGUAGE = "en"
BASE_DIR = "/home/societal/public_html/" 
OUTPUT_FILE = os.path.join(BASE_DIR, "news-sitemap.xml")

def generate_news_sitemap():
    try:
        root = ET.Element("urlset")
        root.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")
        root.set("xmlns:news", "http://www.google.com/schemas/sitemap-news/0.9")

        cutoff = datetime.now() - timedelta(hours=48)
        files_added = 0

        for root_path, dirs, files in os.walk(BASE_DIR):
            for filename in files:
                if filename.endswith(".html"):
                    filepath = os.path.join(root_path, filename)
                    mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
                    
                    if mtime > cutoff:
                        # 1. CLEAN THE URL
                        relative_path = os.path.relpath(filepath, BASE_DIR).replace("\\", "/")
                        
                        # Remove 'index.html' from the end of URLs
                        if relative_path.endswith("index.html"):
                            clean_url_path = relative_path[:-10] # Removes 'index.html'
                        else:
                            clean_url_path = relative_path

                        # 2. SKIP GENERIC TITLES
                        clean_title = filename.replace("-", " ").replace(".html", "").title()
                        if clean_title.lower() == "index":
                            # If it's the homepage or a category index, you might want to 
                            # give it a better name or skip it from "News" sitemap.
                            # For Google News, usually you only want specific articles.
                            continue 

                        url_entry = ET.SubElement(root, "url")
                        loc = ET.SubElement(url_entry, "loc")
                        loc.text = f"{SITE_URL}{clean_url_path}"
                        
                        news_block = ET.SubElement(url_entry, "news:news")
                        pub = ET.SubElement(news_block, "news:publication")
                        ET.SubElement(pub, "news:name").text = PUBLICATION_NAME
                        ET.SubElement(pub, "news:language").text = LANGUAGE
                        
                        ET.SubElement(news_block, "news:publication_date").text = mtime.strftime('%Y-%m-%dT%H:%M:%S+00:00')
                        ET.SubElement(news_block, "news:title").text = clean_title
                        
                        files_added += 1

        tree = ET.ElementTree(root)
        timestamp_log = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(OUTPUT_FILE, "wb") as f:
            f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
            tree.write(f, encoding="utf-8", xml_declaration=False)

        print(f"[{timestamp_log}] ✅ Success! Added {files_added} articles.")

    except Exception as e:
        print(f"❌ Python Error: {str(e)}")

if __name__ == "__main__":
    generate_news_sitemap()