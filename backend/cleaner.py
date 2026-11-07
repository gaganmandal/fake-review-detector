# """
# flipkart_cleaner.py
# =====================================================
# Cleans flipkart_blocks.csv → flipkart_reviews_clean.csv

# Extracted fields:
#   rating         float  — 1.0 to 5.0
#   title          str    — review headline
#   review_for     str    — Color / Size variant
#   review_text    str    — actual review body (cleaned)
#   reviewer_name  str
#   reviewer_city  str
#   helpful_count  int    — upvotes on review
#   verified       bool   — Verified Purchase
#   review_date    str    — "Feb, 2021" or "3 months ago"
#   sentiment      str    — Positive / Neutral / Negative (derived)
#   word_count     int    — word count of review_text

# Run:
#     python3 flipkart_cleaner.py
# """

# import re
# import os
# import pandas as pd
# from typing import Optional

# # ── INPUT / OUTPUT ────────────────────────────────────────────
# INPUT_FILE  = "flipkart_blocks.csv"
# OUTPUT_FILE = "flipkart_reviews_clean.csv"

# # ── COMPILED PATTERNS ─────────────────────────────────────────
# RATING_VALUE    = re.compile(r'^\d\.\d$')
# BULLET          = re.compile(r'^•$')
# REVIEW_FOR      = re.compile(r'^Review for:\s*(.+)$')
# CITY_LINE       = re.compile(r'^,\s*(.+)$')
# HELPFUL_LINE    = re.compile(r'^Helpful for (\d+)$')
# STANDALONE_INT  = re.compile(r'^\d+$')
# VERIFIED_LINE   = re.compile(r'^Verified Purchase$')
# DATE_LINE       = re.compile(r'^·\s*(.+)$')
# TRUNCATED       = re.compile(r'\.{3}\s*more\s*$', re.IGNORECASE)
# MULTI_SPACE     = re.compile(r'  +')
# FOOTER_SENTINEL = 'Hang on, loading content'

# HEADER_NOISE = {
#     'Login', 'More', 'Cart', 'Overall', 'Fabric Quality', 'Colour',
#     'Style', 'Comfort', 'True to Specs', 'Stitching Quality',
#     'User reviews sorted by', 'Most Helpful', 'Latest',
#     'Positive', 'Negative', '★', '•',
# }

# FOOTER_NOISE = {
#     'ABOUT', 'Contact Us', 'About Us', 'Careers', 'Flipkart Stories',
#     'Press', 'Corporate Information', 'GROUP COMPANIES', 'Myntra',
#     'Cleartrip', 'Shopsy', 'HELP', 'Payments', 'Shipping',
#     'Cancellation & Returns', 'FAQ', 'CONSUMER POLICY', 'Terms Of Use',
#     'Security', 'Privacy', 'Sitemap', 'Grievance Redressal',
#     'EPR Compliance', 'FSSAI Food Safety Connect App', 'Mail Us:',
#     'Social:', 'Registered Office Address:', 'Become a Seller',
#     'Advertise', 'Gift Cards', 'Help Center',
#     'Flipkart Internet Private Limited,', 'Buildings Alyssa, Begonia &',
#     'Clove Embassy Tech Village,',
#     'Outer Ring Road, Devarabeesanahalli Village,',
#     'Bengaluru, 560103,', 'Karnataka, India',
#     'CIN : U51109KA2012PTC066107',
#     'Telephone: 044-45614700 / 044-67415800',
#     '© 2007-2026 Flipkart.com',
# }


# # ─────────────────────────────────────────────────────────────
# # STEP 1 — Strip boilerplate, return only review lines
# # ─────────────────────────────────────────────────────────────
# def strip_boilerplate(raw: str) -> list[str]:
#     lines = raw.split('\n')

#     # Find first rating line (start of reviews)
#     start = 0
#     for i, line in enumerate(lines):
#         if RATING_VALUE.match(line.strip()):
#             start = i
#             break

#     # Find footer sentinel
#     end = len(lines)
#     for i, line in enumerate(lines):
#         if FOOTER_SENTINEL in line:
#             end = i
#             break

