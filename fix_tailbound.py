import re

with open(r'paper\main.tex', 'r', encoding='utf-8') as f:
    text = f.read()

# Direct string replacement for TailBound
OLD = (
    '\\emph{Step 1.} From~\\cite[Theorem~4.1]{TailBound}: $\\frac{d}{du}\\log\\lambda \\leq 2 - 6\\pi e^{2u}$\n'
    '(the dominant $n=2$ term of $\\varepsilon^*$ decays as $e^{-6\\pi e^{2u}}$, while $C(u) = O(e^{2u})$).'
)
NEW = (
    '\\emph{Step 1.} Since $C(u) = O(e^{2u})$ (ratio of polynomial-exponential terms) '
    'and the dominant $n=2$ term of $\\varepsilon^*$ decays as $e^{-6\\pi e^{2u}}$, '
    'direct logarithmic differentiation gives $\\frac{d}{du}\\log\\lambda \\leq 2 - 6\\pi e^{2u}$ '
    '(see \\texttt{docs/uniform\\_wtail\\_bound.md}).'
)
if OLD in text:
    new_text = text.replace(OLD, NEW, 1)
    print('Fixed TailBound citation')
    with open(r'paper\main.tex', 'w', encoding='utf-8') as f:
        f.write(new_text)
else:
    print('Direct match failed; TailBound still present')
    idx = text.find('TailBound')
    if idx != -1:
        print(repr(text[idx-50:idx+200]))
