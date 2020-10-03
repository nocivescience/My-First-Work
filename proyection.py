from manimlib.imports import *
class Coordinates(Scene):
        CONFIG={
                "dot_style":{
                        "radius":0.07,
                        "color":YELLOW
                },
                "anim_kwargs":{
                        "run_time":.1,
                        "rate_func":smooth
                }
        }
        def construct(self):
                plane=self.get_plane()
                dots=self.get_points(plane)[0]
                dots_copy=dots.copy()
                for anim in [plane,dots]:
                        self.play(ShowCreation(anim))
                self.get_vertical_update(plane,dots)
                flashes=self.get_points(plane)[1]
                
                texto=self.get_text()
                for t in range(len(texto)):
                        self.play(Transform(dots_copy[t],texto[t]))
                self.wait()
        def get_plane(self):
                return NumberPlane()
        def get_points(self,plane):
                dots=VGroup()
                flashes=VGroup()
                for t in np.arange(-4,5):
                        position=t
                        point=plane.c2p(position,0)
                        dot=Dot().move_to(point)
                        dot.position=position
                        dot.point=point
                        dots.add(dot)
                        line=DashedLine()
                        line.put_start_and_end_on(dot.point,dot.get_center()+np.array([0,0.001,0]))
                        line.add_updater(self.get_update_lines(dot))
                        my_flash=self.get_flash(point)
                        flashes.add(my_flash)
                        self.play(my_flash,**self.anim_kwargs)
                        line.add_updater(self.get_update_lines(dot))
                        self.add(line)
                return VGroup(dots,flashes)
        def get_vertical_update(self,plane,dots):
                points=[]
                for dot,y in zip(dots,np.random.uniform(-4,4,len(dots))):
                        if y>0:
                                dot.set_color(RED)
                        else:
                                dot.set_color(YELLOW)
                        y_point=plane.c2p(dot.position,y)
                        points.append(y_point)
                        self.play(dot.move_to,y_point,**self.anim_kwargs)
                self.wait()
        def get_update_lines(self,dot):
                def update(lin):
                        lin.put_start_and_end_on(dot.point,dot.get_center()+np.array([0,0.001,0]))
                return update
        def get_flash(self,point):
                flash=Flash(point,line_length=.1,flash_radius=.24,run_time=0.55,remover=True)
                flash_mob=flash.mobject
                return ShowCreation(flash_mob)
        def get_text(self):
                texto=TextMobject("these"," are"," all"," projections"," over"," x"," axes")
                texto.to_edge(DOWN,buff=0.5)
                return texto

class DeformingPlane(Scene):
        def construct(self):
                grid_number=NumberPlane()
                self.play(ShowCreation(grid_number))
                point_1=grid_number.c2p(-3,2)
                point_2=grid_number.c2p(4,-3)
                dot_1=Dot().shift(point_1)
                dot_2=Dot().shift(point_2)
                line=Line(dot_1.get_center(),dot_2.get_center())
                for d in [dot_1,dot_2,line]:
                        self.play(FadeIn(d))
                grid_number.prepare_for_nonlinear_transform()
                grid_number.save_state()
                self.play(*it.chain(*[(mob.apply_function,lambda t: t+np.array([np.sin(t[1]),np.cos(t[0]),0])) for mob in [grid_number,dot_1,dot_2,line]]),
                        run_time=2)
                self.wait()
POINTS=np.array([
        [0,0,0],
        [4,0,0],
        [4,3,0]
])
class Pitagorean(MovingCameraScene):
        def construct(self):
                camera=self.camera_frame.set_height(10)
                my_polygon=self.get_polygon()
                self.play(ShowCreation(my_polygon))
                my_lines=VGroup(*[my_polygon[i] for i in [0,2,4]])
                my_squares=self.get_square(my_lines)
                self.play(ShowCreation(my_squares))
                self.play(camera.shift,UP)
                self.wait()
        def get_polygon(self):
                lines=Group()
                polygon=Polygon(*POINTS)
                corners=polygon.get_anchors()
                lines=VGroup(*[Line(a,b,stroke_width=1) for a,b in adjacent_pairs(corners)])
                return lines
        def get_square(self,polygon):
                square=Square(side_length=1)
                normal_x,normal_y,normal_hip=get_norm(POINTS[1]),get_norm(POINTS[2]-POINTS[1]),get_norm(POINTS[2])
                first_squares=VGroup()
                for t in [normal_x,normal_y,normal_hip]:
                        first_square=VGroup(*[square.copy().shift(x*RIGHT+y*UP) for x in range(int(t)) for y in range(int(t))])
                        first_squares.add(first_square)
                x_line,y_line,h_line=polygon
                x_squares,y_squares,h_squares=first_squares
                x_squares.move_to(x_line.get_bottom(),UP)
                y_squares.move_to(y_line.get_right(),LEFT)
                h_squares.move_to(h_line.get_center(),UP)
                h_squares.rotate(h_line.get_angle(),about_point=h_line.get_center())
                return first_squares

class DiferentTriangles(MovingCameraScene):
        CONFIG={
                "triples":[(3,4,5),(5,12,13),(8,15,17),(7,24,25)],
                "anim_kwargs":{
                        "run_time":1,
                        "rate_func":linear
                },
                "colors":[RED,BLUE,YELLOW,GREEN]
        }
        def construct(self):
                camera=self.camera_frame.shift(UP)
                camera.set_height(10)
                self.get_triangles()
        def get_triangles(self):
                for a,b,c in self.triples:
                        coloor=it.cycle(self.colors)
                        square=Square(side_length=1,stroke_width=1,color=next(coloor))
                        polygon=Polygon(ORIGIN,a*RIGHT,a*RIGHT+b*UP,stroke_width=1).move_to(ORIGIN+2*UP)
                        corners=polygon.get_anchors()
                        lines=VGroup(*[Line(a,b,stroke_width=1) for a,b in adjacent_pairs(corners)])
                        squares_first=VGroup()
                        for n in [a,b,c]:
                                squares=VGroup(*[square.copy().shift(x*RIGHT+y*UP) for x in range(n) for y in range(n)])
                                squares_first.add(squares)
                        squares_x,squares_y,squares_h=squares_first
                        squares_x.move_to(lines[0].get_bottom(),UP)
                        squares_y.move_to(lines[2].get_right(),LEFT)
                        squares_h.move_to(lines[4].get_center(),UP)
                        squares_h.rotate(lines[4].get_angle(),about_point=lines[4].get_center())
                        squares_first.add(squares_x,squares_y,squares_h)
                        whole_figure=VGroup(polygon,squares_x,squares_y,squares_h).set_height(4)
                        self.play(ShowCreation(polygon),**self.anim_kwargs)
                        self.play(ShowCreation(squares_first),**self.anim_kwargs)
                        for t in [polygon,squares_first]:
                                self.play(FadeOut(t),**self.anim_kwargs)

