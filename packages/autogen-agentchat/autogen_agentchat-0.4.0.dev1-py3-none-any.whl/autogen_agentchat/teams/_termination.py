import asyncio
from abc import ABC, abstractmethod
from typing import List, Sequence

from ..agents import ChatMessage, MultiModalMessage, StopMessage, TextMessage


class TerminatedException(BaseException): ...


class TerminationCondition(ABC):
    """A stateful condition that determines when a conversation should be terminated.

    A termination condition is a callable that takes a sequence of ChatMessage objects
    since the last time the condition was called, and returns a StopMessage if the
    conversation should be terminated, or None otherwise.
    Once a termination condition has been reached, it must be reset before it can be used again.

    Termination conditions can be combined using the AND and OR operators.

    Example:

        .. code-block:: python

            from autogen_agentchat.teams import MaxTurnsTermination, TextMentionTermination

            # Terminate the conversation after 10 turns or if the text "TERMINATE" is mentioned.
            cond1 = MaxTurnsTermination(10) | TextMentionTermination("TERMINATE")

            # Terminate the conversation after 10 turns and if the text "TERMINATE" is mentioned.
            cond2 = MaxTurnsTermination(10) & TextMentionTermination("TERMINATE")

            ...

            # Reset the termination condition.
            await cond1.reset()
            await cond2.reset()
    """

    @property
    @abstractmethod
    def terminated(self) -> bool:
        """Check if the termination condition has been reached"""
        ...

    @abstractmethod
    async def __call__(self, messages: Sequence[ChatMessage]) -> StopMessage | None:
        """Check if the conversation should be terminated based on the messages received
        since the last time the condition was called.
        Return a StopMessage if the conversation should be terminated, or None otherwise.

        Args:
            messages: The messages received since the last time the condition was called.

        Returns:
            StopMessage | None: A StopMessage if the conversation should be terminated, or None otherwise.

        Raises:
            TerminatedException: If the termination condition has already been reached."""
        ...

    @abstractmethod
    async def reset(self) -> None:
        """Reset the termination condition."""
        ...

    def __and__(self, other: "TerminationCondition") -> "TerminationCondition":
        """Combine two termination conditions with an AND operation."""
        return _AndTerminationCondition(self, other)

    def __or__(self, other: "TerminationCondition") -> "TerminationCondition":
        """Combine two termination conditions with an OR operation."""
        return _OrTerminationCondition(self, other)


class _AndTerminationCondition(TerminationCondition):
    def __init__(self, *conditions: TerminationCondition) -> None:
        self._conditions = conditions
        self._stop_messages: List[StopMessage] = []

    @property
    def terminated(self) -> bool:
        return all(condition.terminated for condition in self._conditions)

    async def __call__(self, messages: Sequence[ChatMessage]) -> StopMessage | None:
        if self.terminated:
            raise TerminatedException("Termination condition has already been reached.")
        # Check all remaining conditions.
        stop_messages = await asyncio.gather(
            *[condition(messages) for condition in self._conditions if not condition.terminated]
        )
        # Collect stop messages.
        for stop_message in stop_messages:
            if stop_message is not None:
                self._stop_messages.append(stop_message)
        if any(stop_message is None for stop_message in stop_messages):
            # If any remaining condition has not reached termination, it is not terminated.
            return None
        content = ", ".join(stop_message.content for stop_message in self._stop_messages)
        source = ", ".join(stop_message.source for stop_message in self._stop_messages)
        return StopMessage(content=content, source=source)

    async def reset(self) -> None:
        for condition in self._conditions:
            await condition.reset()
        self._stop_messages.clear()


class _OrTerminationCondition(TerminationCondition):
    def __init__(self, *conditions: TerminationCondition) -> None:
        self._conditions = conditions

    @property
    def terminated(self) -> bool:
        return any(condition.terminated for condition in self._conditions)

    async def __call__(self, messages: Sequence[ChatMessage]) -> StopMessage | None:
        if self.terminated:
            raise RuntimeError("Termination condition has already been reached")
        stop_messages = await asyncio.gather(*[condition(messages) for condition in self._conditions])
        if any(stop_message is not None for stop_message in stop_messages):
            content = ", ".join(stop_message.content for stop_message in stop_messages if stop_message is not None)
            source = ", ".join(stop_message.source for stop_message in stop_messages if stop_message is not None)
            return StopMessage(content=content, source=source)
        return None

    async def reset(self) -> None:
        for condition in self._conditions:
            await condition.reset()


class StopMessageTermination(TerminationCondition):
    """Terminate the conversation if a StopMessage is received."""

    def __init__(self) -> None:
        self._terminated = False

    @property
    def terminated(self) -> bool:
        return self._terminated

    async def __call__(self, messages: Sequence[ChatMessage]) -> StopMessage | None:
        if self._terminated:
            raise TerminatedException("Termination condition has already been reached")
        for message in messages:
            if isinstance(message, StopMessage):
                self._terminated = True
                return StopMessage(content="Stop message received", source="StopMessageTermination")
        return None

    async def reset(self) -> None:
        self._terminated = False


class MaxMessageTermination(TerminationCondition):
    """Terminate the conversation after a maximum number of messages have been exchanged.

    Args:
        max_messages: The maximum number of messages allowed in the conversation.
    """

    def __init__(self, max_messages: int) -> None:
        self._max_messages = max_messages
        self._message_count = 0

    @property
    def terminated(self) -> bool:
        return self._message_count >= self._max_messages

    async def __call__(self, messages: Sequence[ChatMessage]) -> StopMessage | None:
        if self.terminated:
            raise TerminatedException("Termination condition has already been reached")
        self._message_count += len(messages)
        if self._message_count >= self._max_messages:
            return StopMessage(
                content=f"Maximal number of messages {self._max_messages} reached, current message count: {self._message_count}",
                source="MaxMessageTermination",
            )
        return None

    async def reset(self) -> None:
        self._message_count = 0


class TextMentionTermination(TerminationCondition):
    """Terminate the conversation if a specific text is mentioned.

    Args:
        text: The text to look for in the messages.
    """

    def __init__(self, text: str) -> None:
        self._text = text
        self._terminated = False

    @property
    def terminated(self) -> bool:
        return self._terminated

    async def __call__(self, messages: Sequence[ChatMessage]) -> StopMessage | None:
        if self._terminated:
            raise TerminatedException("Termination condition has already been reached")
        for message in messages:
            if isinstance(message, TextMessage | StopMessage) and self._text in message.content:
                self._terminated = True
                return StopMessage(content=f"Text '{self._text}' mentioned", source="TextMentionTermination")
            elif isinstance(message, MultiModalMessage):
                for item in message.content:
                    if isinstance(item, str) and self._text in item:
                        self._terminated = True
                        return StopMessage(content=f"Text '{self._text}' mentioned", source="TextMentionTermination")
        return None

    async def reset(self) -> None:
        self._terminated = False
