import Vue from 'vue';
import WSClient, { WSListeners, WSOptions } from './client';

export { WSListeners, WSOptions };

// plugin for Vue
// Vue.use has to define these params
const wsPlugin = {
  install: (
    vue,
    connectionUrl: string,
    wsOptions?: WSOptions,
    wsListeners?: WSListeners,
  ) => {
    const socketClient = new WSClient(connectionUrl, wsOptions, wsListeners);
    socketClient.connect();
    Vue.prototype.$socketClient = socketClient;
  },
};

export default wsPlugin;