class ScaleRect(Scene):
        CONFIG={
                "x_min":0,
                "x_max":1000,
                "unit_size":1,
        }
        def construct(self):
                fx= lambda x: np.cos(x.get_value())
                x_value=ValueTracker(0)
                fx_value=ValueTracker(fx(x_value))
                my_rect_fx=self.get_rect(-1,1,1,6)
                my_rect_fx.to_edge(LEFT,buff=0.5)
                my_rect_x=self.get_rect(0,1000,100,.1)
                values=[x_value,fx_value]
                my_rects=VGroup(my_rect_x,my_rect_fx)
                my_rects.arrange(DOWN,buff=2)
                my_rect_x.to_edge(LEFT,buff=1.7)
                indicators=self.get_indicator(my_rects,x_value,fx)
                labels=self.get_number(my_rects,indicators,values,fx)
                self.play(ShowCreation(my_rects))
                self.play(FadeIn(indicators))
                self.play(ShowCreation(labels))
                self.add(labels)
                self.play(values[0].set_value,1000,my_rect_x.set_width,10,{"about_point":my_rect_x.n2p(0)},rate_func=smooth,run_time=2)
                self.wait()
        def get_rect(self,x_min,x_max,interline,unit_size=1):
                my_rect=NumberLine(x_min=x_min,x_max=x_max,stroke_width=1,unit_size=unit_size)
                my_rect.add_numbers(*range(x_min,x_max+1,interline))
                return my_rect
        def get_number(self,rects,tips,values,func):
                x_value,fx_value=values
                tip_x,tip_fx=tips
                x_decimal=DecimalNumber(x_value.get_value()).add_updater(lambda t: t.set_value(x_value.get_value()))
                fx_decimal=DecimalNumber(fx_value.get_value()).add_updater(lambda t: t.set_value(func(x_value)))
                x_label=VGroup(TexMobject("x= "),x_decimal).arrange(RIGHT,buff=.1).scale(0.5)
                fx_label=VGroup(TexMobject("\\cos(x)= "),fx_decimal).arrange(RIGHT,buff=.1).scale(0.5)
                rect_x,rect_fx=rects
                tip_x,tip_fx=tips
                x_label.add_updater(lambda t: t.next_to(tip_x,UP,buff=0.1))
                fx_label.add_updater(lambda t: t.next_to(tip_fx,UP,buff=0.1))
                return VGroup(x_label,fx_label)
        def get_indicator(self,rects,values,func):
                rect_x,rect_fx=rects
                tip_x=ArrowTip(color=GREEN_A).rotate(PI/2)
                tip_x.set_height(1,stretch=True)
                tip_x.set_width(.1,stretch=True)
                tip_fx=tip_x.deepcopy()
                tip_x.add_updater(lambda t: t.next_to(rect_x.number_to_point(values.get_value()),UP,buff=0))
                tip_fx.add_updater(lambda t: t.next_to(rect_fx.number_to_point(func(values)),UP,buff=0))
                return VGroup(tip_x,tip_fx)

class FirstSuccession(Scene):
        def construct(self):
                dots=VGroup(*[Dot() for _ in range(10)])
                dots.arrange(RIGHT,buff=0.5)
                self.play(ShowCreation(dots))
                for dot in dots:
                        self.play(
                                dot.scale,3,dot.set_color,RED,rate_func=there_and_back
                        )
                self.wait()

class SecondSuccession(Scene):
        def construct(self):
                dots=VGroup(*[Dot() for _ in range(10)])
                dots.arrange(RIGHT,buff=0.5)
                self.play(ShowCreation(dots))
                def dot_func(mob):
                        mob.scale(3)
                        mob.set_color(RED)
                        return mob
                self.play(LaggedStart(*[ApplyFunction(dot_func,dot,rate_func=there_and_back) for dot in dots]))
                self.wait()

class ThridSuccession(Scene):
        CONFIG={

        }
        def construct(self):
                dot_L=Dot().shift(LEFT+UP)
                dot_R=Dot().shift(RIGHT)
                dots=VGroup(dot_L,dot_R)
                lista=[dot_L.get_center()[1],dot_R.get_center()[1]]
                for t,dot in zip(lista,dots):
                        if not np.all(t==0):
                                dot.set_color(RED)
                        else:
                                dot.set_color(BLUE)
                self.play(ShowCreation(dots))
                self.wait()

class FourthSuccession(Scene):
        CONFIG={

        }
        def construct(self):
                dot_L=Dot().shift(LEFT+UP)
                dot_R=Dot().shift(RIGHT+DOWN)
                dots=VGroup(dot_L,dot_R)
                lista=[dot_L.get_center()[1],dot_R.get_center()[1]]
                for t,dot in zip(lista,dots):
                        if not np.all(t==0):
                                self.play(dot.set_color,RED)
                        else:
                                self.play(dot.set_color,BLUE)
                self.play(ShowCreation(dots))
                for dot,pos,real in zip(dots,[DOWN,UP],[LEFT,RIGHT]):
                        self.play(dot.move_to,real+pos)
                self.wait()
        
