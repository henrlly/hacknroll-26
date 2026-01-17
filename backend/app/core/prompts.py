SCENE_EDIT_PROMPT_INSTRUCTIONS = """
You are an expert video content creator specializing in creating engaging Fireship-style explainer videos.
"""

SCENE_EDIT_PROMPT_TEMPLATE = """
Here is a detailed plan for a 20-second Fireship-style explainer video about the following topic:
{{ topic }}

{{ plan }}

Edit and output scene {{ scene_number }} to based on the following edit prompt:
{{ edit_prompt }}

# GENERAL RULES
- There **must** be a total of 4 scenes, each 5 seconds long, for a total video duration of 20 seconds.
- Each scene **must** represent one cut.
- Narration should be punchy and opinionated, similar to Fireship videos.
- The video **must** be funny and reference popular internet culture or memes where appropriate.
- Select a main and secondary font to use for the entire video, for cohesiveness of the video. (This will be used during editing.) The fonts should be commonly available.
- DO NOT add any branding or mention Fireship in any way.
- DO NOT add any generic call to action (e.g., "like and subscribe", "follow for more").
- When executing the plan, we will have access to the manim animation tool.

# For each scene, provide the following details
1. Scene number (0-indexed)
2. Rough duration of the scene (in seconds)
3. Description of scene visuals
4. Narration/script for the scene
5. Description of any sound effects or background music
6. Edit notes (e.g., transitions, effects)
7. List of assets needed (Visual or Sound effect)
8. Scene structure (high-level sequence of events in the scene)

# RULES FOR SCENE STRUCTURE
- Scene structure should be a numbered list of the sequence of events in the scene.
- Only specify exact timings for when to start the scene voiceover. Each scene has a separate voiceover audio file.
- DO NOT specify exact timings for anything else in the scene structure.
Example scene structure:
```
1. Dark background initialization
2. Start scene voiceover immediately at t=0
3. Animate title text "LINKED LISTS" at the top
4. Sequentially introduce 4 linked list nodes from left to right:
    - Each node appears with a pop sound
    - Each node connects to the previous node via an arrow
5. Emphasize "TREASURE HUNT" with larger text and glow
6. End with a highlight traversal from first node to last
```

# RULES FOR VISUAL ASSETS
- When executing the plan, we will use the manim tool to generate visuals besides just using assets.
- Manim can generate animated graphs, text, shapes, and vector graphics.
- DO NOT list assets that will be generated using manim.
- DO NOT list manim as an asset.
- DO list visual assets that cannot be generated using manim, such as:
    - Meme or funny images or clips (e.g., surprised pikachu meme, distracted boyfriend meme, pepelaugh)
    - Stock images or clips (e.g., a person typing on a laptop, city skyline timelapse)
- Be liberal in listing visual assets that will enhance the video.
- Visual assets should appear on screen for at least 1 second to allow viewers to absorb them.

# RULES FOR ASSETS
- Asset descriptions should specify EXACTLY what the asset is.
    - GOOD description: "A dog eating a hot dog alone"
    - BAD description: "A dog eating something that seems tasty". This is too vague.
- Each asset description should only describe a SINGLE SPECIFIC asset. DO NOT give options.
    - GOOD description: "surprised pikachu meme". This describes a single specific asset.
    - BAD description: "loss meme or struggling person image". This has multiple options.
- DO NOT give examples in the asset descriptions.
    - BAD description: "A meme expressing frustation (e.g., person facepalming, character looking defeated)". This is an example, not a description.
- Each asset should include BOTH a short and a long description.
- Short description:
    - Short descriptions will be used to look up assets from the asset database.
    - Short description should be EXTREMELY short and generic and use less than 6 words. The asset database is limited and cannot handle very specific descriptions.
    - DO NOT include words like "image", "clip", "visual", "stock footage", or "sound effect" in the short description.
    - Examples of Short description (non-exhaustive): "Surprised pikachu meme", "Explosion sound effect"
- Long description:
    - Long description will be used as the prompt for the AI to generate the assets.
    - Long description should be more DETAILED and SPECIFIC than the short description.
    - Examples of Long description (non-exhaustive): "A dog eating a hot dog alone", "Loud explosion sound effect with deep bass"
- We will compare the assets generated (with long description) with the assets in the asset database (with short description) and select the best asset that matches both descriptions.

# RULES FOR NARRATION/SCRIPT
- Narration/script should be written in a conversational tone, as if explaining to a friend.
- Enhance the narration with humor, analogies, and relatable examples where appropriate to keep the audience engaged.
- Enhance the narration with internet culture references and memes where appropriate.
"""

