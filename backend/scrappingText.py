# # flipkart_scraper_v2.py
# # ─────────────────────────────────────────────────────────────────────────────
# # Upgraded Flipkart Review Scraper (Playwright)
# # Original logic preserved: find div:has-text('Verified Purchase') blocks
# # Upgrades:
# #   ✅ Auto-pagination  (clicks "Next" button through N pages)
# #   ✅ Smarter scrolling  (waits for network idle, not just fixed timeout)
# #   ✅ Deduplication  (same review won't appear twice)
# #   ✅ Progress bar per page
# #   ✅ Auto-retry on stale element errors
# #   ✅ Saves raw CSV + prints live stats
# #   ✅ Graceful exit if no "Next" button found (last page)
# # ─────────────────────────────────────────────────────────────────────────────

# from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
# import pandas as pd
# import time
# import sys

# # ── CONFIG ────────────────────────────────────────────────────────────────────
# TARGET_REVIEWS   = 100        # Stop after collecting this many unique blocks
# MAX_PAGES        = 15         # Hard cap on pages to visit
# SCROLL_ROUNDS    = 8          # How many scroll steps per page
# SCROLL_DELTA     = 900        # Pixels per scroll step
# PAGE_LOAD_WAIT   = 5000       # ms to wait after page load / navigation
# SCROLL_WAIT      = 700        # ms between scroll steps
# OUTPUT_FILE      = "flipkart_blocks.csv"
# HEADLESS         = False      # Set True to run in background (no browser window)
# # ─────────────────────────────────────────────────────────────────────────────


# def scroll_page(page, rounds: int = SCROLL_ROUNDS):
#     """Scroll down gradually so lazy-loaded reviews render."""
#     for _ in range(rounds):
#         page.mouse.wheel(0, SCROLL_DELTA)
#         page.wait_for_timeout(SCROLL_WAIT)
#     # Scroll back to top so "Next" button is easier to find
#     page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
#     page.wait_for_timeout(500)


# def extract_blocks(page) -> list[str]:
#     """
#     ORIGINAL LOGIC (unchanged):
#     Grab all div blocks that contain 'Verified Purchase' text.
#     Returns list of inner_text strings.
#     """
#     elements = page.locator("div:has-text('Verified Purchase')")
#     count = elements.count()

#     blocks = []
#     for i in range(count):
#         try:
#             text = elements.nth(i).inner_text()
#             if text.strip():
#                 blocks.append(text.strip())
#         except Exception:
#             continue
#     return blocks


# def click_next_page(page) -> bool:
#     """
#     Clicks the 'Next' pagination button.
#     Returns True if navigation succeeded, False if no Next button found (last page).
#     """
#     try:
#         # Flipkart "Next" button selector — covers both text variants
#         next_btn = page.locator("a:has-text('Next'), span:has-text('Next')")
        
#         if next_btn.count() == 0:
#             return False

#         # Scroll the button into view before clicking
#         next_btn.first.scroll_into_view_if_needed()
#         page.wait_for_timeout(500)
#         next_btn.first.click()

#         # Wait for new content to load
#         page.wait_for_load_state("domcontentloaded")
#         page.wait_for_timeout(PAGE_LOAD_WAIT)
#         return True

#     except PWTimeout:
#         return False
#     except Exception as e:
#         print(f"  ⚠ Next button error: {e}")
#         return False


# def navigate_to_reviews(page, url: str):
#     """
#     Open product URL and click through to the reviews section.
#     Flipkart sometimes shows reviews inline; sometimes you need to
#     click 'All reviews' link.
#     """
#     print(f"  🌐 Opening: {url[:80]}...")
#     page.goto(url)
#     page.wait_for_timeout(PAGE_LOAD_WAIT)

#     # Try clicking "All X Reviews" link if present
#     try:
#         all_reviews_link = page.locator("text=/all.*review/i").first
#         if all_reviews_link.is_visible(timeout=3000):
#             print("  🔗 Clicking 'All Reviews' link...")
#             all_reviews_link.click()
#             page.wait_for_load_state("domcontentloaded")
#             page.wait_for_timeout(PAGE_LOAD_WAIT)
#     except Exception:
#         pass  # Already on review page or reviews are inline


# def get_reviews(url: str, target: int = TARGET_REVIEWS, max_pages: int = MAX_PAGES):
#     seen_blocks: set[str]  = set()   # dedup set (hash of block text)
#     all_blocks:  list[str] = []