class MakeACoords(Scene):
        CONFIG={
                "axis_config":{
                        "include_tip":False
                },
                "anim_kwargs":{
                        "run_time":5,
                        "rate_func":linear
                }
        }
        def construct(self):    
                axes=self.get_axes()
                background_axes=axes.deepcopy()
                self.play(ShowCreation(axes),**self.anim_kwargs)
                dot_axes=Dot(axes.coords_to_point(4,2))
                self.play(FadeIn(dot_axes),**self.anim_kwargs)
                lines=VGroup()
                line_a=DashedLine(dot_axes.get_center(),axes.coords_to_point(4,0))
                line_b=DashedLine(dot_axes.get_center(),axes.coords_to_point(0,2))
                line_ap=DashedLine(dot_axes.get_center(),axes.coords_to_point(4+line_a.get_length()*np.tan(TAU/20),0))
                line_bp=DashedLine(dot_axes.get_center(),axes.coords_to_point(0,2-line_b.get_length()*np.tan(TAU/20)))
                lines.add(line_a,line_b,line_ap,line_bp)
                self.play(
                        Rotate(background_axes,TAU/20,about_point=ORIGIN),**self.anim_kwargs
                )
                self.play(DrawBorderThenFill(lines),**self.anim_kwargs)
                for a,b,c in ([dot_axes.get_center(),axes.coords_to_point(4,0),axes.coords_to_point(4+line_a.get_length()*np.tan(TAU/20),0)],[dot_axes.get_center(),axes.coords_to_point(0,2),axes.coords_to_point(0,2-line_b.get_length()*np.tan(TAU/20))]):
                        poligono=self.get_triangles(a,b,c)
                        self.play(ShowCreation(poligono),**self.anim_kwargs)
                self.wait()
                self.get_first_tex(axes,background_axes)
                coords=self.get_coord(axes)
                self.play(Write(coords),**self.anim_kwargs)
                self.wait()
        def get_axes(self):
                my_axes=Axes(x_min=-8,x_max=8,y_min=-6,y_max=6,**self.axis_config)
                return my_axes
        def get_triangles(self,a,b,c):
                return Polygon(*[a,b,c],fill_opacity=0.7,fill_color=YELLOW_B,stroke_width=0.6,stroke_color=RED)
        def get_first_tex(self,axes_1,axes_2):
                texto_1=TexMobject("S_1=\\left\\{ O; x,y \\right\\}")
                texto_1.scale(1.5)
                texto_1.to_corner(UL,buff=.4)
                texto_1.set_color(BLUE)
                self.play(TransformFromCopy(VGroup(axes_1,axes_2),texto_1),**self.anim_kwargs)
                self.wait()
        def get_coord(self,axes):
                invertir=True
                textos=["x_A","x_B","y_A","y_B"]
                position=[axes.coords_to_point(4,0),axes.coords_to_point(4+2*np.tan(TAU/20),0),axes.coords_to_point(0,2),axes.coords_to_point(0,2-4*np.tan(TAU/20))]
                Texs=VGroup()
                for tex,pos in zip(textos,position):
                        texto=TexMobject(tex)
                        texto.scale(0.6)
                        if not pos[0]<=0.00001:
                                texto.next_to(pos,DOWN,buff=0.15)
                        else:
                                texto.next_to(pos,LEFT,buff=0.15)
                        Texs.add(texto)
                return Texs
        
class WindmillScene(Scene):
    CONFIG = {
        "windmill_length": 2 * FRAME_WIDTH,
        "windmill_rotation_speed": 0.25,
        "leave_shadows": False,
    }

    def get_random_point_set(self, n_points=11, width=6, height=6):
        return np.array([
            [
                -width / 2 + np.random.random() * width,
                -height / 2 + np.random.random() * height,
                0
            ]
            for n in range(n_points)
        ])

    def get_dots(self, points):
        return VGroup(*[
            Dot(point)
            for point in points
        ])

    def get_windmill(self, points, pivot=None, angle=TAU / 4):
        line = Line(LEFT, RIGHT)
        line.set_length(self.windmill_length)
        line.set_angle(angle)
        line.point_set = points
        if pivot is not None:
            line.pivot = pivot
        else:
            line.pivot = points[0]
        line.rot_speed = self.windmill_rotation_speed
        line.add_updater(lambda l: l.move_to(l.pivot))
        return line

    def get_pivot_dot(self, windmill, color=YELLOW):
        pivot_dot = Dot(color=YELLOW)
        pivot_dot.add_updater(lambda d: d.move_to(windmill.pivot))
        return pivot_dot

    def next_pivot_and_angle(self, windmill):
        curr_angle = windmill.get_angle()
        pivot = windmill.pivot
        non_pivots = list(filter(
            lambda p: not np.all(p == pivot),
            windmill.point_set
        ))
        angles = np.array([
            -(angle_of_vector(point - pivot) - curr_angle) % PI
            for point in non_pivots
        ])
        tiny_indices = angles < 1e-6
        if np.all(tiny_indices):
            return non_pivots[0]
        angles[tiny_indices] = np.inf
        index = np.argmin(angles)
        return non_pivots[index], angles[index]

    def rotate_to_next_pivot(self, windmill, max_time=None):
        new_pivot, angle = self.next_pivot_and_angle(windmill)
        change_pivot_at_end = True
        run_time = angle / windmill.rot_speed
        if max_time is not None and run_time > max_time:
            ratio = max_time / run_time
            rate_func = (lambda t: ratio * t)
            run_time = max_time
            change_pivot_at_end = False
        else:
            rate_func = linear
        self.play(
            Rotate(
                windmill,
                -angle,
                rate_func=rate_func,
                run_time=run_time,
            ),
        )
        if change_pivot_at_end:
            windmill.pivot = new_pivot
        return run_time
        
    def let_windmill_run(self, windmill, time):
        while time > 0:
            last_run_time = self.rotate_to_next_pivot(
                windmill,
                max_time=time,
            )
            time -= last_run_time

class IntroduceWindmill(WindmillScene):
    CONFIG = {
        "final_run_time": 60,
        "windmill_rotation_speed": 0.5,
    }
    def construct(self):
        self.add_points()
        self.add_line()
        self.switch_pivots()
    def add_points(self):
        points = self.get_random_point_set(8)
        self.dots=VGroup(*[Dot().move_to(point) for point in points])
    def add_line(self):
        dots = self.dots
        points = np.array(list(map(Mobject.get_center, dots)))
        p0 = points[0]
        windmill = self.get_windmill(points, p0, angle=60 * DEGREES)
        pivot_dot = self.get_pivot_dot(windmill)
        self.add(windmill, dots)
        self.play(
            GrowFromCenter(windmill)
        )
        self.wait()
        self.play(
            GrowFromCenter(pivot_dot),
            dots.set_color, WHITE,
        )
        self.wait()
        next_pivot, angle = self.next_pivot_and_angle(windmill)
        self.play(
            *[
                Rotate(
                    mob, -0.99 * angle,
                    about_point=p0,
                    rate_func=linear,
                )
                for mob in [windmill]
            ],
        )
        self.windmill = windmill
    def switch_pivots(self):
        windmill = self.windmill
        self.let_windmill_run(windmill, 10)

