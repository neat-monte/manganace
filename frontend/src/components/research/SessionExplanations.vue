<template>
  <div id="explanation">
    <p>There are <strong>6</strong> emotion vectors, therefore:</p>
    <ul>
      <li>
        <p>
          Every session will have
          <strong>{{ 6 * researchSetting.totalAmount }}</strong> trials.
        </p>
      </li>
      <li>
        <p>
          A session will contain
          <strong>{{
            6 * researchSetting.totalAmount * researchSetting.sliderSteps
          }}</strong>
          images in total.
        </p>
      </li>
      <li>
        <p>
          A session <i>might</i> take around <strong>{{ duration }}</strong> to
          generate.
        </p>
      </li>
      <li>
        <p>
          One session will require <i>approximately </i>
          <strong>{{ storage }}</strong> of space.
        </p>
      </li>
    </ul>
  </div>
</template>

<script>
import moment from "moment";
import { ref, watchEffect } from "vue";

export default {
  name: "SessionExplanation",

  props: {
    researchSetting: Object,
    amount: {
      type: Number,
      default: 1,
    },
  },

  setup(props) {
    const duration = ref();
    const storage = ref();

    watchEffect(() => {
      let seconds =
        0.3 /* one image generation duration approximation */ *
        6 /* vector count */ *
        props.researchSetting.totalAmount *
        props.researchSetting.sliderSteps *
        props.amount;

      const dur = moment.duration(seconds, "seconds");
      const hours = Math.floor(dur.asHours());
      const minutes = Math.floor(dur.asMinutes()) - hours * 60;
      if (hours <= 0) {
        duration.value = `${minutes} minutes`;
      } else {
        duration.value = `${hours} hours ${minutes} minutes`;
      }
      let bytes =
        1460497 *
        6 *
        props.researchSetting.totalAmount *
        props.researchSetting.sliderSteps *
        props.amount;
      const megabytes = Math.floor(bytes / 1048576);
      const gigabytes = (megabytes / 1024).toFixed(2);
      if (gigabytes < 1) {
        storage.value = `${megabytes} MB`;
      } else {
        storage.value = `${gigabytes} GB`;
      }
    });

    return {
      duration,
      storage,
    };
  },
};
</script>