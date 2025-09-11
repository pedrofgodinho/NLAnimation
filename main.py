from manim import *
import numpy as np

class Part1_LanguagesAsVectors(Scene):
    def construct(self):
        """
        This scene covers the first 20 seconds of the video plan.
        It transitions from binary code to a word cloud, then highlights
        the relationship between 'King' and 'Queen'.
        """
        
        # -----------------------------------------------------------------
        # [0:00 - 0:05] Binary code flows rapidly across the screen.
        # -----------------------------------------------------------------
        self.camera.background_color = "#1E1E1E" # A dark background
        
        # Generate a block of random binary text
        binary_string = "\n".join(
            ["".join(np.random.choice(["0", "1"], 60)) for _ in range(30)]
        )
        binary_code = Text(binary_string, font="Monospace", font_size=14)
        
        # Animate the appearance of the binary code
        self.play(Write(binary_code), run_time=2.5)
        self.wait(1)

        # -----------------------------------------------------------------
        # [0:05 - 0:12] The binary code morphs into a cloud of words.
        # -----------------------------------------------------------------
        
        words = ["King", "Queen", "Walks", "Running", "France", 
                 "Paris", "Apple", "Software", "Cat", "Dog", "Piano", "Violin"]
        
        word_mobjects = []
        king_text, queen_text = None, None

        # Create Text objects for each word and store them
        for word_str in words:
            text_obj = Text(word_str, font_size=32)
            if word_str == "King":
                king_text = text_obj
            elif word_str == "Queen":
                queen_text = text_obj
            word_mobjects.append(text_obj)
            
        # Arrange the words in a chaotic, random "cloud"
        word_cloud = VGroup(*word_mobjects).arrange_in_grid(
            rows=3, cols=4, buff=1.5
        )
        
        # Add some randomness to position, scale, and rotation
        for word in word_cloud:
            word.move_to(word.get_center() + np.random.rand(3) * 0.5)
            word.scale(np.random.uniform(0.8, 1.2))
            word.rotate(np.random.uniform(-PI/12, PI/12))
            
        # Animate the transformation from binary to the word cloud
        self.play(Transform(binary_code, word_cloud), run_time=3)
        self.wait(1)

        # -----------------------------------------------------------------
        # [0:12 - 0:20] "King" and "Queen" glow and connect,
        # then the line turns into a question mark.
        # -----------------------------------------------------------------
        
        # Create a dashed line connecting King and Queen
        connection_line = DashedLine(
            king_text.get_center(), 
            queen_text.get_center(), 
            color=BLUE
        )
        
        # Play the glow (Indicate) and line creation animations simultaneously
        self.play(
            AnimationGroup(
                Indicate(king_text, color=YELLOW, scale_factor=1.2),
                Indicate(queen_text, color=YELLOW, scale_factor=1.2),
                Create(connection_line),
                run_time=2
            )
        )
        self.wait(1)
        
        # Create the question mark and the final text
        question_mark = Text("?", font_size=144, color=YELLOW)
        
        # Position the question mark in the center and the text below it
        question_mark.move_to(ORIGIN)
        
        # Fade out the word cloud to focus on the new elements
        self.play(FadeOut(word_cloud))
        
        # Transform the connecting line into the giant question mark
        self.play(Transform(connection_line, question_mark), run_time=1.5)
        
        self.wait(2)
