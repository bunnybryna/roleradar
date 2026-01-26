from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from utils.location import normalize_location


@dataclass(frozen=True)
class Job:
    company: str
    job_id: str
    title: str
    url: str
    location: Optional[str] = None


COMPANY = "COMSOL"
BASE_URL = "https://www.comsol.com"
CAREERS_URL = f"{BASE_URL}/company/careers/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; RoleRadar/1.0)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

TIMEOUT = 30

JOB_HREF_RE = re.compile(r"/company/careers/job/(\d+)/?$")


def _country_to_iso2(country_raw: str) -> str:
    c = (country_raw or "").strip()
    c_norm = re.sub(r"\s+", " ", c)
    c_norm = c_norm.replace(".", "")
    key = c_norm.casefold()

    mapping = {
        "usa": "US",
        "us": "US",
        "united states": "US",
        "united states of america": "US",
        "united kingdom": "GB",
        "uk": "GB",
        "great britain": "GB",
        "china": "CN",
        "germany": "DE",
        "france": "FR",
        "italy": "IT",
        "finland": "FI",
        "sweden": "SE",
        "india": "IN",
    }

    return mapping.get(key) or c.strip().upper()


def _normalize_heading_location(heading: str) -> Optional[str]:
    # Examples:
    # - "Burlington, MA, USA"
    # - "Cambridge, United Kingdom"
    # - "Beijing, China"
    parts = [p.strip() for p in (heading or "").split(",") if p.strip()]
    if len(parts) < 2:
        return None

    city = parts[0]

    if len(parts) == 2:
        country = _country_to_iso2(parts[1])
        return normalize_location(country, "", city)

    state = parts[1]
    country = _country_to_iso2(parts[2])
    return normalize_location(country, state, city)


def scrape_comsol() -> List[Job]:
    resp = requests.get(CAREERS_URL, headers=HEADERS, timeout=TIMEOUT)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    h2 = soup.find("h2", string=re.compile(r"Career Opportunities Worldwide", re.IGNORECASE))
    if not h2:
        return []

    jobs: dict[str, Job] = {}

    node = h2.find_next_sibling()
    while node is not None:
        if getattr(node, "name", None) == "h2":
            break

        if getattr(node, "name", None) == "h3":
            loc_heading = node.get_text(" ", strip=True)
            location = _normalize_heading_location(loc_heading)

            ul = node.find_next_sibling("ul")
            if ul:
                for a in ul.find_all("a", href=True):
                    title = a.get_text(" ", strip=True)
                    href = a.get("href") or ""
                    m = JOB_HREF_RE.search(href)
                    if not m or not title:
                        continue
                    num_id = m.group(1)
                    url = urljoin(BASE_URL, href)
                    job_id = f"{COMPANY}:{num_id}"
                    jobs[job_id] = Job(
                        company=COMPANY,
                        job_id=job_id,
                        title=title,
                        url=url,
                        location=location,
                    )

            node = ul.find_next_sibling() if ul else node.find_next_sibling()
            continue

        node = node.find_next_sibling()

    return list(jobs.values())
