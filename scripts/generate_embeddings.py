"""Optional semantic representation. Run from any directory; the site needs no Python."""
from pathlib import Path
import json
import argparse

def main():
    parser=argparse.ArgumentParser(description='Generate multilingual movie embeddings.')
    parser.add_argument('--output',default='embeddings.json')
    args=parser.parse_args()
    from sentence_transformers import SentenceTransformer
    root=Path(__file__).resolve().parents[1]
    movies=json.loads((root/'dist/movies.json').read_text(encoding='utf-8'))
    name='sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
    model=SentenceTransformer(name,device='cpu',trust_remote_code=False)
    texts=[m['description'] for m in movies]
    lengths=[len(model.tokenizer.encode(t)) for t in texts]
    truncated=sum(n>model.max_seq_length for n in lengths)
    vectors=model.encode(texts,normalize_embeddings=True,show_progress_bar=True,convert_to_numpy=True)
    payload={'schema_version':1,'model':name,'dimensions':int(vectors.shape[1]),
             'max_seq_length':model.max_seq_length,'truncated_descriptions':truncated,
             'ids':[m['id'] for m in movies],
             'descriptions':{m['id']:m['description'] for m in movies},
             'vectors':vectors.tolist()}
    path=Path(args.output)
    path.write_text(json.dumps(payload,ensure_ascii=False,allow_nan=False),encoding='utf-8')
    print(f'{len(movies)} embeddings saved to {path.resolve()}; {truncated} descriptions truncated.')

if __name__=='__main__':
    main()
