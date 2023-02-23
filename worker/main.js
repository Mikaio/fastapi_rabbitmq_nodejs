const amqp = require("amqplib");

const worker = async () => {
    const con = await amqp.connect("amqp://localhost");

    const channel = await con.createChannel();

    const workerName = `worker-${process.pid}`;

    await channel.assertExchange("logs", "direct", {
        durable: true,
    });

    const q = await channel.assertQueue("logs_queue", {
        durable: true,
    });

    channel.prefetch(1);

    console.log(`[${workerName}] - Running`);

    channel.consume(q.queue, async (msg) => {
        const data = msg.content.toString();
        console.log(`[${workerName}] - Received: ${data}`);

        await new Promise((r) => setTimeout(r, 3000));
        console.log(`[${workerName}] - Finished`);

        channel.ack(msg);
    }, {
        noAck: false,
    });
};

worker();
