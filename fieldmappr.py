# @title Electric Field Mapping Class
import numpy as np
import matplotlib.pyplot as plt
# Electric field map class
class E_map :
    # Creating unique list charge storage for each E_map object
    def __init__(self) :
        self.charge_map = []
    # Reducing any arbitrary vector into its unit form
    def __unit_vector(self, p1, p2) :
        i = p2[0] - p1[0]
        j = p2[1] - p1[1]
        k = p2[2] - p1[2]
        magnitude = (i**2 + j**2 + k**2)**(1/2)
        m_inv = 1 / magnitude if magnitude != 0 else 0
        return m_inv*i, m_inv*j , m_inv*k
    # Outputs the E field vector in three dimensions
    def __E(self, Q, q, p):
        d = ((p[2] - q[2])**2 + (p[1] - q[1])**2 + (p[0] - q[0])**2)**(1/2)
        magnitude = 8.99e9 * (Q / d**2) if d != 0 else 0
        u = self.__unit_vector(q,p)
        return (magnitude*u[0], magnitude*u[1], magnitude*u[2])
    # Function that builds point charges
    def build_point(self, p, q) :
        self.charge_map.append((p[0],p[1],p[2],q))
    # Function that approximates a rod of charge as a group of point charges
    def build_rod(self, p1, p2, Q, dl) :
        l = ((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2 + (p2[2] - p1[2])**2)**(1/2)
        dq = (dl / l) * Q
        _dir = self.__unit_vector(p1, p2)
        dl_x, dl_y, dl_z = dl*_dir[0], dl*_dir[1],dl* _dir[2]
        for i in range(int(l/dl)) :
            self.charge_map.append((p1[0] + i*dl_x, p1[1] + i*dl_y, p1[2] + i*dl_z, dq))
    # Function that approximates a ring of charge as a cluster of point charges.
    def build_ring(self, c, u, r, Q) :
        # Setting dt (stands for d_theta) and dq
        dt = 1
        dq = Q * (dt / 2*np.pi)
        # Converting the center point into a numpy array
        P = np.array(c)
        # If the normal vector has x=0 and y=0, set its orthogonal unit vector to be (0,1,0)
        if u[0] == u[1] == 0.0 :
            v1 = np.array([0.0,1.0,0.0])
        else :
            # Finds an arbitrary perpedicular vector to u
            v1 = np.array((float(u[1]), float(-u[0]), 0))
            v1 /= np.linalg.norm(v1) if np.linalg.norm(v1) > 0 else 1.0
        # Finds cross product of u and v1 to find another perpendicular vector v2
        v2 = np.cross(np.array(u),v1)
        v2 /= np.linalg.norm(v2) if np.linalg.norm(v2) > 0 else 1.0
        # Lists the test angles to iterate on
        angles = [ i * (np.pi / 180) for i in range (0,360,dt)]
        # Approximating the ring of charge using point charges
        for angle in angles :
            R = P + r*(np.cos(angle)*v1 + np.sin(angle)*v2)
            R_ = list(R)
            self.charge_map.append((R_[0], R_[1], R_[2], dq))
    # Function used to output the meshgrids of the compenents of electric field
    def __build_field(self, X, Y, Z):
        dEx = np.zeros_like(X)
        dEy = np.zeros_like(Y)
        dEz = np.zeros_like(Z)
        # Find the resulting electric field vectors at all points in the meshgrids
        for q in self.charge_map:
            for i in range(X.shape[0]):
                for j in range(X.shape[1]):
                    for k in range(X.shape[2]):
                        e = self.__E(q[3], (q[0], q[1], q[2]), (X[i, j, k], Y[i, j, k], Z[i, j, k]))
                        dEx[i, j, k] += e[0]
                        dEy[i, j, k] += e[1]
                        dEz[i, j, k] += e[2]
        # Normalize the vectors for a coherent visual output
        magnitude = np.sqrt(dEx**2 + dEy**2 + dEz**2)
        # Avoid division by zero
        magnitude[magnitude == 0] = 1.0
        dEx /= magnitude
        dEy /= magnitude
        dEz /= magnitude
        return dEx, dEy, dEz
    # Function outputting the electric field in three dimensions
    def __plot_3d_quiver(self, ax, X, Y, Z, dEx, dEy, dEz, title, elev, azim):
        # Plot a 3D quiver plot representing the electric field
        ax.quiver(X, Y, Z, dEx, dEy, dEz, length=4.5, color='b')
        # Add scatter points for charges in the charge map
        for q in self.charge_map:
            # Color points based on charge polarity
            color = 'red' if q[3] > 0 else 'black'
            ax.scatter(q[0], q[1], q[2], c=color, marker='o')
        # Set limits for the x, y, and z axes
        ax.set_xlim(-25, 25)
        ax.set_ylim(-25, 25)
        ax.set_zlim(-25, 25)
        # Set labels for the x, y, and z axes
        ax.set_xlabel('x (m)')
        ax.set_ylabel('y (m)')
        ax.set_zlabel('z (m)')
        # Set the title of the plot
        ax.set_title(title)
        # Set the elevation and azimuth angles for the view
        ax.view_init(elev=elev, azim=azim)
    # Method to display electric field mappings from different perspectives
    def show_map(self):
        # Define the ranges for x, y, and z coordinates
        x_min, x_max = -25, 25
        y_min, y_max = -25, 25
        z_min, z_max = -25, 25
        # Define the step size for the mesh grid
        step = 6.25
        # Generate arrays of x, y, and z coordinates within specified ranges
        x = np.arange(x_min, x_max + 1, step)
        y = np.arange(y_min, y_max + 1, step)
        z = np.arange(z_min, z_max + 1, step)
        # Create a mesh grid of points
        X, Y, Z = np.meshgrid(x, y, z)
        # Calculate the electric field components at each point
        dEx, dEy, dEz = self.__build_field(X, Y, Z)
        # Create a single figure for all plots
        fig = plt.figure(figsize=(12, 9))
        # Default 3D view
        ax = fig.add_subplot(221, projection='3d')
        self.__plot_3d_quiver(ax, X, Y, Z, dEx, dEy, dEz, 'Electric Field Mapping (Three Dimensional)', elev=30, azim=-45)
        # XY plane view
        ax = fig.add_subplot(222, projection='3d')
        self.__plot_3d_quiver(ax, X, Y, Z, dEx, dEy, dEz, 'Electric Field View Orthogonal to the XY-Plane', elev=90, azim=-90)
        # XZ plane view
        ax = fig.add_subplot(223, projection='3d')
        self.__plot_3d_quiver(ax, X, Y, Z, dEx, dEy, dEz, 'Electric Field View Orthogonal to the XZ-Plane', elev=0, azim=-90)
        # YZ plane view
        ax = fig.add_subplot(224, projection='3d')
        self.__plot_3d_quiver(ax, X, Y, Z, dEx, dEy, dEz, 'Electric Field View Orthogonal to the YZ-Plane', elev=0, azim=0)
        # Adjust layout to prevent overlap
        plt.tight_layout()
        # Show the plot
        plt.show()