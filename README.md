# Scraper UNA-SUS

Este projeto implementa um web scraper para coletar dados de cursos e ofertas da plataforma UNA-SUS (Universidade Aberta do SUS), com foco especial em identificar cursos relacionados a Diversidade, Equidade, Inclusão e Acessibilidade (DEIA).

## 📋 Descrição

O scraper coleta informações detalhadas sobre cursos e suas ofertas disponíveis no portal da UNA-SUS, incluindo:
- Informações básicas dos cursos
- Detalhes das ofertas (vagas, público-alvo, local, formato)
- Identificação automática de cursos relacionados a DEIA
- Salvamento incremental dos dados em formato CSV

## 🚀 Funcionalidades

- **Coleta incremental**: Evita reprocessar cursos já coletados
- **Detecção DEIA**: Identifica automaticamente cursos relacionados a Diversidade, Equidade, Inclusão e Acessibilidade
- **Tratamento de erros**: Sistema robusto com retry automático
- **Salvamento progressivo**: Salva dados a cada lote processado
- **API REST**: Utiliza a API oficial da UNA-SUS para coleta de dados

## 📁 Estrutura do Projeto

```
unsa-sus/
├── README.md                           # Este arquivo
├── requirements.txt                    # Dependências Python
├── scraper_unasus_incremental.py      # Scraper principal
├── teste_scraper.py                   # Script de teste
├── import requests.py                  # Módulo de importação
├── .gitignore                         # Arquivos ignorados pelo Git
├── unasus_ofertas_detalhadas.csv      # Dados coletados
└── teste_unasus.csv                   # Dados de teste
```

## 🛠️ Instalação

1. Clone o repositório:
```bash
git clone https://github.com/eunilo/unsa-sus.git
cd unsa-sus
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 📖 Como Usar

### Teste Inicial
Execute o script de teste para verificar a conectividade:
```bash
python teste_scraper.py
```

### Execução Completa
Para executar o scraper completo:
```bash
python scraper_unasus_incremental.py
```

O script irá:
1. Carregar dados já processados (se existirem)
2. Coletar novos cursos da API da UNA-SUS
3. Identificar cursos relacionados a DEIA
4. Extrair detalhes das ofertas de cada curso
5. Salvar progressivamente em `unasus_ofertas_detalhadas.csv`

## 📊 Dados Coletados

O scraper coleta as seguintes informações:

### Cursos
- ID do curso
- Nome do curso
- Descrição
- Status
- Relação com DEIA

### Ofertas
- ID da oferta
- Código da oferta
- Número de vagas
- Público-alvo
- Local da oferta
- Formato
- URL da oferta

## 🔍 Descritores DEIA

O sistema identifica automaticamente cursos relacionados aos seguintes descritores:
- Diversidade, Equidade e Integração
- Diversidade, Equidade, Inclusão e Pertencimento
- Diversidade, Equidade, Inclusão, Acessibilidade
- Diversidade, Igualdade e Inclusão
- Equidade, Diversidade e Inclusão
- Inclusão, Diversidade, Equidade e Acessibilidade

## ⚙️ Configurações

### Parâmetros Ajustáveis
- `lote = 10`: Número de cursos processados antes de salvar
- `timeout = 30`: Timeout para requisições HTTP
- `sleep = 1`: Intervalo entre requisições (em segundos)

### Headers HTTP
```python
headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json"
}
```

## 📈 Monitoramento

O script exibe progresso em tempo real:
- Cursos já processados
- Páginas processadas
- Salvamentos incrementais
- Erros e retentativas

## 🐛 Tratamento de Erros

- **Timeout de conexão**: Retry automático após 30 segundos
- **Erro de parsing**: Log detalhado do erro
- **Arquivo CSV corrompido**: Recriação automática
- **API indisponível**: Tentativas múltiplas

## 📝 Formato de Saída

Os dados são salvos em CSV com encoding UTF-8-SIG, contendo:
- Todas as colunas originais da API
- Colunas adicionais de DEIA
- Dados detalhados das ofertas
- URLs de referência

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## ⚠️ Aviso Legal

Este scraper foi desenvolvido para fins educacionais e de pesquisa. Respeite os termos de uso da UNA-SUS e implemente delays apropriados entre requisições para não sobrecarregar os servidores.

## 📞 Contato

- **Autor**: Eunilo
- **GitHub**: [@eunilo](https://github.com/eunilo)
- **Projeto**: [unsa-sus](https://github.com/eunilo/unsa-sus)

---

**Desenvolvido com ❤️ para a comunidade de saúde pública brasileira** 