// validação simples de login antes do POST
document.querySelector('form').addEventListener('submit', e => {
    const u = document.querySelector('input[name="username"]').value.trim();
    const p = document.querySelector('input[name="password"]').value.trim();
    if (!u || !p) {
      e.preventDefault();
      alert('Preencha todos os campos.');
    }
  });