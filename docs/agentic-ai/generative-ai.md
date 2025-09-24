# Generative AI: A Base da Agentic AI

A **Generative AI** refere-se a modelos de inteligência artificial que criam conteúdo "novo" (texto, imagem, áudio) com base no que aprenderam durante o treinamento[^1]. Estes sistemas não apenas classificam ou fazem previsões, mas geram saídas originais e criativas.

## 🧠 Large Language Models (LLMs)

Os **Large Language Models (LLMs)** são modelos de base treinados em volumes massivos de dados, capazes de entender e gerar linguagem natural e resolver várias tarefas[^2]. Exemplos incluem:

- **GPT-4** (OpenAI)
- **Claude** (Anthropic)
- **Gemini** (Google)
- **Llama** (Meta)

```python
from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
  model="gpt-4o",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Explain the theory of relativity in simple terms."}
  ]
)

print(response.choices[0].message.content)
```

Output:

```
The theory of relativity, developed by Albert Einstein, ...
```

## 🎯 Embedding Models

Transformam textos, imagens ou outros objetos em vetores numéricos que preservam relações semânticas, viabilizando buscas por similaridade e integração em aplicações de IA[^3].

**Aplicações:**

- Busca semântica
- Sistemas de recomendação
- Classificação de documentos
- RAG (Retrieval-Augmented Generation)

```python
from openai import OpenAI

client = OpenAI()

response = client.embeddings.create(
  model="text-embedding-3-large",
  dimension=512,
  input="Hello, world!"
)

print(response.data[0].embedding)
```

Output:

```
[-0.002306425, 0.003677662, 0.007123456, ...]
```

## 🎨 Diffusion Models

Geram dados (ex.: imagens de alta qualidade) aplicando ruído sucessivo nos dados de treinamento e aprendendo a reverter esse processo[^4]. Este mecanismo é usado em:

- **DALL·E 2** (OpenAI)
- **Stable Diffusion** (Stability AI)
- **Midjourney**
- **Gemini 2.5 Flash Image (Nano Banana)** (Google)

![Google Gemini 2.5 Flash Image (Nano Banana)](https://www.gstatic.com/aistudio/welcome/v3/native_image_generation_hero.png)

## 🌍 Multimodal Models

Processam múltiplas modalidades (texto, imagem, áudio, vídeo) simultaneamente[^6]. Exemplos incluem:

- **GPT-4V** (visão)
- **Gemini Ultra** (multimodal)
- **Claude 3** (visão e texto)

!!! example "Exemplo Prático"
    Um modelo multimodal pode receber uma foto de um prato de comida e gerar automaticamente uma receita detalhada, ou analisar um gráfico em uma imagem e explicar os insights em texto.

---

[^1]: [What is Generative AI? - AWS](https://aws.amazon.com/what-is/generative-ai/)
[^2]: [What Are Large Language Models (LLMs)? - IBM](https://www.ibm.com/think/topics/large-language-models)
[^3]: [What are embeddings in machine learning? - Cloudflare](https://www.cloudflare.com/learning/ai/what-are-embeddings/)
[^4]: [Introduction to Diffusion Models - AssemblyAI](https://www.assemblyai.com/blog/diffusion-models-for-machine-learning-introduction)
[^6]: [What is Multimodal AI? - IBM](https://www.ibm.com/think/topics/multimodal-ai)