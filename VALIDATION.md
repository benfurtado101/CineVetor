# Verificação da entrega

- 217 registros únicos por título/ano; IDs únicos; 18 temas com no mínimo 12 registros; anos entre 1980 e 2026; capas locais presentes.
- 16 testes de Node aprovados. Incluem todos os pares TF-IDF no intervalo 0°–90°, uma fixture TF-IDF calculável à mão, extremos conhecidos 0°/60°/90°/180°, perfil médio, excluídos os vistos e soma das contribuições.
- Oito exemplos representativos (Matrix, Top Gun, Interestelar, Antes do Amanhecer, Rocky III, Entre Facas e Segredos, Toy Story e Whiplash) encontram ao menos três candidatos do mesmo tema entre os dez primeiros. Isso é um teste de coerência didática; tema não é ground truth de relevância, nem entrada do cálculo.
- Revisão visual no navegador desktop: capa inicial, navegação, presets, comparador, 0° e 90°, etapas, histórico e busca.
- CSS inclui layouts para telas pequenas e respeita movimento reduzido. O ambiente de verificação não ofereceu emulação móvel dedicada; o layout móvel não foi validado em um aparelho físico.
- Importação de embeddings verificada com fixtures sintéticas nos testes. O modelo neural não foi baixado/executado e não há scores neurais pré-calculados nesta entrega. O script opcional teve sintaxe verificada.
- Workflow de GitHub Pages preparado a partir da documentação oficial; sua execução depende do repositório/conta do usuário e não foi realizada no GitHub.
- As descrições são resumos editoriais didáticos, não sinopses oficiais. O catálogo não passou por conferência bibliográfica individual de todos os títulos/anos.
