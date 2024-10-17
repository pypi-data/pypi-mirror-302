import numpy as np

from pybott import spin_bott
import kanemele as km

# Parameters for the finite Kane-Mele model
nx, ny = 10, 10
t1 = 1
esite = 1
t2 = 0.23
rashba = 0.2

threshold_psp = -0.1
threshold_energy = -0.0

# Build the Kane-Mele model and solve for eigenvalues/eigenvectors
model = km.get_finite_kane_mele(nx, ny, t1, esite, t2, rashba)
(evals, vecs) = model.solve_all(eig_vectors=True)

N_sites = evals.shape[0]

vr_list = []
for i in range(N_sites):
    vr = np.concatenate((vecs[i, :, 0], vecs[i, :, 1]))
    vr_list.append(vr)
    
def get_sigma_bott(N):
    """Return the σ_z spin operator for Bott index calculation."""
    return np.kron(np.array([[1, 0], [0, -1]]), np.eye(N))

sigma = get_sigma_bott(N_sites // 2)

lattice = model.get_orb()
lattice_x2 = np.concatenate((lattice, lattice))

# Calculate and print the spin Bott index
c_sb = spin_bott(lattice_x2, evals, vr_list, sigma, evals[N_sites // 2], -0.1,)
print(f"{esite=},{t2=},{c_sb=}")
