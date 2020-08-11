import cadquery as cq

a = cq.Workplane("XY").box(1, 2, 3)
print(f"""type(a)={type(a)}
type(a.val())={type(a.val())}""")
#b = cq.Workplane(inPlane=cq.Plane((0, 0, 0), (1, 0, 0), (0, 0, 1)))
s = cq.Workplane(cq.Plane.XY())
sPnts = [
    (2.75, 1.5),
    (2.5, 1.75),
    (2.0, 1.5),
    (1.5, 1.0),
    (1.0, 1.25),
    (0.5, 1.0),
    (0, 1.0),
]
print(f"""type(s)={type(s)}
type(s.val())={type(s.val())}""")
r = s.lineTo(3.0, 0).lineTo(3.0, 1.0).spline(sPnts).close()
print(f"""type(r)={type(r)}
type(r.val())={type(r.val())}""")
b = cq.Workplane(obj=r.val())
print(f"""type(b)={type(b)}
type(b.val())={type(b.val())}""")
