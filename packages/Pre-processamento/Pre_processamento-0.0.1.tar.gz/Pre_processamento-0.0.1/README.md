# Pre_processamento

**Descrição**: 

O pacote **Pre_processamento** oferece uma solução eficiente para o pré-processamento de texto em português e inglês, facilitando a preparação de corpus para tarefas de NLP (Processamento de Linguagem Natural). Ele integra diversas etapas de limpeza e normalização do texto, removendo ruídos e transformando o conteúdo para que esteja pronto para análise, classificação ou modelagem. Utiliza a biblioteca **spaCy**, garantindo suporte a modelos avançados de linguagem para ambos os idiomas.

**Etapas do Pre-processamento:**

**1. Detecção e Carregamento Automático de Modelos SpaCy:**

- O pacote tenta carregar automaticamente o maior modelo SpaCy disponível (large, medium ou small) para o idioma em questão.
- Exemplo: Se os modelos "large" e "medium" não estiverem disponíveis, o modelo "small" será carregado.

**2. Conversão para Minúsculas:**

- Todo o texto é convertido para minúsculas, garantindo uniformidade e padronização para facilitar as comparações entre palavras.
- Exemplo: "Hello World!" ➔ "hello world!"

**3. Remoção de URLs:**

- Todos os links (URLs) que começam com 'http', 'https' ou 'www' são removidos do texto, eliminando conteúdos irrelevantes como referências a sites.
- Exemplo: "Visite https://site.com para mais informações" ➔ "Visite para mais informações."

**4. Remoção de Menções e Hashtags:**

- Menções a usuários (como @usuário) e hashtags (como #exemplo) são removidas automaticamente, filtrando elementos típicos de redes sociais.
- Exemplo: "@joao, veja o #exemplo" ➔ "veja o."

**5. Remoção de Emojis:**

- O pacote utiliza expressões regulares para detectar e remover uma ampla gama de emojis do texto.
- Exemplo: "Estou feliz 😊" ➔ "Estou feliz."

**6. Remoção de Pontuações e Caracteres Especiais:**

- O pacote remove todos os caracteres especiais e pontuações, exceto letras e números.
- Exemplo: "Olá, tudo bem!?" ➔ "Olá tudo bem"

**7. Lematização:**

- O pacote aplica a técnica de lematização, que converte cada palavra para sua forma básica ou "lemma".
- Exemplo: "correram" ➔ "correr"

**8. Remoção de Stopwords:**

- As stopwords (palavras comuns e geralmente irrelevantes para análises, como "e", "de", "o", "para") são removidas com base nas listas pré-definidas do SpaCy, específicas para inglês e português.
- Exemplo: "o gato e o cachorro" ➔ "gato cachorro"

**9. Filtragem de Tokens:**

- Tokens numéricos e tokens com menos de dois caracteres são eliminados, mantendo apenas palavras que têm relevância semântica e eliminando "ruídos" de dados.
- Exemplo: "a 123 casas" ➔ "casas"

## Instalação

Use o gerenciador de pacotes [pip](https://pip.pypa.io/en/stable/) para instalar o pacote:

```bash
pip install Pre_processamento
```

## Modo de uso

Português
```python
from Pre_processamento.Pre_pt_br import Pro_pt_br
Pro_pt_br.P_pt_br("Seu corpus em português aqui.")
```

Inglês
```python
from Pre_processamento.Pre_eng import Pro_eng
Pro_eng.P_eng("Your English corpus here.")
```
## Requisitos
Para assegurar o correto funcionamento do pacote, é necessário realizar o download dos modelos de linguagem do spaCy para português e inglês.

## Modelos do spaCy para Português

Para analisar textos em português, você pode escolher entre três tamanhos de modelos:

**pt_core_news_sm (small)**: Modelo leve e rápido.

- Benefícios: Ideal para análises rápidas ou ambientes com restrições de memória.

- Desvantagens: Menos preciso e captura menos variações linguísticas.

**Comando para instalar**
```python
python -m spacy download pt_core_news_sm
```

**pt_core_news_md (medium)**: Modelo balanceado.

- Benefícios: Melhor precisão do que o modelo "small", com um desempenho razoável.

- Desvantagens: Ocupa mais memória e tempo de processamento.

**Comando para instalar**
```python
python -m spacy download pt_core_news_md
```

**pt_core_news_lg (large)**: Modelo grande, mais preciso.

- Benefícios: Captura mais nuances linguísticas e tem maior precisão nas análises.

- Desvantagens: Mais pesado, consome mais memória e tempo de processamento.

**Comando para instalar**
```python
python -m spacy download pt_core_news_lg
```

## Modelos do spaCy para Inglês

Da mesma forma, para textos em inglês, há diferentes modelos disponíveis:

**en_core_web_sm (small)**: Modelo leve e rápido.

- Benefícios: Ótimo para tarefas simples ou quando o desempenho é uma prioridade.

- Desvantagens: Menor precisão, captura menos informações detalhadas.

**Comando para instalar**
```python
python -m spacy download en_core_web_sm
```
**en_core_web_md (medium)**: Modelo médio, balanceado.

- Benefícios: Melhor precisão em comparação com o modelo pequeno.

- Desvantagens: Um pouco mais lento e consome mais memória.

**Comando para instalar**
```python
python -m spacy download en_core_web_md
```
**en_core_web_lg (large)**: Modelo grande e mais robusto.

- Benefícios: Alta precisão, captura mais nuances do idioma.

- Desvantagens: O modelo mais pesado, consome mais recursos de memória e processamento.

**Comando para instalar**	
```python
python -m spacy download en_core_web_lg
```
## Author
Alexsandro Da Silva Bezerra

## License
[MIT](https://choosealicense.com/licenses/mit/)