class MakeAStupidThing(Scene):
        CONFIG={
                "line_length":FRAME_WIDTH,
                "speed_rot":0.25,
                "anim_kwargs":{
                        "run_time":1,
                        "rate_func":linear
                }
        }
        def construct(self):
                points=self.get_points_and_dots()[0]
                dots=self.get_points_and_dots()[1]
                line=self.get_line(points,points[0])
                my_decimal=VGroup(*[self.get_numerate(line,dot) for dot in dots])#.arrange(DOWN,buff=0.1)
                #my_decimal.to_corner(UL,buff=0.5)
                for t in [dots,line,my_decimal]:
                        self.play(ShowCreation(t),**self.anim_kwargs)
                self.get_rotate(line)
                self.wait()
        def get_points_and_dots(self):
                points=np.array([[-2,0,0],[0,2,0],[2,0,0],[0,-2,0]])
                dots=VGroup(*[Dot().move_to(point) for point in points])
                return points, dots
        def get_line(self,points,pivot=None,angle=TAU/4):
                line=Line()
                line.set_length(self.line_length)
                line.point_set=points
                if pivot is  None:
                        line.pivot=pivot
                else:
                        line.pivot=points[0]
                line.speed_rot=self.speed_rot
                line.add_updater(lambda t: t.move_to(t.pivot))
                return line
        def get_numerate(self,line,dot):
                decimal=DecimalNumber((line.get_angle()-angle_of_vector(dot.get_center()))%PI)\
                        .add_updater(lambda t: t.set_value((line.get_angle()-angle_of_vector(dot.get_center()))%PI))
                decimal.scale(0.5)
                decimal.set_color(ORANGE)
                decimal.move_to(dot)
                vect=dot.get_center()
                vect/=get_norm(vect)
                decimal.shift(vect*0.5)
                return decimal
        def get_rotate(self,line):
                anims_last_hit=[]
                time=3
                while time>0:
                        self.get_rotating(line)
                        time-=1
        def get_rotating(self,line):
                self.play(Rotate(line,angle=PI,about_point=line.pivot))

class MakeAStupidThing2(Scene):
        CONFIG={
                "line_length":FRAME_WIDTH,
                "speed_rot":0.25,
                "anim_kwargs":{
                        "run_time":1,
                        "rate_func":linear
                }
        }
        def construct(self):
                points=self.get_points_and_dots()[0]
                dots=self.get_points_and_dots()[1]
                line=self.get_line(points,points[0])
                my_decimal=VGroup(*[self.get_numerate(line,dot) for dot in dots])
                counts=self.get_count(line)
                for t in [dots,line,my_decimal,counts]:
                        self.play(ShowCreation(t),**self.anim_kwargs)
                self.let_line_run(line,40)
        def get_points_and_dots(self):
                points=np.array([[-2,0,0],[0,2,0],[2,0,0],[0,-2,0]])
                dots=VGroup(*[Dot().move_to(point) for point in points])
                return points, dots
        def get_line(self,points,pivot=None,angle=TAU/4):
                line=Line()
                line.set_length(self.line_length)
                line.point_set=points
                if pivot is  None:
                        line.pivot=pivot
                else:
                        line.pivot=points[0]
                line.speed_rot=self.speed_rot
                line.add_updater(lambda t: t.move_to(t.pivot))
                return line
        def get_numerate(self,line,dot):
                decimal=DecimalNumber((line.get_angle()-angle_of_vector(dot.get_center()))%PI)\
                        .add_updater(lambda t: t.set_value((line.get_angle()-angle_of_vector(dot.get_center()))%PI))
                decimal.scale(0.5)
                decimal.set_color(ORANGE)
                decimal.move_to(dot)
                vect=dot.get_center()
                vect/=get_norm(vect)
                decimal.shift(vect*0.5)
                return decimal
        def get_angle_pivot(self,line):
                curr_angle=line.get_angle()
                non_pivots=list(filter(lambda t: not np.all(t==line.pivot), line.point_set))
                angles=np.array([-(angle_of_vector(point-line.pivot)-curr_angle)%PI 
                        for point in non_pivots])
                tiny_indices=angles<1e-6
                if np.all(tiny_indices):
                        return non_pivots[0],PI
                angles[tiny_indices]=np.inf
                index=np.argmin(angles)
                return non_pivots[index], angles[index]
        def get_rotating(self,line,max_time=None,added_anims=None):
                new_pivot, angle=self.get_angle_pivot(line)
                change_pivot_at_end=True
                if added_anims is None:
                        added_anims=[]
                run_time=angle/line.speed_rot
                if max_time is not None and run_time>max_time:
                        ratio=max_time/run_time
                        rate_func=lambda t: ratio*t
                        run_time=max_time 
                        change_pivot_at_end=False
                else:
                        rate_func=linear
                self.play(Rotate(line,angle=angle,rate_func=rate_func,run_time=run_time))
                if change_pivot_at_end:
                        line.pivot=new_pivot
                return run_time
        def let_line_run(self,line,time):
                while time>0:
                        last_run_time=self.get_rotating(line,max_time=time)
                        time-=last_run_time
        def get_count(self,line):
                counters=VGroup()
                for point in line.point_set:
                        counter=Integer(0)
                        counter.next_to(point,UP,buff=0.7)
                        counter.scale(0.5)
                        counter.set_color(BLUE)
                        counter.point=point
                        counter.is_pivot=False
                        counter.line=line
                        counter.add_updater(self.update_counter)
                        counters.add(counter)
                return counters
        def update_counter(self,counter):
                dist=get_norm(counter.point-counter.line.pivot)
                counter.will_be_pivot=dist<1e-6
                if not counter.is_pivot and counter.will_be_pivot:
                        counter.increment_value()
                counter.is_pivot=counter.will_be_pivot

class Ball(Circle):
        CONFIG={
                "radius":.4,
                "fill_color":BLUE,
                "fill_opacity":1
        }
        def __init__(self,**kwargs):
                Circle.__init__(self,**kwargs)
                self.velocity=np.array([2,0,0])
        def get_top(self):
                return self.get_center()[1]+self.radius
        def get_bottom(self):
                return self.get_center()[1]-self.radius
        def get_left_edge(self):
                return self.get_center()[0]-self.radius
        def get_right_edge(self):
                return self.get_center()[0]+self.radius
class Box(Rectangle):
        CONFIG={
                "width":FRAME_WIDTH-2,
                "height":6,
                "color":RED
        }
        def __init__(self,**kwargs):
                Rectangle.__init__(self,**kwargs)
                self.top=0.5*self.height
                self.bottom=-0.5*self.height
                self.right_edge=0.5*self.width
                self.left_edge=-0.5*self.width
class BouncingBall(Scene):
        CONFIG={
                "bouncing_wait":15,
        }
        def construct(self):
                box=Box()
                ball=Ball()
                self.play(FadeIn(ball),FadeIn(box))
                def update_ball(ball,dt):
                        ball.aceleration=np.array([0,-15,0])
                        ball.velocity=ball.velocity+ball.aceleration*dt
                        ball.shift(ball.velocity*dt)
                        if ball.get_bottom()<=box.bottom*0.96 or ball.get_top()>=box.top*0.96:
                                ball.velocity[1]=-ball.velocity[1]
                        if ball.get_left_edge()<=box.left_edge or ball.get_right_edge()>=box.right_edge:
                                ball.velocity[0]=-ball.velocity[0]
                ball.add_updater(update_ball)
                self.add(ball)
                self.wait(self.bouncing_wait)
                ball.clear_updaters()
                self.wait()

