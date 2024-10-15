from enum import Enum
import json
import time
from typing import (
    Any,
    Dict,
    Iterable,
    List,
    Literal,
    Optional,
    Union,
)

from anthropic import Anthropic, AsyncAnthropic
from anthropic.types import Message
from anthropic.types.message_create_params import (
    Metadata,
    ToolChoice,
    ToolChoiceToolChoiceAny,
    ToolChoiceToolChoiceAuto,
    ToolChoiceToolChoiceTool,
)
from anthropic.types.message_param import MessageParam
from anthropic.types.text_block_param import TextBlockParam
from anthropic.types.tool_param import ToolParam
from openai.types import CompletionUsage
from openai.types.chat import ChatCompletionMessage
from openai.types.chat.chat_completion import Choice
from openai.types.chat.chat_completion_message_tool_call import (
    ChatCompletionMessageToolCall,
    Function,
)
from pydantic import BaseModel

from adapters.abstract_adapters.api_key_adapter_mixin import ApiKeyAdapterMixin
from adapters.abstract_adapters.provider_adapter_mixin import ProviderAdapterMixin
from adapters.abstract_adapters.sdk_chat_adapter import SDKChatAdapter
from adapters.types import (
    AdapterChatCompletion,
    Conversation,
    ConversationRole,
    Cost,
    FinishReason,
    Model,
    ModelProperties,
)
from adapters.utils.general_utils import delete_none_values, process_image_url_anthropic

PROVIDER_NAME = "anthropic"
BASE_URL = "https://api.anthropic.com"
API_KEY_NAME = "ANTHROPIC_API_KEY"
BASE_PROPERTIES = ModelProperties(gdpr_compliant=True)


class AnthropicModel(Model):
    vendor_name: str = PROVIDER_NAME
    provider_name: str = PROVIDER_NAME
    properties: ModelProperties = BASE_PROPERTIES

    supports_tool_choice_required: bool = True
    supports_last_assistant: bool = True
    supports_streaming: bool = True
    supports_json_content: bool = False
    supports_tools: bool = True
    supports_vision: bool = True


SUPPORTED_MODELS = [
    AnthropicModel(
        name="claude-3-sonnet-20240229",
        cost=Cost(prompt=3.0e-6, completion=15.0e-6),
        context_length=200000,
        completion_length=4096,
    ),
    AnthropicModel(
        name="claude-3-opus-20240229",
        cost=Cost(prompt=15.0e-6, completion=75.0e-6),
        context_length=200000,
        completion_length=4096,
    ),
    AnthropicModel(
        name="claude-3-haiku-20240307",
        cost=Cost(prompt=0.25e-6, completion=1.25e-6),
        context_length=200000,
        completion_length=4096,
    ),
    AnthropicModel(
        name="claude-3-5-sonnet-20240620",
        cost=Cost(prompt=3.0e-6, completion=15.0e-6),
        context_length=200000,
        completion_length=4096,
    ),
]


class AnthropicFinishReason(str, Enum):
    end_turn = "end_turn"
    max_tokens = "max_tokens"
    stop_sequence = "stop_sequence"
    tool_use = "tool_use"


FINISH_REASON_MAPPING: Dict[AnthropicFinishReason, FinishReason] = {
    AnthropicFinishReason.end_turn: "stop",
    AnthropicFinishReason.max_tokens: "length",
    AnthropicFinishReason.stop_sequence: "stop",
    AnthropicFinishReason.tool_use: "tool_calls",
}


class AnthropicCreate(BaseModel):
    max_tokens: int
    messages: Iterable[MessageParam]
    metadata: Optional[Metadata] = None
    stop_sequences: Optional[List[str]] = None
    stream: Optional[Literal[False] | Literal[True]] = None
    system: Optional[Union[str, Iterable[TextBlockParam]]] = None
    temperature: Optional[float] = None
    tool_choice: Optional[ToolChoice] = None
    tools: Optional[Iterable[ToolParam]] = None
    top_k: Optional[int] = None
    top_p: Optional[float] = None