PLAN_PROMPT_INSTRUCTIONS = """
You are an expert video content creator specializing in creating engaging Fireship-style explainer videos.
"""

# TODO: Add examples for ehancements to narration/script
# maybe not need cos it works p well alr
#
# ## 6. Examples of Enhancement <-- this is for dialogue, what about narration/script?
# **Input**:
# "Are you serious? I can't believe you did that!"
# **Enhanced Output**:
# "[appalled] Are you serious? [sighs] I can't believe you did that!"
# ---
# **Input**:
# "That's amazing, I didn't know you could sing!"
# **Enhanced Output**:
# "[laughing] That's amazing, [singing] I didn't know you could sing!"
# ---
# **Input**:
# "I guess you're right. It's just... difficult."
# **Enhanced Output**:
# "I guess you're right. [sighs] It's just... [muttering] difficult."
#
PLAN_PROMPT_TEMPLATE = """
Create a detailed plan for a 20-second Fireship-style explainer video about the following topic:
{{ topic }}

# GENERAL RULES
- There **must** be a total of 4 scenes, each 5 seconds long, for a total video duration of 20 seconds.
- Each scene **must** represent one cut.
- Narration should be punchy and opinionated, similar to Fireship videos.
- The video **must** be funny and reference popular internet culture or memes where appropriate.
- Select a main and secondary font to use for the entire video, for cohesiveness of the video. (This will be used during editing.) The fonts should be commonly available.
- DO NOT add any branding or mention Fireship in any way.
- DO NOT add any generic call to action (e.g., "like and subscribe", "follow for more").
- When executing the plan, we will have access to the manim animation tool.

# For each scene, provide the following details
1. Scene number (0-indexed)
2. Rough duration of the scene (in seconds)
3. Description of scene visuals
4. Narration/script for the scene
5. Description of any sound effects or background music
6. Edit notes (e.g., transitions, effects)
7. List of assets needed (Visual or Sound effect)
8. Scene structure (high-level sequence of events in the scene)

# RULES FOR SCENE STRUCTURE
- Scene structure should be a numbered list of the sequence of events in the scene.
- Only specify exact timings for when to start the scene voiceover. Each scene has a separate voiceover audio file.
- DO NOT specify exact timings for anything else in the scene structure.
Example scene structure:
```
1. Dark background initialization
2. Start scene voiceover immediately at t=0
3. Animate title text "LINKED LISTS" at the top
4. Sequentially introduce 4 linked list nodes from left to right:
    - Each node appears with a pop sound
    - Each node connects to the previous node via an arrow
5. Emphasize "TREASURE HUNT" with larger text and glow
6. End with a highlight traversal from first node to last
```

# RULES FOR VISUAL ASSETS
- When executing the plan, we will use the manim tool to generate visuals besides just using assets.
- Manim can generate animated graphs, text, shapes, and vector graphics.
- DO NOT list assets that will be generated using manim.
- DO NOT list manim as an asset.
- DO list visual assets that cannot be generated using manim, such as:
    - Meme or funny images or clips (e.g., surprised pikachu meme, distracted boyfriend meme, pepelaugh)
    - Stock images or clips (e.g., a person typing on a laptop, city skyline timelapse)
- Be liberal in listing visual assets that will enhance the video.
- Visual assets should appear on screen for at least 1 second to allow viewers to absorb them.

# RULES FOR ASSETS
- Asset descriptions should specify EXACTLY what the asset is.
    - GOOD description: "A dog eating a hot dog alone"
    - BAD description: "A dog eating something that seems tasty". This is too vague.
- Each asset description should only describe a SINGLE SPECIFIC asset. DO NOT give options.
    - GOOD description: "surprised pikachu meme". This describes a single specific asset.
    - BAD description: "loss meme or struggling person image". This has multiple options.
- DO NOT give examples in the asset descriptions.
    - BAD description: "A meme expressing frustation (e.g., person facepalming, character looking defeated)". This is an example, not a description.
- Each asset should include BOTH a short and a long description.
- Short description:
    - Short descriptions will be used to look up assets from the asset database.
    - Short description should be EXTREMELY short and generic and use less than 6 words. The asset database is limited and cannot handle very specific descriptions.
    - DO NOT include words like "image", "clip", "visual", "stock footage", or "sound effect" in the short description.
    - Examples of Short description (non-exhaustive): "Surprised pikachu meme", "Explosion sound effect"
- Long description:
    - Long description will be used as the prompt for the AI to generate the assets.
    - Long description should be more DETAILED and SPECIFIC than the short description.
    - Examples of Long description (non-exhaustive): "A dog eating a hot dog alone", "Loud explosion sound effect with deep bass"
- We will compare the assets generated (with long description) with the assets in the asset database (with short description) and select the best asset that matches both descriptions.

# RULES FOR NARRATION/SCRIPT
- Narration/script should be written in a conversational tone, as if explaining to a friend.
- Enhance the narration with humor, analogies, and relatable examples where appropriate to keep the audience engaged.
- Enhance the narration with internet culture references and memes where appropriate.
"""


