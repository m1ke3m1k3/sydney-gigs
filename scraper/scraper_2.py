"""
Sydney Easy Money Scraper
Correr: python3 scraper.py
Genera: ../web/data/opportunities.json
"""

import json
import re
from datetime import datetime
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

def scrape_rtr():
    """Realtime Research — rtr.com.au"""
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(user_agent=UA)
        try:
            page.goto("https://rtr.com.au/projects/", timeout=20000)
            page.wait_for_timeout(3000)
            soup = BeautifulSoup(page.content(), "html.parser")

            # Each project card
            cards = soup.select(".project-card, .card, article.project, [class*='project-item']")
            if not cards:
                # Fallback: look for earn$ pattern
                cards = soup.find_all(lambda tag: tag.name in ["div", "article"] and
                                      tag.get_text() and "earn" in tag.get_text().lower())

            for card in cards[:20]:
                text = card.get_text(" ", strip=True)
                pay_match = re.search(r"earn\s*<?\$?([\d,]+)", text, re.IGNORECASE)
                pay = f"${pay_match.group(1)}" if pay_match else "Ver sitio"

                title_el = card.select_one("h2, h3, h4, .title, .project-title")
                title = title_el.get_text(strip=True) if title_el else text[:60]

                # Prioriza el link que envuelve o está junto al título (más probable que sea el específico)
                link_el = None
                if title_el:
                    link_el = title_el.find("a", href=True) or title_el.find_parent("a", href=True)
                if not link_el:
                    link_el = card.select_one("a[href]")

                link = "https://rtr.com.au" + link_el["href"] if link_el and link_el["href"].startswith("/") else \
                       link_el["href"] if link_el else "https://rtr.com.au/projects/"

                results.append({
                    "source": "Realtime Research",
                    "title": title,
                    "pay": pay,
                    "type": "Focus Group / Survey",
                    "location": "Sydney / Online",
                    "link": link,
                    "scraped_at": datetime.now().isoformat()
                })
        except Exception as e:
            print(f"[RTR] Error: {e}")
        finally:
            browser.close()
    return results


def scrape_research_connections():
    """Research Connections — researchconnections.com.au"""
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(user_agent=UA)
        try:
            page.goto("https://researchconnections.com.au/participate/", timeout=20000)
            page.wait_for_timeout(3000)
            soup = BeautifulSoup(page.content(), "html.parser")

            cards = soup.select(".study, .opportunity, article, .et_pb_blurb")
            for card in cards[:20]:
                text = card.get_text(" ", strip=True)
                if not any(kw in text.lower() for kw in ["earn", "$", "paid", "study", "group"]):
                    continue

                pay_match = re.search(r"\$\s*([\d,]+)", text)
                pay = f"${pay_match.group(1)}" if pay_match else "Ver sitio"

                title_el = card.select_one("h2, h3, h4, strong")
                title = title_el.get_text(strip=True) if title_el else text[:60]

                # Buscar el enlace específico de esta tarjeta (no el genérico)
                link_el = card.select_one("a[href]")
                if link_el and link_el.get("href"):
                    href = link_el["href"]
                    link = "https://researchconnections.com.au" + href if href.startswith("/") else href
                else:
                    link = "https://researchconnections.com.au/participate/"

                results.append({
                    "source": "Research Connections",
                    "title": title,
                    "pay": pay,
                    "type": "Focus Group / Interview",
                    "location": "Sydney / Online",
                    "link": link,
                    "scraped_at": datetime.now().isoformat()
                })
        except Exception as e:
            print(f"[RC] Error: {e}")
        finally:
            browser.close()
    return results


def scrape_sydney_focus_groups():
    """Sydney Focus Groups — sydneyfocusgroups.com.au"""
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(user_agent=UA)
        try:
            page.goto("https://www.sydneyfocusgroups.com.au/", timeout=20000)
            page.wait_for_timeout(3000)
            soup = BeautifulSoup(page.content(), "html.parser")

            # This site often shows current studies on homepage
            items = soup.find_all(lambda tag: tag.name in ["div", "p", "li"] and
                                  "$" in tag.get_text())
            seen = set()
            for item in items[:15]:
                text = item.get_text(" ", strip=True)
                if text in seen or len(text) < 20:
                    continue
                seen.add(text)

                pay_match = re.search(r"\$\s*([\d,]+)", text)
                pay = f"${pay_match.group(1)}" if pay_match else "$80–$150"

                # Buscar enlace específico dentro o cerca de este elemento
                link_el = item.select_one("a[href]") or (item.find_parent("a") if item.find_parent("a") else None)
                if link_el and link_el.get("href"):
                    href = link_el["href"]
                    link = "https://www.sydneyfocusgroups.com.au" + href if href.startswith("/") else href
                else:
                    link = "https://www.sydneyfocusgroups.com.au/"

                results.append({
                    "source": "Sydney Focus Groups",
                    "title": text[:80],
                    "pay": pay,
                    "type": "Focus Group",
                    "location": "Sydney",
                    "link": link,
                    "scraped_at": datetime.now().isoformat()
                })
        except Exception as e:
            print(f"[SFG] Error: {e}")
        finally:
            browser.close()
    return results


