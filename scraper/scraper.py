"""
Sydney Easy Money Scraper
Correr: python3 scraper.py
Genera: ../docs/feed/opportunities.json
"""

import json
import re
from datetime import datetime
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

# Tipos válidos = deben coincidir EXACTAMENTE con los data-value de los botones de filtro en web/index.html
def detect_type(title, default="Focus Group"):
    """
    Detecta el tipo de oportunidad a partir del título.
    Devuelve un valor que coincide exactamente con los filtros de la web.
    """
    t = title.lower()

    if any(kw in t for kw in ["taste test", "product testing", "product test"]):
        return "Taste Test" if "taste" in t else "Product Testing"
    if "interview" in t and "focus" not in t:
        return "Interview"
    if any(kw in t for kw in ["survey", "online panel", "panel"]):
        return "Online Survey"
    if any(kw in t for kw in ["ux", "usability", "user research", "user test"]):
        return "User Research"
    if any(kw in t for kw in ["clinical", "trial", "volunteer", "medical study"]):
        return "Clinical Study"
    if any(kw in t for kw in ["academic", "research study"]):
        return "Academic Research"
    if "focus" in t:
        return "Focus Group"

    return default

def scrape_rtr():
    """Realtime Research — rtr.com.au"""
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(user_agent=UA)
        try:
            page.goto("https://rtr.com.au/projects/", timeout=30000, wait_until="networkidle")
            page.wait_for_timeout(2000)
            soup = BeautifulSoup(page.content(), "html.parser")

            # Cada proyecto es un <article> que contiene un project_grid__badge
            cards = soup.select("article")
            seen_links = set()

            for card in cards[:30]:
                badge = card.select_one(".project_grid__badge")
                if not badge:
                    continue  # no es una tarjeta de proyecto

                title_el = card.select_one("h3")
                title = title_el.get_text(strip=True) if title_el else "Untitled project"

                # Filtrar falsos positivos: títulos genéricos de la página, no de un proyecto real
                if title.lower() in ("current projects", "projects", ""):
                    continue

                # El link específico de la tarjeta
                link_el = card.select_one("a.wpgb-card-layer-link[href]")
                link = link_el["href"] if link_el else "https://rtr.com.au/projects/"

                # Deduplicar: si ya vimos este link exacto, no lo añadimos otra vez
                if link in seen_links:
                    continue
                seen_links.add(link)

                pay_el = badge.select_one(".badge_amount")
                pay = pay_el.get_text(strip=True) if pay_el else "See site"

                location_el = card.select_one(".location")
                location = location_el.get_text(strip=True).rstrip(",") if location_el else "Australia"

                results.append({
                    "source": "Realtime Research",
                    "title": title,
                    "pay": pay,
                    "type": detect_type(title),
                    "location": location,
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
            page.goto("https://researchconnections.com.au/", timeout=30000, wait_until="networkidle")
            page.wait_for_timeout(2000)
            soup = BeautifulSoup(page.content(), "html.parser")

            cards = soup.select(".study, .opportunity, article, .et_pb_blurb")
            for card in cards[:20]:
                text = card.get_text(" ", strip=True)
                if not any(kw in text.lower() for kw in ["earn", "$", "paid", "study", "group"]):
                    continue

                pay_match = re.search(r"\$\s*([\d,]+)", text)
                pay = f"${pay_match.group(1)}" if pay_match else "See site"

                title_el = card.select_one("h2, h3, h4, strong")
                title = title_el.get_text(strip=True) if title_el else text[:60]

                # Buscar el enlace específico de esta tarjeta (no el genérico)
                link_el = card.select_one("a[href]")
                if link_el and link_el.get("href"):
                    href = link_el["href"]
                    link = "https://researchconnections.com.au" + href if href.startswith("/") else href
                else:
                    link = "https://researchconnections.com.au/"

                results.append({
                    "source": "Research Connections",
                    "title": title,
                    "pay": pay,
                    "type": detect_type(title, default="Focus Group"),
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
            page.goto("https://www.sydneyfocusgroups.com.au/", timeout=30000, wait_until="networkidle")
            page.wait_for_timeout(2000)
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
            page.goto("https://app.userinterviews.com/studies", timeout=30000, wait_until="networkidle")
            page.wait_for_timeout(2000)
            soup = BeautifulSoup(page.content(), "html.parser")

            cards = soup.select("[class*='study'], [class*='card'], [data-testid*='study']")
            for card in cards[:20]:
                text = card.get_text(" ", strip=True)
                pay_match = re.search(r"\$\s*([\d,]+)", text)
                pay = f"${pay_match.group(1)}" if pay_match else "See site"

                title_el = card.select_one("h2, h3, h4, [class*='title']")
                title = title_el.get_text(strip=True) if title_el else text[:70]

                link_el = card.select_one("a[href]")
                link = link_el["href"] if link_el else "https://app.userinterviews.com/studies"

                results.append({
                    "source": "User Interviews",
                    "title": title,
                    "pay": pay,
                    "type": detect_type(title, default="User Research"),
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
                    "title": "Paid academic studies (registration required)",
                    "pay": "$6–$15 AUD/hour typical",
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
                    pay = f"${pay_match.group(1)}" if pay_match else "See site"
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


def scrape_scientia():
    """Scientia Clinical Research — scientiaclinicalresearch.com.au (ensayos clínicos Fase I, Sydney)"""
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(user_agent=UA)
        try:
            page.goto("https://www.scientiaclinicalresearch.com.au/find-a-study/", timeout=30000, wait_until="networkidle")
            page.wait_for_timeout(2000)
            soup = BeautifulSoup(page.content(), "html.parser")

            # Cada estudio suele estar en una tarjeta/bloque con título y monto de compensación
            cards = soup.select("article, .study, .study-card, [class*='study'], .et_pb_blurb")
            seen_titles = set()

            for card in cards[:30]:
                text = card.get_text(" ", strip=True)
                if not any(kw in text.lower() for kw in ["study", "volunteer", "$", "trial"]):
                    continue

                title_el = card.select_one("h2, h3, h4, strong")
                title = title_el.get_text(strip=True) if title_el else text[:70]

                if title in seen_titles or len(title) < 5:
                    continue
                seen_titles.add(title)

                pay_match = re.search(r"\$\s*([\d,]+)", text)
                pay = f"${pay_match.group(1)}" if pay_match else "See site (compensation varies)"

                link_el = card.select_one("a[href]")
                if link_el and link_el.get("href"):
                    href = link_el["href"]
                    link = "https://www.scientiaclinicalresearch.com.au" + href if href.startswith("/") else href
                else:
                    link = "https://www.scientiaclinicalresearch.com.au/find-a-study/"

                results.append({
                    "source": "Scientia Clinical Research",
                    "title": title,
                    "pay": pay,
                    "type": "Clinical Study",
                    "location": "Sydney (in-person, medical supervision)",
                    "link": link,
                    "scraped_at": datetime.now().isoformat()
                })
        except Exception as e:
            print(f"[Scientia] Error: {e}")
        finally:
            browser.close()
    return results


def scrape_clinibase():
    """Clinibase — clinibase.com (agregador de ensayos clínicos AU/NZ)"""
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(user_agent=UA)
        try:
            page.goto("https://clinibase.com/current-trials/", timeout=30000, wait_until="networkidle")
            page.wait_for_timeout(2000)
            soup = BeautifulSoup(page.content(), "html.parser")

            cards = soup.select("article, .trial, .trial-card, [class*='trial'], .et_pb_blurb")
            seen_titles = set()

            for card in cards[:30]:
                text = card.get_text(" ", strip=True)
                if not any(kw in text.lower() for kw in ["study", "trial", "volunteer", "$", "sydney"]):
                    continue

                title_el = card.select_one("h2, h3, h4, strong")
                title = title_el.get_text(strip=True) if title_el else text[:70]

                if title in seen_titles or len(title) < 5:
                    continue
                seen_titles.add(title)

                pay_match = re.search(r"\$\s*([\d,]+)", text)
                pay = f"${pay_match.group(1)}" if pay_match else "Reimbursed"

                link_el = card.select_one("a[href]")
                if link_el and link_el.get("href"):
                    href = link_el["href"]
                    link = "https://clinibase.com" + href if href.startswith("/") else href
                else:
                    link = "https://clinibase.com/current-trials/"

                results.append({
                    "source": "Clinibase",
                    "title": title,
                    "pay": pay,
                    "type": "Clinical Study",
                    "location": "Sydney / Australia",
                    "link": link,
                    "scraped_at": datetime.now().isoformat()
                })
        except Exception as e:
            print(f"[Clinibase] Error: {e}")
        finally:
            browser.close()
    return results


def run_all():
    print("🔍 Starting scraping...")
    all_results = []

    scrapers = [
        ("Realtime Research", scrape_rtr),
        ("Research Connections", scrape_research_connections),
        ("Sydney Focus Groups", scrape_sydney_focus_groups),
        ("User Interviews", scrape_user_interviews),
        ("Prolific", scrape_prolific),
        ("Scientia Clinical Research", scrape_scientia),
        ("Clinibase", scrape_clinibase),
        # Gumtree: bloquea activamente el scraping (Access Denied). Queda solo como link manual en la web.
        # ("Gumtree", scrape_gumtree),
    ]

    for name, fn in scrapers:
        print(f"  → {name}...", end=" ", flush=True)
        try:
            results = fn()
            all_results.extend(results)
            print(f"✅ {len(results)} opportunities")
        except Exception as e:
            print(f"❌ {e}")

    output = {
        "last_updated": datetime.now().strftime("%d %b %Y, %H:%M"),
        "total": len(all_results),
        "opportunities": all_results
    }

    with open("../docs/feed/opportunities.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n✅ {len(all_results)} opportunities saved to docs/feed/opportunities.json")


if __name__ == "__main__":
    run_all()
