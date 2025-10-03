document.addEventListener("DOMContentLoaded", function () {
  // Navegação suave para as seções do header
  document.querySelectorAll("nav a").forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      const href = this.getAttribute("href");
      if (href === "#sobre") {
        e.preventDefault();
        const sobreSection = document.querySelector(".rectangle-7");
        if (sobreSection) {
          window.scrollTo({
            top: sobreSection.offsetTop - 20,
            behavior: "smooth",
          });
        }
      } else if (href === "#funcoes") {
        e.preventDefault();
        const funcoesSection = document.querySelector(".rectangle-8");
        if (funcoesSection) {
          window.scrollTo({
            top: funcoesSection.offsetTop - 20,
            behavior: "smooth",
          });
        }
      } else if (href === "#faq") {
        e.preventDefault();
        const faqSection = document.querySelector(".rectangle-9");
        if (faqSection) {
          window.scrollTo({
            top: faqSection.offsetTop - 20,
            behavior: "smooth",
          });
        }
      } else if (href && href.startsWith("#")) {
        e.preventDefault();
        const targetElement = document.querySelector(href);
        if (targetElement) {
          window.scrollTo({
            top: targetElement.offsetTop - 20,
            behavior: "smooth",
          });
        }
      }
    });
  });

  const loginForm = document.getElementById("loginForm");
  const forgotPasswordContainer = document.getElementById(
    "forgotPasswordContainer",
  );

  // Envia credenciais via fetch para /login e redireciona conforme resposta do backend.
  const loginFormElement = document.querySelector("#loginForm form");
  if (loginFormElement) {
    loginFormElement.addEventListener("submit", function (e) {
      e.preventDefault();
      const username = document
        .querySelector('input[name="username"]')
        .value.trim();
      const password = document
        .querySelector('input[name="password"]')
        .value.trim();

      if (!username || !password) {
        alert("Por favor, preencha todos os campos!");
        return;
      }

      const payload = { email: username, senha: password };

      fetch("/login", {
        method: "POST",
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      })
        .then((resp) =>
          resp.json().then((data) => ({ status: resp.status, body: data })),
        )
        .then(({ status, body }) => {
          if (status === 200 && body.redirect_url) {
            window.location.href = body.redirect_url;
          } else if (body.message) {
            alert(body.message);
          } else {
            alert("Erro ao efetuar login.");
          }
        })
        .catch((err) => {
          console.error("Erro no login:", err);
          alert("Erro de rede ao tentar logar.");
        });
    });
  }

  // Botão "Saiba mais"
  const saibaMaisBtn = document.querySelector(".btn-saiba-mais");
  if (saibaMaisBtn) {
    saibaMaisBtn.addEventListener("click", function () {
      alert(
        "O Aquanox é um sistema de controle de irrigação inteligente que utiliza múltiplos parâmetros para otimizar o uso de água.",
      );
    });
  }

  const forgotPasswordLink = document.getElementById("forgotPasswordLink");
  const mainLoginForm = document.getElementById("loginForm"); // Renomeado para evitar conflito

  // Mostrar formulário de recuperação
  forgotPasswordLink.addEventListener("click", function (e) {
    e.preventDefault();

    // Certifique-se de que as classes estão limpas antes de aplicar novas animações
    mainLoginForm.classList.remove("show", "hide");
    mainLoginForm.classList.add("hide"); // Adiciona classe para animação de saída

    setTimeout(() => {
      mainLoginForm.style.display = "none"; // Oculta após a animação
      fetch("/forgot") // Corrigido para usar a rota correta
        .then((response) => {
          if (!response.ok) {
            throw new Error("Erro ao carregar o formulário de recuperação.");
          }
          return response.text();
        })
        .then((html) => {
          forgotPasswordContainer.innerHTML = html;
          forgotPasswordContainer.style.display = "block";

          // Adicionar classe para transição suave
          const forgotPasswordForm =
            document.getElementById("forgotPasswordForm");
          forgotPasswordForm.classList.remove("show"); // Garante estado inicial
          setTimeout(() => forgotPasswordForm.classList.add("show"), 10);

          // Adicionar evento para voltar ao login
          const backToLogin = document.getElementById("backToLogin");
          backToLogin.addEventListener("click", function (e) {
            e.preventDefault();

            forgotPasswordForm.classList.remove("show"); // Remove classe para animação de saída
            setTimeout(() => {
              forgotPasswordContainer.style.display = "none";
              mainLoginForm.style.display = "block";
              mainLoginForm.classList.remove("hide", "show", "from-forgot");
              // Adiciona animação de retorno: começa em -25%
              mainLoginForm.classList.add("from-forgot");
              // Força reflow para garantir a transição
              void mainLoginForm.offsetWidth;
              // Agora anima para -50%
              mainLoginForm.classList.add("show");
              // Remove from-forgot após a animação
              setTimeout(
                () => mainLoginForm.classList.remove("from-forgot"),
                600,
              );
            }, 600); // Tempo ajustado para a transição terminar
          });
        })
        .catch((err) => console.error(err.message));
    }, 600); // Tempo ajustado para a animação de saída do login
  });

  // Evento para mostrar caixa de confirmação após envio do formulário
  const forgotForm = document.getElementById("forgotForm");
  if (forgotForm) {
    forgotForm.addEventListener("submit", function (ev) {
      ev.preventDefault();
      // Aqui você pode adicionar validação do email se quiser
      // Remove o formulário de recuperação
      forgotPasswordForm.classList.remove("show");
      setTimeout(() => {
        // Carrega sent.html via fetch e exibe na mesma área
        fetch("/sent")
          .then((response) => {
            if (!response.ok)
              throw new Error("Erro ao carregar a confirmação de envio.");
            return response.text();
          })
          .then((html) => {
            forgotPasswordContainer.innerHTML = html;
            forgotPasswordContainer.style.display = "block";
            // Animação da sent-box igual ao forgot
            setTimeout(() => {
              const sentBox = document.getElementById("sentBox");
              if (sentBox) sentBox.classList.add("show");
              // Evento para "Nova senha" abre resetar_senha.html via fetch
              const novaSenhaLink = document.getElementById("novaSenhaLink");
              if (novaSenhaLink) {
                novaSenhaLink.addEventListener("click", function (e) {
                  e.preventDefault();
                  sentBox.classList.remove("show");
                  setTimeout(() => {
                    fetch("/resetar_senha")
                      .then((response) => {
                        if (!response.ok)
                          throw new Error(
                            "Erro ao carregar a redefinição de senha.",
                          );
                        return response.text();
                      })
                      .then((html) => {
                        forgotPasswordContainer.innerHTML = html;
                        forgotPasswordContainer.style.display = "block";
                        setTimeout(() => {
                          const novaSenhaBox =
                            document.getElementById("sentResetBox") ||
                            document.getElementById("novaSenhaBox");
                          if (novaSenhaBox) novaSenhaBox.classList.add("show");
                        }, 10);
                      })
                      .catch((err) => alert(err.message));
                  }, 600);
                });
              }
              // Evento para voltar ao login a partir da caixa sent
              const backToLoginFromSent = document.getElementById(
                "backToLoginFromSent",
              );
              if (backToLoginFromSent) {
                backToLoginFromSent.addEventListener("click", function (e) {
                  e.preventDefault();
                  sentBox.classList.remove("show");
                  setTimeout(() => {
                    forgotPasswordContainer.style.display = "none";
                    mainLoginForm.style.display = "block";
                    mainLoginForm.classList.remove(
                      "hide",
                      "show",
                      "from-forgot",
                    );
                    mainLoginForm.classList.add("from-forgot");
                    void mainLoginForm.offsetWidth;
                    mainLoginForm.classList.add("show");
                    setTimeout(
                      () => mainLoginForm.classList.remove("from-forgot"),
                      600,
                    );
                  }, 600);
                });
              }
            }, 10);
          })
          .catch((err) => alert(err.message));
      }, 600);
    });
  }

  // Alternar visibilidade da senha
  const togglePassword = document.getElementById("togglePassword");
  const passwordInput = document.querySelector('input[name="password"]');

  if (togglePassword && passwordInput) {
    togglePassword.addEventListener("click", function () {
      const type =
        passwordInput.getAttribute("type") === "password" ? "text" : "password";
      passwordInput.setAttribute("type", type);

      // Alternar imagem do botão
      const imgSrc =
        type === "password" ? "static/img/olhoa.png" : "static/img/olhof.png"; // Invertida a ordem
      this.style.backgroundImage = `url(${imgSrc})`;
    });

    // Configurar imagem inicial
    togglePassword.style.backgroundImage = "url(static/img/olhoa.png)"; // Invertida para começar com "olhoa"
    togglePassword.style.backgroundRepeat = "no-repeat";
    togglePassword.style.backgroundPosition = "center";
    togglePassword.style.backgroundSize = "contain";
    togglePassword.style.border = "none";
    togglePassword.style.cursor = "pointer";
  }

  // Animação dos rectangles verdes com gradiente fluido via JS
  function addRectangleHoverAnimation(selector) {
    document.querySelectorAll(selector).forEach(function (rect) {
      rect.addEventListener("mouseenter", function () {
        rect.classList.add("hover");
        rect.style.transition =
          "transform 0.7s cubic-bezier(.4,1.5,.5,1), box-shadow 0.7s, background 0.4s, background-position 1s";
        rect.style.background =
          "linear-gradient(315deg, #2ecc71 0%, #1f5b2c 100%)";
        rect.style.backgroundSize = "200% 200%";
        rect.style.backgroundPosition = "100% 50%";
      });
      rect.addEventListener("mouseleave", function () {
        rect.classList.remove("hover");
        rect.style.transition =
          "transform 0.7s cubic-bezier(.4,1.5,.5,1), box-shadow 0.7s, background 0.4s, background-position 1s";
        rect.style.background =
          "linear-gradient(135deg, #2ecc71 0%, #1f5b2c 100%)";
        rect.style.backgroundSize = "200% 200%";
        rect.style.backgroundPosition = "0% 50%";
      });
    });
  }
  addRectangleHoverAnimation(".rectangle-14");
  addRectangleHoverAnimation(".rectangle-14-invertida");

  // Expansão da caixa ao clicar na seta
  const seta = document.getElementById("abrirExpansivel");
  const caixa = document.getElementById("caixaExpansivel");
  if (seta && caixa) {
    seta.addEventListener("click", function () {
      caixa.classList.toggle("show");
      seta.classList.toggle("girada");
    });
  }

  // Voltar ao início ao clicar no link da caixa sobre fim.png
  const voltarInicio = document.getElementById("voltar-inicio");
  if (voltarInicio) {
    voltarInicio.addEventListener("click", function (e) {
      e.preventDefault();
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  // Navegação suave para "Sobre" no fim-link
  const fimSobre = document.querySelector('.fim-link[href="#sobre"]');
  if (fimSobre) {
    fimSobre.addEventListener("click", function (e) {
      e.preventDefault();
      const sobreSection = document.querySelector(".rectangle-7");
      if (sobreSection) {
        window.scrollTo({
          top: sobreSection.offsetTop - 20,
          behavior: "smooth",
        });
      }
    });
  }

  // Navegação suave para "Funções" no fim-link
  const fimFuncoes = document.querySelector('.fim-link[href="#funcoes"]');
  if (fimFuncoes) {
    fimFuncoes.addEventListener("click", function (e) {
      e.preventDefault();
      const funcoesSection = document.querySelector(".rectangle-8");
      if (funcoesSection) {
        window.scrollTo({
          top: funcoesSection.offsetTop - 20,
          behavior: "smooth",
        });
      }
    });
  }

  // Navegação suave para "Faq" no fim-link
  const fimFaq = document.querySelector('.fim-link[href="#faq"]');
  if (fimFaq) {
    fimFaq.addEventListener("click", function (e) {
      e.preventDefault();
      const faqSection = document.querySelector(".rectangle-9");
      if (faqSection) {
        window.scrollTo({
          top: faqSection.offsetTop - 20,
          behavior: "smooth",
        });
      }
    });
  }
});
