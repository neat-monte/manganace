<template>
  <div id="research" class="content">
    <ResearchSettings />
    <a-tabs v-if="currentResearchSetting.id">
      <a-tab-pane key="1" tab="Sessions">
        <Suspense>
          <template #default>
            <Sessions :researchSettingId="currentResearchSetting.id" />
          </template>
          <template #fallback>
            <Loading id="sessions" />
          </template>
        </Suspense>
      </a-tab-pane>
      <a-tab-pane key="2" tab="Results">
        <Suspense>
          <template #default>
            <Results :researchSettingId="currentResearchSetting.id" />
          </template>
          <template #fallback>
            <Loading id="sessions" />
          </template>
        </Suspense>
      </a-tab-pane>
    </a-tabs>
  </div>
</template>

<script>
import ResearchSettings from "@/components/research/ResearchSettings";
import Sessions from "@/components/research/Sessions";
import Results from "@/components/research/Results";
import Loading from "@/components/shared/display/Loading";

import useResearchSettings from "@/modules/researchSettings";

export default {
  name: "Research",

  setup() {
    const { currentResearchSetting } = useResearchSettings();

    return {
      currentResearchSetting,
    };
  },

  components: {
    ResearchSettings,
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