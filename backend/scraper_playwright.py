from playwright.sync_api import sync_playwright
import pandas as pd
import sys
import re
import os

# # ── CONFIG ────────────────────────────────────────────────────────────────────
# TARGET_REVIEWS = 80        # Stop after this many unique reviews
# MAX_PAGES      = 8         # Hard cap on pages
# SCROLL_ROUNDS  = 6         # Scroll steps per page
# SCROLL_DELTA   = 900       # Pixels per scroll step
# PAGE_WAIT      = 2500      # ms after page load
# SCROLL_WAIT    = 600       # ms between scroll steps
# OUTPUT_FILE    = "flipkart_blocks.csv"
# HEADLESS       = True
# # ─────────────────────────────────────────────────────────────────────────────

# ── CONFIG ────────────────────────────────────────────────────────────────────
TARGET_REVIEWS = 40        # Stop after this many unique reviews
MAX_PAGES      = 4         # Hard cap on pages
SCROLL_ROUNDS  = 5         # Scroll steps per page
SCROLL_DELTA   = 600       # Pixels per scroll step
PAGE_WAIT      = 2000     # ms after page load
SCROLL_WAIT    = 300       # ms between scroll steps
OUTPUT_FILE    = "flipkart_blocks.csv"
HEADLESS       = True
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
    

