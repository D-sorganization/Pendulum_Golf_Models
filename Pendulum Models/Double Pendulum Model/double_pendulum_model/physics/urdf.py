import math
import xml.etree.ElementTree as ET
from xml.dom import minidom
from .double_pendulum import DoublePendulumParameters

def prettify(elem: ET.Element) -> str:
    """Return a pretty-printed XML string for the Element."""
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def generate_urdf(params: DoublePendulumParameters, robot_name: str = "double_pendulum") -> str:
    """
    Generate a URDF string for the double pendulum with the given parameters.

    The URDF models the pendulum in 3D. The 'world' frame is fixed.
    'plane_base' is a frame rotated according to `plane_inclination_deg`.
    Joints rotate around the X axis of their local frames.
    Links extend along the negative Z axis.
    """
    # Extract parameters
    # Upper segment
    l1 = params.upper_segment.length_m
    m1 = params.upper_segment.mass_kg
    lc1 = params.upper_segment.center_of_mass_distance
    I1 = params.upper_segment.inertia_about_com

    # Lower segment
    l2 = params.lower_segment.length_m
    m2 = params.lower_segment.total_mass
    lc2 = params.lower_segment.center_of_mass_distance
    I2 = params.lower_segment.inertia_about_com

    # Plane inclination
    inclination_rad = params.plane_inclination_rad

    # Create URDF
    robot = ET.Element('robot', name=robot_name)

    # Materials
    mat_black = ET.SubElement(robot, 'material', name='black')
    ET.SubElement(mat_black, 'color', rgba='0.1 0.1 0.1 1')

    mat_grey = ET.SubElement(robot, 'material', name='grey')
    ET.SubElement(mat_grey, 'color', rgba='0.6 0.6 0.6 1')

    # World link
    world = ET.SubElement(robot, 'link', name='world')

    # Plane base link (rotated to match inclination)
    plane_base = ET.SubElement(robot, 'link', name='plane_base')
    # Inertial for plane_base (dummy, minimal)
    inertial_pb = ET.SubElement(plane_base, 'inertial')
    ET.SubElement(inertial_pb, 'mass', value='0.001')
    ET.SubElement(inertial_pb, 'origin', xyz='0 0 0', rpy='0 0 0')
    ET.SubElement(inertial_pb, 'inertia', ixx='0.0001', ixy='0', ixz='0', iyy='0.0001', iyz='0', izz='0.0001')

    # Joint World -> Plane Base
    # We rotate around Y axis by -inclination to tilt the X axis (rotation axis)
    # If inclination=0, rotation=0. Axis=X (horizontal).
    # If inclination=90, rotation=-90. Axis=Z (vertical).
    joint_world_plane = ET.SubElement(robot, 'joint', name='joint_world_plane', type='fixed')
    ET.SubElement(joint_world_plane, 'parent', link='world')
    ET.SubElement(joint_world_plane, 'child', link='plane_base')
    # rpy is roll, pitch, yaw. Pitch is Y rotation.
    ET.SubElement(joint_world_plane, 'origin', xyz='0 0 0', rpy=f'0 {-inclination_rad} 0')

    # Link 1
    link1 = ET.SubElement(robot, 'link', name='link1')

    # Visual 1 (Cylinder)
    vis1 = ET.SubElement(link1, 'visual')
    ET.SubElement(vis1, 'origin', xyz=f'0 0 {-l1/2}', rpy='0 0 0')
    geom1 = ET.SubElement(vis1, 'geometry')
    ET.SubElement(geom1, 'cylinder', radius='0.02', length=str(l1))
    ET.SubElement(vis1, 'material', name='black')

    # Inertial 1
    inertial1 = ET.SubElement(link1, 'inertial')
    ET.SubElement(inertial1, 'origin', xyz=f'0 0 {-lc1}', rpy='0 0 0')
    ET.SubElement(inertial1, 'mass', value=str(m1))
    # Inertia tensor. Rotation around X.
    ET.SubElement(inertial1, 'inertia',
                  ixx=str(I1), iyy=str(I1), izz='0.001',
                  ixy='0', ixz='0', iyz='0')

    # Joint 1
    joint1 = ET.SubElement(robot, 'joint', name='joint1', type='continuous')
    ET.SubElement(joint1, 'parent', link='plane_base')
    ET.SubElement(joint1, 'child', link='link1')
    ET.SubElement(joint1, 'origin', xyz='0 0 0', rpy='0 0 0')
    ET.SubElement(joint1, 'axis', xyz='1 0 0') # Rotate around X

    # Link 2
    link2 = ET.SubElement(robot, 'link', name='link2')

    # Visual 2 (Cylinder)
    vis2 = ET.SubElement(link2, 'visual')
    ET.SubElement(vis2, 'origin', xyz=f'0 0 {-l2/2}', rpy='0 0 0')
    geom2 = ET.SubElement(vis2, 'geometry')
    ET.SubElement(geom2, 'cylinder', radius='0.015', length=str(l2))
    ET.SubElement(vis2, 'material', name='grey')

    # Inertial 2
    inertial2 = ET.SubElement(link2, 'inertial')
    ET.SubElement(inertial2, 'origin', xyz=f'0 0 {-lc2}', rpy='0 0 0')
    ET.SubElement(inertial2, 'mass', value=str(m2))
    ET.SubElement(inertial2, 'inertia',
                  ixx=str(I2), iyy=str(I2), izz='0.001',
                  ixy='0', ixz='0', iyz='0')

    # Joint 2
    joint2 = ET.SubElement(robot, 'joint', name='joint2', type='continuous')
    ET.SubElement(joint2, 'parent', link='link1')
    ET.SubElement(joint2, 'child', link='link2')
    ET.SubElement(joint2, 'origin', xyz=f'0 0 {-l1}', rpy='0 0 0')
    ET.SubElement(joint2, 'axis', xyz='1 0 0') # Rotate around X

    return prettify(robot)
