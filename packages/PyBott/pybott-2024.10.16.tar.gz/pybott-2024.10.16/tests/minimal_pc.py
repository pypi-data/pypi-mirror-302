import numpy as np

from pybott import bott,sorting_eigenvalues

ham = np.load("effective_hamiltonian_light_honeycomb_lattice.npy")
# The matrix is loaded directly because calculating it is not straightforward.
# For more details, refer to Antezza and Castin: https://arxiv.org/pdf/0903.0765
grid = np.load("honeycomb_grid.npy") # Honeycomb structure
omega = 7

delta_b = 12
delta_ab = 5

def break_symmetries(M, delta_B, delta_AB):
    '''
    This function breaks either TRS or inversion symmetry
    '''
    N = M.shape[0] // 2
    for i in range(N):
        if i < N // 2:
            delta_AB = -delta_AB
        M[2 * i, 2 * i] = 2 * delta_B + 2 * delta_AB
        M[2 * i + 1, 2 * i + 1] = -2 * delta_B + 2 * delta_AB

    return M

modified_ham = break_symmetries(ham, delta_b, delta_ab)

eigenvalues, eigenvectors = np.linalg.eig(modified_ham)

eigenvalues, eigenvectors = sorting_eigenvalues(
    eigenvalues, eigenvectors, True
)

frequencies = -np.real(eigenvalues) / 2

b_pol = bott(
    grid,
    eigenvectors,
    frequencies,
    omega,
    orb=2,
    dagger=True
)

print(f"The Bott index for the given parameters Δ_B={delta_b} and Δ_AB={delta_ab} is: {b_pol}")

