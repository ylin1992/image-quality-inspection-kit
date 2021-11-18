from algo.filters.log import LaplacianOfGaussianFilter

def test():
    import matplotlib.pyplot as plt
    shape = (100,100)
    g = LaplacianOfGaussianFilter(shape=shape, sigma_x=0.1, sigma_y=0.0, type='lp', dir='h')
    print(g.get_frequency_para())
    plt.figure()
    plt.imshow(g.get_filt())
    plt.show()
test()