class MakeAVector(Scene):
        def construct(self):
                dot=Dot()
                vector=Arrow(dot.get_center(),3*UP+4*RIGHT,buff=0)
                self.play(GrowFromCenter(dot),ShowCreation(vector))
                self.wait()

class ZetaTransformaction(ComplexTransformationScene):
        CONFIG={
                "x_min":1,
                "x_max":int(FRAME_X_RADIUS+2),
                "y_min":1,
                "y_max":int(FRAME_Y_RADIUS+2),
                "extra_lines_x_min":-2,
                "extra_lines_x_max":4,
                "extra_lines_y_min":-2,
                "extra_lines_y_max":2,
                "default_apply_complex_function_kwargs":{
                        "run_time":5
                }
        }                
        def get_reflected_plane(self):
                reflected_plane=self.plane.copy()
                reflected_plane.rotate(0*np.pi,UP,about_point=RIGHT)
                for mob in reflected_plane.family_members_with_points():
                        mob.set_color(
                                Color(rgb=1-0.5*color_to_rgb(mob.get_color()))
                        )
                self.prepare_for_transformation(reflected_plane)
                reflected_plane.submobjects=list(reversed(reflected_plane.family_members_with_points()))
                return  reflected_plane
        def add_extra_plane_lines_for_zeta(self,animate=False,**kwargs):
                dense_grid=self.get_dense_grid(**kwargs)
                return dense_grid
        def get_dense_grid(self,step_size=1/2):
                epsilon=0.1
                x_range=np.arange(
                        min(self.x_min,self.extra_lines_y_min),
                        max(self.x_max,self.extra_lines_y_max),
                        step_size
                )
                y_range=np.arange(
                        min(self.y_min,self.extra_lines_y_min),
                        max(self.y_max,self.extra_lines_y_max),
                        step_size
                )
                horizon_lines=VGroup(*[Line(self.x_min*RIGHT,self.x_max*RIGHT).shift(y*UP) for y in y_range if abs(y)>epsilon])
                vert_lines=VGroup(*[
                        Line(self.y_min*UP,self.y_max*UP).shift(x*RIGHT) for x in x_range if abs(x-1)>epsilon
                ])
                horizon_lines.set_color_by_gradient(YELLOW,RED)
                vert_lines.set_color_by_gradient(BLUE,YELLOW)
                dense_grid=VGroup(horizon_lines,vert_lines)
                dense_grid.set_stroke(width=5)
                return dense_grid
        def apply_zeta_function(self,**kwargs):
                transform_kwargs=dict(
                        self.default_apply_complex_function_kwargs
                )
class SquireExtension(ZetaTransformaction):
        CONFIG={
                "anim_kwargs":{
                        "run_time":.1,
                        "rate_func":linear
                }
        }
        def construct(self):
                self.show_negative_one()
                self.get_cyrcle_through_option()
        def show_negative_one(self):
                self.add_transformable_plane()
                thin_plane=self.plane.copy()
                self.remove(self.plane)
                lines=self.add_extra_plane_lines_for_zeta()
                thin_plane.add(self.get_reflected_plane())
                reflected_plane=self.get_reflected_plane()
                self.left_plane=reflected_plane
                self.add(thin_plane,reflected_plane)
                self.play(ShowCreation(lines))
                dots=self.dots=Dot()
                self.apply_zeta_function(added_anims=[
                        ApplyMethod(dots.move_to,self.z_to_point(-1/5),**self.anim_kwargs)
                ])
                self.wait()
        def get_cyrcle_through_option(self):
                gamma=np.euler_gamma
                def shear(point):
                        x,y,z=point
                        return np.array([x,y+.25*(1-x)**2,0])
                def mixed_scalar_func(point):
                        x,y,z=point
                        scalar=1+(gamma-x)/(gamma+FRAME_X_RADIUS)
                        return np.array([(scalar**2)*x,(scalar**3)*y,0])
                def  sinuidal_func(point):
                        x,y,z=point
                        freq=np.pi/gamma
                        return np.array([
                                x-0.2*np.sin(x*freq)*np.sin(y),
                                y-0.2*np.sin(x*freq)*np.sin(y),
                                0
                        ])
                funcs=[
                        shear,
                        mixed_scalar_func,
                        sinuidal_func
                ]
                new_left_planes=[
                        self.left_plane.copy().apply_function(func) for func in funcs
                ]
                new_dots=[self.dots.copy().move_to(func(self.dots.get_center())) for func in funcs]
                self.left_plane.save_state()
                for plane,dot in zip(new_left_planes,new_dots):
                        self.play(
                                Transform(self.left_plane,plane),
                                Transform(self.dots,dot),
                                run_time=3
                        )
                self.wait()

class FunctionGInputScene(SpecialThreeDScene):
        CONFIG={
                "anim_kwargs":{
                        "run_time":.05,
                        "rate_func":linear
                }
        }
        def setup(self):
                self.set_camera_orientation(phi=70,theta=-140)
                self.add(ThreeDAxes())
                #self.play(ShowCreation(ThreeDAxes()),**self.anim_kwargs)
                point=self.init_tracked_point()
                sphere=self.get_sphere()
                self.sphere=sphere
                self.play(ShowCreation(self.sphere),**self.anim_kwargs)
                other_dot=self.init_dot(point.get_center())
                self.play(ShowCreation(other_dot),**self.anim_kwargs)
                self.wait()
        def construct(self):
                pass
        def init_tracked_point(self):
                self.tracked_point=VectorizedPoint([0,0,2])
                return self.tracked_point
        def init_dot(self,point):
                dot=Dot(color=WHITE)
                dot.shift(2.05*OUT)
                dot.apply_matrix(z_to_vector(normalize(point)))
                dot.set_shade_in_3d(True)
                self.dots=always_redraw(lambda: self.point)
                return dot

class MyFirstExerciseIn3d(SpecialThreeDScene):
        CONFIG={
                "anim_kwargs":{
                        "run_time":0.05,
                        "rate_func":linear
                }
        }
        def setup(self):
                self.set_camera_to_default_position()
                self.add(ThreeDAxes())
                self.sphere=self.get_sphere()
                self.play(ShowCreation(self.sphere),**self.anim_kwargs)
        def construct(self):
                my_tracked=self.get_tracked()
                my_dot=self.get_dot(my_tracked.get_center())
                self.play(ShowCreation(my_dot))
                self.wait()
        def get_tracked(self):
                self.tracked_point=VectorizedPoint([0,0,2])
                self.tracked_point.add_updater( lambda t: t.move_to(2*normalize(t.get_center())))
                return self.tracked_point
        def get_dot(self,point):
                dot=Dot(color=WHITE)
                dot.shift(2.05*OUT)
                dot.apply_matrix(z_to_vector(normalize(point)))
                return dot
