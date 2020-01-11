---
{
  "title": "Notebook with inline plots",
  "subtitle": "Generic subtitle",
  "date": "2018-03-03",
  "slug": "notebook-with-inline-plots"
}
---
Let's do an inline plot

```python
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline
```


```python
x = np.linspace(-np.pi, np.pi, 201)
plt.plot(x, np.sin(x))
plt.xlabel('Angle [rad]')
plt.ylabel('sin(x)')
plt.axis('tight')
plt.show()
```


![png](/img/Notebook%20with%20inline%20plots_2_0.png)

