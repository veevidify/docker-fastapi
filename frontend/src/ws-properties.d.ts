import WSClient from './plugins/socketClient/client';

declare module 'vue/types/vue' {
  interface Vue {
    $socketClient: WSClient;
  }

  interface VueConstructor {
    $socketClient: WSClient;
  }
}
