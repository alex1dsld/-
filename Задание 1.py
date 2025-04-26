import numpy as np
import matplotlib.pyplot as plt
x=[]
for i in range(11):
    x.append(i)
x=np.array(x)
plt.plot(x,x,color='orange')
plt.plot(x,2*x,color='blue')
plt.plot(x,3*x,color='green')
plt.plot(x,x**2,color='black')
plt.plot(x,2*x**2,color='yellow')
plt.show()