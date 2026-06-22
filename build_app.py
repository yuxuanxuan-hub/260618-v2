"""Build consolidated islandtrace-app.html from source pages."""
import re
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "islandtrace-app.html"

# Shared nav (index style) — 常見問題 per user link spec
NAV = """<nav id="site-nav">
  <div class="nav-logo" data-go="index" role="link" tabindex="0">島嶼旅跡</div>
  <ul class="nav-links">
    <li><a href="#" data-go="products">探索體驗</a></li>
    <li><a href="#" data-go="about">關於我們</a></li>
    <li><a href="#" data-go="faq">常見問題</a></li>
    <li><a href="#" data-go="profile">我的訂單</a></li>
    <li><a href="#" class="nav-cta" data-go="login">登入／註冊</a></li>
  </ul>
</nav>"""

FOOTER = """<footer id="site-footer">
  <div class="footer-grid">
    <div class="footer-brand">
      <div class="logo">島嶼旅跡</div>
      <p>深入台灣每一個小鎮，<br>感受在地的真實故事。<br>跟著在地嚮導，<br>與那片土地上真實相遇。</p>
    </div>
    <div class="footer-col">
      <h4>探索</h4>
      <ul>
        <li><a href="#" data-go="products">所有體驗</a></li>
        <li><a href="#" data-go="products" data-theme="戶外">戶外登頂</a></li>
        <li><a href="#" data-go="products" data-theme="手作">手作工藝</a></li>
        <li><a href="#" data-go="products" data-theme="美食">美食料理</a></li>
        <li><a href="#" data-go="products" data-theme="文化">文化歷史</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>公司</h4>
      <ul>
        <li><a href="#" data-go="about">關於我們</a></li>
        <li><a href="#" data-go="faq">常見問答</a></li>
        <li><a href="#" data-go="index">加盟嚮導申請</a></li>
        <li><a href="#" data-go="index">媒體合作</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>支援</h4>
      <ul>
        <li><a href="#" data-go="index">退換政策</a></li>
        <li><a href="#" data-go="index">隱私政策</a></li>
        <li><a href="#" data-go="index">服務條款</a></li>
        <li><a href="#" data-go="profile">查看訂單</a></li>
      </ul>
    </div>
  </div>
  <div class="footer-bottom">
    <p>© 2025 島嶼旅跡 IslandTrace. All rights reserved.</p>
    <a href="#" data-go="index">用心定義台灣，一寸土地。</a>
  </div>
</footer>"""

ROUTER_JS = r"""
/* ===== Router ===== */
const App = {
  page: 'index',
  init() {
    document.body.addEventListener('click', e => {
      const el = e.target.closest('[data-go]');
      if (!el) return;
      e.preventDefault();
      const theme = el.dataset.theme || null;
      this.go(el.dataset.go, theme);
    });
    document.querySelector('.nav-logo')?.addEventListener('keydown', e => {
      if (e.key === 'Enter') this.go('index');
    });
    document.querySelectorAll('#view-products .card[data-theme]').forEach(card => {
      card.addEventListener('click', e => {
        if (e.target.closest('.card-fav')) return;
        this.go('detail');
      });
    });
    document.getElementById('btn-book-now')?.addEventListener('click', () => this.go('booking'));
    document.getElementById('btn-success-home')?.addEventListener('click', () => this.go('index'));
    document.getElementById('btn-success-orders')?.addEventListener('click', () => this.go('profile'));
    document.querySelectorAll('[data-go-products]').forEach(el => {
      el.addEventListener('click', e => { e.preventDefault(); this.go('products'); });
    });
    if (typeof initCalendar === 'function') initCalendar();
    if (typeof initAboutReveal === 'function') initAboutReveal();
    if (typeof initFaq === 'function') initFaq();
    if (typeof updateQtyDisplay === 'function') updateQtyDisplay();
  },
  go(page, theme) {
    this.page = page;
    document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
    const view = document.getElementById('view-' + page);
    if (view) view.classList.add('active');
    const login = page === 'login';
    document.getElementById('site-nav').hidden = login;
    document.getElementById('site-footer').hidden = login;
    document.querySelectorAll('.nav-links a:not(.nav-cta)').forEach(a => {
      a.classList.toggle('active', a.dataset.go === page);
    });
    window.scrollTo(0, 0);
    if (page === 'products' && theme) applyThemeFilter(theme);
    if (page === 'booking') showBookingStep('page-step1');
  }
};
document.addEventListener('DOMContentLoaded', () => App.init());
"""

def extract_style(html: str) -> str:
    m = re.search(r'<style>(.*?)</style>', html, re.DOTALL)
    return m.group(1).strip() if m else ""

def extract_body(html: str) -> str:
    m = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL | re.IGNORECASE)
    return m.group(1).strip() if m else ""

def strip_nav_footer(body: str) -> str:
    body = re.sub(r'<!--\s*=+\s*NAV.*?-->\s*<nav[\s\S]*?</nav>', '', body, flags=re.I)
    body = re.sub(r'<nav[\s\S]*?</nav>', '', body, count=1)
    body = re.sub(r'<!--\s*=+\s*FOOTER.*?-->\s*<footer[\s\S]*?</footer>', '', body, flags=re.I)
    body = re.sub(r'<footer[\s\S]*?</footer>', '', body, count=1)
    return body.strip()

def strip_scripts(body: str) -> str:
    return re.sub(r'<script[\s\S]*?</script>', '', body, flags=re.I).strip()

