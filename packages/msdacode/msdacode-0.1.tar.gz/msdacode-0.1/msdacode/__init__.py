from .alexnet import alexnet
from .rnn import *
from .autoencoder import *
from .cnn import *
from .opt import *
from .reg import *
from .pre_model import *
from .filter import *



def help():
    met = '''
    1. alexnet()
    2. rnn() or lstm()
    3. autoencoder_simple() or autoencoder_noise() or autoencoder_sparse() 
    4. cnn()
    5. optimizer() or adv_optimizer()
    6. regularizer()
    7. inception()
    8. resnet()
    9. cnnfilter()
    10. dataaug()
    11. cnnmaxpool()
    12. dropout()
    '''
    print("Available methods in msdacode package:\nExample :\n\timport msda as md\n\tmd.cnn()")
    print(f"\n{met}")
    