# CineVetor
Demonstração de Algoritmo de Recomendação por Similaridade do Cosseno

**Cinema encontra matemática.** Um laboratório interativo em português para explicar recomendações baseadas em descrições de filmes, TF-IDF, similaridade do cosseno e ângulo entre vetores.

217 filmes reais, 18 temas, lançamentos de 1980 a 2026. Inclui Matrix, Top Gun, continuações e exemplos de romance, animação, suspense, aviação, esportes, música, fantasia e outros interesses. Cada tema contém no mínimo 12 filmes. Isso é uma seleção didática, não uma cobertura de todos os gostos possíveis.

## Executar localmente

Você só precisa de um navegador moderno e Python 3 para servir os arquivos:

```sh
cd cinevetor
python -m http.server 8000 --directory dist
```

Abra `http://localhost:8000`. Em Linux/macOS, use `python3` se `python` não estiver disponível. Não abra `index.html` diretamente com `file://`: módulos ES e `fetch` precisam de HTTP.

Não é necessário instalar pacotes npm, obter API keys ou criar uma conta. O modo padrão usa JavaScript nativo, com todos os assets locais. O histórico fica em `localStorage` no navegador; limpar o histórico apaga os favoritos. A seleção de filmes é interpretada como “assisti e gostei”, não como toda reprodução efetivamente assistida.

## Publicar no GitHub Pages

1. Crie um repositório e envie o conteúdo da pasta `cinevetor` extraída, incluindo `.github/workflows/pages.yml`. `package.json`, `dist/` e `.github/` devem estar na raiz do repositório.
2. Use a branch `main` ou ajuste a branch no workflow.
3. Vá a **Settings → Pages → Build and deployment → Source → GitHub Actions**.
4. Execute **Actions → Deploy GitHub Pages → Run workflow**, ou faça um novo push em `main`.
5. Ao terminar, o job `deploy` fornece a URL. Caminhos relativos funcionam tanto na raiz quanto em `usuario.github.io/repositorio/`.

O workflow regenera o catálogo e o ZIP de código, executa os testes e publica `dist/`. Os arquivos pré-gerados já estão incluídos; pode hospedar essa pasta em qualquer servidor estático. Nenhuma conta GitHub foi modificada por esta entrega.

Referência oficial: https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages

## O que explorar

- **Descobrir:** presets, favoritos, recomendações, busca por título/descrição, tema, década, paginação e detalhes.
- **Laboratório:** comparação filme × filme ou perfil × filme; ângulo em graus; similaridade; distância; desenho dos vetores; etapas dos dados; tabela de contribuição por palavra; CSV de todos os candidatos.
- **Como funciona:** processamento, TF-IDF, perfil, cosseno e operação conceitual em plataformas.
- **O projeto:** documentação, referências, créditos e download de todo o código.

Os botões de extremos no laboratório usam dados reais: o mesmo vetor para 0°, e um filme sem termos em comum para 90°. O segundo botão ativa explicitamente o modo TF-IDF. Não altera os scores para forçar uma resposta.

## Matemática usada de fato

1. Minúsculas, remoção de acentos/pontuação, stopwords em português e tokens com até dois caracteres. Sem stemming, lematização ou sinônimos ocultos.
2. Um vocabulário comum é ajustado **sobre todas as descrições** do catálogo. Título, ano e tema não participam.
3. TF é a contagem bruta. `idf(t) = ln((1 + N) / (1 + df(t))) + 1`, onde df conta documentos que contêm o termo.
4. Multiplicar TF por IDF e normalizar cada vetor em L2.
5. Perfil = média dos vetores dos favoritos, seguida de nova normalização L2. Todos recebem peso igual.
6. `s(a,b) = (a · b) / (||a||₂ ||b||₂)`; `ângulo = arccos(s) × 180/π`; `distância = 1 − s`.
7. Excluir favoritos e ordenar cosseno decrescente (ângulo crescente). IDs resolvem empates. O ranking usa precisão completa; a tela arredonda.

| Vetores | Ângulo | Cosseno | Distância |
|---|---:|---:|---:|
| Mesma direção | 0° | 1 | 0 |
| Alinhamento parcial | 60° | 0,5 | 0,5 |
| Ortogonais | 90° | 0 | 1 |
| Direções opostas, possível em embeddings | 180° | −1 | 2 |

TF-IDF tem coordenadas não negativas: 0°–90°. Embeddings podem ter coordenadas negativas: 0°–180°. O desenho 2D preserva o ângulo completo; **não** é PCA e seus eixos não correspondem a duas palavras escolhidas. A contribuição por termo é o produto dos pesos normalizados; a soma completa coincide com o cosseno.

Um vetor zero não tem ângulo definido. O núcleo retorna 0 como convenção defensiva em `cosine` para esse caso; a interface bloqueia comparação/perfil sem direção válida. O catálogo padrão tem apenas vetores não nulos. Perfis vazios não recebem recomendações.