def fix_index_body(body: str) -> str:
    body = body.replace('class="view-all">查看全部 →</a>', 'class="view-all" data-go="products">查看全部 →</a>')
    body = body.replace('class="btn-primary">立即申請嚮導</button>', 'class="btn-primary" data-go="index">立即申請嚮導</button>')
    body = body.replace('class="btn-outline">了解更多</button>', 'class="btn-outline" data-go="about">了解更多</button>')
    return body

def fix_products_body(body: str) -> str:
    body = re.sub(r'<a href="index\.html"[^>]*>', '<a href="#" data-go="index">', body)
    body = strip_scripts(body)
    return body

def fix_detail_body(body: str) -> str:
    body = re.sub(r'<a href="index\.html"[^>]*>', '<a href="#" data-go="index">', body)
    body = body.replace('onclick="bookNow()"', 'id="btn-book-now"')
    body = re.sub(r'<script[\s\S]*?</script>', '', body, flags=re.I)
    return body

def fix_booking_body(body: str) -> str:
    body = strip_nav_footer(body)
    body = strip_scripts(body)
    body = body.replace('class="booking-body single"', 'class="booking-body"')
    body = body.replace("onclick=\"alert('返回首頁（待接入 index.html）')\"", 'id="btn-success-home"')
    body = body.replace("onclick=\"alert('查看我的訂單（待接入訂單頁）')\"", 'id="btn-success-orders"')
    return body

def fix_about_body(body: str) -> str:
    body = body.replace('class="btn-primary">探索所有體驗</a>', 'class="btn-primary" data-go="products">探索所有體驗</a>')
    body = strip_scripts(body)
    return body

def fix_profile_body(body: str) -> str:
    body = body.replace('function switchTab(tab)', 'function switchProfileTab(tab)')
    body = body.replace("onclick=\"switchTab('orders')\"", "onclick=\"switchProfileTab('orders')\"")
    body = body.replace("onclick=\"switchTab('favorites')\"", "onclick=\"switchProfileTab('favorites')\"")
    body = body.replace("onclick=\"switchTab('profile')\"", "onclick=\"switchProfileTab('profile')\"")
    return body

def fix_login_body(body: str) -> str:
    body = strip_scripts(body)
    return body

# Page-specific CSS scoping prefixes for conflicting rules
PAGE_CSS = {
    'index': extract_style((ROOT / 'index.html').read_text(encoding='utf-8')),
    'products': extract_style((ROOT / 'products.html').read_text(encoding='utf-8')),
    'about': extract_style((ROOT / 'about.html').read_text(encoding='utf-8')),
    'faq': extract_style((ROOT / 'faq.html').read_text(encoding='utf-8')),
    'profile': extract_style((ROOT / 'profile-1.html').read_text(encoding='utf-8')),
    'login': extract_style((ROOT / 'login.html').read_text(encoding='utf-8')),
    'detail': extract_style((ROOT / 'product-detail.html').read_text(encoding='utf-8')),
    'booking': extract_style((ROOT / 'booking.html').read_text(encoding='utf-8')),
}