class AnthropicSDKChatProviderAdapter(
    ProviderAdapterMixin,
    ApiKeyAdapterMixin,
    SDKChatAdapter,
):
    @staticmethod
    def get_supported_models():
        return SUPPORTED_MODELS

    @staticmethod
    def get_provider_name() -> str:
        return PROVIDER_NAME

    def get_base_sdk_url(self) -> str:
        return BASE_URL

    @staticmethod
    def get_api_key_name() -> str:
        return API_KEY_NAME

    _sync_client: Anthropic
    _async_client: AsyncAnthropic

    def __init__(
        self,
    ):
        super().__init__()
        self._sync_client = Anthropic(
            api_key=self.get_api_key(),
        )
        self._async_client = AsyncAnthropic(
            api_key=self.get_api_key(),
        )

    def get_sync_client(self):
        return self._sync_client.messages.create

    def get_async_client(self):
        return self._async_client.messages.create

    def adjust_temperature(self, temperature: float) -> float:
        return temperature / 2

    def set_api_key(self, api_key: str) -> None:
        super().set_api_key(api_key)

        self._sync_client.api_key = api_key
        self._async_client.api_key = api_key

    def extract_response(
        self, request: Conversation, response: Message
    ) -> AdapterChatCompletion:
        finish_reason = FINISH_REASON_MAPPING.get(
            AnthropicFinishReason(response.stop_reason), "stop"
        )

        choices: list[Choice] = []
        for content in response.content:
            if content.type == "text":
                choices.append(
                    Choice(
                        index=len(choices),
                        finish_reason=finish_reason,
                        message=ChatCompletionMessage(
                            role=ConversationRole.assistant.value,
                            content=content.text,
                        ),
                    )
                )
            elif content.type == "tool_use":
                choices.append(
                    Choice(
                        index=len(choices),
                        finish_reason=finish_reason,
                        message=ChatCompletionMessage(
                            role=ConversationRole.assistant.value,
                            tool_calls=[
                                ChatCompletionMessageToolCall(
                                    id=content.id,
                                    type="function",
                                    function=Function(
                                        name=content.name,
                                        arguments=json.dumps(content.input),
                                    ),
                                )
                            ],
                        ),
                    )
                )

        usage = CompletionUsage(
            prompt_tokens=response.usage.input_tokens,
            completion_tokens=response.usage.output_tokens,
            total_tokens=response.usage.input_tokens + response.usage.output_tokens,
        )

        cost = (
            self.get_model().cost.prompt * usage.prompt_tokens
            + self.get_model().cost.completion * usage.completion_tokens
            + self.get_model().cost.request
        )

        return AdapterChatCompletion(
            id=response.id,
            created=int(time.time()),
            model=self.get_model().name,
            object="chat.completion",
            cost=cost,
            usage=usage,
            choices=choices,
        )

    # TODO: match openai format 1:1
    def extract_stream_response(self, request, response):
        content = getattr(getattr(response, "delta", None), "text", "")

        if getattr(response, "type", None) == "message_stop":
            content = None

        chunk = json.dumps(
            {
                "choices": [
                    {
                        "delta": {
                            "role": ConversationRole.assistant.value,
                            "content": content,
                        },
                    }
                ]
            }
        )

        return f"data: {chunk}\n\n"

    # pylint: disable=too-many-locals
    def get_params(self, llm_input: Conversation, **kwargs) -> Dict[str, Any]:
        params = super().get_params(llm_input, **kwargs)

        # messages = cast(List[Choice], params["messages"])
        messages = params["messages"]
        system_prompt: Optional[str] = None

        # Extract system prompt if it's the first message
        if len(messages) > 0 and messages[0]["role"] == ConversationRole.system.value:
            system_prompt = messages[0]["content"]
            messages = messages[1:]

        # Remove trailing whitespace from the last assistant message
        if (
            len(messages) > 0
            and messages[-1]["role"] == ConversationRole.assistant.value
        ):
            messages[-1]["content"] = messages[-1]["content"].rstrip()

        # Include base64-encoded images in the request
        for message in messages:
            if (
                isinstance(message["content"], list)
                and message["role"] == ConversationRole.user.value
            ):
                anthropic_content = []

                for content in message["content"]:
                    if content["type"] == "text":
                        anthropic_content.append(content)
                    elif content["type"] == "image_url":
                        anthropic_content.append(
                            process_image_url_anthropic(content["image_url"]["url"])
                        )

                message["content"] = anthropic_content

        # Convert tools to anthropic format
        openai_tools = kwargs.get("tools")
        openai_tools_choice = kwargs.get("tool_choice")

        anthropic_tools: Optional[list[ToolParam]] = None
        anthropic_tool_choice: Optional[ToolChoice] = None

        if openai_tools_choice == "required":
            anthropic_tool_choice = ToolChoiceToolChoiceAny(type="any")
        elif openai_tools_choice == "auto":
            anthropic_tool_choice = ToolChoiceToolChoiceAuto(type="auto")
        elif openai_tools_choice == "none":
            anthropic_tools = None
        elif isinstance(openai_tools_choice, dict):
            anthropic_tool_choice = ToolChoiceToolChoiceTool(
                name=openai_tools_choice["function"]["name"],
                type="tool",
            )

        if openai_tools:
            anthropic_tools = []
            for openai_tool in openai_tools:
                anthropic_tool = ToolParam(
                    name=openai_tool["function"]["name"],
                    description=openai_tool["function"]["description"],
                    input_schema={
                        "type": openai_tool["function"]["parameters"]["type"],
                        "properties": openai_tool["function"]["parameters"][
                            "properties"
                        ],
                        "required": openai_tool["function"]["parameters"]["required"],
                    },
                )

                anthropic_tools.append(anthropic_tool)

        anthropic_create = AnthropicCreate(
            max_tokens=kwargs.get("max_tokens", self.get_model().completion_length),
            messages=messages,
            system=system_prompt,
            tool_choice=anthropic_tool_choice,
            tools=anthropic_tools,
        )

        return delete_none_values(
            {
                **params,
                **anthropic_create.model_dump(),
            }
        )
