#!/usr/bin/env python3
"""
MysteryShop Site Generator
Generates all store pages, category pages, sitemap.xml, and robots.txt
"""

import os
import json
import re
from datetime import datetime

# ─── Load store data from JS file ───────────────────────────────────────────

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def read_js_stores():
    """Parse stores from JS file"""
    with open(os.path.join(BASE_DIR, 'js', 'stores.js'), 'r') as f:
        content = f.read()
    
    # Extract stores array using regex
    stores = []
    pattern = r'\{[^{}]+\}'
    matches = re.findall(pattern, content, re.DOTALL)
    
    for match in matches:
        try:
            # Convert JS object to valid JSON
            obj = match.strip()
            # Fix JS property format to JSON
            obj = re.sub(r'(\w+):', r'"\1":', obj)
            obj = re.sub(r'"\s*:\s*"([^"]+)"', r'": "\1"', obj)
            data = json.loads(obj)
            if 'slug' in data and 'name' in data:
                stores.append(data)
        except:
            pass
    return stores

CATEGORIES = {
    "tech": {"name": "Tech", "icon": "💻", "description": "Computers, gadgets, electronics, and all things digital."},
    "outdoor": {"name": "Outdoor & Sports", "icon": "🏔️", "description": "Gear for hiking, camping, cycling, and outdoor adventures."},
    "gifts": {"name": "Gifts & Novelty", "icon": "🎁", "description": "Unique, personalized, and thoughtful gifts for everyone."},
    "clothing": {"name": "Clothing & Fashion", "icon": "👕", "description": "Apparel, shoes, and accessories for every style."},
    "pets": {"name": "Pets", "icon": "🐾", "description": "Food, toys, and accessories for your beloved pets."},
    "gaming": {"name": "Gaming", "icon": "🎮", "description": "Video games, consoles, collectibles, and gaming gear."},
    "home": {"name": "Home & Kitchen", "icon": "🏠", "description": "Furniture, decor, cookware, and everything for your home."},
}

BASE_URL = "https://mysteryshop.com"
NAV = '''<nav>
  <div class="nav-inner">
    <div class="nav-logo"><a href="../index.html" style="color:inherit;text-decoration:none;">🎲 <span style="color:var(--primary)">Mystery</span>Shop</a></div>
    <div class="nav-links">
      <a href="../categories/">Browse Categories</a>
      <a href="../index.html#how-it-works">How It Works</a>
      <a href="../about.html">About</a>
    </div>
  </div>
</nav>'''

FOOTER = '''<footer>
  <div class="footer-inner">
    <div class="footer-links">
      <a href="../index.html">Home</a>
      <a href="../categories/">Categories</a>
      <a href="../sitemap.xml">Sitemap</a>
      <a href="../about.html">About</a>
      <a href="../privacy.html">Privacy Policy</a>
    </div>
    <p class="footer-disclosure">
      <strong>Affiliate Disclosure:</strong> MysteryShop.com is a participant in various affiliate advertising programs. 
      When you click links on this site and make a purchase, we may earn a small commission at no extra cost to you. 
      This helps us keep the lights on. Thank you for your support!
    </p>
    <p class="footer-copy">© 2025 MysteryShop. All rights reserved.</p>
  </div>
</footer>'''

HEAD_LINKS = '''  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../css/styles.css">'''

ADSENSE_COMMENT = '''  <!-- Google AdSense -->
  <!-- <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXXXXXXXX" crossorigin="anonymous"></script> -->'''

AD_SLOT = '''  <div class="ad-slot">
    <!-- Google AdSense 728x90 -->
    <!-- <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-XXXX" data-ad-slot="XXXX" data-ad-format="auto"></ins> -->
    Advertisement
  </div>'''

def build_store_structured_data(store):
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "ItemPage",
        "name": store['name'],
        "description": store['description'],
        "url": f"{BASE_URL}/stores/{store['slug']}.html",
        "mainEntity": {
            "@type": "Organization",
            "name": store['name'],
            "description": store['description'],
            "url": store['affiliate'],
            "sameAs": store['affiliate']
        }
    }, indent=2)

def generate_store_page(store, all_stores):
    cat = CATEGORIES[store['category']]
    # Related stores: same category, pick up to 4
    related = [s for s in all_stores if s['category'] == store['category'] and s['slug'] != store['slug']]
    import random
    related = random.sample(related, min(4, len(related)))
    
    related_cards = ''.join([f'''
    <div class="store-card">
      <div class="store-cat-badge">{cat["icon"]} {cat["name"]}</div>
      <div class="store-name">{s["name"]}</div>
      <div class="store-desc">{s["description"][:100]}...</div>
      <div class="store-price">💰 {s["priceRange"]}</div>
      <a href="{s["slug"]}.html">View Store →</a>
    </div>''' for s in related])

    tags_html = ' '.join([f'<span style="display:inline-block;background:var(--bg-card2);border:1px solid var(--border);border-radius:20px;padding:3px 12px;font-size:0.75rem;margin:3px;">{t}</span>' for t in store.get('tags', [])])

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{store["name"]} – Mystery Shop</title>
  <meta name="description" content="Discover {store["name"]} on Mystery Shop. {store["description"][:150]}">
  <meta property="og:title" content="{store["name"]} – Mystery Shop">
  <meta property="og:description" content="{store["description"][:200]}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{BASE_URL}/stores/{store["slug"]}.html">
  <meta name="twitter:card" content="summary">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{BASE_URL}/stores/{store["slug"]}.html">
{HEAD_LINKS}
{ADSENSE_COMMENT}
  <script type="application/ld+json">
{build_store_structured_data(store)}
  </script>
