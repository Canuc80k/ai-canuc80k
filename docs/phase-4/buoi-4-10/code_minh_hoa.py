# -*- coding: utf-8 -*-
import numpy as np

# Forward noising: x_t=sqrt(alpha_bar)*x0+sqrt(1-alpha_bar)*epsilon.
x0=np.array([1.,2.]); epsilon=np.array([.5,-1.]); alpha_bar=.25
xt=np.sqrt(alpha_bar)*x0+np.sqrt(1-alpha_bar)*epsilon
print("x0:",x0.tolist(),"xt:",xt.round(6).tolist())
# Nếu predictor dự đoán đúng noise, có thể khôi phục x0 trong fixture này.
predicted_noise=epsilon.copy()
reconstructed=(xt-np.sqrt(1-alpha_bar)*predicted_noise)/np.sqrt(alpha_bar)
print("Recovered x0:",reconstructed.round(6).tolist())
assert np.allclose(reconstructed,x0)
# Đây không phải cả diffusion model: cần network dự đoán noise và schedule nhiều bước.
