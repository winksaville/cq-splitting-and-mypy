import cadquery as cq

c = (
    cq.Workplane("XY")
    .box(1, 1, 1)
    .faces(">Z")
    .circle(0.25)
    .cutThruAll()
)
#show_object(c, name="c")

# Split cube at its mid point and keepTop
r1 = (c
    .faces(">Y")
    .workplane(-0.5)
    .split(keepTop=True)
)
#show_object(r1, name="r1")

# Split the cube at the top of the circular half hole and keepBottom
r2 = (r1
    .faces(">Y")
    .workplane(-0.25)
    .split(keepBottom=True)
)
#show_object(r2, name="r2")
