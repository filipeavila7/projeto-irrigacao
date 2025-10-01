document.addEventListener('DOMContentLoaded', function () {
  // Sempre deixa os campos como texto visível
  document.getElementById('reset-password').type = 'text';
  document.getElementById('reset-password-confirm').type = 'text';

  // Validação de senhas iguais e mínimo de 8 dígitos no envio do formulário
  const form = document.querySelector('.reset-form');
  if (form) {
    form.addEventListener('submit', function (e) {
      const senha = document.getElementById('reset-password').value;
      const confirmar = document.getElementById('reset-password-confirm').value;

      if (!senha || senha !== confirmar) {
        e.preventDefault();
        alert('As senhas devem coincidir.');
      } else if (senha.length < 8) {
        e.preventDefault();
        alert('A senha deve ter no mínimo 8 dígitos.');
      }
    });
  }
});
