from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any, ClassVar, Generator

from autogen_core.base._agent_type import AgentType


class SubscriptionInstantiationContext:
    def __init__(self) -> None:
        raise RuntimeError(
            "SubscriptionInstantiationContext cannot be instantiated. It is a static class that provides context management for subscription instantiation."
        )

    SUBSCRIPTION_CONTEXT_VAR: ClassVar[ContextVar[AgentType]] = ContextVar("SUBSCRIPTION_CONTEXT_VAR")

    @classmethod
    @contextmanager
    def populate_context(cls, ctx: AgentType) -> Generator[None, Any, None]:
        token = SubscriptionInstantiationContext.SUBSCRIPTION_CONTEXT_VAR.set(ctx)
        try:
            yield
        finally:
            SubscriptionInstantiationContext.SUBSCRIPTION_CONTEXT_VAR.reset(token)

    @classmethod
    def agent_type(cls) -> AgentType:
        try:
            return cls.SUBSCRIPTION_CONTEXT_VAR.get()
        except LookupError as e:
            raise RuntimeError(
                "SubscriptionInstantiationContext.runtime() must be called within an instantiation context such as when the AgentRuntime is instantiating an agent. Mostly likely this was caused by directly instantiating an agent instead of using the AgentRuntime to do so."
            ) from e
