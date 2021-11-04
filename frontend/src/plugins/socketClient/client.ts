export interface WSOptions {
  autoRecon: boolean;
  reconIntervalMs: number;
}

// user will provide these methods
// we will wrap user's logic within WebSocket's methods:
// - parse WebSocket's given parameters from callback,
// - extract relevant info and pass them onto user's methods
export interface WSListeners {
  onOpen(event?: Event): void;
  onClose(event?: CloseEvent): void;
  onError(error: Error, event?: Event): void;
  onMsg(msg: string, event?: MessageEvent): void;
}

const ERR_NO_WS_INSTANCE = Error('WebSocket instance gone');
const ERR_NO_WS_LISTENERS = Error('WebSocket listeners gone');
const ERR_CONNECT = Error('Error trying to establish WebSocket connection with backend');
const ERR_SEND = Error('Error trying to send message to backend');

/**
 * WS Client instance to insert into Vue as a plugin
 * responsible for holding WS connector & wrapping send/recv msg
 * plug in Vue store, it will create a singleton of this
 */
class WSClient {
  private opts: WSOptions;
  private listeners: WSListeners | null;
  private wsInstance: WebSocket | null;
  private url: string;
  private timeoutHandler: number;

  constructor(url: string, opts?: WSOptions, listeners?: WSListeners) {
    this.wsInstance = null;
    this.url = url;

    if (listeners) {
      this.listeners = listeners;
    } else {
      this.listeners = this.noopListeners();
    }

    if (opts) {
      this.opts = opts;
    } else {
      this.opts = this.defaultOptions();
    }

    this.timeoutHandler = -1;
  }

  public defaultOptions(): WSOptions {
    return {
      autoRecon: false,
      reconIntervalMs: 0,
    };
  }

  public noopListeners(): WSListeners {
    return {
      onOpen: () => {
        //
      },
      onClose: () => {
        //
      },
      onMsg: () => {
        //
      },
      onError: () => {
        //
      },
    };
  }

  // == GET/SET == //

  public getOpts() {
    return this.opts;
  }

  public setOpts(opts: WSOptions) {
    this.opts = opts;
  }

  public getWsInstance() {
    return this.wsInstance;
  }

  public getUrl() {
    return this.url;
  }

  public setUrl(url: string) {
    this.url = url;
  }

  // component will call set & apply listeners
  public setListeners(listeners: WSListeners) {
    this.listeners = listeners;

    this.applyListenersToWsInstance(this.listeners);
  }

  // == lifecycle == //

  // connect will be called first, ideally when installing plugin
  public connect() {
    this.wsInstance = new WebSocket(this.url);
  }

  public reconnect() {
    delete this.wsInstance;
    this.timeoutHandler = setTimeout(() => {
      this.connect();
    }, this.opts.reconIntervalMs);
  }

  // for native types, convert to string and use this method
  public sendMsg(msg: string) {
    if (! this.wsInstance) {
      throw ERR_NO_WS_INSTANCE;
    }

    this.wsInstance.send(msg);
  }

  // for other types, turn into js object, then use this method
  public sendJsonableObj(obj: { [key: string]: any } | any[]) {
    if (! this.wsInstance) {
      throw ERR_NO_WS_INSTANCE;
    }

    this.wsInstance.send(JSON.stringify(obj));
  }

  // == cleanup == //

  public cleanup() {
    this.opts = this.defaultOptions();

    clearTimeout(this.timeoutHandler);
    delete this.listeners;
    delete this.wsInstance;
  }

  // internal use, invoked subsequently after setListeners is invoked publicly
  private applyListenersToWsInstance(listeners: WSListeners) {
    if (! this.wsInstance) {
      return;
    }

    // WebSocket's even listeners
    this.wsInstance.onopen = (event: Event) => {
      listeners.onOpen(event);
    };

    this.wsInstance.onmessage = (msgEvent: MessageEvent) => {
      const msg = msgEvent.data;
      listeners.onMsg(msg, msgEvent);
    };

    this.wsInstance.onclose = (event: CloseEvent) => {
      listeners.onClose(event);

      if (! event.wasClean && this.opts.autoRecon) {
        this.reconnect();
      }
    };

    this.wsInstance.onerror = (event: Event) => {
      listeners.onError(ERR_SEND, event);
    };
  }
}

export default WSClient;