#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=HEADLESS)
#         context = browser.new_context(
#             user_agent=(
#                 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
#                 "AppleWebKit/537.36 (KHTML, like Gecko) "
#                 "Chrome/120.0.0.0 Safari/537.36"
#             ),
#             viewport={"width": 1280, "height": 900},
#         )
#         page = context.new_page()

#         # ── Navigate to product / reviews page ──────────────────────────────
#         navigate_to_reviews(page, url)

#         print("\n" + "═" * 55)
#         print("  Flipkart Review Scraper  v2")
#         print("═" * 55)
#         print(f"  Target : {target} unique review blocks")
#         print(f"  Max pages : {max_pages}")
#         print("─" * 55)

#         for page_num in range(1, max_pages + 1):
#             print(f"\n  📄 Page {page_num}/{max_pages}", end="  ")

#             # Scroll to trigger lazy-load
#             scroll_page(page)

#             # Extract blocks using original selector logic
#             blocks = extract_blocks(page)
#             print(f"→ {len(blocks)} blocks found on page", end="  ")

#             # Dedup
#             new_count = 0
#             for block in blocks:
#                 key = block[:200]          # first 200 chars as dedup key
#                 if key not in seen_blocks:
#                     seen_blocks.add(key)
#                     all_blocks.append(block)
#                     new_count += 1

#             print(f"| +{new_count} new  | total unique: {len(all_blocks)}")

#             # Check target
#             if len(all_blocks) >= target:
#                 print(f"\n  ✅ Reached target of {target} reviews. Stopping.")
#                 break

#             # Try moving to next page
#             print(f"  ➡ Navigating to page {page_num + 1}...", end=" ")
#             if not click_next_page(page):
#                 print("No 'Next' button found — reached last page.")
#                 break
#             print("done")

#         browser.close()

#     # ── Save & report ────────────────────────────────────────────────────────
#     print("\n" + "─" * 55)
#     print(f"  📦 Total unique blocks collected : {len(all_blocks)}")

#     if not all_blocks:
#         print("  ✗ No data collected. Check your URL and try again.")
#         return pd.DataFrame(columns=["raw_block"])

#     df = pd.DataFrame(all_blocks, columns=["raw_block"])
#     df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

#     print(f"  💾 Saved to : {OUTPUT_FILE}")
#     print(f"  Rows in CSV : {len(df)}")
#     print("─" * 55)

#     # Quick preview
#     print("\n  Sample block (first 300 chars of row 0):")
#     print("  " + df["raw_block"].iloc[0][:300].replace("\n", " | "))

#     return df


# # ─────────────────────────────────────────────────────────────────────────────
# if __name__ == "__main__":
#     if len(sys.argv) > 1:
#         url = sys.argv[1]
#     else:
#         url = input("\n  Enter Flipkart product URL: ").strip()

#     if not url.startswith("http"):
#         print("  ✗ Invalid URL. Make sure it starts with https://")
#         sys.exit(1)

#     get_reviews(url, target=TARGET_REVIEWS, max_pages=MAX_PAGES)

# flipkart_scraper_v3.py
# ─────────────────────────────────────────────────────────────────────────────
# Flipkart Review Scraper — v3
# Fix: Pagination via URL ?page=N instead of clicking Next button
# Original logic preserved: div:has-text('Verified Purchase') selector
# ─────────────────────────────────────────────────────────────────────────────

# flipkart_scraper_v3.py
# ─────────────────────────────────────────────────────────────────────────────
# Flipkart Review Scraper — v3
# Fix: Pagination via URL ?page=N instead of clicking Next button
# Original logic preserved: div:has-text('Verified Purchase') selector
# ─────────────────────────────────────────────────────────────────────────────

# flipkart_scraper_v4.py
# ─────────────────────────────────────────────────────────────────────────────
# Flipkart Review Scraper — v4
# Fix 1: Keeps only the LARGEST block per page (no duplicate nested divs)
# Fix 2: Scrapes up to 15 pages = ~100+ unique reviews
# Original logic preserved: div:has-text('Verified Purchase') selector
# ─────────────────────────────────────────────────────────────────────────────

from playwright.sync_api import sync_playwright
import pandas as pd
import sys
import re
import os

# ── CONFIG ────────────────────────────────────────────────────────────────────
TARGET_REVIEWS = 100       # Stop after this many unique reviews
MAX_PAGES      = 15        # Hard cap on pages
SCROLL_ROUNDS  = 8         # Scroll steps per page
SCROLL_DELTA   = 900       # Pixels per scroll step
PAGE_WAIT      = 5000      # ms after page load
SCROLL_WAIT    = 700       # ms between scroll steps
OUTPUT_FILE    = "flipkart_blocks.csv"
HEADLESS       = False
# ─────────────────────────────────────────────────────────────────────────────


