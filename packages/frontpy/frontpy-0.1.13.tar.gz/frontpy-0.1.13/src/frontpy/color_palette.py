import numpy as np
import colorsys

def read_color_palette(path):
    try:
        with open(path) as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"File {path} not found")
        return None

    x, r, g, b = [], [], [], []
    colorModel = 'RGB'

    for line in lines:
        if line.startswith('#'):
            if line.strip().endswith('HSV'):
                colorModel = 'HSV'
            continue
        
        parts = line.split()
        
        if parts[0] in ['B', 'F', 'N']:
            continue
        
        x.append(float(parts[0]))
        r.append(float(parts[1]))
        g.append(float(parts[2]))
        b.append(float(parts[3]))

        x.append(float(parts[4]))
        r.append(float(parts[5]))
        g.append(float(parts[6]))
        b.append(float(parts[7]))

    x = np.array(x)
    r = np.array(r)
    g = np.array(g)
    b = np.array(b)

    if colorModel == 'HSV':
        for i in range(r.shape[0]):
            rr, gg, bb = colorsys.hsv_to_rgb(r[i] / 360.0, g[i], b[i])
            r[i], g[i], b[i] = rr, gg, bb

    if colorModel == 'RGB':
        r, g, b = r / 255.0, g / 255.0, b / 255.0

    xNorm = (x - x[0]) / (x[-1] - x[0])

    colorDict = {
        'red':   [[xNorm[i], r[i], r[i]] for i in range(len(x))],
        'green': [[xNorm[i], g[i], g[i]] for i in range(len(x))],
        'blue':  [[xNorm[i], b[i], b[i]] for i in range(len(x))]
    }

    return colorDict