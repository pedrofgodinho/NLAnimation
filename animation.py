from manim import *
import numpy as np

# A consistent, dark background for all scenes
BACKGROUND_COLOR = "#1E1E1E"

# Seed RNG
np.random.seed(42)

class Part1(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR

        self.animate_binary_code()
        self.animate_word_cloud_transition()
        self.animate_king_queen_question()

    def animate_binary_code(self):
        ### 2.5s - Computer's understand numbers perfectly
        binary_string = "\n".join(
            ["".join(np.random.choice(["0", "1"], 70)) for _ in range(40)]
        )
        self.binary_code = Text(binary_string, font="Monospace", font_size=16, fill_opacity=0.4)
        
        self.play(Write(self.binary_code), run_time=2.5)
        self.wait(1)

    def animate_word_cloud_transition(self):
        ### (4s) But language? It's messy, subjective, and full of context.
        words = ["King", "Queen", "Walks", "Running", "France", 
                 "Paris", "Apple", "Software", "Cat", "Dog", "Piano", "Violin"]
        
        word_mobjects = VGroup()
        self.text_map = {} 

        for word_str in words:
            text_obj = Text(word_str, font_size=32)
            word_mobjects.add(text_obj)
            self.text_map[word_str] = text_obj
        
        word_mobjects.arrange_in_grid(rows=3, cols=4, buff=2.0)
        
        for word in word_mobjects:
            word.shift(np.random.rand(3) * 0.75)
            word.scale(np.random.uniform(0.9, 1.3))
            word.rotate(np.random.uniform(-PI/12, PI/12))
            
        self.play(
            LaggedStart(
                *[FadeIn(word, shift=UP*0.2) for word in word_mobjects],
                lag_ratio=0.1
            ),
            FadeOut(self.binary_code, scale=0.8),
            run_time=3
        )
        self.wait(1)

    def animate_king_queen_question(self):
        ### (7s) How can we teach a machine that words like 'King' and 'Queen' are related, but also different?

        king_text = self.text_map["King"]
        queen_text = self.text_map["Queen"]
        
        connection_line = Line(
            king_text.get_right() + (RIGHT * 0.1), 
            queen_text.get_left() + (LEFT * 0.2), # The Q is wider 
            color=YELLOW,
            stroke_width=5
        )
        
        self.play(
            Indicate(king_text, color=YELLOW, scale_factor=1.2),
            Indicate(queen_text, color=YELLOW, scale_factor=1.2),
            ShowPassingFlash(connection_line, time_width=0.4, run_time=1),
            run_time=2
        )

        self.wait(2)
        
        question_mark = Text("?", font_size=144, color=YELLOW)
        final_text = Text("Meaning = Math?", font_size=48).next_to(question_mark, DOWN, buff=0.5)

        vgroup = VGroup(king_text, queen_text)
        
        other_words = VGroup(*[m for k, m in self.text_map.items() if k not in ["King", "Queen"]])
        self.play(
            FadeOut(other_words),
        )
        
        ### (3s) What if we could turn meaning into math?
        self.play(Transform(vgroup, question_mark), run_time=1.5)
        self.wait(3)
        self.play(Write(final_text))
        
        self.wait(3)

        self.play(
            FadeOut(vgroup),
            FadeOut(final_text)
        )


class Part2(Scene):
    def animate_axes(self):
        ### (7s) The solution is to represent words as vectors in a multi-dimensional space, a concept called word embedding.
        # Axes
        self.axes = Axes(
            x_range=[-8, 8, 1],
            y_range=[-4, 4, 1],
            x_length=10 * self.scale_factor,
            y_length=7 * self.scale_factor,
            axis_config={"color": BLUE},
        ).shift(self.graph_shift)

        self.play(Create(self.axes), run_time=2)

        # Show some random vectors to illustrate the space
        vectors = VGroup(*[
            Arrow(
                self.axes.get_origin(), 
                np.array([
                    -2, 2, 0
                ]) * self.scale_factor + self.graph_shift,
                color=WHITE, buff=0
            ),
            Arrow(
                self.axes.get_origin(), 
                np.array([
                    3, -1, 0
                ]) * self.scale_factor + self.graph_shift,
                color=WHITE, buff=0
            ),
            Arrow(
                self.axes.get_origin(), 
                np.array([
                    -4, -2, 0
                ]) * self.scale_factor + self.graph_shift,
                color=WHITE, buff=0
            ),
            Arrow(
                self.axes.get_origin(), 
                np.array([
                    1, 3, 0
                ]) * self.scale_factor + self.graph_shift,
                color=WHITE, buff=0
            ),
            Arrow(
                self.axes.get_origin(), 
                np.array([
                    5, 1, 0
                ]) * self.scale_factor + self.graph_shift,
                color=WHITE, buff=0
            ),
        ])

        # play all vectors without lagged start
        ### (8s) Think of it like giving every single word a coordinate. In this space, words with similar meanings are placed close together.
        self.play([GrowArrow(vec) for vec in vectors], run_time=1.5)
        self.wait(8)

        self.play([FadeOut(vec) for vec in vectors], lag_ratio=0.5, run_time=1)

            
    def animate_labels(self):
        ### (6s) Let's simplify this. Let's label the vertical axis 'Royalty' and the horizontal axis 'Gender'.
        # Labels
        self.y_label = self.axes.get_y_axis_label(
            Text("Royalty", font_size=36 * self.scale_factor, color=WHITE), 
            edge=UP, direction=UP, buff=0.1 * self.scale_factor
        )
        self.x_label_masculine = self.axes.get_x_axis_label(
            Text("Masculine", font_size=36 * self.scale_factor, color=WHITE),
            edge=RIGHT, direction=DOWN, buff=0.3 * self.scale_factor
        )
        self.x_label_feminine = self.axes.get_x_axis_label(
            Text("Feminine", font_size=36 * self.scale_factor, color=WHITE),
            edge=LEFT, direction=DOWN, buff=0.3 * self.scale_factor
        )
        self.play(
            Write(self.y_label),
            Write(self.x_label_masculine),
            Write(self.x_label_feminine),
        )

    
    def animate_vectors_drawing(self):
        self.coords = {
            "Queen": (np.array([-3, 2.5, 0]) * self.scale_factor) + self.graph_shift,
            "King":  (np.array([3, 2.5, 0]) * self.scale_factor) + self.graph_shift,
            "Woman": (np.array([-3, -2.5, 0]) * self.scale_factor) + self.graph_shift,
            "Man":   (np.array([3, -2.5, 0]) * self.scale_factor) + self.graph_shift,
        }

        self.vector_objects = {}
        for word, coord in self.coords.items():
            # Determine label direction based on the word to avoid overlap
            if word in ["Queen", "Woman"]:
                label_direction = UL
            else:
                label_direction = UR

            self.vector_objects[word] = VGroup(
                Arrow(self.axes.get_origin(), coord, color=YELLOW, buff=0),
                Dot(point=coord, color=YELLOW),
                Text(word, font_size=32 * self.scale_factor).next_to(coord, direction=label_direction, buff=0.1)
            )

        ### (5s) A word like 'King' would have a high Royalty score and a masculine Gender score.
        # Animate initial vectors
        self.play(
            GrowArrow(self.vector_objects["Queen"][0]), FadeIn(self.vector_objects["Queen"][1]), Write(self.vector_objects["Queen"][2]),
            run_time=0.5
        )
        self.wait(5)
        ### (5s) 'Queen' would be similar in Royalty, but with a feminine score.
        self.play(
            GrowArrow(self.vector_objects["King"][0]), FadeIn(self.vector_objects["King"][1]), Write(self.vector_objects["King"][2]),
            run_time=0.5
        )
        self.wait(5)
        self.play(
            GrowArrow(self.vector_objects["Woman"][0]), FadeIn(self.vector_objects["Woman"][1]), Write(self.vector_objects["Woman"][2]),
            GrowArrow(self.vector_objects["Man"][0]), FadeIn(self.vector_objects["Man"][1]), Write(self.vector_objects["Man"][2]),
            run_time=1.5
        )
    
    def animate_equation_write(self):
        ### (8s) This is where it gets amazing. Because words are now vectors, we can perform arithmetic on them. Watch this.

        self.equation = MathTex(
            r"\vec{King}", r"-", r"\vec{Man}", r"+", r"\vec{Woman}", r"=", r"?"
        ).to_edge(UP)

        self.play(Write(self.equation))
        self.wait(7)

        ### (4s) Let's rewrite the equation to make what we're doing clearer.

        second_equation = MathTex(
            r"\vec{King}", r"+", r"(", r"\vec{Woman}", r"-", r"\vec{Man}", r")", r"=", r"?"
        ).to_edge(UP)
        self.wait(4)

        self.play(Transform(self.equation, second_equation))

    def animate_vector_arithmetic(self):
        self.play(Indicate(self.equation[2:7])) 
        self.wait(1)
        self.play(
            Indicate(self.vector_objects["Woman"][0]),
            Indicate(self.vector_objects["Man"][0])
        )
        self.wait(1)

        woman_vec_copy = self.vector_objects["Woman"][0].copy().set_color(GREEN)
        man_vec_copy = self.vector_objects["Man"][0].copy().set_color(RED)

        self.play(man_vec_copy.animate.rotate(PI, about_point=man_vec_copy.get_start()))
        self.play(man_vec_copy.animate.shift(woman_vec_copy.get_end() - woman_vec_copy.get_start()))
        self.wait(1)

        gender_diff_vec = Arrow(
            woman_vec_copy.get_start(), man_vec_copy.get_end(), 
            color=BLUE, buff=0
        )
        ### (5s) This vector, 'Woman - Man', is now a transformation that when applied to King...
        self.play(GrowArrow(gender_diff_vec))
        self.wait(2)
        
        self.play(FadeOut(woman_vec_copy, man_vec_copy))

        self.play(Indicate(self.equation[0])) # Highlight King in equation
        self.play(Indicate(self.vector_objects["King"][0]))
        self.wait(1)
        
        king_end_point = self.vector_objects["King"][0].get_end()
        self.play(gender_diff_vec.animate.shift(king_end_point - gender_diff_vec.get_start()))
        self.wait(2)

        final_result_vec = Arrow(self.axes.get_origin(), gender_diff_vec.get_end(), color=ORANGE, buff=0)
        self.play(GrowArrow(final_result_vec))
        self.wait(1)

        ### (3s) ...lands almost exactly where 'Queen' is located.
        ### (4s) This is how a model can learn the relationship between these concepts.
        self.play(
            Flash(self.vector_objects["Queen"][1], color=ORANGE, flash_radius=0.5),
        )

        final_equation = MathTex(
            r"\vec{King}", r"+", r"(", r"\vec{Woman}", r"-", r"\vec{Man}", r")", r"\approx", r"\vec{Queen}"
        ).to_edge(UP)
        self.play(Transform(self.equation, final_equation))
        self.wait(3)

        self.play(FadeOut(gender_diff_vec, final_result_vec))

    def construct(self):
        self.camera.background_color = "#1E1E1E"

        self.scale_factor = 0.7
        self.graph_shift = DOWN * 1.2

        self.animate_axes()
        self.wait(1)
        self.animate_labels()
        self.wait(2)

        self.animate_vectors_drawing()
        self.wait(3)

        self.animate_equation_write()
        self.wait(3)

        self.animate_vector_arithmetic()
        self.wait(3)

        # Fade out all remaining elements for a clean transition
        mobjects_to_fade = VGroup(
            self.axes,
            self.y_label,
            self.x_label_masculine,
            self.x_label_feminine,
            self.equation,
            *self.vector_objects.values()
        )
        self.play(FadeOut(mobjects_to_fade))


class Part3(ThreeDScene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        self.set_camera_orientation(phi=0, theta=-PI/2)

        axes = ThreeDAxes(
            x_range=[-7, 7, 1], y_range=[-5, 5, 1], z_range=[-5, 5, 1],
            x_length=14, y_length=10, z_length=8,
            axis_config={"color": BLUE_C, "stroke_width": 2, "stroke_opacity":0.5}
        )
        self.play(FadeIn(axes))
        self.wait()

        points = VGroup(*[
            Dot(
                point=[np.random.uniform(-7, 7), np.random.uniform(-5, 5), np.random.uniform(-4, 4)],
                radius=0.04, color=WHITE, fill_opacity=0.6
            ) for _ in range(300)
        ])
        
        self.move_camera(phi=70 * DEGREES, theta=-45 * DEGREES, zoom=0.8, run_time=3)
        
        self.play(
            FadeIn(points, scale=0.5, lag_ratio=0.01)
        )
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(1)
        
        self.stop_ambient_camera_rotation()
        self.play(
            FadeOut(points),
            FadeOut(axes)
        )

        self.move_camera(phi=0, theta=-PI/2, zoom=1.0, run_time=1)
        
        title = Text("Languages as Vectors", font_size=60)
        subtitle = Text("Turning Meaning into Math", font_size=36).next_to(title, DOWN, buff=0.4)
        final_card = VGroup(title, subtitle)

        self.play(Write(final_card))
        self.wait(3)

