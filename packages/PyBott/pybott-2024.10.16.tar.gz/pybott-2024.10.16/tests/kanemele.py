#!/usr/bin/env python

"""This module implements a finite 2D Kane-Mele model to compute the
density of states (DOS) and visualize a topologically protected edge
state. The Kane-Mele model is designed to capture quantum spin Hall
states and includes spin-orbit coupling and Rashba interactions. 

Key Functions:
- `get_finite_kane_mele`: Builds a finite Kane-Mele model with a specified number of supercells.
- `plot_dos`: Plots the density of states (DOS) based on the eigenvalues.
- `plot_edge_state`: Visualizes the spatial density of a selected edge state.

"""

from pythtb import *
import numpy as np
import matplotlib.pyplot as plt
from pybott.spin_bott import spin_bott

def get_finite_kane_mele(nx=6, ny=6, t1=1, esite=0,  t2=0, rashba=0.25, pbc=True):
    """
    Returns a finite Kane-Mele model with nx sites along the x-axis and ny sites along the y-axis.

    Args:
        nx (int): Number of sites along the x-axis.
        ny (int): Number of sites along the y-axis.
        esite (float): On-site energy for the Kane-Mele model.
        t2 (float): Strength of the spin-orbit coupling (second neighbor hopping).
        rashba (float): Strength of the Rashba coupling.

    Returns:
        tb_model: A finite tight-binding model representing the Kane-Mele system.
    """
    
    # Define lattice vectors and atomic site coordinates
    lat = [[1.0, 0.0], [0.5, np.sqrt(3.0)/2.0]]
    orb = [[1./3., 1./3.], [2./3., 2./3.]]
    
    # Create the 2D Kane-Mele model with nx * ny supercells
    model = tb_model(2, 2, lat, orb, nspin=2)
    
    spin_orb = t2

    
    # Set on-site energies
    model.set_onsite([esite, -esite])
    
    # Useful definitions for spin matrices
    sigma_x = np.array([0., 1., 0., 0])
    sigma_y = np.array([0., 0., 1., 0])
    sigma_z = np.array([0., 0., 0., 1])
    
    # First-neighbor hopping (without spin)
    model.set_hop(t1, 0, 1, [0, 0])
    model.set_hop(t1, 0, 1, [0, -1])
    model.set_hop(t1, 0, 1, [-1, 0])
    
    # Second-neighbor hopping with spin-orbit interaction (s_z)
    model.set_hop(-1.j * spin_orb * sigma_z, 0, 0, [0, 1])
    model.set_hop(1.j * spin_orb * sigma_z, 0, 0, [1, 0])
    model.set_hop(-1.j * spin_orb * sigma_z, 0, 0, [1, -1])
    model.set_hop(1.j * spin_orb * sigma_z, 1, 1, [0, 1])
    model.set_hop(-1.j * spin_orb * sigma_z, 1, 1, [1, 0])
    model.set_hop(1.j * spin_orb * sigma_z, 1, 1, [1, -1])
    
    # Rashba (first-neighbor hopping with spin)
    r3h = np.sqrt(3.0) / 2.0
    model.set_hop(1.j * rashba * (0.5 * sigma_x - r3h * sigma_y), 0, 1, [0, 0], mode="add")
    model.set_hop(1.j * rashba * (-1.0 * sigma_x), 0, 1, [0, -1], mode="add")
    model.set_hop(1.j * rashba * (0.5 * sigma_x + r3h * sigma_y), 0, 1, [-1, 0], mode="add")
    
    # Create a finite model (e.g., a ribbon of size nx * ny)
    tmp_model = model.cut_piece(nx, 0, glue_edgs=pbc)
    fin_model = tmp_model.cut_piece(ny, 1, glue_edgs=pbc)

    (evals, evecs) = fin_model.solve_all(eig_vectors=True)
    
    return fin_model

def plot_dos(evals, eta=0.05, num_bins=200):
    """
    Plot the density of states (DOS) based on the eigenvalues.

    Args:
        evals (array): Array of eigenvalues of the system.
        eta (float, optional): A small broadening parameter for visualization. Defaults to 0.05.
        num_bins (int, optional): Number of bins for the histogram. Defaults to 200.

    Returns:
        None: Displays the DOS plot.
    """
    plt.figure(figsize=(6, 4))
    plt.hist(evals, color="black", bins=num_bins)
    plt.xlabel('Energy')
    plt.ylabel('Density of States (DOS)')
    plt.title('Density of States (DOS)')
    plt.axvline(x=evals[evals.shape[0] // 2], color="red")
    plt.show()

def plot_edge_state(model, evals, vecs, state_index, nx, ny):
    """
    Visualize the density of a localized edge state.

    Args:
        model (tb_model): The tight-binding model.
        evals (array): Array of eigenvalues of the system.
        vecs (array): Array of eigenvectors of the system.
        state_index (int): Index of the edge state to visualize.
        nx (int): Number of sites along the x-axis.
        ny (int): Number of sites along the y-axis.

    Returns:
        None: Displays and saves a plot of the edge state's spatial density.
    """
    (fig, ax) = model.visualize(0, 1, eig_dr=vecs[state_index, :, 1], draw_hoppings=False)
    ax.set_title("Edge state for finite model without periodic direction")
    ax.set_xlabel("x coordinate")
    ax.set_ylabel("y coordinate")
    fig.tight_layout()
    fig.savefig("edge_state.pdf")
    plt.show()

if __name__ == "__main__":
    # Parameters for the finite Kane-Mele model
    nx, ny = 10, 10
    t1 = 1
    esite = 1
    t2 = 0.23
    rashba = 0.2

    threshold_psp = -0.1
    threshold_energy = -0.0

    # Build the Kane-Mele model and solve for eigenvalues/eigenvectors
    model = get_finite_kane_mele(nx, ny, t1, esite, t2, rashba)
    (evals, vecs) = model.solve_all(eig_vectors=True)

    # Plot the density of states
    plot_dos(evals)

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
    c_sb = spin_bott(lattice_x2, evals, vr_list, sigma, evals[N_sites // 2], -0.1, True, f"spectrum_psp_{rashba}")
    print(f"{esite=},{t2=},{c_sb=}")
    exit()
    
    # Calculate and print the spin Bott index for all eigenvalues
    asb = pb.all_spin_bott(lattice_x2, evals, vr_list, sigma, evals[N_sites // 2])
    print(f"{esite=},{t2=},{asb=}")
