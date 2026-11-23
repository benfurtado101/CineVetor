import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
const root=fileURLToPath(new URL('..',import.meta.url));
const py=process.platform==='win32'?'python':'python3';
execFileSync(py,['scripts/assets.py'],{cwd:root,stdio:'inherit'});
execFileSync(py,['scripts/package_source.py'],{cwd:root,stdio:'inherit'});