class FunctionGInputSpace2(SpecialThreeDScene):
    CONFIG={
                "anim_kwargs":{
                        "run_time":0.05,
                        "rate_func":linear
                },
                "time_wait":0.2
        }
    def setup(self):
        self.init_tracked_point()
        sphere = self.get_sphere()
        sphere.set_fill(BLUE_E, opacity=0.5)
        self.sphere = sphere

        self.set_camera_orientation(
            phi=70 * DEGREES,
            theta=-120 * DEGREES,
        )
        self.begin_ambient_camera_rotation(rate=0.02)

        self.init_dot()

        self.add(ThreeDAxes())

    def construct(self):
        self.show_input_dot()
        self.show_start_path()
        self.show_antipodal_point()
        self.show_equator()
        self.deform_towards_north_pole()

    def show_input_dot(self):
        sphere = self.sphere
        dot = self.dot
        point_mob = self.tracked_point
        start_point = self.get_start_point()

        arrow = Arrow(
            start_point + (LEFT + OUT + UP), start_point,
            color=BLUE,
            buff=MED_LARGE_BUFF,
        )
        arrow.rotate(90 * DEGREES, axis=arrow.get_vector())
        arrow.add_to_back(arrow.copy().set_stroke(BLACK, 5))

        p_label = self.p_label = TexMobject("\\vec{\\textbf{p}}")
        p_label.set_color(YELLOW)
        p_label.next_to(arrow.get_start(), OUT, buff=0.3)
        p_label.set_shade_in_3d(True)

        self.play(Write(sphere, **self.anim_kwargs))
        self.add(dot)
        self.add_fixed_orientation_mobjects(p_label)
        self.play(
            point_mob.move_to, start_point,
            GrowArrow(arrow),
            FadeInFrom(p_label, IN),**self.anim_kwargs
        )
        self.wait(self.time_wait)
        self.play(
            arrow.scale, 0, {"about_point": arrow.get_end()},
            p_label.next_to, dot, OUT + LEFT, SMALL_BUFF,
            **self.anim_kwargs
        )
        p_label.add_updater(lambda p: p.next_to(dot, OUT + LEFT, SMALL_BUFF))
        self.wait(self.time_wait)

    def show_start_path(self):
        path = self.get_start_path()
        self.draw_path(path, uncreate=True)
        self.wait(self.time_wait)

    def show_antipodal_point(self):
        path = self.get_antipodal_path()
        end_dot = always_redraw(
            lambda: self.get_dot(
                path[-1].point_from_proportion(1)
            ).set_color(RED)
        )

        neg_p = TexMobject("-\\vec{\\textbf{p}}")
        neg_p.add_updater(
            lambda p: p.next_to(end_dot, UP + RIGHT + IN)
        )
        neg_p.set_color(RED)
        neg_p.set_shade_in_3d(True)

        self.move_camera(
            phi=100 * DEGREES,
            theta=30 * DEGREES,
            added_anims=[ShowCreation(path)],
            **self.anim_kwargs,
        )
        self.wait(self.time_wait)
        self.add_fixed_orientation_mobjects(neg_p)
        self.play(
            FadeInFromLarge(end_dot),
            Write(neg_p),
            **self.anim_kwargs
        )
        self.wait(self.time_wait)
        self.move_camera(
            phi=70 * DEGREES,
            theta=-120 * DEGREES,
            **self.kwargs
        )
        self.wait(self.time_wait)
        # Flip
        self.move_camera(
            phi=100 * DEGREES,
            theta=30 * DEGREES,
            **self.anim_kwargs,
        )
        self.wait(self.time_wait)
        self.move_camera(
            phi=70 * DEGREES,
            theta=-120 * DEGREES,
            added_anims=[
                FadeOut(end_dot),
                FadeOut(neg_p),
                FadeOut(path),
            ],
            **self.anim_kwargs,
        )

    def show_equator(self):
        point_mob = self.tracked_point
        equator = self.get_lat_line()

        self.play(point_mob.move_to, equator[0].point_from_proportion(0),**self.anim_kwargs)
        self.play(ShowCreation(equator, **self.anim_kwargs))
        for x in range(2):
            self.play(
                Rotate(point_mob, PI, about_point=ORIGIN, axis=OUT),
                **self.anim_kwargs
            )
            self.wait(self.time_wait)
        self.play(
            FadeOut(self.dot),
            FadeOut(self.p_label),
            **self.anim_kwargs
        )

        self.equator = equator

    def deform_towards_north_pole(self):
        equator = self.equator

        self.play(UpdateFromAlphaFunc(
            equator,
            lambda m, a: m.become(self.get_lat_line(a * PI / 2)),
            **self.anim_kwargs
        ))
        self.wait(self.time_wait)

    #
    def init_tracked_point(self):
        self.tracked_point = VectorizedPoint([0, 0, 2])
        self.tracked_point.add_updater(
            lambda p: p.move_to(2 * normalize(p.get_center()))
        )
        self.add(self.tracked_point)

    def init_dot(self):
        self.dot = always_redraw(
            lambda: self.get_dot(self.tracked_point.get_center())
        )

    def get_start_path(self):
        path = ParametricFunction(
            lambda t: np.array([
                -np.sin(TAU * t + TAU / 4),
                np.cos(2 * TAU * t + TAU / 4),
                0
            ]),
            color=RED
        )
        path.scale(0.5)
        path.shift(0.5 * OUT)
        path.rotate(60 * DEGREES, RIGHT, about_point=ORIGIN)
        path.shift(
            self.get_start_point() - path.point_from_proportion(0)
        )
        path.apply_function(lambda p: 2 * normalize(p))
        return path

    def get_antipodal_path(self):
        start = self.get_start_point()
        path = ParametricFunction(
            lambda t: 2.03 * np.array([
                0,
                np.sin(PI * t),
                np.cos(PI * t),
            ]),
            color=YELLOW
        )
        path.apply_matrix(z_to_vector(start))

        dashed_path = DashedVMobject(path)
        dashed_path.set_shade_in_3d(True)

        return dashed_path

    def get_lat_line(self, lat=0):
        equator = ParametricFunction(lambda t: 2.03 * np.array([
            np.cos(lat) * np.sin(TAU * t),
            np.cos(lat) * (-np.cos(TAU * t)),
            np.sin(lat)
        ]))
        equator.rotate(-90 * DEGREES)
        dashed_equator = DashedVMobject(
            equator,
            num_dashes=40,
            color=RED,
        )
        dashed_equator.set_shade_in_3d(True)
        return dashed_equator

    def draw_path(self, path,
                  run_time=4,
                  dot_follow=True,
                  uncreate=False,
                  added_anims=None
                  ):
        added_anims = added_anims or []
        point_mob = self.tracked_point
        anims = [ShowCreation(path)]
        if dot_follow:
            anims.append(UpdateFromFunc(
                point_mob,
                lambda p: p.move_to(path.point_from_proportion(1))
            ))
        self.add(path, self.dot)
        self.play(*anims, **self.anim_kwargs)

        if uncreate:
            self.wait(self.time_wait)
            self.play(
                Uncreate(path),
                **self.anim_kwargs
            )

    def modify_path(self, path):
        return path

    def get_start_point(self):
        return 2 * normalize([-1, -1, 1])

    def get_dot(self, point):
        dot = Dot(color=WHITE)
        dot.shift(2.05 * OUT)
        dot.apply_matrix(z_to_vector(normalize(point)))
        dot.set_shade_in_3d(True)
        return dot

