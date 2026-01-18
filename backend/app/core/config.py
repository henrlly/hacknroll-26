from openai.types.shared.reasoning_effort import ReasoningEffort
from pydantic_settings import BaseSettings, SettingsConfigDict


# Override by setting environment variables or directly modifying here for dev/testing
# e.g. to change MOCK_PLAN, export APP_MOCK_PLAN=False
class Config(BaseSettings):
    MOCK_PLAN: bool = False
    MOCK_VISUAL_ASSET: bool = False
    MOCK_SFX: bool = False
    MOCK_NARRATION: bool = False
    MOCK_CODE_GEN: bool = False
    MOCK_CODE_FIX: bool = False
    MOCK_CODE_RENDER: bool = False  # rendering 4 scenes in parallel takes 5s
    MOCK_EDIT_SCENE: bool = False  # rendering 4 scenes in parallel takes 5s
    USE_LOCAL_TTS: bool = False
    # if we mock everything it takes 7s on my computer

    CALLBACK_DELAY: float = 0.1  # seconds
    STREAMING_DELAY: float = 0  # seconds
    CHARS_PER_STREAM_MESSAGE: int = 200

    # Visual generation
    ENABLE_IMAGE_GENERATION: bool = False
    ENABLE_IMAGE_SELECTION: bool = False

    # Number of candidates to fetch from database per asset
    NUM_STOCK_IMAGES: int = 2  # dont set this below 1, will error
    NUM_STOCK_CLIPS: int = 2  # dont set this below 1, will error
    NUM_MEME_CLIPS: int = 2  # dont set this below 1, will error

    NUM_CODE_VERSIONS_PER_SCENE: int = 2  # the most important setting!
    MANIM_SCENE_MAX_RETRIES: int = 5
    MANIM_RENDER_TIMEOUT_SECONDS: int = 300  # 5 minutes

    AUDIO_TRANSCRIPTION_KEEP_TAGS: bool = False

    RETRY_ON_NONE_RESPONSE: bool = True  # retry if LLM structured output is None

    # By default:
    # Anthropic has 1024 reasoning token budget
    # Gemini has "high" reasoning effort
    # GPT-5 has "none" reasoning effort
    #
    # Reasoning token budget:
    # budget_tokens = max(min(max_tokens * {effort_ratio}, 128000), 1024)

    # model="moonshotai/kimi-k2-thinking",
    # model="x-ai/grok-4.1-fast:online",
    # model="x-ai/grok-4:online",
    # model="google/gemini-3-flash-preview",
    # model="anthropic/claude-opus-4.5",

    CODE_FIX_MODEL: str = "anthropic/claude-opus-4.5"
    CODE_FIX_REASONING_EFFORT: ReasoningEffort | None = None
    CODE_FIX_TEMPERATURE: float = 0

    CODE_GEN_MODEL: str = "anthropic/claude-opus-4.5"
    CODE_GEN_REASONING_EFFORT: ReasoningEffort | None = None
    CODE_GEN_TEMPERATURE: float = 0.1

    # LOW PRIORITY TODO: Try diff models and temperatures for plan generation
    # Plan has to be streamed
    PLAN_GEN_MODEL: str = "anthropic/claude-sonnet-4.5"
    PLAN_GEN_REASONING_EFFORT: ReasoningEffort | None = None
    PLAN_GEN_TEMPERATURE: float = 0.7

    model_config = SettingsConfigDict(
        env_prefix="APP_",
        case_sensitive=False,
    )


app_config = Config()


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    ELEVENLABS_API_KEY: str
    KLIPY_API_KEY: str
    PEXELS_API_KEY: str
    OPENROUTER_API_KEY: str
    PIXABAY_API_KEY: str
    FISH_API_KEY: str

    # Load from .env file
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()  # pyright: ignore
