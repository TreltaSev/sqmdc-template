/* eslint-disable @typescript-eslint/no-explicit-any */

type WebsocketCallback = (error?: string, data?: any) => void | Promise<void>;

type WebsocketListener = {
    [operation: string]: {
        callback: WebsocketCallback;
    };
};

export class Websocket {
    private href: string;
    public connection: WebSocket | undefined;
    private listeners: WebsocketListener = {};

    public base_url: string = `api.${window.location.hostname}`;

    // Optional global error handler
    public onerror: (error: string, data?: any) => void = () => {};

    constructor(href: string) {
        this.href = href;
    }

    private listen = async (event: MessageEvent) => {
        let response: any;

        try {
            response = JSON.parse(event.data);
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
        } catch (e) {
            console.error("Failed to parse WebSocket message:", event.data);
            return;
        }

        const { operation, data, error } = response;

        const listener = this.listeners[operation];
        if (listener?.callback) {
            try {
                await listener.callback(error, data);
            } catch (e) {
                console.error(`Error in listener for "${operation}":`, e);
            }
        }

        if (error && this.onerror) {
            this.onerror(error, data);
        }
    };

    public async connect(): Promise<void> {
        this.connection = new WebSocket(`wss://${this.base_url}${this.href}`);

        await new Promise<void>((resolve, reject) => {
            this.connection!.onopen = () => {
                this.connection!.onmessage = this.listen;
                resolve();
            };

            this.connection!.onerror = (err) => {
                reject(err);
            };
        });
    }

    public send(operation: string, data: Record<string, any>) {
        if (!this.connection || this.connection.readyState !== WebSocket.OPEN) {
            console.warn("WebSocket not ready, skipping send:", operation);
            return;
        }

        const data_buffer = { operation, data };
        this.connection.send(JSON.stringify(data_buffer));
    }

    public on(operation: string, callback: WebsocketCallback) {
        this.listeners[operation] = { callback };
    }
}
