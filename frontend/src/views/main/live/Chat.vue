<template>
  <v-container>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Live Chat Room</div>
      </v-card-title>
      <v-card-text>
        <template>
          <div class="my-3">
            <div class="primary--text text--lighten-3">
              User email here
            </div>
            <v-layout row justify-start>
              <v-flex shrink>
                <!-- rounded-xl not working for this version of vuetify -->
                <div class="subheading secondary text--darken-2 pa-2 text-center text-wrap" style="border-radius: 8px">
                  Chat text here
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
                  v-model="message"
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