#     return [
#         ln for ln in lines[start:end]
#         if ln.strip() not in FOOTER_NOISE
#         and ln.strip() not in HEADER_NOISE
#         and not re.match(r'^\d{1,3}(,\d{3})*$', ln.strip())   # drop count lines like "7,930"
#         and not re.match(r'^\d[\d,]+ ratings and \d[\d,]+ reviews$', ln.strip())
#     ]


# # ─────────────────────────────────────────────────────────────
# # STEP 2 — State-machine parser
# # ─────────────────────────────────────────────────────────────
# def parse_reviews(lines: list[str]) -> list[dict]:
#     reviews = []
#     i = 0
#     n = len(lines)

#     while i < n:
#         line = lines[i].strip()

#         if not RATING_VALUE.match(line):
#             i += 1
#             continue

#         rev = {
#             'rating':        float(line),
#             'title':         None,
#             'review_for':    None,
#             'review_text':   None,
#             'reviewer_name': None,
#             'reviewer_city': None,
#             'helpful_count': 0,
#             'verified':      False,
#             'review_date':   None,
#         }
#         i += 1

#         # skip bullet
#         if i < n and BULLET.match(lines[i].strip()):
#             i += 1

#         # title
#         if i < n and lines[i].strip():
#             rev['title'] = lines[i].strip()
#             i += 1

#         # review_for (optional)
#         if i < n and REVIEW_FOR.match(lines[i].strip()):
#             rev['review_for'] = REVIEW_FOR.match(lines[i].strip()).group(1).strip()
#             i += 1

#         # review body — collect lines until we hit reviewer name
#         # KEY: stop when next line is a city marker (", City") → current line = reviewer name
#         body_lines = []
#         while i < n:
#             candidate  = lines[i].strip()
#             next_line  = lines[i + 1].strip() if i + 1 < n else ''

#             if (
#                 RATING_VALUE.match(candidate)
#                 or HELPFUL_LINE.match(candidate)
#                 or VERIFIED_LINE.match(candidate)
#                 or DATE_LINE.match(candidate)
#                 or CITY_LINE.match(candidate)
#             ):
#                 break

#             # lookahead: if next line is a city, this line is the reviewer name
#             if CITY_LINE.match(next_line):
#                 break

#             if candidate:
#                 body_lines.append(candidate)
#             i += 1

#         if body_lines:
#             body = ' '.join(body_lines)
#             body = TRUNCATED.sub('', body)
#             body = MULTI_SPACE.sub(' ', body).strip()
#             rev['review_text'] = body

#         # reviewer name
#         if i < n:
#             candidate = lines[i].strip()
#             if candidate and not any([
#                 CITY_LINE.match(candidate),
#                 HELPFUL_LINE.match(candidate),
#                 VERIFIED_LINE.match(candidate),
#                 DATE_LINE.match(candidate),
#                 RATING_VALUE.match(candidate),
#             ]):
#                 rev['reviewer_name'] = MULTI_SPACE.sub(' ', candidate).strip()
#                 i += 1

#         # city
#         if i < n and CITY_LINE.match(lines[i].strip()):
#             rev['reviewer_city'] = CITY_LINE.match(lines[i].strip()).group(1).strip()
#             i += 1

#         # helpful count
#         if i < n and HELPFUL_LINE.match(lines[i].strip()):
#             rev['helpful_count'] = int(HELPFUL_LINE.match(lines[i].strip()).group(1))
#             i += 1
#             # skip standalone upvote integer
#             if i < n and STANDALONE_INT.match(lines[i].strip()):
#                 i += 1

#         # verified purchase
#         if i < n and VERIFIED_LINE.match(lines[i].strip()):
#             rev['verified'] = True
#             i += 1

#         # date
#         if i < n and DATE_LINE.match(lines[i].strip()):
#             rev['review_date'] = DATE_LINE.match(lines[i].strip()).group(1).strip()
#             i += 1

#         reviews.append(rev)

#     return reviews


# # ─────────────────────────────────────────────────────────────
# # STEP 3 — Derive sentiment from rating
# # ─────────────────────────────────────────────────────────────
# def assign_sentiment(rating: float) -> str:
#     if rating >= 4.0:
#         return 'Positive'
#     elif rating == 3.0:
#         return 'Neutral'
#     else:
#         return 'Negative'