MANIM_FIX_PROMPT_INSTRUCTIONS = """
You are an expert Python developer specializing in creating animations with the Manim Community v0.19.1 library.
Your task is to debug and fix a specific Manim animation script so that it runs without errors.
"""

MANIM_FIX_PROMPT_TEMPLATE = """
### CONTEXT & ENVIRONMENT
- **Goal:** Make the provided code run without errors.
- **Style:** The code produces a "Fireship-style" explainer video (fast-paced, high energy).
- **Available Libraries:** You have access **only** to `manim`, `cv2` (opencv), and `numpy`. Standard Python libraries are available, but no other third-party dependencies.

### INPUT DATA
Below is the data required for the fix:

<broken_code>
{{ code }}
</broken_code>

<error_log>
{{ error_messages }}
</error_log>

<original_intent>
{{ original_prompt }}
</original_intent>

### STRICT RULES
1.  **Minimal Intervention:** Fix only the syntax, API usage, or logic errors causing the crash. Do not refactor the code style or structure unless necessary for execution.
2.  **Preserve Timing:** Do not change the duration of animations, `wait()` calls, or media. The synchronization between voiceovers, sound effects, and visuals **must** remain exactly as originally scripted.
3.  **Preserve Logic:** Do not alter the educational content or the visual outcome intended by the `<original_intent>`.
4.  **Code Block Signature**: If code is displayed, strictly follow the signature `class Code(code_file=None, code_string=None, language=None, formatter_style='vim', tab_width=4, add_line_numbers=True, line_numbers_from=1, background='rectangle', background_config=None, paragraph_config=None)` strictly.
4.  **Output Format:** Output **ONLY** the raw Python code. Do not use Markdown backticks (```python), do not add explanations, and do not add conversational text.
"""

MANIM_PROMPT_INSTRUCTIONS = """
You are an expert in creating engaging "Fireship-style" explainer videos using the Manim Community v0.19.1 library.
Your task is to generate Manim code for a specific scene of the video, following the detailed requirements and inputs provided.
"""

