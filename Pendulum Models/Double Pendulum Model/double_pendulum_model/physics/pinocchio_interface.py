try:
    import pinocchio as pin
except ImportError:
    pin = None

import numpy as np

from .double_pendulum import DoublePendulumParameters, DoublePendulumState
from .urdf import generate_urdf


class PinocchioDoublePendulum:
    """
    Interface to Pinocchio for the double pendulum.

    This class generates a URDF matching the provided parameters and loads it into Pinocchio.
    It provides methods to compute dynamics quantities using Pinocchio's efficient algorithms.
    """

    def __init__(self, params: DoublePendulumParameters | None = None) -> None:
        """Initialize the Pinocchio model with the given parameters."""
        self.params = params or DoublePendulumParameters.default()
        self.urdf_str = generate_urdf(self.params)

        if pin is None:
            raise ImportError(
                "Pinocchio is not installed. Please install it to use this class."
            )

        self.model = pin.buildModelFromXML(self.urdf_str)
        self.data = self.model.createData()

    def _get_q_v(self, state: DoublePendulumState) -> tuple[np.ndarray, np.ndarray]:
        """Extract configuration q and velocity v from the state."""
        q = np.array([state.theta1, state.theta2])
        v = np.array([state.omega1, state.omega2])
        return q, v

    def mass_matrix(self, state: DoublePendulumState) -> np.ndarray:
        """Compute the mass matrix M(q)."""
        q, _ = self._get_q_v(state)
        pin.crba(self.model, self.data, q)
        # Ensure symmetry and copy
        M = self.data.M
        return np.array(M)

    def bias_forces(self, state: DoublePendulumState) -> np.ndarray:
        """Compute the Coriolis, Centrifugal and Gravity terms: h(q, v) = C(q, v)v + g(q)."""
        q, v = self._get_q_v(state)
        return np.array(pin.rnea(self.model, self.data, q, v, np.zeros(self.model.nv)))

    def gravity_vector(self, state: DoublePendulumState) -> np.ndarray:
        """Compute the gravity vector g(q)."""
        q, _ = self._get_q_v(state)
        return np.array(pin.computeGeneralizedGravity(self.model, self.data, q))

    def forward_dynamics(
        self, state: DoublePendulumState, tau: np.ndarray
    ) -> np.ndarray:
        """Compute joint accelerations qddot = M^-1 (tau - h(q, v))."""
        q, v = self._get_q_v(state)
        return np.array(pin.aba(self.model, self.data, q, v, tau))

    def inverse_dynamics(
        self, state: DoublePendulumState, acc: np.ndarray
    ) -> np.ndarray:
        """Compute required torques tau = M qddot + h(q, v)."""
        q, v = self._get_q_v(state)
        return np.array(pin.rnea(self.model, self.data, q, v, acc))

    def total_energy(self, state: DoublePendulumState) -> float:
        """Compute total energy (Kinetic + Potential)."""
        q, v = self._get_q_v(state)
        pin.computeAllTerms(self.model, self.data, q, v)
        return float(self.data.kinetic_energy + self.data.potential_energy)
