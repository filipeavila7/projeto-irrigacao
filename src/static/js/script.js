document.addEventListener('DOMContentLoaded', function() {
  // ===== MENU HAMBÚRGUER =====
  const hamburger = document.createElement('button');
  hamburger.className = 'hamburger';
  hamburger.setAttribute('aria-label', 'Menu');
  hamburger.innerHTML = `
    <span></span>
    <span></span>
    <span></span>
  `;
  
  const headerContent = document.querySelector('.header-content');
  const nav = document.querySelector('nav');
  
  if (headerContent && nav) {
    // Insere o hamburger antes do nav
    headerContent.insertBefore(hamburger, nav);
    
    // Toggle menu
    hamburger.addEventListener('click', function(e) {
      e.stopPropagation();
      this.classList.toggle('active');
      nav.classList.toggle('active');
      document.body.style.overflow = nav.classList.contains('active') ? 'hidden' : '';
    });
    
    // Fecha menu ao clicar em link
    nav.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', function() {
        hamburger.classList.remove('active');
        nav.classList.remove('active');
        document.body.style.overflow = '';
      });
    });
    
    // Fecha menu ao clicar fora
    document.addEventListener('click', function(e) {
      if (nav.classList.contains('active') && !nav.contains(e.target) && !hamburger.contains(e.target)) {
        hamburger.classList.remove('active');
        nav.classList.remove('active');
        document.body.style.overflow = '';
      }
    });
  }

  // ===== HEADER SCROLL EFFECT =====
  let lastScroll = 0;
  const header = document.querySelector('header');
  
  window.addEventListener('scroll', function() {
    const currentScroll = window.pageYOffset;
    
    if (currentScroll > 100) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
    
    lastScroll = currentScroll;
  });

  // ===== NAVEGAÇÃO SUAVE =====
  document.querySelectorAll('nav a, .fim-link').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const href = this.getAttribute('href');
      
      if (href === '#sobre') {
        e.preventDefault();
        const sobreSection = document.querySelector('.rectangle-7');
        if (sobreSection) {
          sobreSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      } else if (href === '#funcoes') {
        e.preventDefault();
        const funcoesSection = document.querySelector('.rectangle-8');
        if (funcoesSection) {
          funcoesSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      } else if (href === '#faq') {
        e.preventDefault();
        const faqSection = document.querySelector('.rectangle-9');
        if (faqSection) {
          faqSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      } else if (href && href.startsWith('#')) {
        e.preventDefault();
        const targetElement = document.querySelector(href);
        if (targetElement) {
          targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      }
    });
  });

  // ===== LOGIN FORM =====
  const loginForm = document.getElementById('loginForm');
  const forgotPasswordContainer = document.getElementById('forgotPasswordContainer');
  const loginFormElement = document.querySelector('#loginForm form');
  
  if (loginFormElement) {
    loginFormElement.addEventListener('submit', function(e) {
      e.preventDefault();
      const username = document.querySelector('input[name="username"]').value.trim();
      const password = document.querySelector('input[name="password"]').value.trim();
      
      if (!username || !password) {
        showNotification('Por favor, preencha todos os campos!', 'error');
        return;
      }
      
      // Mostra modal de confirmação
      const modal = document.getElementById('cadastroConfirmModal');
      if (modal) {
        modal.style.display = 'flex';
        document.getElementById('btnIrPainel').onclick = function() {
          window.location.href = '/painel_admin';
        };
      }
    });
  }

  // ===== BOTÃO SAIBA MAIS =====
  const saibaMaisBtn = document.querySelector('.btn-saiba-mais');
  if (saibaMaisBtn) {
    saibaMaisBtn.addEventListener('click', function() {
      showNotification('O Aquanox é um sistema de controle de irrigação inteligente que utiliza múltiplos parâmetros para otimizar o uso de água.', 'info');
    });
  }

  // ===== FORGOT PASSWORD =====
  const forgotPasswordLink = document.getElementById('forgotPasswordLink');
  const mainLoginForm = document.getElementById('loginForm');
  
  if (forgotPasswordLink && mainLoginForm) {
    forgotPasswordLink.addEventListener('click', function(e) {
      e.preventDefault();
      mainLoginForm.classList.add('hide');
      
      setTimeout(() => {
        mainLoginForm.style.display = 'none';
        fetch('/forgot')
          .then(response => response.text())
          .then(html => {
            if (forgotPasswordContainer) {
              forgotPasswordContainer.innerHTML = html;
              forgotPasswordContainer.style.display = 'block';
              
              const forgotPasswordForm = document.getElementById('forgotPasswordForm');
              if (forgotPasswordForm) {
                setTimeout(() => forgotPasswordForm.classList.add('show'), 10);
                
                const backToLogin = document.getElementById('backToLogin');
                if (backToLogin) {
                  backToLogin.addEventListener('click', function(e) {
                    e.preventDefault();
                    forgotPasswordForm.classList.remove('show');
                    
                    setTimeout(() => {
                      forgotPasswordContainer.style.display = 'none';
                      mainLoginForm.style.display = 'block';
                      mainLoginForm.classList.remove('hide');
                      mainLoginForm.classList.add('show');
                    }, 600);
                  });
                }
              }
            }
          })
          .catch(err => showNotification('Erro ao carregar formulário', 'error'));
      }, 600);
    });
  }

  // ===== PASSWORD TOGGLE =====
  const togglePassword = document.getElementById('togglePassword');
  const passwordInput = document.querySelector('input[name="password"]');
  
  if (togglePassword && passwordInput) {
    togglePassword.addEventListener('click', function() {
      const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
      passwordInput.setAttribute('type', type);
      
      const imgSrc = type === 'password' ? 'static/img/olhoa.png' : 'static/img/olhof.png';
      this.style.backgroundImage = `url(${imgSrc})`;
    });
    
    togglePassword.style.backgroundImage = 'url(static/img/olhoa.png)';
  }

  // ===== RECTANGLE HOVER ANIMATION =====
  function addRectangleHoverAnimation(selector) {
    document.querySelectorAll(selector).forEach(function(rect) {
      rect.addEventListener('mouseenter', function() {
        this.style.willChange = 'transform';
      });
      rect.addEventListener('mouseleave', function() {
        this.style.willChange = 'auto';
      });
    });
  }
  
  addRectangleHoverAnimation('.rectangle-14');
  addRectangleHoverAnimation('.rectangle-14-invertida');

  // ===== FAQ EXPANSION =====
  const seta = document.getElementById('abrirExpansivel');
  const caixa = document.getElementById('caixaExpansivel');
  const rectangle162 = document.querySelector('.rectangle-162');
  
  if (seta && caixa && rectangle162) {
    rectangle162.addEventListener('click', function() {
      caixa.classList.toggle('show');
      seta.classList.toggle('girada');
      this.classList.toggle('expanded');
    });
  }

  // ===== VOLTAR AO INÍCIO =====
  const voltarInicio = document.getElementById('voltar-inicio');
  if (voltarInicio) {
    voltarInicio.addEventListener('click', function(e) {
      e.preventDefault();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // ===== TOUCH GESTURES PARA CARDS =====
  const swipeableCards = document.querySelectorAll('.rectangle-14, .rectangle-14-invertida');
  
  swipeableCards.forEach(card => {
    let startX = 0;
    let startY = 0;
    let startTime = 0;
    let isSwiping = false;
    
    card.addEventListener('touchstart', function(e) {
      startX = e.touches[0].clientX;
      startY = e.touches[0].clientY;
      startTime = Date.now();
      isSwiping = false;
      this.classList.add('swipeable');
    }, { passive: true });
    
    card.addEventListener('touchmove', function(e) {
      if (!isSwiping) {
        const diffX = Math.abs(e.touches[0].clientX - startX);
        const diffY = Math.abs(e.touches[0].clientY - startY);
        
        if (diffX > diffY && diffX > 10) {
          isSwiping = true;
          this.classList.add('swiping');
        }
      }
      
      if (isSwiping) {
        const deltaX = e.touches[0].clientX - startX;
        const scale = 1 - Math.abs(deltaX) / 1000;
        this.style.transform = `translateX(${deltaX}px) scale(${scale})`;
      }
    }, { passive: true });
    
    card.addEventListener('touchend', function(e) {
      this.classList.remove('swiping');
      
      if (isSwiping) {
        const endX = e.changedTouches[0].clientX;
        const deltaX = endX - startX;
        const duration = Date.now() - startTime;
        const velocity = Math.abs(deltaX) / duration;
        
        if (Math.abs(deltaX) > 100 || velocity > 0.5) {
          // Swipe detectado
          this.style.transition = 'transform 0.3s ease-out';
          this.style.transform = `translateX(${deltaX > 0 ? '100%' : '-100%'}) scale(0.8)`;
          
          setTimeout(() => {
            this.style.transition = 'transform 0.5s cubic-bezier(0.4, 0, 0.2, 1)';
            this.style.transform = '';
          }, 300);
        } else {
          // Volta para posição original
          this.style.transition = 'transform 0.3s ease-out';
          this.style.transform = '';
        }
      }
      
      isSwiping = false;
      setTimeout(() => this.classList.remove('swipeable'), 300);
    }, { passive: true });
  });

  // ===== SCROLL REVEAL ANIMATION =====
  const revealElements = document.querySelectorAll('.rectangle-14, .rectangle-14-invertida, .weather-card, .valvula-box');
  
  const revealOnScroll = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('reveal', 'active');
      }
    });
  }, {
    threshold: 0.15,
    rootMargin: '0px 0px -50px 0px'
  });
  
  revealElements.forEach(el => {
    el.classList.add('reveal');
    revealOnScroll.observe(el);
  });

  // ===== NOTIFICATION SYSTEM =====
  function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.style.cssText = `
      position: fixed;
      top: 100px;
      right: 20px;
      background: ${type === 'error' ? '#e33629' : type === 'success' ? '#77dd77' : '#73a8ce'};
      color: white;
      padding: 16px 24px;
      border-radius: 12px;
      box-shadow: 0 8px 24px rgba(0,0,0,0.25);
      z-index: 10000;
      max-width: 300px;
      animation: slideInRight 0.3s ease-out;
      font-family: 'Inria Sans Regular Local', Arial, sans-serif;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
      notification.style.animation = 'slideOutRight 0.3s ease-out';
      setTimeout(() => notification.remove(), 300);
    }, 3000);
  }
  
  // Adiciona keyframes para notificações
  const style = document.createElement('style');
  style.textContent = `
    @keyframes slideInRight {
      from {
        transform: translateX(400px);
        opacity: 0;
      }
      to {
        transform: translateX(0);
        opacity: 1;
      }
    }
    @keyframes slideOutRight {
      from {
        transform: translateX(0);
        opacity: 1;
      }
      to {
        transform: translateX(400px);
        opacity: 0;
      }
    }
  `;
  document.head.appendChild(style);

  // ===== LAZY LOADING IMAGES =====
  const images = document.querySelectorAll('img[data-src]');
  const imageObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const img = entry.target;
        img.src = img.dataset.src;
        img.removeAttribute('data-src');
        imageObserver.unobserve(img);
      }
    });
  });
  
  images.forEach(img => imageObserver.observe(img));

  // ===== PREVENÇÃO DE ZOOM MOBILE =====
  document.addEventListener('gesturestart', function(e) {
    e.preventDefault();
  });
  
  document.addEventListener('gesturechange', function(e) {
    e.preventDefault();
  });
  
  document.addEventListener('gestureend', function(e) {
    e.preventDefault();
  });

  // ===== PERFORMANCE OPTIMIZATION =====
  let ticking = false;
  
  window.addEventListener('scroll', function() {
    if (!ticking) {
      window.requestAnimationFrame(function() {
        // Scroll handlers aqui
        ticking = false;
      });
      ticking = true;
    }
  });

  // ===== ACCESSIBILITY: ESC FECHA MODAL =====
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
      const nav = document.querySelector('nav');
      const hamburger = document.querySelector('.hamburger');
      
      if (nav && nav.classList.contains('active')) {
        hamburger.classList.remove('active');
        nav.classList.remove('active');
        document.body.style.overflow = '';
      }
      
      const modal = document.getElementById('cadastroConfirmModal');
      if (modal && modal.style.display === 'flex') {
        modal.style.display = 'none';
      }
    }
  });

  // ===== ANIMAÇÃO DE CARREGAMENTO =====
  window.addEventListener('load', function() {
    document.body.classList.add('loaded');
    
    // Adiciona animação aos elementos principais
    setTimeout(() => {
      document.querySelectorAll('.text-overlay, .login-overlay').forEach(el => {
        el.style.opacity = '1';
        el.style.transform = 'translateY(0)';
      });
    }, 100);
  });

  // ===== TOUCH FEEDBACK =====
  document.querySelectorAll('button, a, .btn-saiba-mais').forEach(el => {
    el.addEventListener('touchstart', function() {
      this.style.opacity = '0.7';
    }, { passive: true });
    
    el.addEventListener('touchend', function() {
      this.style.opacity = '1';
    }, { passive: true });
  });

  console.log('✅ Aquanox JavaScript carregado com sucesso!');
});