</head>
<body>

{NAV}

<div class="store-page">

  <nav class="breadcrumb">
    <a href="../index.html">Home</a>
    <span>›</span>
    <a href="../categories/{store["category"]}.html">{cat["name"]}</a>
    <span>›</span>
    {store["name"]}
  </nav>

  <div class="store-hero-badge">{cat["icon"]} {cat["name"]}</div>
  <h1>{store["name"]}</h1>
  <p class="store-desc-long">{store["description"]}</p>

  <div class="info-grid">
    <div class="info-box">
      <div class="info-label">Category</div>
      <div class="info-value">{cat["name"]}</div>
    </div>
    <div class="info-box">
      <div class="info-label">Price Range</div>
      <div class="info-value price">{store["priceRange"]}</div>
    </div>
  </div>

  <div style="margin-bottom:28px;">{tags_html}</div>

  <div class="btn-group">
    <a class="btn-visit" href="{store["affiliate"]}" target="_blank" rel="noopener nofollow sponsored">
      🛍️ Visit {store["name"]}
    </a>
    <a class="btn-another" href="../index.html" onclick="sessionStorage.setItem('excludeSlug','{store["slug"]}')">
      🎲 Try Another
    </a>
  </div>

  <!-- Ad Slot -->
  <div style="margin:32px 0;">{AD_SLOT}</div>

  <div class="related-section">
    <h2>More {cat["name"]} Stores</h2>
    <div class="store-grid">
      {related_cards}
    </div>
  </div>

  <div style="margin-top:40px;padding:20px;background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius);">
    <p style="font-size:0.8rem;color:var(--text-muted);">
      <strong>Affiliate Disclosure:</strong> The link above is an affiliate link. If you make a purchase, 
      MysteryShop may earn a small commission at no additional cost to you.
    </p>
  </div>

</div>

{FOOTER}

<script src="../js/stores.js"></script>
<script>
  // Try Another button with exclude
  document.querySelector('.btn-another').addEventListener('click', function(e) {{
    e.preventDefault();
    const store = getRandomStore('{store["slug"]}');
    window.location.href = store.slug + '.html';
  }});
</script>
</body>
</html>'''
    return html

def generate_category_page(cat_key, all_stores):
    cat = CATEGORIES[cat_key]
    stores = [s for s in all_stores if s['category'] == cat_key]
    
    store_cards = ''.join([f'''
    <div class="store-card">
      <div class="store-cat-badge">{cat["icon"]} {cat["name"]}</div>
      <div class="store-name">{s["name"]}</div>
      <div class="store-desc">{s["description"]}</div>
      <div class="store-price">💰 {s["priceRange"]}</div>
      <a href="../stores/{s["slug"]}.html">View Store →</a>
    </div>''' for s in stores])

    schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": f"{cat['name']} Stores – Mystery Shop",
        "description": cat['description'],
        "url": f"{BASE_URL}/categories/{cat_key}.html",
        "numberOfItems": len(stores)
    }, indent=2)

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{cat["name"]} Stores – Mystery Shop</title>
  <meta name="description" content="Browse {len(stores)} {cat["name"].lower()} stores on Mystery Shop. {cat["description"]}">
  <meta property="og:title" content="{cat["name"]} Stores – Mystery Shop">
  <meta property="og:description" content="{cat["description"]}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{BASE_URL}/categories/{cat_key}.html">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{BASE_URL}/categories/{cat_key}.html">
{HEAD_LINKS}
{ADSENSE_COMMENT}
  <script type="application/ld+json">
{schema}
  </script>
</head>
<body>

{NAV}

<div class="cat-page-header">
  <div class="cat-page-icon">{cat["icon"]}</div>
  <h1>{cat["name"]} Stores</h1>
  <p>{cat["description"]} — {len(stores)} stores to explore.</p>
</div>

<div class="section">
  <nav class="breadcrumb">
    <a href="../index.html">Home</a>
    <span>›</span>
    <a href="./">Categories</a>
    <span>›</span>
    {cat["name"]}
  </nav>

  {AD_SLOT}

  <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:24px;flex-wrap:wrap;gap:12px;">
    <div>
      <h2 class="section-title">All {cat["name"]} Stores</h2>
      <p class="section-sub">{len(stores)} stores • Click any to learn more</p>
    </div>
    <button onclick="goRandomCategory()" style="background:linear-gradient(135deg,var(--primary),var(--accent));color:white;border:none;padding:12px 24px;border-radius:50px;font-size:0.95rem;font-weight:700;cursor:pointer;">
      🎲 Random {cat["name"]} Store
    </button>
  </div>

  <div class="store-grid">
    {store_cards}
  </div>
</div>

<div style="max-width:1100px;margin:0 auto;padding:0 24px 40px;">
  {AD_SLOT}
</div>

{FOOTER}

<script src="../js/stores.js"></script>
<script>
function goRandomCategory() {{
  const stores = getStoresByCategory('{cat_key}');
  const store = stores[Math.floor(Math.random() * stores.length)];
  window.location.href = '../stores/' + store.slug + '.html';
}}
</script>
</body>
</html>'''
    return html