O problema dos sinônimos é visível: “máquinas” e “inteligência artificial” não são automaticamente equivalentes. Há descrições próximas semanticamente com pouco ou nenhum termo compartilhado. Ângulos relativamente altos também podem ser os melhores disponíveis; não existe limiar universal de gosto. Cosseno não é probabilidade, avaliação de qualidade ou percentual de acerto.

## Transformer opcional, funcional e separado

O site já funciona com TF-IDF. Para experimentar representação semântica multilíngue:

```sh
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements-transformer.txt
python scripts/generate_embeddings.py --output embeddings.json
```

No site, abra **Laboratório → Carregar embeddings JSON** e selecione o arquivo gerado. O seletor “Representação” passa a permitir alternar entre TF-IDF e os embeddings. Os dados são lidos localmente, sem upload a um servidor, e ficam somente em memória até recarregar a página. O histórico permanece igual entre representações.

O script usa `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` no CPU. A primeira execução baixa os pesos e exige internet e memória compatível; não foi executada como parte desta entrega. O modelo gera representações de 384 dimensões e possui limite de sequência; o script informa quantas descrições excederam esse limite. Para comparação de execuções científicas, fixe a revisão do modelo e as versões exatas das bibliotecas no seu ambiente.

O JSON inclui modelo, IDs, descrições e vetores. O importador exige todos os 217 IDs, descrições idênticas ao catálogo, dimensões consistentes, valores finitos e vetores não nulos. Arquivos têm limite de 25 MiB. As dimensões neurais não são explicadas como se fossem palavras: o laboratório troca a tabela de termos por coordenadas e produtos. A validação estrutural não autentica quem gerou os embeddings nem a qualidade do modelo informado.

## Testar e reconstruir

Requer Node.js 22+ para testes e Python 3 para regeneração; sem instalação npm:

```sh
npm test
npm run build
```

`npm run build` regenera `movies.json`, as capas SVG e `dist/cinevetor-source.zip`. A foto local da NASA já está incluída. O ZIP exclui Git, credenciais, identidade de hospedagem, caches, ambientes Python e o próprio ZIP; ele pode ser publicado em um repositório diferente.

Há 16 testes automatizados: propriedades matemáticas, casos analíticos conhecidos, TF-IDF manual, isolamento dos metadados, normalização, todos os pares do catálogo, média do perfil, ordenação, exclusão de vistos, contribuições, exemplos temáticos e importação válida/inválida de embeddings. Os testes de exemplos são verificações didáticas, não uma avaliação estatística de acurácia. Consulte `VALIDATION.md` para o escopo verificado.

## Estrutura

| Caminho | Papel |
|---|---|
| `dist/index.html` | Estrutura, explicações e acessibilidade |
| `dist/style.css` | Visual responsivo e estados de foco |
| `dist/app.js` | Navegação, histórico, comparação e interface |
| `dist/engine.js` | Matemática pura, compartilhada com testes |
| `dist/movies.json` | Catálogo gerado |
| `dist/assets/` | Capas SVG locais e foto NASA |
| `scripts/catalog.txt` | Fonte editorial dos filmes |
| `scripts/assets.py` | Gera JSON e capas |
| `scripts/generate_embeddings.py` | Extensão opcional Sentence Transformers |
| `scripts/build.mjs` | Orquestra a reconstrução |
| `scripts/package_source.py` | Cria ZIP portátil |
| `tests/engine.test.mjs` | Testes com Node nativo |
| `.github/workflows/pages.yml` | Publicação GitHub Pages |

Para acrescentar filmes, edite `scripts/catalog.txt` no formato `Título|Ano|Descrição`, sob uma seção `@Tema`, e execute `npm run build`. Atualize contagens editoriais e testes. Os IDs atuais são posicionais: para um catálogo em evolução, migre para IDs persistentes antes de reordenar os registros, para não invalidar históricos. Embeddings devem ser regenerados quando as descrições mudarem.

## Ensino e uso real

As sinopses foram redigidas e revisadas com vocabulário coerente para permitir comparações transparentes. Isso introduz viés editorial. Não há boosting secreto, pontuações simuladas ou filtro de tema dentro do ranking. Os filtros afetam somente a exploração do catálogo.

Este sistema é **baseado em conteúdo**, não colaborativo. Em escala, plataformas podem pré-calcular embeddings, indexar vizinhos, atualizar perfis e reordenar resultados usando contexto e diversidade. Para avaliar, use dados reais consentidos, separação temporal, Recall@K/NDCG@K e testes controlados; este projeto não mede retenção, acurácia ou comportamento de usuários reais.

Limitações: sem feedback negativo, recência, pesos por intensidade de gosto, diversidade automática ou atualização dinâmica do catálogo. Um único perfil médio pode diluir interesses distintos. Nenhum algoritmo garante representar todos os gostos.

## Referências e licença

- Cosseno: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html
- TF-IDF: https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html
- Modelo: https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
- API de embeddings: https://www.sbert.net/docs/package_reference/sentence_transformer/model.html

Código, textos e artes originais: MIT. Nomes de filmes e conteúdo de terceiros não são relicenciados. Créditos e origem dos assets em `ASSETS.md`.
