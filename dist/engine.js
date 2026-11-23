// Núcleo puro, compartilhado entre interface e testes. Sem gêneros no cálculo.
export const STOP = new Set('a o os as um uma uns umas de da do das dos e em no na nos nas por para com ao aos que se sua seu suas seus ele ela eles elas enquanto após sobre entre pelo pela pelos pelas durante através até já mais muito onde quando como ser ter tem são foi é ou ao às à num numa isso essa esse esta este também sem sob cada outro outra outros outras'.normalize('NFD').replace(/[\u0300-\u036f]/g,'').split(' '));
export function tokens(text){return (text.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').match(/[a-z0-9]+/g)||[]).filter(t=>t.length>2&&!STOP.has(t));}
export function dot(a,b){let s=0;for(let i=0;i<a.length;i++)s+=a[i]*b[i];return s;}
export function norm(a){return Math.sqrt(dot(a,a));}
export function normalize(a){const n=norm(a);return a.map(x=>n?x/n:0);}
export function cosine(a,b){const n=norm(a)*norm(b);return n?Math.max(-1,Math.min(1,dot(a,b)/n)):0;}
export function angle(sim){return Math.acos(Math.max(-1,Math.min(1,sim)))*180/Math.PI;}
export function fit(movies){
 const documents=movies.map(m=>tokens(m.description));
 const vocab=[...new Set(documents.flat())].sort();const index=new Map(vocab.map((t,i)=>[t,i]));
 const df=new Array(vocab.length).fill(0);for(const ts of documents)for(const t of new Set(ts))df[index.get(t)]++;
 const idf=df.map(d=>Math.log((1+movies.length)/(1+d))+1);
 const counts=documents.map(ts=>{const v=new Array(vocab.length).fill(0);for(const t of ts)v[index.get(t)]++;return v;});
 const raw=counts.map(v=>v.map((n,i)=>n*idf[i]));const vectors=raw.map(normalize);
 return {documents,vocab,df,idf,counts,raw,vectors,kind:'tfidf'};
}
export function profile(engine,watched,movies){const indices=watched.map(id=>movies.findIndex(m=>m.id===id)).filter(i=>i>=0);if(!indices.length)return null;const mean=new Array(engine.vectors[0].length).fill(0);for(const i of indices)engine.vectors[i].forEach((x,j)=>mean[j]+=x/indices.length);return norm(mean)?normalize(mean):null;}
export function rank(engine,watched,movies){const p=profile(engine,watched,movies);if(!p)return [];const seen=new Set(watched);return movies.map((movie,i)=>{const score=cosine(p,engine.vectors[i]);return {movie,index:i,score,angle:angle(score),distance:1-score};}).filter(r=>!seen.has(r.movie.id)).sort((a,b)=>b.score-a.score||a.movie.id.localeCompare(b.movie.id));}
export function contributions(a,b,vocab){return a.map((x,i)=>({term:vocab[i],a:x,b:b[i],product:x*b[i],index:i})).filter(r=>r.product>0).sort((a,b)=>b.product-a.product);}
export function validateEmbeddings(data,movies){
 if(!data||typeof data.model!=='string'||!Array.isArray(data.ids)||!Array.isArray(data.vectors)||data.ids.length!==movies.length||new Set(data.ids).size!==movies.length||data.vectors.length!==movies.length)throw Error('Arquivo incompatível: inclua todos os IDs do catálogo, sem duplicatas.');
 const dimensions=data.vectors[0]?.length;if(!Number.isInteger(dimensions)||dimensions<2||dimensions>4096)throw Error('Dimensões inválidas.');
 if(data.vectors.some(v=>!Array.isArray(v)||v.length!==dimensions||!v.every(Number.isFinite)||norm(v)===0))throw Error('Há vetores vazios, inconsistentes ou inválidos.');
 const lookup=new Map(data.ids.map((id,i)=>[id,data.vectors[i]]));
 if(movies.some(m=>!lookup.has(m.id)||data.descriptions?.[m.id]!==m.description))throw Error('Descrições ou IDs não correspondem a esta versão do catálogo. Gere o arquivo novamente.');
 return {kind:'embedding',model:data.model,vectors:movies.map(m=>normalize(lookup.get(m.id)))};
}
