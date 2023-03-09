const amqp = require("amqplib");

const worker = async () => {
    try {
        const con = await amqp.connect("amqp://localhost");

        con.on("close", () => {
            console.log("connection to RabbitQM closed!");
            setTimeout(worker, 5000);
        });

        const channel = await con.createChannel();

        const workerName = `worker-${process.pid}`;

        await channel.assertExchange("logs", "direct", {
            durable: true,
        });

        const q = await channel.assertQueue("logs_queue", {
            durable: true,
        });

        channel.prefetch(1);

        await channel.bindQueue(q.queue, "logs", "");

        console.log(`[${workerName}] - Running`);

        channel.consume(q.queue, async (msg) => {
            try {
                const data = msg.content.toString();
                console.log(`[${workerName}] - Received: ${data}`);

                await new Promise((r) => setTimeout(r, 6000));
                console.log(`[${workerName}] - Finished`);

                channel.ack(msg);
            } catch (err) {
                if (err.message === "Channel closed")
                    throw new Error("Channel closed");
                console.log("error before acknowledment:", err);
            }
        }, {
            noAck: false,
        });
    } catch (err) {
        console.log("error outside:", err)
        setTimeout(worker, 5000);
    }

};

worker();
