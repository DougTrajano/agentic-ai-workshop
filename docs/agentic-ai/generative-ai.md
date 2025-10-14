# Generative AI: A Base da Agentic AI

**Generative AI** é um tipo de inteligência artificial capaz de gerar conteúdo original, como texto, imagens, música, vídeo e código, a partir de uma solicitação (prompt)[^1].

Esses modelos são treinados em grandes volumes de dados e aprendem padrões complexos para criar novos dados combinando os dados de treinamento com a solicitação do usuário.

## :brain: Large Language Models (LLMs)

Os **Large Language Models (LLMs)** são modelos treinados em grandes volumes de textos, capazes de entender e gerar linguagem natural e resolver várias tarefas[^2].

- **GPT-5** (OpenAI)
- **Claude Sonnet 4.5** (Anthropic)
- **Gemini 2.5 Pro** (Google)
- **Llama 4** (Meta)

![Transformer Explainer](https://miro.medium.com/v2/resize:fit:1400/1*iCKo6UH8I285n329j3YbBA.png)
///Caption
[Transformer Explainer: LLM Transformer Model Visually Explained](https://poloclub.github.io/transformer-explainer/)
///

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

```md
The theory of relativity, developed by Albert Einstein, ...
```

## :material-vector-polyline: Embedding Models

Transformam textos, imagens ou outros objetos em vetores numéricos que preservam relações semânticas, viabilizando buscas por similaridade e integração em aplicações de IA[^3].

![Embedding Model](https://weaviate.io/assets/images/embedding_model-83a51fb9487ceeb03d7af8aeccde3ffb.png)

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

```python
[-0.002306425, 0.003677662, 0.007123456, ...]
```

## :art: Diffusion Models

Geram dados (ex.: imagens de alta qualidade) aplicando ruído sucessivo nos dados de treinamento e aprendendo a reverter esse processo[^4]. Este mecanismo é usado em:

- **Sora** (OpenAI)
- **Stable Diffusion** (Stability AI)
- **Midjourney**
- **Gemini 2.5 Flash Image (Nano Banana)** (Google)

![Google Gemini 2.5 Flash Image (Nano Banana)](https://www.gstatic.com/aistudio/welcome/v3/native_image_generation_hero.png)

## :material-multimedia: Multimodal Models

Um modelo multimodal pode receber uma foto de um prato de comida e gerar automaticamente uma receita detalhada, ou analisar um gráfico em uma imagem e explicar os insights em texto. Eles processam múltiplas modalidades (texto, imagem, áudio, vídeo) nativamente[^6].

<div class="grid cards" markdown>

-   **GPT-5**

    ---

    - Input: text, images, and audio.
    - Output: text.

-   **Gemini 2.5 Pro**

    ---

    - Input: Text, Image, Video, Audio, PDF
    - Output: Text

-   **Claude Sonnet 4.5**

    ---

    - Input: Text, Image
    - Output: Text

-   **Llama 4**

    ---

    - Input: Text, Image
    - Output: Text

-   **Grok 4**

    ---

    - Input: Text, Image
    - Output: Text

</div>

![Multimodal Example](https://lh3.googleusercontent.com/-Ps0G2TK1Q-LUbTU0vowBhng7sKV8BiFigEmmm7ub5bxC2lV8hg81EjYAB4Eij4meyRLTSu1Txim=s944-w944-rw-lo)

---

[^1]: [What is Generative AI? - AWS](https://aws.amazon.com/what-is/generative-ai/)
[^2]: [What Are Large Language Models (LLMs)? - IBM](https://www.ibm.com/think/topics/large-language-models)
[^3]: [What are embeddings in machine learning? - Cloudflare](https://www.cloudflare.com/learning/ai/what-are-embeddings/)
[^4]: [Introduction to Diffusion Models - AssemblyAI](https://www.assemblyai.com/blog/diffusion-models-for-machine-learning-introduction)
[^6]: [What is Multimodal AI? - IBM](https://www.ibm.com/think/topics/multimodal-ai)