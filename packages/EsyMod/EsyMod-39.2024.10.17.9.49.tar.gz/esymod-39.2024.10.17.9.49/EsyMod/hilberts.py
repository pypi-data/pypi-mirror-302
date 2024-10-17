import EsyPro
sfs = EsyPro.ScriptFileSaver(__file__, locals())


from hilbert import decode, encode
import torch

def hilbert_index_matrix(size=4):
    """
    生成希尔伯特整数矩阵
    :param dimensions: 维度
    :param bits: 每维度的位数
    :return: 希尔伯特整数矩阵
    """
    hilbert_integers = torch.arange(size ** 2)
    locations = decode(hilbert_integers, 2, size)
    matrix = torch.zeros(size, size)
    for i, (x, y) in enumerate(locations):
        matrix[x, y] = hilbert_integers[i]
    return matrix

class HilbertDecoder(torch.nn.Module):
    def __init__(self, size=4):
        super().__init__()
        self.size = size
        self.hilbert_integers = torch.arange(size ** 2)
        self.locations = decode(self.hilbert_integers, 2, size)
        self.matrix = torch.zeros(size, size)
        for i, (x, y) in enumerate(self.locations):
            self.matrix[x, y] = self.hilbert_integers[i]
        self.matrix = self.matrix.long()
    
    def forward(self, x):
        return x.T[self.matrix].T

if __name__ == '__main__':

    model = HilbertDecoder(16)
    
    line = torch.arange(16*16)
    
    r = model(line)
    
    sfs.end_script()
