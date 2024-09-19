from subsystems.thruster import solve_motion
from mainloop import motors as mobjs, Thruster
import pickle


motors = str(list(map(Thruster.serialize, mobjs)))

try:
    with open("table.obj", "rb") as f:
        table = pickle.loads(f.read())
        # input(table)
except Exception as e:
    input(e)
    table = {}
if motors not in table:
    table[motors] = {}
p = 2

try:
    for fx in range(-5*p,6*p):
        for fy in range(-5*p,6*p):
            for fz in range(-5*p,6*p):
                for rx in range(-5*p,6*p):
                    for ry in range(-5*p,6*p):
                        for rz in range(-5*p,6*p):
                            motion = fx/p, fy/p, fz/p, rx/p, ry/p, rz/p
                            print(motion)
                            if motion not in table[motors]:
                                table[motors][motion] = solve_motion(mobjs, *motion)["speeds"]
                            else:
                                print("pass")
except:
    print(table)
    with open("table.obj", "wb") as f:
        f.write(pickle.dumps(table))