# # ─────────────────────────────────────────────────────────────
# # STEP 4 — Post-process & enrich
# # ─────────────────────────────────────────────────────────────
# def post_process(df: pd.DataFrame) -> pd.DataFrame:
#     # Drop rows with no review text
#     df = df[df['review_text'].notna() & (df['review_text'].str.strip() != '')]

#     # Deduplicate on reviewer + text
#     df = df.drop_duplicates(subset=['reviewer_name', 'review_text'], keep='first')

#     # Add derived columns
#     df['sentiment']  = df['rating'].apply(assign_sentiment)
#     df['word_count'] = df['review_text'].apply(lambda x: len(str(x).split()))

#     # Clean reviewer name casing (ALL CAPS → Title Case)
#     df['reviewer_name'] = df['reviewer_name'].apply(
#         lambda x: x.title() if isinstance(x, str) and x.isupper() else x
#     )

#     df = df.reset_index(drop=True)
#     return df


# # ─────────────────────────────────────────────────────────────
# # MAIN PIPELINE
# # ─────────────────────────────────────────────────────────────
# def run(input_path: str, output_path: str) -> pd.DataFrame:
#     print('═' * 58)
#     print('  Flipkart Review Cleaner')
#     print('═' * 58)

#     raw_df = pd.read_csv(input_path)
#     print(f'\n[1] Loaded {len(raw_df)} raw blocks from  →  {input_path}')

#     all_reviews = []
#     for idx, row in raw_df.iterrows():
#         lines   = strip_boilerplate(row['raw_block'])
#         reviews = parse_reviews(lines)
#         all_reviews.extend(reviews)
#         print(f'    Block {idx:2d} → {len(reviews)} reviews extracted')

#     print(f'\n[2] Total extracted  : {len(all_reviews)}')

#     df = pd.DataFrame(all_reviews)
#     df = post_process(df)

#     print(f'[3] After dedup/clean: {len(df)} reviews')
#     print(f'[4] Saving to        : {os.path.abspath(output_path)}')
#     df.to_csv(output_path, index=False, encoding='utf-8-sig')

#     # ── Report ────────────────────────────────────────────────
#     print('\n' + '─' * 58)
#     print('  DATA QUALITY REPORT')
#     print('─' * 58)
#     print(f'  Total reviews      : {len(df)}')
#     print(f'  Verified Purchase  : {df["verified"].sum()} ({df["verified"].mean()*100:.1f}%)')
#     print(f'  Avg rating         : {df["rating"].mean():.2f}')
#     print(f'  Avg word count     : {df["word_count"].mean():.1f} words')
#     print(f'  Missing text       : {df["review_text"].isna().sum()}')
#     print(f'  Missing name       : {df["reviewer_name"].isna().sum()}')
#     print(f'  Missing city       : {df["reviewer_city"].isna().sum()}')
#     print(f'  Missing date       : {df["review_date"].isna().sum()}')

#     print(f'\n  Sentiment split:')
#     for s, c in df['sentiment'].value_counts().items():
#         bar = '█' * (c // 3)
#         print(f'    {s:<10} {c:4d}  {bar}')

#     print(f'\n  Rating distribution:')
#     for r, c in df['rating'].value_counts().sort_index().items():
#         bar = '█' * (c // 2)
#         print(f'    {r}★  {c:4d}  {bar}')

#     print(f'\n  Top 5 cities:')
#     for city, c in df['reviewer_city'].value_counts().head(5).items():
#         print(f'    {str(city):<35} {c}')

#     print('\n  Sample reviews:')
#     for _, r in df.head(3).iterrows():
#         print(f'\n  [{r["rating"]}★ | {r["sentiment"]}] "{r["title"]}"')
#         print(f'  Variant  : {r["review_for"]}')
#         print(f'  Text     : {str(r["review_text"])[:100]}...')
#         print(f'  Author   : {r["reviewer_name"]}, {r["reviewer_city"]}')
#         print(f'  Date     : {r["review_date"]}  | Verified: {r["verified"]}  | Helpful: {r["helpful_count"]}')

#     print('\n' + '─' * 58)
#     return df


