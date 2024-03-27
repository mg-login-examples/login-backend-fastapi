import pytest
import asyncio
import time
from unittest.mock import patch

from utils.pubsub.subscriber import Subscriber, Unsubscribed
from utils.pubsub.event import Event


async def test_subscriber_put():
    # init test data
    event = Event(channel="ch", message="m")

    # init subscriber
    subscriber = Subscriber()
    # can pass event to subscriber
    await subscriber.put(event)
    # assert subscriber queue stores event
    assert await subscriber._queue.get() == event


async def test_subscriber_get():
    # init test data
    event1 = Event(channel="ch", message="m1")
    event2 = Event(channel="ch", message="m2")
    # init subscriber
    subscriber = Subscriber()
    # pass events to subscriber
    await subscriber.put(event1)
    await subscriber.put(event2)

    # assert can get latest event from subscriber
    assert await subscriber.get() == event1
    assert await subscriber.get() == event2


async def test_subscriber_get_with_timeout():
    # init timeout val in sec
    timeout = 2
    # init subscriber
    subscriber = Subscriber()
    # set start time to measure get timeout duration
    start_time = time.monotonic()
    # assert that get raises TimeoutError after 2 second timeout
    with pytest.raises(TimeoutError):
        await subscriber.get(timeout=timeout)
    # assert subscriber get timed out after given timeout value
    end_time = time.monotonic()
    elapsed_time = end_time - start_time
    assert elapsed_time >= timeout and elapsed_time < timeout + 0.1


async def test_subscriber_get_from_empty_queue():
    # init subscriber
    subscriber = Subscriber()
    # assert subscriber get does not return anything if queue is empty
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(subscriber.get(), timeout=1)


async def test_subscriber_get_None():
    # init subscriber
    subscriber = Subscriber()

    # pass None to subscriber
    await subscriber.put(None)
    # assert subscriber raises Unsubscribed when None is received from queue
    with pytest.raises(Unsubscribed):
        await subscriber.get()


async def test_subscriber_async_for_loop():
    # init test data
    event1 = Event(channel="ch", message="m1")
    event2 = Event(channel="ch", message="m2")
    event3 = Event(channel="ch", message="m3")

    # init subscriber
    subscriber = Subscriber()
    # add subscriber events
    await subscriber.put(event1)
    await subscriber.put(event2)
    await subscriber.put(event3)

    subscriber_emitted_events = []

    async def run_subscriber_async_loop(events_catcher):
        async for event in subscriber:
            events_catcher.append(event)

    subscriber_task = asyncio.create_task(
        run_subscriber_async_loop(subscriber_emitted_events))

    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(subscriber_task, timeout=1)

    assert subscriber_emitted_events == [event1, event2, event3]


async def test_subscriber_async_for_loop_exit_by_passing_None():
    # init test data
    event1 = Event(channel="ch", message="m1")
    event2 = Event(channel="ch", message="m2")

    # init subscriber
    subscriber = Subscriber()
    # add subscriber events
    await subscriber.put(event1)
    await subscriber.put(event2)
    await subscriber.put(None)

    subscriber_emitted_events = []

    async def run_subscriber_async_loop(events_catcher):
        async for event in subscriber:
            events_catcher.append(event)

    subscriber_task = asyncio.create_task(
        run_subscriber_async_loop(subscriber_emitted_events))

    await subscriber_task
    assert subscriber_emitted_events == [event1, event2]


async def test_subscriber_exit_async_for_loop():
    # init subscriber
    subscriber = Subscriber()
    subscriber_emitted_events = []

    async def run_subscriber_async_loop(events_catcher):
        async for _ in subscriber:
            pass
    subscriber_task = asyncio.create_task(
        run_subscriber_async_loop(subscriber_emitted_events))

    # async for loop continues (indefintely)
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(asyncio.shield(subscriber_task), timeout=1)
    # async for loop continues (indefintely)
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(asyncio.shield(subscriber_task), timeout=1)

    # call exit_async_iter to end async for loop
    await subscriber.exit_async_iter()
    # assert subscriber async for loop ends
    await subscriber_task


async def test_subscriber_aenter_aexit():
    with patch.object(Subscriber, 'exit_async_iter') as mock_exit_async_iter:
        async with Subscriber() as _:
            mock_exit_async_iter.assert_not_called()
        mock_exit_async_iter.assert_called_once()
