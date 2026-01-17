MANIM_PROMPT_TEMPLATE_V0 = """
Generate Manim Community v0.19.1 code for the scene {{ scene_number }} of a Fireship-style explainer video about {{ topic }}.

# MANIM SCENE REQUIREMENTS
- Align the timings of transitions, animations, effects, voiceover, text, captions and sound effects with the word-level timing information provided.
- Use the assets provided for the scene.
- Include animated captions for the voiceover.
- Follow the edit notes provided in the plan where appropriate.
- Use the main and secondary fonts provided in the plan where appropriate. Other fonts may be used if they fit the style of the video, and are commonly available.
- Do not add any branding or mention Fireship in any way.
- The scene must be engaging, funny, and in the style of Fireship.

# RULES
- You only have access to the following libaries:
    1. `manim`
    2. `cv2`
    3. `numpy`
- Name the scene class "Scene{{ scene_number }}".
- Output only the raw python code. Do not enclose it in any markdown or code blocks.

# INPUTS PROVIDED
You are provided with the following inputs:
1. Asset files and voiceover file needed for this scene.
2. The full script and word-level timing information for the voiceover of this scene.
3. The full video plan of all scenes in the video.

## SCENE ASSETS
Scene assets are located in the "static/{{ session_id }}" folder with filenames as "{asset_id}.ext", where ".ext" is the appropriate file extension:
1. ".mp4" if the asset is a visual. We have converted image assets to static mp4 video clips that are 1 frame long. Loop them as needed.
2. ".mp3" if the asset is a sound effect.

For example, an asset with asset_id "abc123" that is a visual will be located at "static/{{ session_id }}/abc123.mp4".

The voiceover file of scene {{ scene_number }} is "narration_scene_{{ scene_number }}.mp3", located in "static/{{ session_id }}" (the same folder as the assets).

### USAGE OF VISUAL MP4 ASSETS IN MANIM
- All visual assets are in mp4 format.
- Some visual assets are single-frame mp4 videos (i.e., images converted to mp4 format).
- Loop the mp4 video or cut them to fit the duration of the scene appropriately.
- Resize each video frame as needed to fit the scene. You can use `frame_img.scale_to_fit_height(height)` or `frame_img.scale_to_fit_width(width)` to scale to manim units while maintaining the aspect ratio. The default frame size in manim is 14.22 units wide and 8 units high.
- Assume that all visual assets have roughly square aspect ratios.

To use visual mp4 assets in Manim, please adapt the example below.
```python
cap = cv2.VideoCapture("path to mp4 asset")
flag = True
while flag : # modify condition to fit duration of scene
    flag, frame = cap.read()
    if flag:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_img = ImageMobject(frame)
        self.add(frame_img)
        self.wait(0.04) # for 25 fps video
        self.remove(frame_img)

cap.release()
```

### USAGE OF VOICEOVER AND SOUND EFFECT MP3 ASSETS IN MANIM
Use `self.add_sound("path to mp3 asset")` to add voiceover and sound effects in Manim.

## VOICEOVER SCRIPT AND TIMINGS
- Use the full script and word-level timing information to:
    1. Aligning transitions, animations and effects with timings in the scene.
    2. Adding animated captions for the voiceover, including titles and subtitles as appropriate.
- Words enclosed in square brackets (e.g., `[laughing]`) are audio tags that describe non-verbal sounds or emotional delivery in the voiceover. These audio tags should NOT be included in the captions.

Full script for the voiceover of scene {{ scene_number }} is provided below.

{{ full_script }}


Word-level timing information for the voiceover of scene {{ scene_number }} is provided below.
`word_start_times_seconds` and `word_end_times_seconds` contain the start and end times of each word from the start of this scene (scene {{ scene_number }}), not the whole video.

{{ word_timings }}



## FULL VIDEO PLAN
Use the full video plan of all scenes in the video for context on the overall video style and flow.
Remember to ONLY generate Manim code for scene {{ scene_number }}.

Full plan of the whole video:

{{ full_plan }}

"""