# # ─────────────────────────────────────────────────────────────
# if __name__ == '__main__':
#     import sys
#     inp = sys.argv[1] if len(sys.argv) > 1 else INPUT_FILE
#     out = sys.argv[2] if len(sys.argv) > 2 else OUTPUT_FILE
#     run(inp, out)

import re
import os
import pandas as pd
from typing import Optional

INPUT_FILE  = "flipkart_blocks.csv"
OUTPUT_FILE = "flipkart_reviews_clean.csv"

RATING_VALUE    = re.compile(r'^\d\.\d$')
BULLET          = re.compile(r'^•$')
REVIEW_FOR      = re.compile(r'^Review for:\s*(.+)$')
CITY_LINE       = re.compile(r'^,\s*(.+)$')
HELPFUL_LINE    = re.compile(r'^Helpful for (\d+)$')
STANDALONE_INT  = re.compile(r'^\d+$')
VERIFIED_LINE   = re.compile(r'^Verified Purchase$')
DATE_LINE       = re.compile(r'^·\s*(.+)$')
TRUNCATED       = re.compile(r'\.{3}\s*more\s*$', re.IGNORECASE)
MULTI_SPACE     = re.compile(r'  +')
FOOTER_SENTINEL = 'Hang on, loading content'

HEADER_NOISE = {
    'Login', 'More', 'Cart', 'Overall', 'Fabric Quality', 'Colour',
    'Style', 'Comfort', 'True to Specs', 'Stitching Quality',
    'User reviews sorted by', 'Most Helpful', 'Latest',
    'Positive', 'Negative', '★', '•',
}

FOOTER_NOISE = {
    'ABOUT', 'Contact Us', 'About Us', 'Careers', 'Flipkart Stories',
    'Press', 'Corporate Information', 'GROUP COMPANIES', 'Myntra',
    'Cleartrip', 'Shopsy', 'HELP', 'Payments', 'Shipping',
    'Cancellation & Returns', 'FAQ', 'CONSUMER POLICY', 'Terms Of Use',
    'Security', 'Privacy', 'Sitemap', 'Grievance Redressal',
    'EPR Compliance', 'FSSAI Food Safety Connect App', 'Mail Us:',
    'Social:', 'Registered Office Address:', 'Become a Seller',
    'Advertise', 'Gift Cards', 'Help Center',
    'Flipkart Internet Private Limited,', 'Buildings Alyssa, Begonia &',
    'Clove Embassy Tech Village,',
    'Outer Ring Road, Devarabeesanahalli Village,',
    'Bengaluru, 560103,', 'Karnataka, India',
    'CIN : U51109KA2012PTC066107',
    'Telephone: 044-45614700 / 044-67415800',
    '© 2007-2026 Flipkart.com',
}

# ─────────────────────────────────────────────
def strip_boilerplate(raw: str) -> list[str]:
    lines = raw.split('\n')

    start = 0
    for i, line in enumerate(lines):
        if RATING_VALUE.match(line.strip()):
            start = i
            break

    end = len(lines)
    for i, line in enumerate(lines):
        if FOOTER_SENTINEL in line:
            end = i
            break

    return [
        ln for ln in lines[start:end]
        if ln.strip() not in FOOTER_NOISE
        and ln.strip() not in HEADER_NOISE
        and not re.match(r'^\d{1,3}(,\d{3})*$', ln.strip())
        and not re.match(r'^\d[\d,]+ ratings and \d[\d,]+ reviews$', ln.strip())
    ]