# Merge: use index as base, append unique page rules (simplified - prefix view scopes)
BASE_CSS = PAGE_CSS['index']
EXTRA_CSS = """

/* ===== SPA shell ===== */
.view { display: none; }
.view.active { display: block; }
body.login-mode { overflow: hidden; }
#view-login { min-height: 100vh; }
.nav-links a.active { color: #fff; font-weight: 500; }
.nav-logo { cursor: pointer; }

/* ===== Products (from products.html, deduped nav/footer) ===== */
.breadcrumb { margin-top: 60px; padding: 14px 48px; background: var(--warm-white); border-bottom: 1px solid var(--border); display: flex; align-items: center; gap: 8px; font-size: 12px; color: var(--text-muted); }
.breadcrumb a { color: var(--text-muted); } .breadcrumb a:hover { color: var(--orange); }
.breadcrumb .sep { color: var(--border); } .breadcrumb .current { color: var(--text-main); }
.explore-wrapper { display: flex; max-width: 1280px; margin: 0 auto; padding: 32px 48px 80px; align-items: flex-start; }
.filter-sidebar { width: 220px; flex-shrink: 0; position: sticky; top: 76px; padding-right: 32px; }
.filter-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px; }
.filter-header h2 { font-family: var(--serif); font-size: 15px; font-weight: 700; }
.filter-clear { font-size: 12px; color: var(--orange); cursor: pointer; background: none; border: none; font-family: var(--sans); }
.filter-section { margin-bottom: 24px; padding-bottom: 24px; border-bottom: 1px solid var(--border); }
.filter-section:last-child { border-bottom: none; }
.filter-section-title { font-size: 12px; font-weight: 600; margin-bottom: 12px; }
.tag-group { display: flex; flex-wrap: wrap; gap: 8px; }
.tag-btn { padding: 5px 12px; border: 1.5px solid var(--border); border-radius: 20px; font-size: 12px; font-family: var(--sans); background: #fff; cursor: pointer; transition: all .18s; }
.tag-btn:hover { border-color: var(--orange); color: var(--orange); }
.tag-btn.active { background: var(--orange); border-color: var(--orange); color: #fff; }
.tag-btn.has-icon { display: flex; align-items: center; gap: 5px; }
.price-range { display: flex; align-items: center; gap: 8px; }
.price-input { flex: 1; min-width: 0; padding: 7px 10px; border: 1.5px solid var(--border); border-radius: 8px; font-size: 12px; font-family: var(--sans); outline: none; }
.explore-main { flex: 1; min-width: 0; }
.explore-toolbar { display: flex; align-items: center; justify-content: space-between; margin-bottom: 24px; }
.result-count { font-size: 13px; color: var(--text-muted); }
.sort-select { padding: 7px 32px 7px 12px; border: 1.5px solid var(--border); border-radius: 8px; font-size: 12px; font-family: var(--sans); appearance: none; outline: none; cursor: pointer; }
#view-products .cards-grid { grid-template-columns: repeat(3, 1fr); }
#view-products .card { border: 1px solid var(--border); }
.card-fav.liked { color: var(--orange); }

/* ===== About ===== */
.about-hero { background: var(--navy); padding: 120px 72px 72px; position: relative; overflow: hidden; min-height: 300px; display: flex; align-items: center; }
.about-hero-decoration { position: absolute; right: 80px; top: 50%; transform: translateY(-50%); width: 280px; height: 280px; border-radius: 50%; background: rgba(60,40,60,.55); pointer-events: none; }
.about-hero-content { position: relative; z-index: 2; max-width: 560px; }
.about-hero h1 { font-family: var(--serif); font-size: clamp(36px,4.5vw,54px); font-weight: 900; color: #fff; line-height: 1.25; margin-bottom: 20px; }
.about-hero h1 .accent { color: var(--orange); }
.about-hero p { font-size: 13px; color: rgba(255,255,255,.65); line-height: 1.9; max-width: 420px; }
.brand-story { padding: 80px 72px; background: #fff; }
.brand-story-inner { display: grid; grid-template-columns: 1fr 1.1fr; gap: 72px; align-items: center; }
.brand-story-img { border-radius: 12px; overflow: hidden; aspect-ratio: 4/3; }
.brand-story-img img { width: 100%; height: 100%; object-fit: cover; display: block; }
.brand-story-text h2 { font-family: var(--serif); font-size: clamp(24px,2.6vw,32px); font-weight: 900; margin-bottom: 24px; }
.brand-story-text p { font-size: 13px; color: #555; line-height: 1.9; margin-bottom: 14px; }
.core-values { background: var(--warm-white); padding: 80px 72px; }
.values-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 24px; }
.value-card { background: #fff; border-radius: 14px; padding: 28px 24px; border: 1.5px solid var(--border); }
.value-icon { font-size: 28px; margin-bottom: 16px; display: block; }
.value-card h3 { font-family: var(--serif); font-size: 16px; font-weight: 700; margin-bottom: 12px; }
.value-card p { font-size: 12px; color: #666; line-height: 1.85; }
.team-section { padding: 80px 72px; background: #fff; }
.team-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 20px; }
.team-card { position: relative; border-radius: 12px; overflow: hidden; aspect-ratio: 3/4; cursor: pointer; }
.team-card img { width: 100%; height: 100%; object-fit: cover; filter: grayscale(20%); transition: transform .35s, filter .35s; }
.team-card:hover img { transform: scale(1.04); filter: grayscale(0); }
.team-card-overlay { position: absolute; inset: 0; background: linear-gradient(to top, rgba(20,20,40,.75) 0%, transparent 55%); }
.team-card-info { position: absolute; bottom: 0; left: 0; right: 0; padding: 16px; }
.team-card-role { font-size: 10px; color: var(--orange); letter-spacing: .08em; margin-bottom: 4px; }
.team-card-name { font-family: var(--serif); font-size: 15px; font-weight: 700; color: #fff; }
.numbers-section { background: var(--navy); padding: 72px; }
.numbers-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 40px; }
.number-value { font-family: var(--serif); font-size: clamp(40px,5vw,60px); font-weight: 900; color: #fff; line-height: 1; margin-bottom: 10px; }
.number-value .accent { color: var(--orange); }
.number-label { font-size: 12px; color: rgba(255,255,255,.5); }
.reveal { opacity: 0; transform: translateY(24px); transition: opacity .55s ease, transform .55s ease; }
.reveal.visible { opacity: 1; transform: translateY(0); }

/* ===== FAQ ===== */
#view-faq { display: flex; flex-direction: column; min-height: calc(100vh - 60px); }
#view-faq.active { display: flex; }
.faq-hero { background: var(--warm-white); text-align: center; padding: 64px 72px 56px; border-bottom: 1px solid var(--border); margin-top: 60px; }
.faq-hero-eyebrow { display: flex; align-items: center; justify-content: center; gap: 10px; font-size: 11px; color: var(--orange); letter-spacing: .12em; text-transform: uppercase; margin-bottom: 16px; }
.faq-hero-eyebrow::before, .faq-hero-eyebrow::after { content: ''; display: block; width: 32px; height: 1.5px; background: var(--orange); }
.faq-hero h1 { font-family: var(--serif); font-size: clamp(28px,4vw,40px); font-weight: 900; margin-bottom: 12px; }
.faq-content { flex: 1; max-width: 800px; margin: 0 auto; padding: 56px 24px 80px; width: 100%; }
.faq-tabs { display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 40px; }
.tab-btn { padding: 9px 20px; border-radius: 24px; border: 1.5px solid var(--border); background: #fff; font-size: 13px; font-family: var(--sans); cursor: pointer; transition: all .2s; }
.tab-btn.active { background: var(--orange); border-color: var(--orange); color: #fff; font-weight: 500; }
.faq-section { display: none; } .faq-section.active { display: block; }
.faq-section-title { display: flex; align-items: center; gap: 8px; font-family: var(--serif); font-size: 16px; font-weight: 700; margin-bottom: 20px; padding-bottom: 16px; border-bottom: 1.5px solid var(--border); }
.accordion-item { border-bottom: 1px solid var(--border); }
.accordion-header { display: flex; align-items: center; justify-content: space-between; padding: 18px 0; cursor: pointer; gap: 16px; }
.accordion-header.open .accordion-question { color: var(--orange); }
.accordion-question { font-size: 14px; transition: color .2s; }
.accordion-icon { width: 26px; height: 26px; border-radius: 50%; border: 1.5px solid var(--border); display: flex; align-items: center; justify-content: center; flex-shrink: 0; font-size: 16px; color: var(--text-muted); }
.accordion-header.open .accordion-icon { background: var(--orange); border-color: var(--orange); color: #fff; }
.accordion-body { display: none; padding: 0 0 20px; } .accordion-body.open { display: block; }
.accordion-body p { font-size: 13px; color: var(--text-muted); line-height: 1.9; }
.contact-card { background: var(--warm-white); border: 1.5px solid var(--border); border-radius: 16px; padding: 40px 32px; text-align: center; margin-top: 52px; }
.contact-card h3 { font-family: var(--serif); font-size: 20px; font-weight: 700; margin-bottom: 10px; }
.contact-actions { display: flex; justify-content: center; gap: 14px; flex-wrap: wrap; }
.btn-outline-dark { background: transparent; color: var(--text-main); border: 1.5px solid var(--border); border-radius: 28px; padding: 11px 26px; font-size: 13px; font-family: var(--sans); cursor: pointer; }

/* ===== Profile ===== */
.profile-page { padding-top: 60px; min-height: 100vh; background: var(--warm-white); }
.profile-container { max-width: 1080px; margin: 0 auto; padding: 40px 32px; display: grid; grid-template-columns: 220px 1fr; gap: 28px; align-items: start; }
.sidebar { background: #fff; border-radius: 16px; border: 1px solid var(--border); overflow: hidden; }
.profile-card { padding: 32px 20px 24px; text-align: center; border-bottom: 1px solid var(--border); }
.avatar-wrap { position: relative; display: inline-block; margin-bottom: 14px; }
.avatar { width: 76px; height: 76px; border-radius: 50%; object-fit: cover; border: 3px solid #fff; box-shadow: 0 2px 12px rgba(0,0,0,.14); }
.avatar-edit { position: absolute; bottom: 2px; right: 2px; width: 22px; height: 22px; background: var(--orange); border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer; font-size: 10px; color: #fff; }
.profile-name { font-family: var(--serif); font-size: 16px; font-weight: 700; margin-bottom: 4px; }
.profile-email { font-size: 11px; color: var(--text-muted); margin-bottom: 14px; }
.member-badge { display: inline-flex; align-items: center; gap: 5px; background: #fff9f0; border: 1.5px solid #f5d89e; border-radius: 20px; padding: 4px 12px; font-size: 11px; color: #b07d1a; }
.sidebar-menu { padding: 8px 0; }
.menu-item { display: flex; align-items: center; gap: 11px; padding: 13px 20px; font-size: 13px; cursor: pointer; border-left: 3px solid transparent; transition: background .15s, color .15s; }
.menu-item:hover { background: var(--warm-white); color: var(--orange); }
.menu-item.active { background: #fef4f0; color: var(--orange); font-weight: 500; border-left-color: var(--orange); }
.menu-item.logout { color: var(--text-muted); margin-top: 4px; border-top: 1px solid var(--border); }
.content-title { font-family: var(--serif); font-size: 20px; font-weight: 700; margin-bottom: 20px; }
.order-table-wrap { background: #fff; border-radius: 16px; border: 1px solid var(--border); overflow: hidden; }
.order-table-head, .order-row { display: grid; grid-template-columns: 2.8fr 1.4fr 1.2fr 1fr 1.2fr; padding: 14px 20px; align-items: center; }
.order-table-head { border-bottom: 1px solid var(--border); font-size: 12px; color: var(--text-muted); font-weight: 500; }
.order-row { padding: 18px 20px; border-bottom: 1px solid var(--border); }
.order-exp { display: flex; align-items: center; gap: 12px; }
.order-exp-img { width: 52px; height: 42px; border-radius: 8px; object-fit: cover; flex-shrink: 0; }
.order-exp-name { font-size: 13px; font-weight: 600; margin-bottom: 3px; }
.order-exp-location { display: flex; align-items: center; gap: 4px; font-size: 11px; color: var(--text-muted); }
.location-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--orange); }
.order-price { font-size: 13px; font-weight: 600; color: var(--orange); }
.status-badge { display: inline-flex; padding: 5px 12px; border-radius: 20px; font-size: 11px; font-weight: 500; }
.status-badge.upcoming { background: #fef0ef; color: #E63329; border: 1px solid #f5c0bc; }
.status-badge.completed { background: #edf7f2; color: #3DAA6E; border: 1px solid #b8e4cc; }
.btn-cancel { padding: 7px 14px; border-radius: 20px; border: 1.5px solid var(--orange); background: #fff; color: var(--orange); font-size: 12px; font-weight: 500; font-family: var(--sans); cursor: pointer; }

/* ===== Login ===== */
#view-login .page { display: grid; grid-template-columns: 1fr 1fr; min-height: 100vh; }
#view-login .hero { position: relative; overflow: hidden; }
#view-login .hero__photo { position: absolute; inset: 0; background: linear-gradient(to bottom,rgba(0,0,0,.25),rgba(0,0,0,.55)), url('https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=1200&q=80') center/cover; }
#view-login .hero__logo { position: absolute; top: 32px; left: 32px; font-family: var(--serif); font-size: 18px; font-weight: 700; color: #fff; }
#view-login .hero__copy { position: absolute; bottom: 56px; left: 40px; right: 40px; }
#view-login .hero__tagline { font-family: var(--serif); font-size: clamp(28px,3.5vw,44px); font-weight: 700; color: #fff; line-height: 1.4; margin-bottom: 12px; }
#view-login .hero__tagline .accent { color: #F26522; }
#view-login .form-panel { background: #fff; display: flex; align-items: center; justify-content: center; padding: 60px 40px; }
#view-login .form-inner { width: 100%; max-width: 360px; }
#view-login .tabs { display: grid; grid-template-columns: 1fr 1fr; background: #f5f5f5; border-radius: 12px; padding: 4px; margin-bottom: 36px; }
#view-login .tab { border: none; background: transparent; border-radius: 9px; padding: 10px; font-family: var(--sans); font-size: 15px; color: #888; cursor: pointer; }
#view-login .tab.active { background: #fff; color: #1a1a1a; box-shadow: 0 1px 4px rgba(0,0,0,.12); }
#view-login .field { margin-bottom: 18px; }
#view-login .field label { display: block; font-size: 13px; font-weight: 500; margin-bottom: 6px; }
#view-login .input-wrap input { width: 100%; border: 1.5px solid #e0e0e0; border-radius: 10px; padding: 12px 44px 12px 14px; font-size: 14px; font-family: var(--sans); outline: none; }
#view-login .btn-primary { width: 100%; background: #E63329; color: #fff; border: none; border-radius: 10px; padding: 14px; font-size: 16px; font-weight: 700; font-family: var(--sans); cursor: pointer; margin-top: 24px; }
#view-login .btn-social { width: 100%; display: flex; align-items: center; justify-content: center; gap: 10px; border: 1.5px solid #e0e0e0; border-radius: 10px; padding: 12px; font-size: 14px; background: #fff; cursor: pointer; margin-bottom: 10px; }
#view-login .divider { display: flex; align-items: center; gap: 12px; margin: 20px 0; color: #888; font-size: 12px; }
#view-login .divider::before, #view-login .divider::after { content: ''; flex: 1; height: 1px; background: #e0e0e0; }

/* ===== Detail ===== */
.detail-wrapper { display: flex; gap: 48px; max-width: 1280px; margin: 0 auto; padding: 32px 48px 80px; align-items: flex-start; }
.detail-main { flex: 1; min-width: 0; }
.gallery-main { width: 100%; height: 440px; border-radius: 16px; overflow: hidden; background: #ddd; margin-bottom: 14px; }
.gallery-main img { width: 100%; height: 100%; object-fit: cover; }
.gallery-thumbs { display: flex; gap: 12px; margin-bottom: 32px; }
.thumb { width: 100px; height: 76px; border-radius: 10px; overflow: hidden; cursor: pointer; border: 2px solid transparent; opacity: .75; }
.thumb.active { border-color: var(--orange); opacity: 1; }
.thumb img { width: 100%; height: 100%; object-fit: cover; }
.product-title { font-family: var(--serif); font-size: 28px; font-weight: 700; margin-bottom: 12px; }
.product-meta { display: flex; align-items: center; gap: 16px; font-size: 13px; color: var(--text-muted); padding-bottom: 24px; margin-bottom: 28px; border-bottom: 1px solid var(--border); flex-wrap: wrap; }
.detail-section { margin-bottom: 36px; }
.detail-section .section-title { font-family: var(--serif); font-size: 18px; font-weight: 700; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid var(--border); }
.section-desc { font-size: 13.5px; line-height: 1.9; }
.highlight-list { list-style: none; }
.highlight-list li { display: flex; gap: 10px; padding: 10px 0; font-size: 13.5px; border-bottom: 1px solid var(--border); }
.highlight-list .hl-icon { color: var(--orange); flex-shrink: 0; }
.fee-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
.fee-box { background: var(--cream); border-radius: 12px; padding: 20px 22px; }
.fee-box h4 { font-size: 13px; font-weight: 600; margin-bottom: 14px; }
.fee-box.included h4 { color: #2E7D4F; } .fee-box.excluded h4 { color: #C0392B; }
.fee-box ul { list-style: none; } .fee-box li { font-size: 12.5px; margin-bottom: 9px; padding-left: 14px; position: relative; }
.fee-box li::before { content: '•'; position: absolute; left: 0; color: var(--text-muted); }
.review { display: flex; gap: 14px; padding: 20px 0; border-bottom: 1px solid var(--border); }
.review-avatar { width: 42px; height: 42px; border-radius: 50%; object-fit: cover; flex-shrink: 0; }
.review-name { font-weight: 600; font-size: 13.5px; }
.review-date { font-size: 11px; color: var(--text-muted); margin-left: 8px; }
.review-stars { color: var(--star); font-size: 12px; margin: 5px 0 8px; }
.review-text { font-size: 13px; line-height: 1.8; }
.booking-card { width: 340px; flex-shrink: 0; position: sticky; top: 84px; background: #fff; border: 1px solid var(--border); border-radius: 16px; padding: 28px; box-shadow: 0 6px 24px rgba(0,0,0,.08); }
.price-now { font-family: var(--serif); font-size: 26px; font-weight: 700; }
.price-unit { font-size: 12px; color: var(--text-muted); }
.rating-row { display: flex; align-items: center; gap: 6px; font-size: 13px; margin: 10px 0 20px; padding-bottom: 20px; border-bottom: 1px solid var(--border); color: var(--text-muted); }
.qty-row { display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px; font-size: 13px; font-weight: 500; }
.qty-control { display: flex; align-items: center; gap: 14px; }
.qty-btn { width: 28px; height: 28px; border-radius: 50%; border: 1.5px solid var(--border); background: #fff; font-size: 16px; cursor: pointer; display: flex; align-items: center; justify-content: center; font-family: var(--sans); }
.qty-btn:disabled { opacity: .4; cursor: not-allowed; }
.qty-num { font-size: 15px; font-weight: 600; min-width: 18px; text-align: center; }
.total-row { display: flex; align-items: center; justify-content: space-between; margin-bottom: 22px; padding-top: 20px; border-top: 1px solid var(--border); font-size: 13px; font-weight: 500; }
.total-amount { font-family: var(--serif); font-size: 19px; font-weight: 700; color: var(--orange); }
.book-btn { width: 100%; padding: 14px; background: var(--orange); color: #fff; border: none; border-radius: 30px; font-size: 14px; font-weight: 600; cursor: pointer; font-family: var(--sans); }
.book-btn:hover { background: var(--orange-light); }
.booking-note { text-align: center; font-size: 11px; color: var(--text-muted); margin-top: 14px; }

/* ===== Booking (calendar fix) ===== */
#view-booking { background: var(--warm-white); padding-top: 60px; }
.booking-page { display: none; } .booking-page.active { display: block; }
.stepper-wrap { background: #fff; border-bottom: 1px solid var(--border); padding: 24px 0 20px; }
.stepper { display: flex; align-items: center; justify-content: center; max-width: 520px; margin: 0 auto; }
.step-item { display: flex; flex-direction: column; align-items: center; gap: 8px; }
.step-circle { width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 14px; font-weight: 600; border: 2px solid var(--border); background: #fff; color: var(--text-muted); }
.step-item.done .step-circle { background: #3BAA6E; border-color: #3BAA6E; color: #fff; }
.step-item.active .step-circle { background: var(--orange); border-color: var(--orange); color: #fff; }
.step-label { font-size: 11px; color: var(--text-muted); white-space: nowrap; }
.step-item.active .step-label { color: var(--orange); font-weight: 600; }
.step-line { height: 2px; width: 100px; background: var(--border); margin-bottom: 20px; flex-shrink: 0; }
.step-line.done { background: var(--orange); }
.booking-body { max-width: 1060px; margin: 0 auto; padding: 48px 24px 64px; display: grid; grid-template-columns: 1fr 320px; gap: 28px; align-items: start; }
.booking-card-inner { background: #fff; border-radius: 16px; padding: 32px; box-shadow: 0 2px 12px rgba(0,0,0,.06); }
.card-section-title { display: flex; align-items: center; gap: 8px; font-family: var(--serif); font-size: 16px; font-weight: 700; margin-bottom: 24px; }
.calendar-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px; }
.cal-month { font-family: var(--serif); font-size: 16px; font-weight: 700; }
.cal-nav { background: none; border: 1.5px solid var(--border); border-radius: 8px; width: 32px; height: 32px; cursor: pointer; font-size: 14px; color: var(--text-muted); display: flex; align-items: center; justify-content: center; }
.calendar-grid { display: grid; grid-template-columns: repeat(7, minmax(0, 1fr)); gap: 6px; text-align: center; width: 100%; }
.cal-dow { font-size: 11px; color: var(--text-muted); padding: 8px 0; font-weight: 500; }
.cal-day { aspect-ratio: 1; width: 100%; max-width: 44px; margin: 0 auto; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 13px; cursor: pointer; transition: background .15s, color .15s; user-select: none; }
.cal-day:hover:not(.disabled):not(.empty) { background: #FDF1EC; color: var(--orange); }
.cal-day.selected { background: var(--orange); color: #fff; font-weight: 600; }
.cal-day.today { border: 1.5px solid var(--orange); color: var(--orange); font-weight: 600; }
.cal-day.today.selected { background: var(--orange); color: #fff; }
.cal-day.disabled { color: #ccc; cursor: not-allowed; }
.cal-day.empty { cursor: default; pointer-events: none; }
.session-label { font-size: 13px; font-weight: 600; margin: 28px 0 14px; }
.session-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.session-btn { border: 1.5px solid var(--border); border-radius: 12px; padding: 16px; cursor: pointer; background: #fff; text-align: left; }
.session-btn.selected { border-color: var(--orange); background: #FDF1EC; }
.session-btn .time { font-family: var(--serif); font-size: 22px; font-weight: 700; margin-bottom: 4px; }
.session-btn .tag { font-size: 11px; color: var(--text-muted); }
.dot-am { background: #F5A623; } .dot-pm { background: var(--orange); }
.session-btn .tag .dot { display: inline-block; width: 7px; height: 7px; border-radius: 50%; margin-right: 5px; }
.next-btn { width: 100%; background: var(--orange); color: #fff; border: none; border-radius: 40px; padding: 15px; font-size: 15px; font-weight: 500; cursor: pointer; font-family: var(--sans); margin-top: 28px; }
.next-btn:disabled { background: #ddd; color: #aaa; cursor: not-allowed; }
.summary-card { background: #fff; border-radius: 16px; padding: 24px; box-shadow: 0 2px 12px rgba(0,0,0,.06); position: sticky; top: 80px; }
.summary-card h3 { font-family: var(--serif); font-size: 15px; font-weight: 700; margin-bottom: 16px; }
.summary-img { width: 100%; height: 130px; object-fit: cover; border-radius: 10px; margin-bottom: 14px; }
.summary-name { font-family: var(--serif); font-size: 14px; font-weight: 700; margin-bottom: 14px; }
.summary-row { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid var(--border); font-size: 13px; }
.summary-row .label { color: var(--text-muted); }
.summary-row .value.price { font-family: var(--serif); font-size: 16px; color: var(--orange); font-weight: 700; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-bottom: 14px; }
.form-group { display: flex; flex-direction: column; gap: 6px; margin-bottom: 14px; }
.form-group label { font-size: 12px; font-weight: 600; }
.form-group label .req { color: var(--orange); }
.form-input { border: 1.5px solid var(--border); border-radius: 10px; padding: 11px 14px; font-size: 13px; font-family: var(--sans); outline: none; }
.form-group.has-error .form-input { border-color: #e74c3c; }
.error-msg { font-size: 11px; color: #e74c3c; display: none; }
.form-group.has-error .error-msg { display: block; }
.pay-options { display: flex; flex-direction: column; gap: 10px; margin-bottom: 20px; }
.pay-option { border: 1.5px solid var(--border); border-radius: 12px; padding: 14px 18px; display: flex; align-items: center; gap: 14px; cursor: pointer; }
.pay-option.selected { border-color: var(--orange); background: #FDF1EC; }
.pay-icon { width: 36px; height: 28px; border-radius: 6px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; font-size: 13px; font-weight: 700; color: #fff; }
.pay-icon.cc { background: #1A73E8; } .pay-icon.line { background: #00B900; } .pay-icon.apple { background: #000; }
.confirm-btn { width: 100%; background: var(--orange); color: #fff; border: none; border-radius: 40px; padding: 16px; font-size: 15px; font-weight: 600; cursor: pointer; font-family: var(--sans); margin-top: 8px; }
.success-page { background: #fff; position: relative; overflow: hidden; }
.success-inner { position: relative; z-index: 2; display: flex; flex-direction: column; align-items: center; padding: 60px 24px 80px; }
.check-icon { width: 72px; height: 72px; background: #3BAA6E; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 30px; color: #fff; margin-bottom: 28px; }
.success-title { font-family: var(--serif); font-size: clamp(24px,4vw,36px); font-weight: 900; text-align: center; margin-bottom: 12px; }
.order-card { background: var(--warm-white); border: 1.5px solid var(--border); border-radius: 16px; padding: 28px 32px; width: 100%; max-width: 480px; margin-bottom: 36px; }
.order-card-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px; }
.order-id { background: var(--dark); color: #fff; font-size: 11px; padding: 4px 10px; border-radius: 6px; }
.success-actions { display: flex; gap: 14px; flex-wrap: wrap; justify-content: center; }
.btn-orange { background: var(--orange); color: #fff; border: none; border-radius: 40px; padding: 13px 28px; font-size: 14px; font-weight: 500; cursor: pointer; font-family: var(--sans); }

@media (max-width: 1024px) {
  .explore-wrapper { padding: 32px 28px 60px; }
  .filter-sidebar { display: none; }
  #view-products .cards-grid { grid-template-columns: repeat(2, 1fr); }
  .brand-story-inner { grid-template-columns: 1fr; gap: 32px; }
  .values-grid, .numbers-grid { grid-template-columns: repeat(2, 1fr); }
  .team-grid { grid-template-columns: repeat(2, 1fr); }
  .detail-wrapper { flex-direction: column; padding: 32px 28px 60px; }
  .booking-card { width: 100%; position: static; }
  .booking-body { grid-template-columns: 1fr; }
  .profile-container { grid-template-columns: 1fr; }
}
@media (max-width: 768px) {
  #view-login .page { grid-template-columns: 1fr; }
  #view-login .hero { min-height: 220px; }
}
@media (max-width: 680px) {
  .nav-links { display: none; }
  #view-products .cards-grid, .cards-grid { grid-template-columns: 1fr; }
  .fee-grid, .session-grid { grid-template-columns: 1fr; }
  .form-row { grid-template-columns: 1fr; }
  .order-table-head { display: none; }
  .order-row { grid-template-columns: 1fr; gap: 10px; }
}
"""

