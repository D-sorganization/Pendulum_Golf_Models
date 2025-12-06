#!/usr/bin/env python3
import sys
import os

# Ensure the current directory is in the python path to allow importing the package
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from double_pendulum_model.physics.double_pendulum import DoublePendulumState, DoublePendulumParameters
from double_pendulum_model.physics.urdf import generate_urdf

def run_demo():
    print("Double Pendulum Pinocchio Interface Demo")
    print("========================================")

    # 1. Demonstrate URDF Generation (always available)
    print("\nGenerating URDF (preview):")
    try:
        urdf = generate_urdf(DoublePendulumParameters.default())
        print(urdf[:500] + "...\n(truncated)")
    except Exception as e:
        print(f"Failed to generate URDF: {e}")
        return

    # 2. Try to use Pinocchio Interface
    print("\nInitializing Pinocchio Double Pendulum...")
    try:
        from double_pendulum_model.physics.pinocchio_interface import PinocchioDoublePendulum
        interface = PinocchioDoublePendulum()
        print("Model loaded successfully into Pinocchio.")

        state = DoublePendulumState(theta1=0.5, theta2=-0.5, omega1=0.1, omega2=-0.1)
        print(f"\nState: {state}")

        M = interface.mass_matrix(state)
        print("\nMass Matrix M(q):")
        print(M)

        g = interface.gravity_vector(state)
        print("\nGravity Vector g(q):")
        print(g)

        nle = interface.bias_forces(state)
        print("\nNon-linear effects h(q, v):")
        print(nle)

        print("\nPinocchio interface verification complete.")

    except ImportError as e:
        print(f"\nPinocchio not available: {e}")
        print("Install 'pinocchio' (and 'meshcat' for vis) to enable full dynamics verification.")

if __name__ == "__main__":
    run_demo()
