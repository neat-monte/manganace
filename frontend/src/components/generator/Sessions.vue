<template>
  <div id="sessions">
    <div class="controls">
      <Suspense>
        <template #default>
          <SessionSelect @session-id-set="setCurrentSession" />
        </template>
      </Suspense>
    </div>
    <Suspense>
      <template #default>
        <Activity />
      </template>
      <template #fallback>
        <Loading id="activity" />
      </template>
    </Suspense>
  </div>
</template>

<script>
import Activity from "@/components/generator/Activity";
import SessionSelect from "@/components/actions/session/SessionSelect";
import Loading from "@/components/shared/Loading";
import useGenerator from "@/modules/generator";

export default {
  name: "Sessions",

  async setup() {
    const { setCurrentSession } = useGenerator();

    return {
      setCurrentSession,
    };
  },

  components: {
    Loading,
    SessionSelect,
    Activity,
  },
};
</script>

<style lang="scss" scoped>
#sessions {
  max-width: 100%;
  padding: 20px;
  display: flex;
  flex-direction: column;

  .controls {
    margin-bottom: 20px;
    display: flex;
  }
}

@include tablet {
  #sessions {
    border-radius: 2px;
    box-shadow: $box-double-shadow;
  }
}
</style>