# Extract and process bodies
pages = {}
for name, fname in [
    ('index', 'index.html'),
    ('products', 'products.html'),
    ('about', 'about.html'),
    ('faq', 'faq.html'),
    ('profile', 'profile-1.html'),
    ('login', 'login.html'),
    ('detail', 'product-detail.html'),
    ('booking', 'booking.html'),
]:
    html = (ROOT / fname).read_text(encoding='utf-8')
    body = extract_body(html)
    body = strip_nav_footer(body)
    if name == 'index':
        body = fix_index_body(body)
    elif name == 'products':
        body = fix_products_body(body)
    elif name == 'detail':
        body = fix_detail_body(body)
    elif name == 'booking':
        body = fix_booking_body(body)
    elif name == 'about':
        body = fix_about_body(body)
    elif name == 'profile':
        body = fix_profile_body(body)
    elif name == 'login':
        body = fix_login_body(body)
    elif name == 'faq':
        body = strip_scripts(body)
        body = re.sub(r'<main>\s*', '', body)
        body = re.sub(r'\s*</main>\s*$', '', body)
    pages[name] = body

# Booking: rename conflicting classes
pages['booking'] = pages['booking'].replace('class="booking-card"', 'class="booking-card-inner"', 1)
pages['booking'] = pages['booking'].replace('class="page active"', 'class="booking-page active"')
pages['booking'] = re.sub(r'class="page"', 'class="booking-page"', pages['booking'])
pages['booking'] = pages['booking'].replace("document.querySelectorAll('.page')", "document.querySelectorAll('.booking-page')")