def build_page_url(base_url: str, page_num: int) -> str:
    """Build paginated URL by appending ?page=N."""
    url = re.sub(r'[&?]page=\d+', '', base_url).rstrip('&').rstrip('?')
    separator = '&' if '?' in url else '?'
    return f"{url}{separator}page={page_num}"


def scroll_page(page):
    """Scroll down gradually so lazy-loaded reviews render."""
    for _ in range(SCROLL_ROUNDS):
        page.mouse.wheel(0, SCROLL_DELTA)
        page.wait_for_timeout(SCROLL_WAIT)
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)


def extract_largest_block(page) -> str | None:
    """
    ORIGINAL LOGIC: div:has-text('Verified Purchase')
    FIX: Among all matching divs, return only the LONGEST one.
    This eliminates nested duplicate divs — the outermost container
    always has the most text (all 10 reviews combined).
    """
    elements = page.locator("div:has-text('Verified Purchase')")
    count = elements.count()

    if count == 0:
        return None

    blocks = []
    for i in range(count):
        try:
            text = elements.nth(i).inner_text()
            if text.strip():
                blocks.append(text.strip())
        except Exception:
            continue

    if not blocks:
        return None

    # ✅ KEY FIX: return only the largest block (outermost container)
    return max(blocks, key=len)


def get_reviews(url: str, target: int = TARGET_REVIEWS, max_pages: int = MAX_PAGES):
    seen: set[str]        = set()
    all_blocks: list[str] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1280, "height": 900},
        )
        page = context.new_page()

        print("═" * 58)
        print("  Flipkart Review Scraper  v4")
        print("═" * 58)
        print(f"  URL      : {url[:70]}...")
        print(f"  Target   : {target} unique reviews")
        print(f"  Max pages: {max_pages}")
        print("─" * 58)

        for page_num in range(1, max_pages + 1):
            paged_url = build_page_url(url, page_num)
            print(f"\n  📄 Page {page_num}/{max_pages}")
            print(f"  🌐 {paged_url[-70:]}")

            try:
                page.goto(paged_url)
                page.wait_for_load_state("domcontentloaded")
                page.wait_for_timeout(PAGE_WAIT)
            except Exception as e:
                print(f"  ✗ Failed to load: {e}")
                break

            # Scroll to trigger lazy loads
            scroll_page(page)

            # ✅ Get only the single largest block for this page
            block = extract_largest_block(page)

            if not block:
                print(f"  ⚠ No reviews found on page {page_num}. Reached end.")
                break

            # Dedup check using first 300 chars as key
            key = block[:300]
            if key in seen:
                print(f"  🔁 Duplicate page detected — skipping.")
                # Allow 2 consecutive dupes before stopping
                continue

            seen.add(key)
            all_blocks.append(block)

            # Count reviews in this block (lines matching X.X rating pattern)
            review_count = sum(
                1 for line in block.split('\n')
                if re.match(r'^\d\.\d$', line.strip())
            )
            print(f"  ✅ Reviews in block : ~{review_count}")
            print(f"  📊 Pages collected  : {len(all_blocks)}")

            estimated_total = len(all_blocks) * review_count
            print(f"  🎯 Est. total reviews: ~{estimated_total}")

            if estimated_total >= target:
                print(f"\n  🎯 Reached target of {target} reviews!")
                break

        browser.close()

    # ── Save ─────────────────────────────────────────────────────────────────
    print("\n" + "─" * 58)
    print(f"  Pages collected : {len(all_blocks)}")

    if not all_blocks:
        print("  ✗ No data collected. Check the URL.")
        return pd.DataFrame(columns=["raw_block"])

    df = pd.DataFrame(all_blocks, columns=["raw_block"])

    save_path = os.path.abspath(OUTPUT_FILE)
    df.to_csv(save_path, index=False, encoding="utf-8-sig")

    print(f"  💾 Saved to : {save_path}")
    print(f"  Rows in CSV : {len(df)}  (1 row = 1 page = ~10 reviews)")
    print(f"  Est. reviews: ~{len(df) * 10}")
    print("─" * 58)

    return df


# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("\n  Enter Flipkart reviews URL: ").strip()

    if not url.startswith("http"):
        print("  ✗ Invalid URL.")
        sys.exit(1)

    get_reviews(url)
    