import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import ldl

from pythtb import *

import haldane

def localized_dirac_operator(lambda_param, x_op, y_op, ham):
    """
    Generates the localized dirac operator based on https://arxiv.org/abs/1907.11791 eq. (2.3)
    
    L_lambda(X0, Y0, H) = [[ H - lambda_3,  (X0 - lambda_1) + i*(Y0 - lambda_2) ],
                           [ (X0 - lambda_1) - i*(Y0 - lambda_2), -H + lambda_3 ]]
    
    Args:
    - x_op (numpy.ndarray): The matrix corresponding to X0 in the formula.
    - y_op (numpy.ndarray): The matrix corresponding to Y0 in the formula.
    - ham (numpy.ndarray): The matrix corresponding to H in the formula.
    - lambda_param (numpy.ndarray): A vector of three elements [lambda_1, lambda_2, lambda_3].
    
    Returns:
    - result (numpy.ndarray): The resulting matrix from the given formula, with complex entries.
    """
    
    lambda_1 = lambda_param[0]
    lambda_2 = lambda_param[1]
    lambda_3 = lambda_param[2]
    
    top_left = ham - lambda_3
    top_right = (x_op - lambda_1) + 1j * (y_op - lambda_2)
    bottom_left = (x_op - lambda_1) - 1j * (y_op - lambda_2)
    bottom_right = -ham + lambda_3
    
    result = np.block([[top_left, top_right], [bottom_left, bottom_right]])
    
    return result

def localizer_index(kappa, lambda_param, x_op, y_op, ham):
    ldo = localized_dirac_operator(lambda_param, kappa*x_op, kappa*y_op, ham)
    L, D, perm = ldl(ldo)
    # plt.imshow(np.real(D))
    # plt.show()

    n_blocks = D.shape[0] // 2
    eigenvalues = []

    for i in range(n_blocks):
        block = D[2*i:2*i+2, 2*i:2*i+2]
        vals = np.linalg.eigvals(block)
        eigenvalues.extend(vals)

    eigenvalues = np.array(eigenvalues)

    # Λ, _ = np.linalg.eig(ldo) # opt: avoid finding eigenvalues, prefer LDLT
    # return 1/2*(np.sum(np.where(Λ>=0))-np.sum(np.where(Λ<0)))
    return 1/2*(np.sum(np.where(eigenvalues>=0))-np.sum(np.where(eigenvalues<0)))
    
def haldane_model(n_side=6, t1=1, t2=0.2j, delta=0, pbc=True):
    t2c = t2.conjugate()

    lat=[[1.0,0.0],[0.5,np.sqrt(3.0)/2.0]]
    orb=[[1./3.,1./3.],[2./3.,2./3.]]

    my_model=tb_model(2,2,lat,orb)

    my_model.set_onsite([-delta,delta])

    my_model.set_hop(t1, 0, 1, [ 0, 0])
    my_model.set_hop(t1, 1, 0, [ 1, 0])
    my_model.set_hop(t1, 1, 0, [ 0, 1])

    my_model.set_hop(t2 , 0, 0, [ 1, 0])
    my_model.set_hop(t2 , 1, 1, [ 1,-1])
    my_model.set_hop(t2 , 1, 1, [ 0, 1])
    my_model.set_hop(t2c, 1, 1, [ 1, 0])
    my_model.set_hop(t2c, 0, 0, [ 1,-1])
    my_model.set_hop(t2c, 0, 0, [ 0, 1])

    # cutout finite model first along direction x
    tmp_model=my_model.cut_piece(n_side,0,glue_edgs=pbc)
    # cutout also along y direction 
    fin_model=tmp_model.cut_piece(n_side,1,glue_edgs=pbc)
    
    (evals,evecs)=fin_model.solve_all(eig_vectors=True)
    
    return fin_model.get_orb(), evals, evecs.T, fin_model._gen_ham()

if __name__ == "__main__":
    n_side = 6
    t1 = 1
    t2 = 1j
    delta = 0
    grid, eigenvalues, eigenvectors, ham = haldane_model(
        n_side=n_side, t1=t1, t2=t2, delta=delta, pbc=False
    )

    x_grid,y_grid = grid.T

    plt.scatter(x_grid,y_grid)
    plt.show()

    x_op = np.diag(x_grid)
    y_op = np.diag(y_grid)

    lambda_param = np.array([0,0,1])

    grid_size = 30
    side_length = 1
    sample = np.linspace(-side_length,side_length,grid_size)
    data_matrix = np.zeros((grid_size, grid_size))

    kappa = 1

    lambda_param = np.array([0, 0, 0])
    li = localizer_index(kappa, lambda_param, x_op, y_op, ham)
    # print(li)
    # exit()
    

    for idkappa, kappa in enumerate(np.linspace(0.1, 5, 100)):
        print(kappa)
        for idx,x in enumerate(sample):
            for idy,y in enumerate(sample):
                lambda_param = np.array([x, y, 0])
                li = localizer_index(kappa, lambda_param, x_op, y_op, ham)
                data_matrix[idx, idy] = li


        plt.imshow(data_matrix, extent=(-side_length, side_length, -side_length, side_length), origin='lower', cmap='hot', interpolation='nearest')
        plt.colorbar(label='Localizer Index')
        plt.title(f'Heatmap of Localizer Index $\\kappa={np.round(kappa,2)}$')
        plt.xlabel('X')
        plt.ylabel('Y')

        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
        plt.savefig(f"localizer/{idkappa}.png",format="png",bbox_inches='tight')
        plt.clf()
        plt.cla()