MANIM_PROMPT_TEMPLATE_V1 = """
Generate Manim Community v0.19.1 code for **Scene {{ scene_number }}** of a Fireship-style explainer video about **{{ topic }}**.

### 1. STYLE GUIDELINES (FIRESHIP AESTHETIC)
- **Visuals:** Fast-paced, high-contrast, and professional. Use a dark background (Hex: `#0a0a0a`).
- **Typography:** Use bold, sans-serif fonts. Main titles should be vibrant (e.g., Neon Green `#00ff00` or Cyan `#00e6ff`).
- **Transitions:** Use quick `FadeIn`, `Create`, or "pop-in" scale animations. Avoid long, slow transitions.
- **Humor:** If the script includes a joke, emphasize it with a visual gag or a sudden zoom/shake effect.

### 2. TECHNICAL CONSTRAINTS
- **Libraries:** Only use `manim`, `cv2`, and `numpy`.
- **Class Name:** `Scene{{ scene_number }}`.
- **Output:** Raw Python code only. No markdown, no commentary.

### 3. ASSET HANDLING
- **Visual Assets:** Located at `static/{{ session_id }}/{asset_id}.mp4`.
- **Audio Assets:** Narration is `static/{{ session_id }}/narration_scene_{{ scene_number }}.mp3`. SFX are `static/{{ session_id }}/{asset_id}.mp3`.
- **Video Rendering Logic:** You must use the `cv2` frame-by-frame logic to display the mp4 assets. To prevent code bloat, create a helper method within the class or a concise loop. Ensure the `cv2` loop respects the word-timing durations provided.
    - *Crucial:* Because `cv2` frame rendering is manual, ensure you use `self.add()` and `self.wait(0.04)` inside the logic to keep the scene moving.

### 4. ANIMATED CAPTIONS & TIMING
- Use the provided `word_start_times_seconds` and `word_end_times_seconds`.
- **Captions:** Display the voiceover text at the bottom-center of the screen. Highlight the *current* word being spoken (e.g., change color to yellow) while the rest of the sentence remains white.
- **Sync:** Sound effects (SFX) must be triggered exactly at the `word_start_times_seconds` of the relevant word or as noted in the edit plan.

### 5. INPUT DATA

**VOICEOVER SCRIPT OF SCENE {{ scene_number }}:**
{{ full_script }}

**WORD-LEVEL TIMINGS OF SCENE {{ scene_number }}:**
{{ word_timings }}

**VISUAL ASSETS LIST OF SCENE {{ scene_number }}:**
{{ scene_assets }}

**FULL VIDEO PLAN OF ALL SCENES (CONTEXT ONLY):**
{{ full_plan }}

### 6. EXECUTION INSTRUCTIONS
1. Initialize the scene and add the voiceover audio immediately.
2. Construct the "Fireship" background and layout.
3. Implement the dynamic caption system using the word-level timings.
4. Layer the visual assets (`.mp4`) as specified in the plan, using `cv2` to read and `ImageMobject` to display them.
5. Apply "Shake" or "Wiggle" animations to text or images if the script is high-energy or humorous at that timestamp.

**Generate the code for Scene {{ scene_number }} now.**
"""


MANIM_PROMPT_TEMPLATE = """
# OBJECTIVE
Generate **Manim Community v0.19.1** Python code for **Scene {{ scene_number }}** of a "Fireship-style" explainer video about **{{ topic }}**.

# SCENE {{ scene_number }} STRUCTURE
The scene must follow this exact high-level sequence:

{{ scene_structure }}

# OUTPUT SPECIFICATIONS
- **Class Name:** Define the main class as `Scene{{ scene_number }}`.
- **Format:** Output **only** the raw Python code. Do not use Markdown formatting, backticks, or code blocks.
- **Libraries Allowed:** You have access to `manim`, `cv2`, and `numpy` only.

# STYLE & ANIMATION GUIDELINES
1.  **Fireship Style:** The scene must be fast-paced, engaging, funny, and high-energy.
2.  **No Branding:** Do not mention Fireship or add any branding.
3.  **Visuals:** Use the main and secondary fonts provided in the plan. You may use other common fonts if they fit the style.
4.  **Boundaries:** Ensure all visual elements, including animated captions, images, and text, remain strictly within the frame boundaries. No element should be clipped by the edges of the screen.
5.  **Code Blocks:** If code snippets are required, you must strictly instantiate the `Code` class using the following signature (filling in `code_string` and `language` as needed):
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
6.  **Captions:**
    *   Include animated captions for the voiceover.
    *   Captions must be SEMANTIC PHRASES, not individual words.
    *   Each caption should span the combined duration of its associated words.
    *   DO NOT create one caption per word.
    *   **Filter:** Do not caption audio tags enclosed in square brackets (e.g., `[laughing]`).
    *   **Placement:** Ensure captions do not overlap with other essential visual elements and stay within frame boundaries.
7.  **Synchronization:** Strictly align transitions, animations, effects, text, and sound effects with the provided `word_start_times_seconds` and `word_end_times_seconds`.
8.  **Colors**: Do not use standard Manim color constants (e.g., RED, GREEN). You must strictly define colors as ManimColor objects using integer RGB tuples. Use the exact format: `ManimColor.from_rgb((R, G, B), alpha=1.0)`.

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
*   **Aspect Ratio:** Assume roughly square aspect ratios.
*   **Logic:** If there are visual assets, you **must** adapt the following `cv2` pattern to display these assets, ensuring you loop or cut them to fit the scene duration:

```python
cap = cv2.VideoCapture("path to mp4 asset")

while condition: # modify condition to fit duration of visual in the scene
    flag, frame = cap.read()

    # If video ended (flag is False), reset to start
    if not flag:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        flag, frame = cap.read() # Try reading immediately after reset

    if flag:
        # Process and show frame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_img = ImageMobject(frame).scale_to_fit_height(5)
        self.add(frame_img)

        # Advance time (Renders the frame)
        self.wait(0.04)

        self.remove(frame_img)
    else:
        # Necessary to force time advancement to prevent infinite loop.
        self.wait(0.04)

cap.release()
```

# INPUT DATA

## 1. Full Video Plan
Use this plan for context on flow and edit notes. **Only generate code for Scene {{ scene_number }}.**

{{ full_plan }}

## 2. Voiceover Script (Scene {{ scene_number }})
Use this text for caption content (excluding bracketed tags).

{{ full_script }}

## 3. Timing Data
Use the lists below for precise alignment. Times are in seconds relative to the start of this scene.
*   `word_start_times_seconds`: Start time of each word.
*   `word_end_times_seconds`: End time of each word.

{{ word_timings }}

# TIMING SPECIFICATIONS
- Use the provided `word_start_times_seconds` and `word_end_times_seconds` lists to align animations and captions with the voiceover.
- Times are relative to the start of this scene (scene {{ scene_number }}).
- Animation start times should be within ±0.1s of the narration timing.
- Captions may slightly overlap transitions for readability.
- Visual assets may appear before or after their described timing for better flow.
- Visual coherence takes precedence over exact timing.
"""