class FirstCase3D(SpecialThreeDScene):
        CONFIG={
                "anim_kwargs":{
                        "run_time":0.4,
                        "rate_func":linear
                }
        }
        def setup(self):
                self.set_camera_orientation(phi=70,theta=-150)
                self.sphere=self.get_sphere()
                self.init_tracked_point()
                self.init_dot()
                self.sphere.set_opacity(opacity=0.4)
        def construct(self):
                self.play(ShowCreation(self.sphere),**self.anim_kwargs)
                self.play(ShowCreation(self.dot))
                self.show_equator()
                self.wait()
        def init_tracked_point(self):
                self.tracked_point=VectorizedPoint([2,0,0])
                self.tracked_point.add_updater(lambda t: t.move_to(2*normalize(t.get_center())))
                self.add(self.tracked_point)
        def init_dot(self):
                self.dot=always_redraw(lambda: self.get_dot(self.tracked_point.get_center()))
        def get_dot(self,point):
                dot=Dot(color=WHITE,radius=0.08)
                dot.shift(2.05*OUT)
                dot.apply_matrix(z_to_vector(normalize(point)))
                return dot
        def show_equator(self):
                equator=self.get_lat_line()
                self.play(self.tracked_point.move_to,equator[0].point_from_proportion(0))
                for x in range(2):
                        self.play(Rotate(
                                self.tracked_point,PI,about_point=ORIGIN,axis=OUT
                        ),
                        run_time=1
                )
                self.wait()
                self.equator=equator
        def get_lat_line(self,lat=0):
                equator=ParametricFunction(
                        lambda t: 2.03*np.array([
                                np.cos(lat)*np.sin(TAU*t),
                                np.cos(lat)*(-np.cos(TAU*t)),
                                np.sin(lat)
                        ])
                )
                equator.rotate(-90*DEGREES)
                dashed_equator=DashedVMobject(equator,num_dashed=40,color=RED)
                dashed_equator.set_shade_in_3d(True)
                return dashed_equator

class SecondExercise(ThreeDScene):
        CONFIG={
                "anim_kwargs":{
                        "run_time":0.1,
                        "rate_func":linear
                },
                "time_wait":0.5,
                "dot_kwargs":{
                        "radius":0.05,
                },
                "vector_kwargs":{
                        "stroke_width":0.8
                }
        }
        def construct(self):
                self.set_camera_orientation(phi=60*DEGREES,theta=-140*DEGREES)
                sphere=self.get_sphere()
                self.play(ShowCreation(sphere),**self.anim_kwargs)
                circle=self.flat_circle()
                self.play(ShowCreation(circle),**self.anim_kwargs)
                self.wait(self.time_wait)
                dot_center=self.get_dot_center(sphere)
                self.play(ShowCreation(dot_center),**self.anim_kwargs)
                dot_sphere=self.get_dot_sphere()
                my_dot=self.get_dot()
                self.play(ShowCreation(my_dot),**self.anim_kwargs)
                arrow=self.get_arrow(dot_center,my_dot)
                self.play(ShowCreation(arrow))
                self.play(Rotate(my_dot,50*DEGREES,about_point=sphere.get_center(),axis=X_AXIS),**self.anim_kwargs)
                self.wait()
        def get_sphere(self):
                superficie=ParametricSurface(
                        lambda u,v: 2*np.array([
                                np.cos(u)*np.sin(v),
                                np.sin(u)*np.sin(v),
                                np.cos(v)
                        ]),
                        u_min=0,
                        u_max=2*PI,
                        v_min=0,
                        v_max=PI,
                        fill_opacity=0,
                        resolution=[40,25]
                )
                return superficie
        def flat_circle(self):
                circle=Circle(radius=2,color=BLUE,stroke_width=0,fill_opacity=0.5)
                return circle
        def get_dot_center(self,sphere):
                return Dot(**self.dot_kwargs).move_to(sphere.get_center())
        def get_dot_sphere(self):
                point=self.point=VectorizedPoint([0,0,2])
                point.add_updater(lambda t: t.move_to(2*normalize(t.get_center())))
                return point
        def get_dot(self):
                dot=Dot(**self.dot_kwargs)
                dot.shift(self.point.get_center())
                return dot
        def get_arrow(self,center,dot):
                arrow=DashedLine(center.get_center(),dot.get_center(),max_stroke_width_to_length_ratio=0,\
                        max_tip_length_to_length_ratio=0.25,preserve_tip_size_when_scaling=False,**self.vector_kwargs)
                arrow.add_updater(lambda t: t.put_start_and_end_on(center.get_center(),dot.get_center()))
                return arrow
