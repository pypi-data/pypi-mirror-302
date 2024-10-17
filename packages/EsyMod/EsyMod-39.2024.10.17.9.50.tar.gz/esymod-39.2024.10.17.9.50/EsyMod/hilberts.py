import EsyPro
sfs = EsyPro.ScriptFileSaver(__file__, locals())

import torch

def hilbert_curve(n):
    def hilbert(x, y, xi, xj, yi, yj, n):
        if n <= 0:
            return [(x + (xi + yi) // 2, y + (xj + yj) // 2)]
        else:
            points = []
            points += hilbert(x, y, yi // 2, yj // 2, xi // 2, xj // 2, n - 1)
            points += hilbert(x + xi // 2, y + xj // 2, xi // 2, xj // 2, yi // 2, yj // 2, n - 1)
            points += hilbert(x + xi // 2 + yi // 2, y + xj // 2 + yj // 2, xi // 2, xj // 2, yi // 2, yj // 2, n - 1)
            points += hilbert(x + xi // 2 + yi, y + xj // 2 + yj, -yi // 2, -yj // 2, -xi // 2, -xj // 2, n - 1)
            return points

    return hilbert(0, 0, 2**n, 0, 0, 2**n, n)


def hilbert_index_matrix(level=4):
    """
    生成希尔伯特整数矩阵
    :param dimensions: 维度
    :param bits: 每维度的位数
    :return: 希尔伯特整数矩阵
    """
    locations = hilbert_curve(level)
    matrix = torch.zeros(2**level, 2**level)
    for i, (x, y) in enumerate(locations):
        matrix[x, y] = i
    return matrix

class HilbertDecoder(torch.nn.Module):
    def __init__(self, level=4):
        super().__init__()
        self.size = level
        self.matrix = hilbert_index_matrix(level).long()
    
    def forward(self, x):
        return x.T[self.matrix].T

if __name__ == '__main__':
    level = 8

    model = HilbertDecoder(level)
    
    line = torch.arange(2**(level*2))
    
    r = model(line)
    
    sfs.end_script()
