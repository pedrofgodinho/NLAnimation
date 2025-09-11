from manim import *
import numpy as np

class Part2_TheSolution(Scene):
    def animate_axes(self):
        # Axes
        self.axes = Axes(
            x_range=[-8, 8, 1],
            y_range=[-4, 4, 1],
            x_length=10 * self.scale_factor,
            y_length=7 * self.scale_factor,
            axis_config={"color": BLUE},
        ).shift(self.graph_shift)

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

        self.play(Create(self.axes), run_time=2)
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

        # Animate initial vectors
        self.play(
            GrowArrow(self.vector_objects["Queen"][0]), FadeIn(self.vector_objects["Queen"][1]), Write(self.vector_objects["Queen"][2]),
            run_time=1.5
        )
        self.wait(1)
        self.play(
            GrowArrow(self.vector_objects["King"][0]), FadeIn(self.vector_objects["King"][1]), Write(self.vector_objects["King"][2]),
            run_time=1.5
        )
        self.wait(1)
        self.play(
            GrowArrow(self.vector_objects["Woman"][0]), FadeIn(self.vector_objects["Woman"][1]), Write(self.vector_objects["Woman"][2]),
            GrowArrow(self.vector_objects["Man"][0]), FadeIn(self.vector_objects["Man"][1]), Write(self.vector_objects["Man"][2]),
            run_time=1.5
        )
    
    def animate_equation_write(self):
        # Create the initial equation as a class attribute
        self.equation = MathTex(
            r"\vec{King}", r"-", r"\vec{Man}", r"+", r"\vec{Woman}", r"=", r"?"
        ).to_edge(UP)

        self.play(Write(self.equation))
        self.wait(3)

        # Create the second form of the equation
        second_equation = MathTex(
            r"\vec{King}", r"+", r"(", r"\vec{Woman}", r"-", r"\vec{Man}", r")", r"=", r"?"
        ).to_edge(UP)

        # Transform the original self.equation into the second_equation
        # This keeps self.equation on the screen, just with a new shape.
        self.play(Transform(self.equation, second_equation))

    def animate_vector_arithmetic(self):
        # 1. Focus on (Woman - Man)
        self.play(Indicate(self.equation[2:7])) # Highlight (Woman-Man) in equation
        self.wait(1)
        self.play(
            Indicate(self.vector_objects["Woman"][0]),
            Indicate(self.vector_objects["Man"][0])
        )
        self.wait(1)

        # Create copies to animate
        woman_vec_copy = self.vector_objects["Woman"][0].copy().set_color(GREEN)
        man_vec_copy = self.vector_objects["Man"][0].copy().set_color(RED)

        # Animate "Woman - Man" by adding a flipped "Man" vector to "Woman"
        self.play(man_vec_copy.animate.rotate(PI, about_point=man_vec_copy.get_start()))
        self.play(man_vec_copy.animate.shift(woman_vec_copy.get_end() - woman_vec_copy.get_start()))
        self.wait(1)

        # Draw the resulting "gender difference" vector
        gender_diff_vec = Arrow(
            woman_vec_copy.get_start(), man_vec_copy.get_end(), 
            color=BLUE, buff=0
        )
        self.play(GrowArrow(gender_diff_vec))
        self.wait(2)
        
        # We don't need the intermediate vectors anymore
        self.play(FadeOut(woman_vec_copy, man_vec_copy))

        # 2. Now, add this result to King
        self.play(Indicate(self.equation[0])) # Highlight King in equation
        self.play(Indicate(self.vector_objects["King"][0]))
        self.wait(1)
        
        # Move the gender_diff_vec to the end of the King vector
        king_end_point = self.vector_objects["King"][0].get_end()
        self.play(gender_diff_vec.animate.shift(king_end_point - gender_diff_vec.get_start()))
        self.wait(2)

        # 3. Show the final result
        final_result_vec = Arrow(self.axes.get_origin(), gender_diff_vec.get_end(), color=ORANGE, buff=0)
        self.play(GrowArrow(final_result_vec))
        self.wait(1)

        # 4. Highlight that this matches Queen
        self.play(
            Flash(self.vector_objects["Queen"][1], color=ORANGE, flash_radius=0.5),
            Indicate(self.vector_objects["Queen"][0], color=ORANGE)
        )

        # 5. Update the equation to its final form
        final_equation = MathTex(
            r"\vec{King}", r"+", r"(", r"\vec{Woman}", r"-", r"\vec{Man}", r")", r"\approx", r"\vec{Queen}"
        ).to_edge(UP)
        # This transform now works correctly because self.equation is the mobject on screen
        self.play(Transform(self.equation, final_equation))
        self.wait(3)

        # 6. Clean up the animation vectors
        self.play(FadeOut(gender_diff_vec, final_result_vec))

    def construct(self):
        """
        This scene covers the second and third parts of the video plan.
        It introduces word embeddings and then demonstrates vector arithmetic.
        """
        self.camera.background_color = "#1E1E1E"

        self.scale_factor = 0.7
        self.graph_shift = DOWN * 1.2

        self.animate_axes()
        self.wait(3)

        self.animate_vectors_drawing()
        self.wait(3)

        self.animate_equation_write()
        self.wait(3)

        self.animate_vector_arithmetic()
        self.wait(3)

