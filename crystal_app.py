import streamlit as st
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# ----- Functions from your original code -----

def plot_structure(coordinates, edges, title, highlight_points=None):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_box_aspect([1, 1, 1])

    for edge in edges:
        poly = Poly3DCollection([edge], alpha=0.25, linewidths=1, edgecolors='r')
        poly.set_facecolor((0, 0, 1, 0.1))
        ax.add_collection3d(poly)

    x, y, z = zip(*coordinates)
    ax.scatter(x, y, z, color='b', s=50, label="Corner atoms")

    if highlight_points:
        hx, hy, hz = zip(*highlight_points)
        ax.scatter(hx, hy, hz, color='g', s=100, label="Face-centered atoms")

    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')
    ax.set_xlim(0, 1.5)
    ax.set_ylim(0, 1.5)
    ax.set_zlim(0, 1.5)
    plt.title(title)
    plt.legend()
    st.pyplot(fig)

def display_bcc():
    coordinates = [
        (0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1),
        (1, 1, 0), (1, 0, 1), (0, 1, 1), (1, 1, 1)
    ]
    edges = [
        [coordinates[0], coordinates[1], coordinates[4], coordinates[2]],
        [coordinates[0], coordinates[1], coordinates[5], coordinates[3]],
        [coordinates[0], coordinates[2], coordinates[6], coordinates[3]],
        [coordinates[7], coordinates[6], coordinates[2], coordinates[4]],
        [coordinates[7], coordinates[6], coordinates[3], coordinates[5]],
        [coordinates[7], coordinates[4], coordinates[1], coordinates[5]],
    ]
    plot_structure(coordinates, edges, "BCC Crystal System")

def display_fcc():
    corners = [
        (0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1),
        (1, 1, 0), (1, 0, 1), (0, 1, 1), (1, 1, 1)
    ]
    face_centers = [
        (0.5, 0.5, 0), (0.5, 0, 0.5), (0, 0.5, 0.5),
        (0.5, 0.5, 1), (0.5, 1, 0.5), (1, 0.5, 0.5)
    ]
    edges = [
        [corners[0], corners[1], corners[4], corners[2]],
        [corners[0], corners[1], corners[5], corners[3]],
        [corners[0], corners[2], corners[6], corners[3]],
        [corners[7], corners[6], corners[2], corners[4]],
        [corners[7], corners[6], corners[3], corners[5]],
        [corners[7], corners[4], corners[1], corners[5]],
    ]
    plot_structure(corners + face_centers, edges, "FCC Crystal System", face_centers)

def display_slip_plane_bcc(plane):
    planes = {
        "(110)": [(0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0)],
        "(112)": [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0.5, 0.5, 1)],
        "(123)": [(0, 0, 0), (1, 0, 0), (0.5, 1, 0.5), (0.33, 0.67, 1)],
    }
    if plane not in planes:
        st.error("Invalid slip plane selected.")
        return
    plot_plane(planes[plane], f"BCC Slip Plane {plane}")

def display_slip_plane_fcc(plane):
    planes = {
        "(111)": [(0, 0, 1), (0, 1, 0), (1, 0, 0)],
        "(-111)": [(0, 0, -1), (0, -1, 0), (-1, 0, 0)],
        "(1-11)": [(1, 0, 0), (0, -1, 0), (0, 0, 1)],
        "(-1-11)": [(-1, 0, 0), (0, -1, 0), (0, 0, 1)],
    }
    if plane not in planes:
        st.error("Invalid slip plane selected.")
        return
    plot_plane(planes[plane], f"FCC Slip Plane {plane}")

def plot_plane(points, title):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_box_aspect([1, 1, 1])

    ax.add_collection3d(Poly3DCollection([points], alpha=0.5, facecolors='cyan'))

    x, y, z = zip(*points)
    ax.scatter(x, y, z, color='r', s=50)

    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')
    plt.title(title)
    st.pyplot(fig)

# ----- Streamlit UI -----

st.title("🔬 Crystal Plasticity Visualizer")
st.write("Explore BCC and FCC crystal systems and their slip planes.")

system = st.selectbox("Choose crystal system:", ["BCC", "FCC"])

if system == "BCC":
    display_bcc()
    plane = st.selectbox("Select BCC slip plane:", ["(110)", "(112)", "(123)"])
    display_slip_plane_bcc(plane)
else:
    display_fcc()
    plane = st.selectbox("Select FCC slip plane:", ["(111)", "(-111)", "(1-11)", "(-1-11)"])
    display_slip_plane_fcc(plane)
