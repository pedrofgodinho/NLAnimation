from manim import *
import numpy as np

# A consistent, dark background for both scenes
BACKGROUND_COLOR = "#1E1E1E"

class Part1_TheProblem(Scene):
    """
    This scene covers the first 20 seconds of the video plan.
    It transitions from binary code to a word cloud, then highlights
    the relationship between 'King' and 'Queen'.
    """
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR

        # -----------------------------------------------------------------
        # [0:00 - 0:05] Binary code flows rapidly across the screen.
        # -----------------------------------------------------------------
        
        # Generate a block of random binary text
        binary_string = "\n".join(
            ["".join(np.random.choice(["0", "1"], 70)) for _ in range(40)]
        )
        binary_code = Text(binary_string, font="Monospace", font_size=16, fill_opacity=0.4)
        
        self.play(Write(binary_code), run_time=2.5)
        self.wait(1)

        # -----------------------------------------------------------------
        # [0:05 - 0:12] The binary code morphs into a cloud of words.
        # -----------------------------------------------------------------
        
        words = ["King", "Queen", "Walks", "Running", "France", 
                 "Paris", "Apple", "Software", "Cat", "Dog", "Piano", "Violin"]
        
        word_mobjects = VGroup()
        # REFINEMENT: Use a dictionary to easily access key mobjects later
        text_map = {} 

        for word_str in words:
            text_obj = Text(word_str, font_size=32)
            word_mobjects.add(text_obj)
            text_map[word_str] = text_obj
        
        # Arrange the words in a more spread-out, chaotic "cloud"
        word_mobjects.arrange_in_grid(rows=3, cols=4, buff=2.0)
        
        # Add randomness to position, scale, and rotation for a more natural look
        for word in word_mobjects:
            word.shift(np.random.rand(3) * 0.75)
            word.scale(np.random.uniform(0.9, 1.3))
            word.rotate(np.random.uniform(-PI/12, PI/12))
            
        # REFINEMENT: Use ReplacementTransform and LaggedStart for a more dynamic effect.
        # The words will appear one by one as the binary code fades out.
        self.play(
            LaggedStart(
                *[FadeIn(word, shift=UP*0.2) for word in word_mobjects],
                lag_ratio=0.1
            ),
            FadeOut(binary_code, scale=0.8),
            run_time=3
        )
        self.wait(1)

        # -----------------------------------------------------------------
        # [0:12 - 0:20] "King" and "Queen" glow, connect, and pose the question.
        # -----------------------------------------------------------------
        
        king_text = text_map["King"]
        queen_text = text_map["Queen"]
        
        connection_line = DashedLine(
            king_text.get_bottom(), 
            queen_text.get_top(), 
            color=BLUE_C,
            stroke_width=5
        )
        
        # REFINEMENT: Simplified the simultaneous animation by removing AnimationGroup.
        self.play(
            Indicate(king_text, color=YELLOW, scale_factor=1.2),
            Indicate(queen_text, color=YELLOW, scale_factor=1.2),
            Create(connection_line),
            run_time=2
        )
        self.wait(1)
        
        # Create the question mark and the final text
        question_mark = Text("?", font_size=144, color=YELLOW)
        final_text = Text("Meaning = Math?", font_size=48).next_to(question_mark, DOWN, buff=0.5)
        
        # Fade out the word cloud, leaving only the key elements
        other_words = VGroup(*[m for k, m in text_map.items() if k not in ["King", "Queen"]])
        self.play(
            FadeOut(other_words),
            FadeOut(king_text),
            FadeOut(queen_text)
        )
        
        # Transform the connecting line into the giant question mark
        self.play(Transform(connection_line, question_mark), run_time=1.5)
        self.play(Write(final_text))
        
        self.wait(2)