MANIM_PROMPT_TEMPLATE = """
# OBJECTIVE
Generate **Manim Community v0.19.1** Python code for **Scene {{ scene_number }}** of a "Fireship-style" explainer video about **{{ topic }}**.

# SCENE {{ scene_number }} STRUCTURE
The scene must follow this exact high-level sequence:

{{ scene_structure }}

# OUTPUT SPECIFICATIONS
- **Class Name:** Define the main class as `Scene{{ scene_number }}`.
- **Format:** Output **only** the raw Python code. Do not use Markdown formatting, backticks, or code blocks.
- **Libraries Allowed:** You have access to `manim`, `cv2`, and `numpy` only.

# STYLE & ANIMATION GUIDELINES
1.  **Fireship Style:** The scene must be fast-paced, engaging, funny, and high-energy.
2.  **No Branding:** Do not mention Fireship or add any branding.
3.  **Visuals:** Use the main and secondary fonts provided in the plan. You may use other common fonts if they fit the style.
4.  **Boundaries:** Ensure all visual elements, including animated captions, images, and text, remain strictly within the frame boundaries. No element should be clipped by the edges of the screen.
5.  **Code Blocks:** If code snippets are required, you must strictly instantiate the `Code` class using the following signature (filling in `code_string` and `language` as needed):
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
6.  **Captions:**
    *   Include animated captions for the voiceover.
    *   Captions must be SEMANTIC PHRASES, not individual words.
    *   Each caption should span the combined duration of its associated words.
    *   DO NOT create one caption per word.
    *   **Filter:** Do not caption audio tags enclosed in square brackets (e.g., `[laughing]`).
    *   **Placement:** Ensure captions do not overlap with other essential visual elements and stay within frame boundaries.
7.  **Synchronization:** Strictly align transitions, animations, effects, text, and sound effects with the provided `word_start_times_seconds` and `word_end_times_seconds`.

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
*   **Aspect Ratio:** Assume roughly square aspect ratios.
*   **Logic:** If there are visual assets, you **must** adapt the following `cv2` pattern to display these assets, ensuring you loop or cut them to fit the scene duration:

```python
cap = cv2.VideoCapture("path to mp4 asset")

while condition: # modify condition to fit duration of visual in the scene
    flag, frame = cap.read()

    # If video ended (flag is False), reset to start
    if not flag:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        flag, frame = cap.read() # Try reading immediately after reset

    if flag:
        # Process and show frame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_img = ImageMobject(frame).scale_to_fit_height(5)
        self.add(frame_img)

        # Advance time (Renders the frame)
        self.wait(0.04)

        self.remove(frame_img)
    else:
        # Necessary to force time advancement to prevent infinite loop.
        self.wait(0.04)

cap.release()
```

# INPUT DATA

## 1. Full Video Plan
Use this plan for context on flow and edit notes. **Only generate code for Scene {{ scene_number }}.**

{{ full_plan }}

## 2. Voiceover Script (Scene {{ scene_number }})
Use this text for caption content (excluding bracketed tags).

{{ full_script }}

## 3. Timing Data
Use the lists below for precise alignment. Times are in seconds relative to the start of this scene.
*   `word_start_times_seconds`: Start time of each word.
*   `word_end_times_seconds`: End time of each word.

{{ word_timings }}

# TIMING SPECIFICATIONS
- Use the provided `word_start_times_seconds` and `word_end_times_seconds` lists to align animations and captions with the voiceover.
- Times are relative to the start of this scene (scene {{ scene_number }}).
- Animation start times should be within ±0.1s of the narration timing.
- Captions may slightly overlap transitions for readability.
- Visual assets may appear before or after their described timing for better flow.
"""
