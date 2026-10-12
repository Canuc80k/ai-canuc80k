// Đọc JSON [{tex, display}] từ stdin, in JSON [html] ra stdout. Dùng KaTeX (MIT) đóng kèm.
const path = require('path');
const katex = require(path.join(__dirname, 'katex', 'katex.min.js'));
const items = JSON.parse(require('fs').readFileSync(0, 'utf8'));
const macros = {'\\R': '\\mathbb{R}', '\\E': '\\mathbb{E}', '\\argmin': '\\operatorname*{arg\\,min}', '\\argmax': '\\operatorname*{arg\\,max}'};
const out = items.map(({tex, display}) => katex.renderToString(tex, {displayMode: display, throwOnError: true, strict: 'ignore', macros: {...macros}}));
process.stdout.write(JSON.stringify(out));
