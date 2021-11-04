<template>
  <v-container>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Live Chat Room</div>
      </v-card-title>
      <v-card-text>
        <template>
          <div class="my-3" v-for="msg in messages" v-bind:key="msg.id">
            <div class="primary--text text--lighten-3">
              {{ msg.from }}
            </div>
            <v-layout row justify-start>
              <v-flex shrink>
                <!-- rounded-xl not working for this version of vuetify -->
                <div class="subheading secondary text--darken-2 pa-2 text-center text-wrap" style="border-radius: 8px">
                  {{ msg.message }}
                </div>
              </v-flex>
            </v-layout>
          </div>
        </template>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-container fluid grid-list-md>
          <v-layout row justify-space-around>
            <v-flex>
              <v-form
                v-model="valid"
                ref="form"
                lazy-validation
              >
                <v-text-field
                  label="Say something"
                  v-model="currentMessage"
                  required
                ></v-text-field>
              </v-form>
            </v-flex>
            <v-flex shrink align-self-center>
              <v-btn
                @click="send"
                :disabled="!valid"
              >
                Send
              </v-btn>
            </v-flex>
          </v-layout>
        </v-container>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import wsPlugin, { WSListeners } from '@/plugins/socketClient';
import { commitAddNotification, commitRemoveNotification } from '@/store/main/mutations';
import { IWSMessage } from '@/interfaces';

@Component
export default class LiveChat extends Vue {
  // implement listeners to interact with store, and with backend via WS, here

  public connectionStatus: string = 'connecting';
  public errorMessage: string | null = null;
  public currentMessage: string = '';
  public valid: boolean = true;
  public messages = [
    {
      id: 1,
      from: 'App',
      message: 'Welcome to Live Chat',
    },
  ];

  public listeners: WSListeners = {
    onOpen: (event: Event) => {
      // console.log('== connected to backend via ws');
      this.connectionStatus = 'connected';
    },
    onClose: (event: CloseEvent) => {
      // console.log('== disconnected from backend via ws');
      this.connectionStatus = 'disconnected';
    },
    onError: (error: Error, event: Event) => {
      // console.log(error);
      this.errorMessage = error.message;
      this.connectionStatus = 'error';
    },
    onMsg: (msg: string, event: MessageEvent) => {
      const decodedMsg: IWSMessage = JSON.parse(msg);
      const msgObj = {
        id: this.messages.slice(-1)[0].id + 1,
        from: decodedMsg.by,
        message: decodedMsg.message,
      };
      this.messages.push(msgObj);
    },
  };

  public async mounted() {
    this.$socketClient.setListeners(this.listeners);
  }

  public send() {
    // console.log('== send msg: ', this.currentMessage);
    if (this.currentMessage !== '') {
      this.$socketClient.sendMsg(this.currentMessage);
    }
    this.currentMessage = '';
  }

  public unmounted() {
    this.$socketClient.cleanup();
  }
}

</script>
