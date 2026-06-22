const App = {
  page: 'index',
  init() {
    document.body.addEventListener('click', e => {
      const el = e.target.closest('[data-go]');
      if (!el) return;
      e.preventDefault();
      this.go(el.dataset.go, el.dataset.theme || null);
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
    if (typeof initCalendar === 'function') initCalendar();
    if (typeof initAboutReveal === 'function') initAboutReveal();
    if (typeof initFaq === 'function') initFaq();
    if (typeof updateQtyDisplay === 'function') updateQtyDisplay();
  },
  go(page, theme) {
    this.page = page;
    document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
    document.getElementById('view-' + page)?.classList.add('active');
    const login = page === 'login';
    document.getElementById('site-nav').hidden = login;
    document.getElementById('site-footer').hidden = login;
    document.querySelectorAll('.nav-links a:not(.nav-cta)').forEach(a => {
      a.classList.toggle('active', a.dataset.go === page);
    });
    window.scrollTo(0, 0);
    if (page === 'products' && theme && typeof applyThemeFilter === 'function') applyThemeFilter(theme);
    if (page === 'booking' && typeof showBookingStep === 'function') showBookingStep('page-step1');
    if (page === 'about' && typeof initAboutReveal === 'function') initAboutReveal();
  }
};
document.addEventListener('DOMContentLoaded', () => App.init());