# ─────────────────────────────────────────────
def parse_reviews(lines: list[str]) -> list[dict]:
    reviews = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i].strip()

        if not RATING_VALUE.match(line):
            i += 1
            continue

        rev = {
            'rating':        float(line),
            'title':         None,
            'review_for':    None,
            'review_text':   None,
            'reviewer_name': None,
            'reviewer_city': None,
            'helpful_count': 0,
            'verified':      False,
            'review_date':   None,
        }
        i += 1

        if i < n and BULLET.match(lines[i].strip()):
            i += 1

        if i < n and lines[i].strip():
            rev['title'] = lines[i].strip()
            i += 1

        if i < n and REVIEW_FOR.match(lines[i].strip()):
            rev['review_for'] = REVIEW_FOR.match(lines[i].strip()).group(1).strip()
            i += 1

        body_lines = []
        while i < n:
            candidate = lines[i].strip()
            next_line = lines[i + 1].strip() if i + 1 < n else ''

            if (
                RATING_VALUE.match(candidate)
                or HELPFUL_LINE.match(candidate)
                or VERIFIED_LINE.match(candidate)
                or DATE_LINE.match(candidate)
                or CITY_LINE.match(candidate)
            ):
                break

            if CITY_LINE.match(next_line):
                break

            if candidate:
                body_lines.append(candidate)
            i += 1

        if body_lines:
            body = ' '.join(body_lines)
            body = TRUNCATED.sub('', body)
            body = MULTI_SPACE.sub(' ', body).strip()
            rev['review_text'] = body

        if i < n:
            candidate = lines[i].strip()
            if candidate and not any([
                CITY_LINE.match(candidate),
                HELPFUL_LINE.match(candidate),
                VERIFIED_LINE.match(candidate),
                DATE_LINE.match(candidate),
                RATING_VALUE.match(candidate),
            ]):
                rev['reviewer_name'] = MULTI_SPACE.sub(' ', candidate).strip()
                i += 1

        if i < n and CITY_LINE.match(lines[i].strip()):
            rev['reviewer_city'] = CITY_LINE.match(lines[i].strip()).group(1).strip()
            i += 1

        if i < n and HELPFUL_LINE.match(lines[i].strip()):
            rev['helpful_count'] = int(HELPFUL_LINE.match(lines[i].strip()).group(1))
            i += 1
            if i < n and STANDALONE_INT.match(lines[i].strip()):
                i += 1

        # 🔥 FIXED VERIFIED LOGIC (window check)
        for j in range(i, min(i + 3, n)):
            if VERIFIED_LINE.match(lines[j].strip()):
                rev['verified'] = True
                i = j + 1
                break

        if i < n and DATE_LINE.match(lines[i].strip()):
            rev['review_date'] = DATE_LINE.match(lines[i].strip()).group(1).strip()
            i += 1

        reviews.append(rev)

    return reviews

# ─────────────────────────────────────────────
def assign_sentiment(rating: float) -> str:
    if rating >= 4.0:
        return 'Positive'
    elif rating == 3.0:
        return 'Neutral'
    else:
        return 'Negative'

# ─────────────────────────────────────────────
def post_process(df: pd.DataFrame) -> pd.DataFrame:
    df = df[df['review_text'].notna() & (df['review_text'].str.strip() != '')]

    df = df.drop_duplicates(subset=['reviewer_name', 'review_text'], keep='first')

    df['sentiment']  = df['rating'].apply(assign_sentiment)
    df['word_count'] = df['review_text'].apply(lambda x: len(str(x).split()))

    df['reviewer_name'] = df['reviewer_name'].apply(
        lambda x: x.title() if isinstance(x, str) and x.isupper() else x
    )

    df = df.reset_index(drop=True)
    return df

# ─────────────────────────────────────────────
def run(input_path: str, output_path: str) -> pd.DataFrame:
    print('═' * 58)
    print('  Flipkart Review Cleaner')
    print('═' * 58)

    raw_df = pd.read_csv(input_path)
    print(f'\n[1] Loaded {len(raw_df)} raw blocks')

    all_reviews = []
    for idx, row in raw_df.iterrows():
        lines   = strip_boilerplate(row['raw_block'])
        reviews = parse_reviews(lines)
        all_reviews.extend(reviews)
        print(f'    Block {idx:2d} → {len(reviews)} reviews')

    df = pd.DataFrame(all_reviews)
    df = post_process(df)

    df.to_csv(output_path, index=False, encoding='utf-8-sig')

    print('\n' + '─' * 58)
    print(f'  Total reviews      : {len(df)}')
    print(f'  Verified Purchase  : {df["verified"].sum()} ({df["verified"].mean()*100:.1f}%)')

    return df

# ─────────────────────────────────────────────
if __name__ == '__main__':
    import sys
    inp = sys.argv[1] if len(sys.argv) > 1 else INPUT_FILE
    out = sys.argv[2] if len(sys.argv) > 2 else OUTPUT_FILE
    run(inp, out)