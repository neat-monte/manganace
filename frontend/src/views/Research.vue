<template>
  <div id="research" class="content">
    <a-tabs>
      <a-tab-pane key="1" tab="Sessions">
        <Suspense>
          <template #default>
            <Sessions />
          </template>
          <template #fallback>
            <Loading id="sessions" />
          </template>
        </Suspense>
      </a-tab-pane>
      <a-tab-pane key="2" tab="Results">
        <Results />
      </a-tab-pane>
    </a-tabs>
  </div>
</template>

<script>
import Sessions from "@/components/research/Sessions";
import Results from "@/components/research/Results";
import Loading from "@/components/shared/Loading";

export default {
  name: "Research",

  components: {
    Sessions,
    Results,
    Loading,
  },
};
</script>

<style lang="scss" scoped>
#research {
  &.content {
    padding-top: 0;
  }

  .ant-tabs-content {
    .ant-tabs-tabpane {
      min-height: 300px;
    }
  }
}
</style>