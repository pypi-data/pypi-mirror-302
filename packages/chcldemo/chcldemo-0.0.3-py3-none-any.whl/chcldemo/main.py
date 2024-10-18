"""MHGCL runner."""
from .DataProcess import PrepareBinData
from torch import optim
from .param import parameter_parser
from .Module import MHGCL
from .DataSet import Dataset_MDA
import warnings
from .trainer import train_epoch_MDA, train_epoch_MDA_ST, train_epoch_MDA_TP
import os

warnings.filterwarnings("ignore")

def run(data_dir='data', output_dir='output'):
    """
    Parsing command line parameters.
    Fitting an MHGCL.
    Saving the embedding.
    """
    opt = parameter_parser()

    # Build paths based on input parameters
    opt.Bin_data_path = os.path.join(data_dir, "782-association.csv")
    opt.SimWalk_RNA_path = os.path.join(data_dir, "MDA_mi_Walker.csv")
    opt.SimWalk_Dis_path = os.path.join(data_dir, "MDA_disease_Walker.csv")
    opt.SimST_RNA_path = os.path.join(data_dir, "MDA_mi_ST.csv")
    opt.SimST_Dis_path = os.path.join(data_dir, "MDA_disease_ST.csv")
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Configure output paths
    opt.Save_RNA_BinFeature_path = os.path.join(output_dir, "RNABinFea.csv")
    opt.Save_DIS_BinFeature_path = os.path.join(output_dir, "DISBinFea.csv")
    opt.Save_RNAWalkerFeature_path = os.path.join(output_dir, "RNAWalkerFea.csv")
    opt.Save_DISWalkerFeature_path = os.path.join(output_dir, "DISWalkerFea.csv")
    opt.Save_RNA_STFeature_path = os.path.join(output_dir, "RNASTFea.csv")
    opt.Save_DIS_STFeature_path = os.path.join(output_dir, "DISSTFea.csv")

    dataset = PrepareBinData(opt)
    model_MDA = MHGCL(opt.mi_num, opt.dis_num, opt.hidden_list, opt.proj_hidden)
    optimizer = optim.Adam(model_MDA.parameters(), lr=0.0001)
    train_data_MDA = Dataset_MDA(opt, dataset)

    train_epoch_MDA(model_MDA, train_data_MDA[0], optimizer, opt)
    train_epoch_MDA_ST(model_MDA, train_data_MDA[0], optimizer, opt)
    train_epoch_MDA_TP(model_MDA, train_data_MDA[0], optimizer, opt)

    return 0



if __name__ == "__main__":

    run()