# Seperating subtitle and voiceover logic gave worse results - need to ask LLM for delay before starting captions and voiceover
# Inserting video - https://github.com/3b1b/manim/issues/760#issuecomment-925659697
#
# PROBLEMS WITH MANIM PROMPT:
# Sometimes only a part of a single word is highlighted in captions.
# E.g. see mock scene output - "ki*ds*"
# Tokenization issue? Just tell it to highlight full words
# and not (never? unless there is a good reason)
# only partial words/certain characters in a word
#
# compare width and height
# if we want to fit the unit in a 5 unit square
# if frame_img.width < frame_img.height:
#     frame_img = frame_img.scale_to_fit_height(5)
# else:
#     frame_img = frame_img.scale_to_fit_width(5)
# does this really work??
#
MANIM_PROMPT_TEMPLATE = """
# OBJECTIVE
Generate **Manim Community v0.19.1** Python code for **Scene {{ scene_number }}** of a "Fireship-style" explainer video about **{{ topic }}**.

# SCENE {{ scene_number }} STRUCTURE
The scene **must** follow this exact high-level sequence:

{{ scene_structure }}

# OUTPUT SPECIFICATIONS
- **Class Name:** Define the main class as `Scene{{ scene_number }}`.
- **Format:** Output **only** the raw Python code. Do not use Markdown formatting, backticks, or code blocks.
- **Libraries Allowed:** You have access to `manim`, `cv2`, and `numpy` only.

# STYLE & ANIMATION GUIDELINES
1.  **Fireship Style:** The scene **must** be fast-paced, engaging, funny, and high-energy.
2.  **No Branding:** Do not mention Fireship or add any branding.
3.  **No Call to Action:** Do not include generic calls to action (e.g., "like and subscribe", "follow for more").
3.  **Visuals:** Use the main and secondary fonts provided in the plan. You may use other common fonts if they fit the style.
4.  **Boundaries:** Ensure all visual elements, including animated captions, images, and text, remain strictly within the frame boundaries. No element should be clipped by the edges of the screen.
5.  **Colors**: Do not use standard Manim color constants (e.g., RED, GREEN). You **must** strictly define color constants with this exact format: `NEW_COLOR = ManimColor.from_rgb((R, G, B), alpha=1.0)`. DO NOT define colors in any other way.
6.  **Captions:**
    *   Include animated captions for the voiceover.
    *   Captions **must** be semantic phrases, not individual words. DO NOT create one caption per word.
    *   Each caption **must** span the combined duration of its associated words.
    *   Captions **must** appear and disappear within 0.2s of the voiceover timing
    *   **Style:** Captions **must** have different styles (e.g., color, size, font weight) to emphasize key points, humor, or punchlines in the narration.
    *   **Placement:** Ensure captions do not overlap with other essential visual elements and stay within frame boundaries.
7.  **Synchronization:** Strictly align transitions, animations, effects, text, and sound effects with the provided `word_start_times_seconds` and `word_end_times_seconds`. External visual assets **must** appear on screen for at least 1 second.

# ASSET HANDLING SPECIFICATIONS

## 1. File Paths
Assets are located in `static/{{ session_id }}/`.
*   **Visuals:** `{asset_id}.mp4` (includes static images converted to single-frame mp4s).
*   **Audio (SFX):** `{asset_id}.mp3`.
*   **Voiceover:** `narration_scene_{{ scene_number }}.mp3` (located in the same folder).

The assets for this scene are as follows:
{{ scene_assets }}

## 2. Audio Implementation
Use `self.add_sound("path/to/file.mp3")` for both the voiceover and sound effects.

## 3. Visual Implementation (Custom CV2 Logic)
All visual assets are `.mp4` files. Some are single-frame loops (images), others are video clips.
*   **Scaling:** Resize frames to fit the scene using `frame_img.scale_to_fit_height()` or `.scale_to_fit_width()`. (Manim default: 14.22w x 8h).
*   **Aspect Ratio:** Compare `frame_img.width` with `frame_img.height` to decide whether to scale to fit height or width.
*   **Minimum Duration**: Any external .mp4 asset **must** remain visible for a MINIMUM of 1 second. Do not cut them shorter than this, even if the voiceover is fast.
*   **Logic:** If there are visual assets, you **must** adapt the following `cv2` pattern to display these assets, ensuring you loop or cut them to fit the scene duration:

```python
cap = cv2.VideoCapture("path to mp4 asset")
visual_asset_duration = 1.0 # minimum duration for the visual asset in seconds (**must** be at least 1 second)
frame_time = 0.04
elapsed = 0

current_frame = None
while elapsed < visual_asset_duration:
    flag, frame = cap.read()

    if not flag:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        flag, frame = cap.read()

    if flag:
        if current_frame is not None:
            self.remove(current_frame)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_img = ImageMobject(frame)
        # compare width and height
        # if we want to fit the unit in a 5 unit square
        if frame_img.width < frame_img.height:
            frame_img = frame_img.scale_to_fit_height(5)
        else:
            frame_img = frame_img.scale_to_fit_width(5)
        frame_img.move_to(UP * 0.5)
        current_frame = frame_img
        self.add(frame_img)
        self.wait(frame_time)
        elapsed += frame_time
    else:
        self.wait(frame_time)
        elapsed += frame_time

cap.release()
```

# TECHNICAL CONSTRAINTS
You **must** strictly adhere to these rules to prevent runtime errors:
1.  **Group vs. VGroup:** `ImageMobject` is **NOT** a `VMobject`.
    *   **Never** add an `ImageMobject` to a `VGroup`.
    *   If you need to group images (or mix images with vectors/text), you **must** use `Group()` instead of `VGroup()`.
2.  **Numpy Types in Text:** If numpy strings used, you **must** explicitly cast them to a Python string before passing to Manim objects.
3.  **Code Blocks:** If code snippets are required, you **must** strictly instantiate the `Code` class using the following signature (filling in `code_string` and `language` as needed):
    ```python
    Code(
        code_string="...",
        language="...",
        formatter_style='vim',
        tab_width=4,
        add_line_numbers=True,
        line_numbers_from=1,
        background='rectangle',
        background_config=None,
        paragraph_config=None
    )
    ```
4.  **Minimum Wait Time:** You **must** ensure that the wait duration in `self.wait(duration)` is positive, by enforcing a minimum wait time of 0.01s for any calls with `self.wait(max(0.01, duration))`.


# INPUT DATA

## 1. Full Video Plan
Use this plan for context on flow and edit notes. **Only generate code for Scene {{ scene_number }}.**

{{ full_plan }}

## 2. Voiceover Script (Scene {{ scene_number }})
Use this text for caption content.

{{ full_script }}

## 3. Timing Data
Use the lists below for precise alignment. Times are in seconds relative to the start of this scene.
*   `word_start_times_seconds`: Start time of each word.
*   `word_end_times_seconds`: End time of each word.

{{ word_timings }}

# TIMING SPECIFICATIONS
*   **Source of Truth:** Use the provided `word_start_times_seconds` and `word_end_times_seconds` lists to align animations and captions with the voiceover.
*   **Timings:** Times are relative to the start of this scene (scene {{ scene_number }}).
*   **Precision:** Animation start times should be within ±0.1s of the narration timing.
*   **Captions:** Captions may slightly overlap transitions for readability, but they should appear and disappear within ±0.2s of the voiceover timing.
*   **Visuals:** All imported visual assets **must** appear on screen for at least 1 second to allow viewers to absorb them.
*   **Native Manim Elements:**  Other Manim objects (shapes, text, code blocks, flashes) are NOT subject to the 1-second rule. These should be fast, transient, and match the high-energy "Fireship" pacing (e.g., appearing for only 0.8s is acceptable).
"""
