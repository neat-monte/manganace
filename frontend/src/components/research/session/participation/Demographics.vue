<template>
  <div class="demographics">
    <div class="title">Demographics</div>
    <a-form class="form">
      <a-form-item label="Enter your age">
        <a-input-number
          :value="age"
          :min="18"
          :max="120"
          @change="$emit('update:age', $event)"
        />
      </a-form-item>
      <a-form-item label="Select your gender">
        <a-radio-group
          :value="genderId"
          @change="$emit('update:genderId', $event.target.value)"
        >
          <a-radio
            v-for="gender in genderOptions"
            :key="gender.id"
            :value="gender.id"
            class="radio"
          >
            {{ gender.option }}
          </a-radio>
        </a-radio-group>
      </a-form-item>
    </a-form>
  </div>
</template>

<script>
import { ref, watchEffect } from "vue";

import useExtras from "@/modules/extras";

export default {
  name: "Demographics",

  props: {
    age: Number,
    genderId: Number,
  },

  async setup() {
    const { loadGendersAsync, gendersById } = useExtras();

    const genderOptions = ref([]);

    watchEffect(() => {
      genderOptions.value = Object.values(gendersById);
    });

    await loadGendersAsync();

    return {
      genderOptions,
    };
  },
};
</script>

<style lang="scss" scoped>
.demographics {
  .form {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-around;

    .radio {
      display: block;
      height: 30px;
      line-height: 30px;
    }
  }
}
</style>