# Collect inline scripts from source files
products_js = re.search(r'<script>(.*?)</script>', (ROOT / 'products.html').read_text(encoding='utf-8'), re.DOTALL).group(1)
detail_js = re.search(r'<script>(.*?)</script>', (ROOT / 'product-detail.html').read_text(encoding='utf-8'), re.DOTALL).group(1)
booking_js = re.search(r'<script>(.*?)</script>', (ROOT / 'booking.html').read_text(encoding='utf-8'), re.DOTALL).group(1)
faq_js = re.search(r'<script>(.*?)</script>', (ROOT / 'faq.html').read_text(encoding='utf-8'), re.DOTALL).group(1)
profile_js = re.search(r'<script>(.*?)</script>', (ROOT / 'profile-1.html').read_text(encoding='utf-8'), re.DOTALL).group(1)
login_js = re.search(r'<script>(.*?)</script>', (ROOT / 'login.html').read_text(encoding='utf-8'), re.DOTALL).group(1)

# Products filter: add applyThemeFilter
products_js += """

function applyThemeFilter(theme) {
  document.querySelectorAll('#theme-tags .tag-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.theme === theme);
  });
  filterCards();
}
"""

# Booking fixes
booking_js = booking_js.replace("function showPage(id)", "function showBookingStep(id)")
booking_js = booking_js.replace("showPage('page-step2')", "showBookingStep('page-step2')")
booking_js = booking_js.replace("showPage('page-success')", "showBookingStep('page-success')")
booking_js = re.sub(r"\n\s*// make step1 layout two-column[\s\S]*$", "", booking_js)

