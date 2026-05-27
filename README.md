# RPA - Validador e Consultor de CEP 🚀

Uma ferramenta de automação (RPA) desenvolvida em Python com interface gráfica (GUI) que lê uma planilha Excel contendo uma lista de CEPs, consulta as informações de endereço de forma automática através da API pública do ViaCEP e gera um novo arquivo formatado para download.

O grande diferencial deste projeto é o uso de **Multithreading**, o que impede que a interface gráfica trave ou fique congelada (sem responder) enquanto o processamento em lote é realizado em segundo plano.

---

## Funcionalidades

* **Interface Gráfica:** Desenvolvida com `Tkinter`, simples e intuitiva.
* **Processamento em Lote:** Importe uma planilha `.xlsx` ou `.xls` com dezenas ou centenas de linhas.
* **Preenchimento Automático:** Identifica a coluna `CEP` e adiciona as colunas `Logradouro`, `Bairro`, `Cidade` e `Estado`.
* **Tratamento de Erros e Validação:** Identifica CEPs inválidos, não encontrados ou problemas de conexão sem interromper o fluxo das outras linhas.
* **Barra de Progresso em Tempo Real:** Acompanhe exatamente qual linha está sendo consultada.
* **Segurança dos Dados:** O arquivo original **nunca** é alterado. O sistema gera uma cópia na memória e permite escolher onde salvar o novo arquivo processado.

---

## 🛠️ Tecnologias Utilizadas

* **[Python](https://www.python.org/):** Linguagem base do projeto.
* **[Pandas](https://pandas.pydata.org/):** Manipulação, leitura e exportação dos dados do Excel.
* **[Requests](https://requests.readthedocs.io/):** Consumo da API HTTP do ViaCEP.
* **[Tkinter](https://docs.python.org/3/library/tkinter.html):** Construção da interface visual (GUI).
* **[Threading](https://docs.python.org/3/library/threading.html):** Execução do processo em segundo plano para manter a interface responsiva.


Desenvolvido por Erica Franco Fidelis.

