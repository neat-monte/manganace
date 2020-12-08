<template>
  <div id="not-found" class="content">
    <a-result
      status="404"
      title="404"
      sub-title="Sorry, the page you visited does not exist."
    >
      <template #extra>
        <a-button type="primary" @click="goHome"> Back Home </a-button>
      </template>
    </a-result>
  </div>
</template>

<script>
import { useRouter } from "vue-router";

export default {
  name: "NotFound",

  setup() {
    const router = useRouter();
    function goHome() {
      router.push({ path: "/" });
    }
    return { goHome };
  },
};
</script>