class Make2D(Scene):
        CONFIG={
                "radius":3,
                "arrow_kwargs":{
                        "stroke_width": 1,
                        "buff": 0,
                        "max_tip_length_to_length_ratio": 0.25,
                        "max_stroke_width_to_length_ratio": 1,
                        "preserve_tip_size_when_scaling": False,
                },
                "anim_kwargs":{
                        "run_time":2,
                        "rate_func":linear
                }
        }
        def construct(self):
                axes=Axes()
                circle=Circle(radius=self.radius)
                self.play(ShowCreation(axes),ShowCreation(circle),**self.anim_kwargs)
                theta=30*DEGREES
                alpha=ValueTracker(theta)
                dot=Dot()
                dot.add_updater(lambda t: t.move_to(axes.coords_to_point(self.\
                        radius*np.cos(alpha.get_value()),self.radius*np.sin(alpha.get_value()))))
                self.play(GrowFromCenter(dot),**self.anim_kwargs)
                arrow=self.get_my_arrow(circle,dot)
                self.play(ShowCreation(arrow),**self.anim_kwargs)
                for t in np.random.random(size=10)*360*DEGREES:
                        self.play(alpha.set_value,t,**self.anim_kwargs)
                line_h_coord=DashedLine(axes.coords_to_point(self.radius*0,self.radius*np.sin(alpha.get_value())),axes.coords_to_point(self.radius*np.cos(alpha.get_value()),self.radius*np.sin(alpha.get_value())))
                line_v_coord=DashedLine(axes.coords_to_point(self.radius*np.cos(alpha.get_value()),self.radius*0),axes.coords_to_point(self.radius*np.cos(alpha.get_value()),self.radius*np.sin(alpha.get_value())))
                #line_h_coord.set_color(GREEN)
                #line_v_coord.set_color(YELLOW)
                group=VGroup(line_h_coord,line_v_coord)
                def update_elements(VGroup):
                        line_h_coord_u,line_v_coord_u=group
                        line_h_coord_u.put_start_and_end_on(axes.coords_to_point(self.radius*0,self.radius*np.sin(alpha.get_value())),axes.coords_to_point(self.radius*np.cos(alpha.get_value()),self.radius*np.sin(alpha.get_value())))
                        line_v_coord_u.put_start_and_end_on(axes.coords_to_point(self.radius*np.cos(alpha.get_value()),self.radius*0),axes.coords_to_point(self.radius*np.cos(alpha.get_value()),self.radius*np.sin(alpha.get_value())))
                self.wait()
                group.add_updater(update_elements)
                for mob in line_h_coord,line_v_coord:
                        self.play(ShowCreation(mob),**self.anim_kwargs)
                self.add(group)
                for ang in np.random.random(size=10)*360*DEGREES:
                        self.play(alpha.set_value,ang,**self.anim_kwargs)
                self.wait()
                group_line=VGroup(line_v_coord,line_h_coord)
                numbers=self.get_numbers(group_line,alpha)
                self.play(ShowCreation(numbers),**self.anim_kwargs)
                for ang in np.random.random(size=10)*360*DEGREES:
                        self.play(alpha.set_value,ang,**self.anim_kwargs)
                self.wait()
        def get_my_arrow(self,circle,dot):
                arrow=Arrow(circle.get_center(),dot.get_center(),**self.arrow_kwargs)
                arrow.add_updater(lambda t: t.put_start_and_end_on(circle.get_center(),dot.get_center()))
                return arrow
        def get_numbers(self,lines,alpha):
                line_h,line_v=lines
                decimal_v_axis=DecimalNumber(self.radius*np.sin(alpha.get_value()))
                decimal_v_axis.scale(.5)
                decimal_h_axis=DecimalNumber(self.radius*np.cos(alpha.get_value()))
                decimal_h_axis.scale(.5)
                decimal_v_axis.add_updater(lambda t: t.set_value(self.radius*np.sin(alpha.get_value())))
                decimal_h_axis.add_updater(lambda t: t.set_value(self.radius*np.cos(alpha.get_value())))
                def update_position_h(num_h):
                        if line_v.get_end()[1]>0.00001:
                                decimal_h_axis.next_to(line_h.get_start(),DOWN,buff=0.15)
                        else:
                                decimal_h_axis.next_to(line_h.get_start(),UP,buff=0.15)#
                def update_position_v(num_v):
                        if line_h.get_end()[0]>0.00001:
                                decimal_v_axis.next_to(line_v.get_start(),LEFT,buff=0.15)#
                        else:
                                decimal_v_axis.next_to(line_v.get_start(),RIGHT,buff=0.15)
                decimal_h_axis.add_updater(update_position_h)
                decimal_v_axis.add_updater(update_position_v)
                return VGroup(decimal_v_axis,decimal_h_axis)

class Example2(Scene):
        def construct(self):
                dot=Dot().move_to(2*LEFT)
                dot_center=Dot().move_to(ORIGIN)
                line=DashedLine()
                line.put_start_and_end_on(dot_center.get_center(),dot.get_center()+0.0001*RIGHT)    
                def update_line(line):
                        line.put_start_and_end_on(dot_center.get_center(),dot.get_center()+0.0001*RIGHT)
                line.add_updater(update_line)            
                self.play(ShowCreation(dot),ShowCreation(dot_center))
                self.add(line)
                texto=self.get_texto(dot)
                self.play(Write(texto))
                time=0
                while time<10:
                        my_time=1
                        time+=my_time
                        self.play(dot.move_to,2*LEFT,run_time=my_time)
                        self.play(dot.move_to,2*RIGHT,run_time=my_time)
                self.wait()
        def get_texto(self,dot):
                texto=TextMobject("Prueba")
                def get_update_text0(text0):
                        if np.all(dot.get_center()[0]>0):
                                texto.next_to(dot.get_center(),RIGHT,buff=0.2)
                        else:
                                texto.next_to(dot.get_center(),LEFT,buff=0.2)
                texto.add_updater(get_update_text0)
                return texto

class WhatIsSurfaceArea(SpecialThreeDScene):
    CONFIG = {
        "change_power": True,
    }

    def construct(self):
        title = TextMobject("What is surface area?")
        title.scale(1.5)
        title.to_edge(UP)
        title.shift(0.035 * RIGHT)
        self.add_fixed_in_frame_mobjects(title)

        power_tracker = ValueTracker(1)
        surface = always_redraw(
            lambda: self.get_surface(
                radius=3,
                amplitude=1,
                power=power_tracker.get_value()
            )
        )

        pieces = surface.copy()
        pieces.clear_updaters()
        random.shuffle(pieces.submobjects)

        self.set_camera_to_default_position()
        self.begin_ambient_camera_rotation()
        # self.add(self.get_axes())
        self.play(LaggedStartMap(
            DrawBorderThenFill, pieces,
            lag_ratio=0.2,
        ))
        self.remove(pieces)
        self.add(surface)
        if self.change_power:
            self.play(
                power_tracker.set_value, 5,
                run_time=2
            )
            self.play(
                power_tracker.set_value, 1,
                run_time=2
            )
        self.wait(2)

    def get_surface(self, radius, amplitude, power):
        def alt_pow(x, y):
            return np.sign(x) * (np.abs(x) ** y)
        return ParametricSurface(
            lambda u, v: radius * np.array([
                v * np.cos(TAU * u),
                v * np.sin(TAU * u),
                0,
            ]) + amplitude * np.array([
                0,
                0,
                (v**2) * alt_pow(np.sin(5 * TAU * u), power),
            ]),
            resolution=(100, 20),
            v_min=0.01
        )

class 