# Agrupamento de Texto usando Notícias do InfoMoney e Ferramentas de LLM

## Objetivo

Este projeto tem como objetivo colocar em prática os conhecimentos adquiridos no **Capítulo 5** do livro *Hands-On Large Language Models*, focando em técnicas de agrupamento de texto aplicadas a notícias financeiras.

## Metodologia

### 1. Coleta de Dados
- Desenvolvimento de um scraper automatizado para extrair notícias do site InfoMoney
- Criação de um dataset com artigos financeiros em português

### 2. Pipeline de Processamento
Seguindo a metodologia sugerida pelo livro, implementei o seguinte pipeline:

1. **Embedding Generation**: Conversão dos documentos de entrada em embeddings utilizando um modelo de embedding
2. **Dimensionality Reduction**: Redução da dimensionalidade dos embeddings com técnicas apropriadas
3. **Clustering**: Identificação de grupos de documentos semanticamente similares através de algoritmos de clustering

### 3. Análise Detalhada
Para mais detalhes sobre a implementação e análise dos resultados, consulte o **Jupyter Notebook** do projeto.

## Resultados

A tabela abaixo apresenta os tópicos identificados antes e após o processamento:

| Topic | Original | Updated |
|-------|----------|---------|
| 0 | de \| que \| os \| em \| uma | traders \| mystic \| texas \| eua \| amber |
| 1 | de \| com \| do \| em \| pontos | ibovespa \| shoppings \| em142 \| em143 \| oifr |
| 2 | de \| do \| que \| da \| em | cazétv \| pilgrim \| tv \| paulo \| fhc |
| 3 | de \| em \| no \| na \| do | fluminense \| chelsea \| ufrj \| paulo \| guarulhos |
| 4 | de \| vibra \| da \| natura \| que | societário \| etanol \| reuters \| bdr \| chairman |

## Análise dos Resultados

### Observações Principais:
- **Tópico 0**: Relacionado a traders e mercado americano (EUA, Texas)
- **Tópico 1**: Focado no mercado brasileiro (Ibovespa, shopping centers)
- **Tópico 2**: Mídia e comunicação (TV, personalidades públicas)
- **Tópico 3**: Esportes e instituições (Fluminense, Chelsea, UFRJ)
- **Tópico 4**: Mercado corporativo (aspectos societários, combustíveis, BDRs)

### Melhorias Identificadas:
- A versão "Updated" mostra termos mais específicos e informativos
- Redução significativa de palavras funcionais (preposições, artigos)
- Melhor separação semântica entre os clusters

## Tecnologias Utilizadas

- **Python**: Linguagem principal do projeto
- **Jupyter Notebook**: Ambiente de desenvolvimento e análise
- **Modelos de Embedding**: Para conversão de texto em vetores
- **Algoritmos de Clustering**: Para agrupamento semântico
- **Web Scraping**: Para coleta automatizada de dados

## Próximos Passos

- Implementar avaliação quantitativa dos clusters
- Testar diferentes modelos de embedding
- Expandir o dataset com mais fontes de notícias
- Desenvolver interface web para visualização dos resultados

## Referências

- *Hands-On Large Language Models* - Capítulo 5
- [InfoMoney](https://www.infomoney.com.br/) - Fonte dos dados
