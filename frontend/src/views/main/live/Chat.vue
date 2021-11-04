<template>
  <v-container>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Live Chat Room</div>
      </v-card-title>
      <v-card-text>
        <template>
          <div class="my-3" v-for="msg in mockMsgs" v-bind:key="msg.id">
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

@Component
export default class LiveChat extends Vue {
  // implement listeners to interact with store, and with backend via WS, here
  public mockMsgs = [
    {
      id: '1',
      from: 'User1',
      message: 'Hello',
    },
    {
      id: '2',
      from: 'User2',
      message: 'Hi',
    },
  ];

  public async mounted() {
    this.$socketClient.connect();
  }

  // const listeners: WSListeners = {}
  // open: log event, text - status: connected
  // close: log event, text - status: closed
  // error: log event, text - status: error
  // recon: log event, text - status: attempting to recon
  // msg: log event, add notif? display message

  // send msg: use ws to send

  // this.$socketClient.setListeners(listeners)


}

</script>
