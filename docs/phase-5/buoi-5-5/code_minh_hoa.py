# -*- coding: utf-8 -*-
import numpy as np

tokens=["A","B","C"]
inputs=tokens[:-1]; targets=tokens[1:]
print("Inputs:",inputs,"Targets:",targets)
# Xác suất đúng của hai next-token predictions được cấp trong fixture.
true_token_prob=np.array([.5,.25])
nll=-np.log(true_token_prob).mean()
perplexity=np.exp(nll)
print("Mean NLL:",round(nll,6),"Perplexity:",round(perplexity,6))
assert np.isclose(perplexity,np.sqrt(8))
# Không so perplexity giữa các tokenizers khác nhau như cùng một metric.
