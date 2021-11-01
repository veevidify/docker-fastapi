<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Queue new task</div>
      </v-card-title>
      <v-card-text>
        <template>
          <div class="my-3">
            <div class="subheading secondary--text text--lighten-2">Task payload</div>
            <div
              class="title primary--text text--darken-2"
              v-if="task"
            >{{task.msg}}</div>
          </div>
          <v-form
            v-model="valid"
            ref="form"
            lazy-validation
          >
            <v-text-field
              label="Message"
              name="message"
              v-model="message"
              required
            >
            </v-text-field>
          </v-form>
        </template>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          @click="queueTask"
          :disabled="!valid"
        >
          Send
        </v-btn>
      </v-card-actions>
    </v-card>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Poll Results</div>
      </v-card-title>
      <v-card-text>
        <template>
          <div class="my-3">
            <div class="subheading secondary--text text--lighten-2">Task</div>
            <div
              class="title primary--text text--darken-2"
              v-if="task"
            >{{task.task_id}}</div>
            <v-spacer></v-spacer>
            <div class="subheading secondary--text text--lighten-2">Status</div>
            <div
              class="title primary--text text--darken-2"
              v-if="task"
            >{{task.task_status}}</div>
            <div class="subheading secondary--text text--lighten-2">Result</div>
            <div
              class="title primary--text text--darken-2"
              v-if="task"
            >{{task.task_result}}</div>
          </div>
        </template>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="reset">Reset</v-btn>
        <v-btn @click="pollTask">
          Poll
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { IMsg, ITaskPayload, ITaskStatus, WithTaskId } from '@/interfaces';
import { dispatchQueueTask, dispatchPollTaskResult, dispatchClearTask } from '@/store/admin/actions';
import { readCurrentTask, readTaskResult } from '@/store/admin/getters';

@Component
export default class QueueTask extends Vue {
  public message: string = '';
  public setMessage = false;
  public valid = true;
  public pollValid = true;

  public async mounted() {
    //
  }

  public reset() {
    this.message = '';
    dispatchClearTask(this.$store);
  }

  public async queueTask() {
    if (await this.$validator.validateAll()) {
      const payload: IMsg = {
        msg: this.message,
      };

      //
      await dispatchQueueTask(this.$store, payload);
    }
  }

  public async pollTask() {
    const taskId = this.task?.task_id;

    if (taskId) {
      await dispatchPollTaskResult(this.$store, { task_id: taskId });
    }
  }

  get task() {
    return readTaskResult(this.$store);
  }
}

</script>
