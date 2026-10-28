# 📊 Analisador de Dados Eleitorais (1º e 2º Turno)

Aplicação em Python desenvolvida com **Pandas** e **Tkinter** para análise e visualização interativa de dados eleitorais em grande escala (arquivos CSV disponibilizados pelo TSE). 

O sistema permite analisar votos do 1º e 2º Turno em vários níveis de detalhamento (Nacional, Estadual, Municipal, Local de Votação e Seção) sem estourar a memória RAM do computador.

---

## 🚀 Funcionalidades

A aplicação está organizada em 6 abas interativas:

1. **Total Geral (BR):** Exibe o somatório total de votos de cada candidato no país no 1º e 2º Turno, mostrando a diferença absoluta de votos e a variação percentual (%).
2. **Por Estado (UF):** Filtra e compara a votação de cada candidato por Estado.
3. **Por Município:** Permite pesquisar e filtrar por qualquer município do Brasil para analisar os votos recebidos por cada candidato.
4. **Por Local de Votação:** Detalhamento até ao nível do colégio/escola eleitoral, navegando de forma encadeada (`UF -> Município -> Local`).
5. **Desempenho do Candidato:** Exibe os locais de votação onde um candidato específico teve o maior crescimento nominal e percentual de votos entre os turnos.
6. **100% dos Votos (2ºT):** Mapeia todas as zonas (`NR_ZONA`) e seções (`NR_SECAO`) do país onde um determinado candidato obteve **unanimidade (100% dos votos válidos)** no 2º Turno.

---

## 🛠️ Pré-requisitos e Dependências

Para executar este projeto, precisa do **Python 3.8+** instalado.

Os dados utilizados neste projeto são públicos e foram obtidos diretamente do portal do TSE:
* 🌐 **Fonte Oficial:** [Portal de Dados Abertos do TSE](https://dadosabertos.tse.jus.br/dataset/resultados-2026/resource/01ea4ccd-f443-469c-9f29-c69ff97f7d4c)
necessário baixar e colocar na mesma pasta, para o funcionamento do código.


### Bibliotecas necessárias:
* pandas

*Nota: A biblioteca `tkinter` já vem incluída por padrão nas instalações do Python para Windows e macOS.*

Para instalar o Pandas, executa no terminal:
pip install pandas

