from __future__ import annotations
import time
import numpy as np

def accel(r, mu=1.0):
    """Compute gravitational acceleration."""
    rnorm = np.linalg.norm(r)
    return -mu * r / (rnorm**3)

def energy(r, v, mu=1.0):
    """Specific orbital energy."""
    return 0.5 * np.dot(v, v) - mu / np.linalg.norm(r)

def angular_momentum_z(r, v):
    """Scalar z-component of angular momentum in 2D."""
    return r[0]*v[1] - r[1]*v[0]

def integrate(r0: np.ndarray, v0: np.ndarray, mu: float, t_final: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Integrate planar two-body motion from t=0 to t_final.

    Parameters
    ----------
    r0 : np.ndarray
        Initial position vector shape (2,) in Cartesian coordinates (x, y).
        Must be finite and non-zero length (cannot start at the singularity r=0).
    v0 : np.ndarray
        Initial velocity vector shape (2,) (vx, vy). Must contain finite floats.
    mu : float
        Gravitational parameter (GM). For this challenge it is fixed to 1.0.
    t_final : float
        Final simulation time (> 0). The solver should advance from t=0 up to
        exactly t_final (inclusive or very close within floating-point tolerance).

    Returns
    -------
    times : np.ndarray
        1D array shape (N,) strictly increasing, with times[0] == 0.0 and
        times[-1] approximately t_final. N depends on your chosen step strategy.
    positions : np.ndarray
        2D array shape (N, 2). positions[i] gives (x, y) at times[i]. Must not
        contain NaN or Inf; orbit should remain bound for all samples.
    velocities : np.ndarray
        2D array shape (N, 2). velocities[i] gives (vx, vy) at times[i]. Same
        finiteness constraints as positions.

    Expected Invariants 
    --------------------
    - Energy drift |E(t_end) - E(0)| / |E(0)| should remain small.
    - Angular momentum about origin should be nearly constant.


    Choice of Method
    -------
    I've used rk4 as my stepper, due to it being efficient while providing correct results. The 
    energy drift is relatively minimal especially when comparing it to the Euler method, and it
    is very easy to implement. I also only saved the position/velocity every 10th point, while 
    still advancing the stepper every point, in order to maximise efficiency and still have
    coherent results.
    """
    # Setting up variables
    dt = 0.001
    skip = 10
    N = int(t_final/(dt)) + 1
    N_saved = N //skip
    T = np.zeros(N_saved)
    positions = np.zeros((N_saved,2))
    velocities = np.zeros((N_saved,2))
    T[0] = 0.0
    positions[0] = r0.copy()
    velocities[0] = v0.copy()
    t = 0.0
    r = r0.copy()
    v = v0.copy()
    save_index = 0
    # Integration Loop, saves the points every 10th point for performance
    for i in range (1, N):
        r, v = stepper(t, r, v, dt, mu)
        t += dt
        if i % skip == 0:
            T[save_index] = t
            positions[save_index] = r
            velocities[save_index] = v
            save_index += 1
    return T, positions, velocities


def stepper(t:float, r:np.ndarry, v:np.ndarray, dt:float, mu:float):
    """RK4 Stepper function

    Parameters
    ----------
    t : float
        Initial time (>= 0)
    r : np.ndarray
        Current position, vector shape (2,) in Cartesian coordinates (x, y)
        Must be finite and non-zero length (cannot start at the singularity r=0).
    v : np.ndarray
        Current velocity vector shape (2,) (vx, vy). Must contain finite floats.
    mu : float
        Gravitational parameter (GM). For this challenge it is fixed to 1.0.
    dt: float
        Time step value. Must be non zero

    Returns
    -------
    r : np.ndarray
        Next position, vector shape (2,) in Cartesian coordinates (x, y)
    v : np.ndarray
        Next velocity vector shape (2,) (vx, vy)
    """
    y = np.hstack((r,v))
    ### rk4 Stepper
    k1 = dynamics(t,y, mu)
    k2 = dynamics(t + dt*0.5, y + dt*0.5*k1, mu)
    k3 = dynamics(t + dt*0.5, y + dt*0.5*k2, mu)
    k4 = dynamics(t + dt, y + dt*k3, mu)
    y_n_plus_one = y + dt/6 * (k1 + 2*k2 + 2*k3 + k4)
    r = y_n_plus_one[:2]
    v = y_n_plus_one[2:]
    return r, v

def dynamics(t:float, y:np.ndarray, mu:float):
    """RK4 Stepper function

    Parameters
    ----------
    t : float
        Initial time (>= 0)
    y : np.ndarray
        Current position/velocity, vector shape (4,) in Cartesian coordinates (x, y, vx, vy)
        Must be finite and non-zero length for the position  (cannot start at the singularity r=0).
    mu : float
        Gravitational parameter (GM). For this challenge it is fixed to 1.0.

    Returns
    -------
    y : np.ndarray
        Next position/velocity, vector shape (4,) in Cartesian coordinates (x, y, vx, vy)
    """
    ### Calculates acceleration using two body approximation
    r = y[:2]
    v = y[2:]
    a = accel(r,mu)
    y = np.hstack((v, a))
    return y



def run_orbit(A, E):
    R_P = A * (1 - E)
    V_P = np.sqrt(MU * (1 + E) / (A * (1 - E)))
    T_ORBIT = 2 * np.pi * np.sqrt(A**3 / MU)
    T_TOTAL = 100 * T_ORBIT
    r0 = np.array([R_P, 0.0], dtype=np.float64)
    v0 = np.array([0.0, V_P], dtype=np.float64)

    start = time.perf_counter()
    t, r, v = integrate(r0, v0, MU, T_TOTAL)
    runtime_ms = (time.perf_counter() - start) * 1000.0

    E0 = energy(r[0], v[0], MU)
    L0 = angular_momentum_z(r[0], v[0])
    E_end = energy(r[-1], v[-1], MU)
    L_end = angular_momentum_z(r[-1], v[-1])

    energy_drift = abs(E_end - E0) / abs(E0)
    angular_drift = abs(L_end - L0) / abs(L0)

    result = {
        "energy_drift": float(energy_drift),
        "angular_momentum_drift": float(angular_drift),
        "runtime_ms": float(runtime_ms),
        "n_points": len(t)
    }

    return result

MU = 1.0
A = 1.0
E = 0.95
print(run_orbit(A,E))