def generate_categories_index(all_stores):
    cat_cards = ''
    for key, cat in CATEGORIES.items():
        count = len([s for s in all_stores if s['category'] == key])
        cat_cards += f'''
    <a class="cat-card" href="{key}.html" style="padding:28px 20px;">
      <div class="cat-icon" style="font-size:2.5rem;">{cat["icon"]}</div>
      <div class="cat-name" style="font-size:1rem;">{cat["name"]}</div>
      <div style="color:var(--text-muted);font-size:0.85rem;margin-top:6px;">{cat["description"][:60]}...</div>
      <div class="cat-count" style="margin-top:10px;font-weight:700;color:var(--primary);">{count} stores</div>
    </a>'''

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Browse All Categories – Mystery Shop</title>
  <meta name="description" content="Browse all {len(all_stores)} stores across 7 categories on Mystery Shop: tech, outdoor, gifts, clothing, pets, gaming, and home.">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{BASE_URL}/categories/">
{HEAD_LINKS}
{ADSENSE_COMMENT}
</head>
<body>

{NAV}

<div class="section" style="padding-top:50px;">
  <nav class="breadcrumb">
    <a href="../index.html">Home</a>
    <span>›</span>
    Categories
  </nav>
  <h1 class="section-title">Browse All Categories</h1>
  <p class="section-sub">Explore {len(all_stores)} stores across 7 categories — or <a href="../index.html">roll the dice</a> for a random one.</p>

  <div class="cat-grid" style="grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:20px;margin-top:32px;">
    {cat_cards}
  </div>
</div>

{FOOTER}
</body>
</html>'''
    return html

def generate_sitemap(all_stores):
    today = datetime.now().strftime('%Y-%m-%d')
    urls = [
        f'  <url><loc>{BASE_URL}/</loc><lastmod>{today}</lastmod><changefreq>daily</changefreq><priority>1.0</priority></url>',
        f'  <url><loc>{BASE_URL}/categories/</loc><lastmod>{today}</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>',
    ]
    for key in CATEGORIES:
        urls.append(f'  <url><loc>{BASE_URL}/categories/{key}.html</loc><lastmod>{today}</lastmod><changefreq>weekly</changefreq><priority>0.7</priority></url>')
    for store in all_stores:
        urls.append(f'  <url><loc>{BASE_URL}/stores/{store["slug"]}.html</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>0.6</priority></url>')
    
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>'''

def main():
    # Hardcode stores since parsing JS is complex — use the actual store data
    import subprocess
    result = subprocess.run(['node', '-e', '''
const fs = require('fs');
eval(fs.readFileSync('js/stores.js','utf8'));
console.log(JSON.stringify(STORES));
'''], capture_output=True, text=True, cwd=BASE_DIR)
    
    stores = json.loads(result.stdout)
    print(f"Loaded {len(stores)} stores")

    # Create dirs
    os.makedirs(os.path.join(BASE_DIR, 'stores'), exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, 'categories'), exist_ok=True)

    # Generate store pages
    for store in stores:
        path = os.path.join(BASE_DIR, 'stores', f'{store["slug"]}.html')
        with open(path, 'w') as f:
            f.write(generate_store_page(store, stores))
    print(f"Generated {len(stores)} store pages")

    # Generate category pages
    for cat_key in CATEGORIES:
        path = os.path.join(BASE_DIR, 'categories', f'{cat_key}.html')
        with open(path, 'w') as f:
            f.write(generate_category_page(cat_key, stores))
    print(f"Generated {len(CATEGORIES)} category pages")

    # Category index
    with open(os.path.join(BASE_DIR, 'categories', 'index.html'), 'w') as f:
        f.write(generate_categories_index(stores))
    print("Generated categories index")

    # Sitemap
    with open(os.path.join(BASE_DIR, 'sitemap.xml'), 'w') as f:
        f.write(generate_sitemap(stores))
    print("Generated sitemap.xml")

    # Robots.txt
    with open(os.path.join(BASE_DIR, 'robots.txt'), 'w') as f:
        f.write(f"""User-agent: *
Allow: /

Sitemap: {BASE_URL}/sitemap.xml

Disallow: /api/
""")
    print("Generated robots.txt")

    print(f"\n✅ Site generation complete! {len(stores)} stores, {len(CATEGORIES)} categories")
    print(f"Total pages: {len(stores) + len(CATEGORIES) + 3} (stores + categories + home/about/privacy)")

if __name__ == '__main__':
    main()