def scrape_user_interviews():
    """User Interviews — userinterviews.com (global, incluye AU)"""
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(user_agent=UA)
        try:
            page.goto("https://app.userinterviews.com/studies", timeout=20000)
            page.wait_for_timeout(4000)
            soup = BeautifulSoup(page.content(), "html.parser")

            cards = soup.select("[class*='study'], [class*='card'], [data-testid*='study']")
            for card in cards[:20]:
                text = card.get_text(" ", strip=True)
                pay_match = re.search(r"\$\s*([\d,]+)", text)
                pay = f"${pay_match.group(1)}" if pay_match else "Ver sitio"

                title_el = card.select_one("h2, h3, h4, [class*='title']")
                title = title_el.get_text(strip=True) if title_el else text[:70]

                link_el = card.select_one("a[href]")
                link = link_el["href"] if link_el else "https://app.userinterviews.com/studies"

                results.append({
                    "source": "User Interviews",
                    "title": title,
                    "pay": pay,
                    "type": "User Research / Interview",
                    "location": "Online",
                    "link": link,
                    "scraped_at": datetime.now().isoformat()
                })
        except Exception as e:
            print(f"[UI] Error: {e}")
        finally:
            browser.close()
    return results


def scrape_prolific():
    """Prolific — prolific.com (academia, paga bien)"""
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(user_agent=UA)
        try:
            # Prolific requires login, but we can show the signup page as a source
            page.goto("https://app.prolific.com/studies", timeout=20000)
            page.wait_for_timeout(3000)
            # If logged in, scrape; otherwise return static entry
            content = page.content()
            if "login" in content.lower() or "sign in" in content.lower():
                results.append({
                    "source": "Prolific",
                    "title": "Estudios académicos pagados (requiere registro)",
                    "pay": "$6–$15 AUD/hora típico",
                    "type": "Academic Research",
                    "location": "Online",
                    "link": "https://www.prolific.com",
                    "scraped_at": datetime.now().isoformat()
                })
            else:
                soup = BeautifulSoup(content, "html.parser")
                cards = soup.select("[class*='study'], [class*='card']")
                for card in cards[:15]:
                    text = card.get_text(" ", strip=True)
                    pay_match = re.search(r"\$\s*([\d.]+)", text)
                    pay = f"${pay_match.group(1)}" if pay_match else "Ver sitio"
                    title_el = card.select_one("h2, h3, h4")
                    title = title_el.get_text(strip=True) if title_el else text[:70]
                    results.append({
                        "source": "Prolific",
                        "title": title,
                        "pay": pay,
                        "type": "Academic Research",
                        "location": "Online",
                        "link": "https://app.prolific.com/studies",
                        "scraped_at": datetime.now().isoformat()
                    })
        except Exception as e:
            print(f"[Prolific] Error: {e}")
        finally:
            browser.close()
    return results


def scrape_gumtree():
    """Gumtree AU — anuncios de estudios pagados en Sydney"""
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(user_agent=UA)
        try:
            page.goto(
                "https://www.gumtree.com.au/s-jobs/sydney/paid+research/k0c9300l3005796",
                timeout=20000
            )
            page.wait_for_timeout(3000)
            soup = BeautifulSoup(page.content(), "html.parser")

            listings = soup.select("article.user-ad-row, .user-ad-collection-new-design__item, [data-q='ad-list-item']")
            for listing in listings[:20]:
                title_el = listing.select_one("h3, .user-ad-row__title, [data-q='ad-title']")
                title = title_el.get_text(strip=True) if title_el else "Ver anuncio"

                price_el = listing.select_one(".user-ad-price, [data-q='price']")
                pay = price_el.get_text(strip=True) if price_el else "Ver anuncio"

                link_el = listing.select_one("a[href]")
                link = "https://www.gumtree.com.au" + link_el["href"] if link_el and link_el["href"].startswith("/") else \
                       link_el["href"] if link_el else "https://www.gumtree.com.au"

                if title and len(title) > 5:
                    results.append({
                        "source": "Gumtree",
                        "title": title,
                        "pay": pay,
                        "type": "Varios",
                        "location": "Sydney",
                        "link": link,
                        "scraped_at": datetime.now().isoformat()
                    })
        except Exception as e:
            print(f"[Gumtree] Error: {e}")
        finally:
            browser.close()
    return results


def run_all():
    print("🔍 Iniciando scraping...")
    all_results = []

    scrapers = [
        ("Realtime Research", scrape_rtr),
        ("Research Connections", scrape_research_connections),
        ("Sydney Focus Groups", scrape_sydney_focus_groups),
        ("User Interviews", scrape_user_interviews),
        ("Prolific", scrape_prolific),
        ("Gumtree", scrape_gumtree),
    ]

    for name, fn in scrapers:
        print(f"  → {name}...", end=" ", flush=True)
        try:
            results = fn()
            all_results.extend(results)
            print(f"✅ {len(results)} oportunidades")
        except Exception as e:
            print(f"❌ {e}")

    output = {
        "last_updated": datetime.now().strftime("%d %b %Y, %H:%M"),
        "total": len(all_results),
        "opportunities": all_results
    }

    with open("../web/data/opportunities.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n✅ {len(all_results)} oportunidades guardadas en web/data/opportunities.json")


if __name__ == "__main__":
    run_all()