# Detail: rename bookNow conflict
detail_js = detail_js.replace('function bookNow()', 'function updateQtyDisplay()')
detail_js = detail_js.replace('function updateDisplay()', 'function updateQtyDisplay()')
detail_js = detail_js.replace('updateDisplay();', 'updateQtyDisplay();')
detail_js = detail_js.replace('updateDisplay();', 'updateQtyDisplay();')
detail_js = re.sub(r'function bookNow\(\)[\s\S]*?}\s*', '', detail_js)

# Login: rename switchTab
login_js = login_js.replace('function switchTab(tab)', 'function switchLoginTab(tab)')
login_js = login_js.replace("switchTab('register')", "switchLoginTab('register')")
login_js = login_js.replace("switchTab('login')", "switchLoginTab('login')")
login_js = login_js.replace("onclick=\"switchTab('register')", "onclick=\"switchLoginTab('register')")
login_js = login_js.replace("onclick=\"switchTab('login')", "onclick=\"switchLoginTab('login')")

about_js = """
function initAboutReveal() {
  const els = document.querySelectorAll('#view-about .reveal');
  if (!els.length) return;
  const obs = new IntersectionObserver(entries => {
    entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); obs.unobserve(e.target); } });
  }, { threshold: 0.12 });
  els.forEach(el => obs.observe(el));
}
"""

