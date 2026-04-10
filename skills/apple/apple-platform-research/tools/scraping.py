"""
HTML scraping helpers with BeautifulSoup.
"""
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional

def select_text(html: str, selector: str) -> List[str]:
    soup = BeautifulSoup(html, "html.parser")
    return [el.get_text(strip=True) for el in soup.select(selector)]

def select_attrs(html: str, selector: str, attr: str) -> List[str]:
    soup = BeautifulSoup(html, "html.parser")
    return [el.get(attr, "") for el in soup.select(selector) if el.has_attr(attr)]

def get_links_with_text(html: str, selector: str = "a") -> List[Dict[str, str]]:
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for a in soup.select(selector):
        href = a.get("href", "")
        text = a.get_text(strip=True)
        if href:
            links.append({"href": href, "text": text})
    return links
