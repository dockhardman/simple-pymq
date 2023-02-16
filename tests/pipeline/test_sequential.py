import asyncio

import pytest

from simple_pymq import (
    NullConsumer,
    PrintConsumer,
    QueueBroker,
    SimpleFileBroker,
    SimpleMessageQueue,
    TimeCounterProducer,
)
from tests.config import settings as test_settings


test_id = str(test_settings.test_uuid).split("-")[0]


@pytest.mark.asyncio
async def test_simple_message_queue_basic_operation():
    q = QueueBroker(maxsize=50)
    c = PrintConsumer(max_consume_count=49)
    p = TimeCounterProducer(count_seconds=0.001, max_produce_count=50)
    mq = SimpleMessageQueue()

    await mq.run(broker=q, producers=p, consumers=c)
    assert await q.qsize() == 1


@pytest.mark.asyncio
async def test_simple_message_queue_massive_tasks():
    total_tasks = 10000
    consumer_count = 10
    producer_count = 10

    q = QueueBroker(maxsize=128)
    consumers = [
        PrintConsumer(max_consume_count=total_tasks // consumer_count)
        for _ in range(consumer_count)
    ]
    producers = [
        TimeCounterProducer(
            count_seconds=0.0, max_produce_count=total_tasks // producer_count
        )
        for _ in range(producer_count)
    ]
    mq = SimpleMessageQueue()

    await mq.run(broker=q, producers=producers, consumers=consumers)
    assert await q.qsize() == 0
