/* ═══════════════════════════════════════════════════════════════
   DEMO BEACH RESORT — Main JavaScript
   ═══════════════════════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', () => {

  // ── NAV SCROLL EFFECT ──────────────────────────────────────
  const header = document.getElementById('site-header');
  if (header) {
    const onScroll = () => {
      header.classList.toggle('scrolled', window.scrollY > 50);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  // ── MOBILE MENU ────────────────────────────────────────────
  const navToggle = document.getElementById('nav-toggle');
  const mobileMenu = document.getElementById('mobile-menu');
  if (navToggle && mobileMenu) {
    navToggle.addEventListener('click', () => {
      const isOpen = mobileMenu.classList.toggle('open');
      navToggle.setAttribute('aria-expanded', isOpen);
      document.body.style.overflow = isOpen ? 'hidden' : '';
    });
    // Close on link click
    mobileMenu.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        mobileMenu.classList.remove('open');
        document.body.style.overflow = '';
      });
    });
    // Close on outside click
    document.addEventListener('click', (e) => {
      if (!navToggle.contains(e.target) && !mobileMenu.contains(e.target)) {
        mobileMenu.classList.remove('open');
        document.body.style.overflow = '';
      }
    });
  }

  // ── AUTO-DISMISS MESSAGES ──────────────────────────────────
  document.querySelectorAll('.message').forEach(msg => {
    setTimeout(() => {
      msg.style.opacity = '0';
      msg.style.transform = 'translateX(40px)';
      msg.style.transition = 'all .4s ease';
      setTimeout(() => msg.remove(), 400);
    }, 5000);
  });

  // ── SCROLL ANIMATIONS (IntersectionObserver) ───────────────
  const animTargets = document.querySelectorAll('[data-aos]');
  if (animTargets.length && 'IntersectionObserver' in window) {
    // Inject basic AOS styles dynamically
    const style = document.createElement('style');
    style.textContent = `
      [data-aos] { opacity: 0; transform: translateY(30px); transition: opacity .7s ease, transform .7s ease; }
      [data-aos].aos-animate { opacity: 1; transform: none; }
    `;
    document.head.appendChild(style);

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry, i) => {
        if (entry.isIntersecting) {
          const delay = i * 100;
          setTimeout(() => entry.target.classList.add('aos-animate'), delay);
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });

    animTargets.forEach(el => observer.observe(el));
  }

  // ── FORM INPUT FOCUS EFFECT ────────────────────────────────
  document.querySelectorAll('.form-input').forEach(input => {
    const group = input.closest('.form-group');
    if (!group) return;
    input.addEventListener('focus', () => group.classList.add('focused'));
    input.addEventListener('blur', () => group.classList.remove('focused'));
  });

  // ── SMOOTH ANCHOR SCROLLING ────────────────────────────────
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
      const target = document.querySelector(anchor.getAttribute('href'));
      if (target) {
        e.preventDefault();
        const offset = parseInt(getComputedStyle(document.documentElement)
          .getPropertyValue('--nav-h')) || 80;
        window.scrollTo({
          top: target.getBoundingClientRect().top + window.scrollY - offset - 20,
          behavior: 'smooth'
        });
      }
    });
  });

  // ── BOOKING: Date Validation ───────────────────────────────
  const checkIn = document.getElementById('check_in');
  const checkOut = document.getElementById('check_out');
  if (checkIn && checkOut) {
    checkIn.addEventListener('change', () => {
      if (!checkIn.value) return;
      const nextDay = new Date(new Date(checkIn.value).getTime() + 86400000)
        .toISOString().split('T')[0];
      checkOut.min = nextDay;
      if (!checkOut.value || checkOut.value <= checkIn.value) {
        checkOut.value = nextDay;
      }
    });
  }

  // ── PHONE FORMAT HINT ──────────────────────────────────────
  document.querySelectorAll('input[type="tel"]').forEach(tel => {
    tel.addEventListener('input', () => {
      // Basic phone cleanup
      let val = tel.value.replace(/[^\d+\s\-()]/g, '');
      tel.value = val;
    });
  });

  // ── VILLA CARD KEYBOARD SUPPORT ────────────────────────────
  document.querySelectorAll('.villa-option').forEach(card => {
    card.setAttribute('tabindex', '0');
    card.setAttribute('role', 'radio');
    card.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        const radio = card.querySelector('input[type="radio"]');
        if (radio) {
          radio.checked = true;
          radio.dispatchEvent(new Event('change', { bubbles: true }));
          card.click();
        }
      }
    });
  });

  // ── PRINT BOOKING REFERENCE ────────────────────────────────
  const refNumber = document.querySelector('.ref-number');
  if (refNumber) {
    refNumber.style.cursor = 'pointer';
    refNumber.title = 'Click to copy';
    refNumber.addEventListener('click', () => {
      navigator.clipboard?.writeText(refNumber.textContent).then(() => {
        const orig = refNumber.textContent;
        refNumber.textContent = '✓ Copied!';
        setTimeout(() => refNumber.textContent = orig, 1800);
      });
    });
  }

});
