from vpython import *
import numpy as np

prob = 0.005
N, L = 400, 7E-9/2.0
E = 1000000
q, m, size = 1.6E-19, 1E-6/6E23, 0.1E-9 #artificial charge particle
t, dt, vrms = 0, 1E-16, 10000.0
atoms, atoms_v = [],[]
cCounter = 0 # counter of collision of all particles of all times

#initialization
scene = canvas(width=575, height=600,align = 'left', background=vector(0.2,0.2,0))
scenev = canvas(width=575, height=600, align = 'right', range = 4E4, background=vector(0.2, 0.2,0))
container = box(canvas=scene, length = 2*L, height = 2*L, width = 2*L, opacity=0.2, color = color.yellow )
pos_array = -L + 2*L*np.random.rand(N,3) # atoms' position array

# Gaussian distribution of velovity align x, y, z axis respectively
X, Y, Z = np.random.normal(0, vrms, N), np.random.normal(0, vrms, N), np.random.normal(0, vrms, N)

v_array = np.transpose([X, Y, Z])

def a_to_v(a): # array to vector
    return vector(a[0], a[1], a[2])

for i in range(N):
    atom = sphere(canvas = scene, pos = a_to_v(pos_array[i]), radius = size, color=a_to_v(np.random.rand(3,1)))
    atoms.append(atom)
    atoms_v.append(sphere(canvas = scenev, pos=a_to_v(v_array[i]), radius = vrms/30, color=a_to_v(np.random.rand(3,1))))
    
# the average velocity and two axes in velocity space
vd_ball = sphere(canvas = scenev, pos = vec(0,0,0),radius = vrms/15, color=color.red)
x_axis = curve(canvas = scenev, pos = [vector(-2*vrms,0,0), vector(2*vrms,0,0)], radius=vrms/100)
y_axis = curve(canvas = scenev, pos = [vector(0,-2*vrms,0), vector(0,2*vrms,0)], radius=vrms/100)
vv = vector(0, 0, 0) # for calculating the average velocity
total_c = 0 # the total number of collisions

while True:
    t += dt
    rate(10000)
    v_array[:,0] += q*E/m*dt
    pos_array += v_array*dt # calculate new positions for all atoms
    outside = abs(pos_array) >= L
    pos_array[outside] = - pos_array[outside]
    
    # handle collision here
    prob_array = np.random.random(N) # return an array which size is N, and every tuples are in [0.0, 1.0)
    collision = np.less_equal(prob_array, prob)
    for hit, n in zip(collision, range(N)):
        if hit:
            theta = np.random.random() * np.pi * 2
            phi = np.random.random() * np.pi * 2
            v_array[n] = np.array([np.sin(phi)*np.cos(theta), np.sin(phi)*np.sin(theta), np.cos(phi)])*vrms
            cCounter += 1
            
    vv += a_to_v(np.sum(v_array,axis = 0)/N)
    
    if int(t/dt)%2000 == 0:
        # collision time: tau = (total time t*N) / (total collision number of all particles of all time)
        tau = t*N/cCounter  # need to be modified
        print(tau, vv/(t/dt), q*E*tau/m)
    vd_ball.pos = vv/(t/dt)
    
    for i in range(N): atoms_v[i].pos, atoms[i].pos = a_to_v(v_array[i]), a_to_v(pos_array[i])