faq_js = faq_js.replace('function initFaq', 'function initFaqOrig')
faq_js = """
function initFaq() {
  const tabBtns = document.querySelectorAll('#view-faq .tab-btn');
  const faqSections = document.querySelectorAll('#view-faq .faq-section');
  tabBtns.forEach(btn => {
    btn.onclick = () => {
      tabBtns.forEach(b => b.classList.remove('active'));
      faqSections.forEach(s => s.classList.remove('active'));
      btn.classList.add('active');
      document.getElementById(btn.dataset.target).classList.add('active');
    };
  });
}
""" + faq_js

profile_js = profile_js.replace('switchTab', 'switchProfileTab')

out_html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>島嶼旅跡 IslandTrace</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@400;600;700;900&family=Noto+Sans+TC:wght@300;400;500;600&display=swap" rel="stylesheet" />
  <style>
{BASE_CSS}
{EXTRA_CSS}
  </style>
</head>
<body>
{NAV}

<div id="view-index" class="view active">
{pages['index']}
</div>

<div id="view-products" class="view">
{pages['products']}
</div>

<div id="view-about" class="view">
{pages['about']}
</div>

<div id="view-faq" class="view">
{pages['faq']}
</div>

<div id="view-profile" class="view">
{pages['profile']}
</div>

<div id="view-login" class="view">
{pages['login']}
</div>

<div id="view-detail" class="view">
{pages['detail']}
</div>

<div id="view-booking" class="view">
{pages['booking']}
</div>

{FOOTER}

<script>
{ROUTER_JS}

{products_js}

{detail_js}

{booking_js}

{faq_js}

{profile_js}

{login_js}

{about_js}
</script>
</body>
</html>
"""

OUT.write_text(out_html, encoding='utf-8')
print(f"Written {OUT} ({len(out_html):,} bytes)")
