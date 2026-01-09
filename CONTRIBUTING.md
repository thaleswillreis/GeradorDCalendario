# 🇧🇷 Contribuindo para o Calendário Brasil BI 📅

Primeiramente, obrigado por se interessar em contribuir! Este projeto visa facilitar a vida de analistas de dados, analistas de business intelligence, engenheiros de dados e demais profissionais de dados que precisam gerar tabelas dimensão de data robustas e adaptadas ao calendário brasileiro e calendários regionais.

Como este é um projeto de código aberto, sua ajuda é fundamental para mantê-lo atualizado (especialmente com as mudanças constantes em feriados estaduais) e com o surgimento de novas práticas na área de dados.

---

## 🚀 Como você pode contribuir?

### 1. Relatando Bugs ou Sugerindo Funcionalidades
Se você encontrou um erro nos cálculos ou tem uma ideia de nova coluna (ex: datas fiscais, data relevantes para determinadas atividades comerciais ou industriais, etc.):

1. Verifique se já não existe uma [Issue](https://github.com/thaleswillreis/GeradorDCalendario/issues) aberta sobre o assunto.
2. Caso não exista, abra uma nova **Issue** descrevendo detalhadamente o problema ou a sugestão.

### 2. Atualização de Feriados

Os feriados estaduais e municipais podem mudar por decretos. Se você notar que algum feriado no arquivo `app.py` está incorreto ou faltando:

* Envie um Pull Request com a correção na lista `state_data`.

### 3. Melhorias no Código (Pull Requests)
Se você quer colocar a mão na massa:
1. Faça um **Fork** do projeto.
2. Crie uma branch para sua modificação: `git checkout -b feature/minha-melhoria`.
3. Mantenha o padrão de código (PEP 8).
4. **Importante:** Se alterar a lógica de datas, atualize ou crie novos testes em `test_app2.py`.
5. Garanta que todos os testes passem executando: `pytest`.
6. Envie o **Pull Request**.

---

## 🛠️ Configuração do Ambiente de Desenvolvimento

Para rodar o projeto localmente e testar suas mudanças:

**PASSO 1:** Faça um **fork** do projeto e **clone** seu fork para a sua estação de trabalho:
   ```bash
   $ git clone git@github.com:SEU_USUARIO/GeradorDCalendario.git  #SSH
   $ git clone https://github.com/SEU_USUARIO/ProjetoCalendario.git  #HTTPS
   ```

**PASSO 2:** **`(Linux)`** Crie e ative um ambiente virtual dentro da pasta do seu fork:
```bash
$ python3 -m venv .venv
$ source .venv/bin/activate
```
**PASSO 2:** **`(Windows)`** Crie e ative um ambiente virtual dentro da pasta do seu fork:
```bash
> python3 -m venv venv 
> venv\Scripts\activate.bat
```

**PASSO 3:** Instale dependências e bibliotecas auxiliares:
```bash
$ python3 -m pip install --upgrade pip
$ pip install -r requirements.txt
```

**PASSO 4:** Execute os testes:
```bash
$ pytest
```

**PASSO 5:** Teste o funcionamento do `app.py`:
```bash
$ streamlit run app.py
```
**Pronto!** Agora está alinhado para iniciar a codificação.

## ⚖️ Dicas de boas práticas

- Use nomes de variáveis claros (ou conforme o padrão já estabelecido).
- Adicione comentários em funções complexas para facilitar o debug (como lógica de datas móveis).
- Evite adicionar bibliotecas pesadas desnecessariamente no **requirements.txt**.
- Verifique se há a necessidade ou não de atualizar o arquivo .gitignore do projeto antes de realizar o último **commit** antes do **pull request**.
- Caso conte com a ajuda de algum colega ou de alguém, e queira dar o crédito, por favor use o campo de descrição do **pull request** deixando os dados do Linkedin, será um prazer deixar um agradecimento depois ou fazer uma recomendação no Linkedin.

---

## **Obrigado pela sua colaboração!** Vamos construir o melhor gerador automático de arquivos de tabela dimensão de data para a comunidade de dados do Brasil. 🇧🇷