# FieldMappr
Library mapping electric fields in three dimensions with the help of user inputted configuration of points, rods and/or rings of charge.

`E_map` is a class containing the necesseary methods to build charge configurations, calculate the electric field over a grid of $50 \times 50 \times 50$ meters and print the electric vector field in three dimensions.

* `build_point` creates a point in the field at a coordinate $p$ with a charge $q$
* `build_rod` approximates a rod of charge as multiple point charges alinged in a segment of a linear path with initial and terminal coordinates $p_1$ and $p_2$.  The charge values of each point charge within the rod are calculated with the equation $dq = Q \cdot \frac{dl}{l}$, where $Q$ is the total charge of the rod and $l$ is the distance between $p_1$ and $p_2$.
* `build_ring` approximates a ring of charge as a group of point charges alligned on a circular path. The method finds two arbitrary perpendicular vector ($v_1$ and $v_2$) to the ring's normal at point ($x_0$,$y_0$,$z_0$). The method then itterates the following formula

    $$\vec{r}(t)= (x_0, y_0,z_0) + r(cos t\cdot \vec{v}_1+ sin t\cdot \vec{v}_2)$$
    
    over $[0, 2\pi]$ with an angle step of $\frac{\pi}{180}$ to calculate the coordinates of the charges necessary to approximate the ring of charge.






  
