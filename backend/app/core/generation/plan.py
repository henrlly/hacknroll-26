from app.api.types import PlanStreamedResponse
from app.core.config import app_config
from app.core.models import PipelineCallback, VideoPlan
from app.core.prompts import PLAN_PROMPT_INSTRUCTIONS, PLAN_PROMPT_TEMPLATE
from app.services.openrouter import generate_response
from app.utils.template import render_prompt


async def generate_plan(
    input_plan: VideoPlan | None,
    topic: str,
    callback: PipelineCallback,
    streaming_delay: float = app_config.STREAMING_DELAY,
    mock_plan: bool = app_config.MOCK_PLAN,
    chars_per_stream_message: int = app_config.CHARS_PER_STREAM_MESSAGE,
    plan_prompt_template: str = PLAN_PROMPT_TEMPLATE,
    plan_prompt_instructions: str = PLAN_PROMPT_INSTRUCTIONS,
) -> VideoPlan:
    if input_plan:
        return input_plan

    async def plan_stream_callback(message: str):
        await callback(
            PlanStreamedResponse(event_type="plan_stream", delta=message),
            delay=streaming_delay,
        )

    if mock_plan:
        with open("mock/video_plan.json", "r") as f:
            plan_json = f.read()

        for i in range(0, len(plan_json), chars_per_stream_message):
            chunk = plan_json[i : min(i + chars_per_stream_message, len(plan_json))]
            await plan_stream_callback(chunk)

        return VideoPlan.model_validate_json(plan_json)

    else:
        plan_prompt = render_prompt(plan_prompt_template, topic=topic)
        return await generate_response(
            input=plan_prompt,
            instructions=plan_prompt_instructions,
            model=app_config.PLAN_GEN_MODEL,
            response_model=VideoPlan,
            temperature=app_config.PLAN_GEN_TEMPERATURE,
            reasoning_effort=app_config.PLAN_GEN_REASONING_EFFORT,
            callback=plan_stream_callback,
        )
