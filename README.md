# Gerador de senhas seguras

Projeto educacional em Python para praticar geração de valores aleatórios com segurança, validação de entrada e testes automatizados.

O programa usa `secrets` — adequado para geração de credenciais — em vez de `random`, garante pelo menos um caractere de cada grupo habilitado e embaralha o resultado com `SystemRandom`.

## Funcionalidades

- senhas de 12 a 128 caracteres;
- letras minúsculas, maiúsculas e números;
- símbolos opcionais;
- exclusão opcional de caracteres visualmente confusos (`O`, `0`, `I`, `l`);
- geração de até 100 senhas por vez;
- estimativa didática de entropia;
- cópia para a área de transferência no macOS, Windows e Linux;
- histórico somente em memória durante a execução.

## Decisões de segurança

- Senhas não são gravadas em arquivo. Armazenar credenciais em texto puro seria uma prática insegura.
- O histórico existe apenas na memória do processo e pode ser limpo pelo menu.
- A cópia automática vem desativada. Outros aplicativos podem observar ou substituir o conteúdo da área de transferência.
- A entropia exibida é uma estimativa baseada no tamanho do alfabeto e no comprimento. Ela não verifica vazamentos, reutilização nem a segurança do dispositivo.

Este projeto demonstra fundamentos; não substitui um gerenciador de senhas auditado.

## Como executar

Requisito: Python 3.9 ou superior.

```bash
python3 password_generator.py
```

Não há dependências externas obrigatórias. No Linux, a cópia para a área de transferência requer `xclip` ou `xsel`.

## Testes

```bash
python3 -m unittest discover -s tests -v
```

Os testes cobrem tamanho, grupos obrigatórios, exclusão de caracteres confusos e cálculo de entropia.

## Estrutura

```text
.
├── password_generator.py
├── tests/
│   └── test_password_generator.py
├── .gitignore
├── README.md
└── SECURITY.md
```

## Limitações e próximos passos

- a interface é apenas de terminal;
- as configurações não persistem entre execuções;
- falta uma opção de frase-senha com palavras aleatórias;
- ainda não há integração contínua no GitHub Actions.

## Uso responsável

Não inclua senhas reais em issues, commits ou capturas de tela. Para contas importantes, prefira um gerenciador de senhas reconhecido e autenticação multifator.
