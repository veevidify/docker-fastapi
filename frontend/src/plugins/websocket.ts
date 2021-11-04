import Vue from 'vue';

import wsPlugin from './socketClient';

Vue.use(wsPlugin, 'ws://localhost/api/live', {
  autoRecon: true,
  reconIntervalMs: 5000,
});
