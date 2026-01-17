# type: ignore
from manim import *
import cv2
import numpy as np

# Color definitions
DARK_BG = ManimColor.from_rgb((18, 18, 24), alpha=1.0)
NODE_COLOR = ManimColor.from_rgb((100, 200, 255), alpha=1.0)
LINE_COLOR = ManimColor.from_rgb((150, 150, 180), alpha=1.0)
TEXT_WHITE = ManimColor.from_rgb((240, 240, 240), alpha=1.0)
TEXT_YELLOW = ManimColor.from_rgb((255, 220, 100), alpha=1.0)
TEXT_RED = ManimColor.from_rgb((255, 100, 100), alpha=1.0)
TEXT_GREEN = ManimColor.from_rgb((100, 255, 150), alpha=1.0)
CHAOS_COLOR = ManimColor.from_rgb((255, 80, 80), alpha=1.0)
HIGHLIGHT_COLOR = ManimColor.from_rgb((255, 200, 50), alpha=1.0)

class Scene0(Scene):
    def construct(self):
        self.camera.background_color = DARK_BG

        # Add voiceover at t=0
        self.add_sound("static/3391d98b-47cf-4e8a-bdec-2fcf1bb2bc4e/narration_scene_1.mp3")

        # Word timings
        words = ["Think", "of", "it", "like", "a", "family", "tree,", "except", "every", "parent", "practices", "extreme", "family", "planning", "and", "stops", "at", "exactly", "two", "kids.", "No", "exceptions.", "This", "isn't", "the", "Duggar", "family."]
        starts = [0.0, 0.3, 0.45, 0.6, 0.85, 0.95, 1.3, 1.6, 1.95, 2.25, 2.6, 3.1, 3.5, 3.85, 4.3, 4.5, 4.8, 4.95, 5.35, 5.55, 5.85, 6.0, 6.6, 6.85, 7.15, 7.35, 7.7]
        ends = [0.25, 0.4, 0.55, 0.8, 0.9, 1.25, 1.55, 1.9, 2.2, 2.55, 3.05, 3.45, 3.8, 4.25, 4.45, 4.75, 4.9, 5.3, 5.5, 5.8, 5.95, 6.55, 6.8, 7.1, 7.3, 7.65, 8.05]

        # Create chaotic family tree (many children per parent)
        def create_chaotic_tree():
            nodes = VGroup()
            lines = VGroup()

            # Root
            root = Circle(radius=0.25, color=CHAOS_COLOR, fill_opacity=0.8).move_to(UP * 2.5)
            nodes.add(root)

            # Level 1 - 4 children
            l1_positions = [UP * 1.2 + LEFT * 2.5, UP * 1.2 + LEFT * 0.8, UP * 1.2 + RIGHT * 0.8, UP * 1.2 + RIGHT * 2.5]
            for pos in l1_positions:
                node = Circle(radius=0.2, color=CHAOS_COLOR, fill_opacity=0.8).move_to(pos)
                line = Line(root.get_center(), pos, color=LINE_COLOR, stroke_width=2)
                nodes.add(node)
                lines.add(line)

            # Level 2 - many grandchildren
            l2_positions = [
                DOWN * 0.2 + LEFT * 3.2, DOWN * 0.2 + LEFT * 2.5, DOWN * 0.2 + LEFT * 1.8,
                DOWN * 0.2 + LEFT * 0.5, DOWN * 0.2 + RIGHT * 0.2,
                DOWN * 0.2 + RIGHT * 1.5, DOWN * 0.2 + RIGHT * 2.2, DOWN * 0.2 + RIGHT * 2.9
            ]
            parent_indices = [0, 0, 0, 1, 1, 2, 3, 3]
            for i, pos in enumerate(l2_positions):
                node = Circle(radius=0.15, color=CHAOS_COLOR, fill_opacity=0.8).move_to(pos)
                parent_pos = l1_positions[parent_indices[i]]
                line = Line(parent_pos, pos, color=LINE_COLOR, stroke_width=2)
                nodes.add(node)
                lines.add(line)

            return VGroup(lines, nodes)

        # Create clean binary tree (max 2 children)
        def create_binary_tree():
            nodes = VGroup()
            lines = VGroup()

            # Root
            root = Circle(radius=0.3, color=NODE_COLOR, fill_opacity=0.9).move_to(UP * 2.2)
            nodes.add(root)

            # Level 1 - exactly 2 children
            l1_left = Circle(radius=0.25, color=NODE_COLOR, fill_opacity=0.9).move_to(UP * 0.8 + LEFT * 1.5)
            l1_right = Circle(radius=0.25, color=NODE_COLOR, fill_opacity=0.9).move_to(UP * 0.8 + RIGHT * 1.5)
            lines.add(Line(root.get_center(), l1_left.get_center(), color=LINE_COLOR, stroke_width=3))
            lines.add(Line(root.get_center(), l1_right.get_center(), color=LINE_COLOR, stroke_width=3))
            nodes.add(l1_left, l1_right)

            # Level 2 - max 2 children each
            l2_positions = [DOWN * 0.4 + LEFT * 2.3, DOWN * 0.4 + LEFT * 0.7, DOWN * 0.4 + RIGHT * 0.7, DOWN * 0.4 + RIGHT * 2.3]
            parents = [l1_left, l1_left, l1_right, l1_right]
            for i, pos in enumerate(l2_positions):
                node = Circle(radius=0.2, color=NODE_COLOR, fill_opacity=0.9).move_to(pos)
                line = Line(parents[i].get_center(), pos, color=LINE_COLOR, stroke_width=3)
                nodes.add(node)
                lines.add(line)

            return VGroup(lines, nodes)

        # Caption 1: "Think of it like a family tree,"
        caption1 = Text("Think of it like a family tree,", font="JetBrains Mono", font_size=32, color=TEXT_WHITE)
        caption1.to_edge(DOWN, buff=0.5)

        # Show chaotic tree
        chaotic_tree = create_chaotic_tree()
        chaotic_tree.shift(DOWN * 0.3)

        chaos_label = Text("CHAOTIC FAMILY TREE", font="Helvetica", font_size=28, color=CHAOS_COLOR, weight=BOLD)
        chaos_label.to_edge(UP, buff=0.3)

        self.play(FadeIn(caption1), FadeIn(chaotic_tree), FadeIn(chaos_label), run_time=0.5)
        self.wait(max(0.01, 1.55 - 0.5))  # Until "tree," ends

        # Caption 2: "except every parent practices"
        self.play(FadeOut(caption1), run_time=0.15)
        caption2 = Text("except every parent practices", font="JetBrains Mono", font_size=32, color=TEXT_YELLOW)
        caption2.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(caption2), run_time=0.15)
        self.wait(max(0.01, 3.05 - 1.6 - 0.3))

        # Transition to binary tree
        binary_tree = create_binary_tree()
        binary_tree.shift(DOWN * 0.3)

        binary_label = Text("BINARY TREE (MAX 2 KIDS)", font="Helvetica", font_size=28, color=TEXT_GREEN, weight=BOLD)
        binary_label.to_edge(UP, buff=0.3)

        # Caption 3: "extreme family planning"
        self.play(FadeOut(caption2), run_time=0.15)
        caption3 = Text("extreme family planning", font="JetBrains Mono", font_size=36, color=TEXT_RED, weight=BOLD)
        caption3.to_edge(DOWN, buff=0.5)

        self.play(
            ReplacementTransform(chaotic_tree, binary_tree),
            ReplacementTransform(chaos_label, binary_label),
            FadeIn(caption3),
            run_time=0.6
        )
        self.wait(max(0.01, 4.25 - 3.1 - 0.6))

        # Caption 4: "and stops at exactly two kids."
        self.play(FadeOut(caption3), run_time=0.15)
        caption4 = Text("and stops at exactly TWO kids.", font="JetBrains Mono", font_size=34, color=TEXT_WHITE)
        caption4[22:25].set_color(TEXT_YELLOW)  # Highlight "TWO"
        caption4.to_edge(DOWN, buff=0.5)

        # Add "2" emphasis on tree
        two_text = Text("2", font="JetBrains Mono", font_size=72, color=HIGHLIGHT_COLOR, weight=BOLD)
        two_text.move_to(RIGHT * 4 + UP * 1)

        self.play(FadeIn(caption4), FadeIn(two_text, scale=1.5), run_time=0.4)
        self.wait(max(0.01, 5.8 - 4.3 - 0.55))

        # Caption 5: "No exceptions."
        self.play(FadeOut(caption4), FadeOut(two_text), run_time=0.15)
        caption5 = Text("No exceptions.", font="JetBrains Mono", font_size=42, color=TEXT_RED, weight=BOLD)
        caption5.to_edge(DOWN, buff=0.5)

        self.play(FadeIn(caption5, scale=1.2), run_time=0.3)

        # Fade out tree for meme
        self.play(FadeOut(binary_tree), FadeOut(binary_label), run_time=0.3)
        self.wait(max(0.01, 6.55 - 5.85 - 0.6))

        # Show Anakin Padme meme
        self.play(FadeOut(caption5), run_time=0.15)

        # Caption 6: "This isn't the Duggar family."
        caption6 = Text("This isn't the Duggar family.", font="JetBrains Mono", font_size=34, color=TEXT_WHITE)
        caption6.to_edge(DOWN, buff=0.3)

        # Display meme using cv2
        cap = cv2.VideoCapture("static/3391d98b-47cf-4e8a-bdec-2fcf1bb2bc4e/anakin_padme_meme.mp4")
        visual_asset_duration = 1.5
        frame_time = 0.04
        elapsed = 0

        current_frame = None
        meme_text_top = Text("I can have unlimited children!", font="Helvetica", font_size=20, color=TEXT_WHITE)
        meme_text_bottom = Text("Right... only 2?", font="Helvetica", font_size=20, color=TEXT_YELLOW)

        first_frame = True
        while elapsed < visual_asset_duration:
            flag, frame = cap.read()

            if not flag:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                flag, frame = cap.read()

            if flag:
                if current_frame is not None:
                    self.remove(current_frame)

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_img = ImageMobject(frame).scale_to_fit_height(5)
                frame_img.move_to(UP * 0.8)
                current_frame = frame_img
                self.add(frame_img)

                if first_frame:
                    meme_text_top.next_to(frame_img, UP, buff=0.2)
                    meme_text_bottom.next_to(frame_img, DOWN, buff=0.2)
                    self.add(meme_text_top, meme_text_bottom, caption6)
                    first_frame = False

                self.wait(frame_time)
                elapsed += frame_time
            else:
                self.wait(frame_time)
                elapsed += frame_time

        cap.release()

        # Highlight effect on max 2 children rule
        if current_frame is not None:
            self.remove(current_frame)
        self.remove(meme_text_top, meme_text_bottom)

        # Final emphasis
        final_text = Text("MAX 2 CHILDREN", font="JetBrains Mono", font_size=56, color=HIGHLIGHT_COLOR, weight=BOLD)
        final_text.move_to(UP * 0.5)

        highlight_box = SurroundingRectangle(final_text, color=HIGHLIGHT_COLOR, buff=0.3, stroke_width=4)

        self.play(
            FadeIn(final_text, scale=0.5),
            Create(highlight_box),
            run_time=0.4
        )

        # Flash effect
        self.play(
            final_text.animate.set_color(TEXT_WHITE),
            highlight_box.animate.set_color(TEXT_RED),
            run_time=0.2
        )
        self.play(
            final_text.animate.set_color(HIGHLIGHT_COLOR),
            highlight_box.animate.set_color(HIGHLIGHT_COLOR),
            run_time=0.2
        )

        self.wait(max(0.01, 8.05 - 7.7 - 0.4))

        # Fade out
        self.play(FadeOut(final_text), FadeOut(highlight_box), FadeOut(caption6), run_time=0.3)
