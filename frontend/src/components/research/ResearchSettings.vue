<template>
  <div id="research-settings">
    <div v-if="!currentResearchSetting.id" class="no-setting-selected">
      <span class="message">Choose</span>
      <Suspense>
        <template #default>
          <ResearchSettingSelect
            placeholder="an already existing"
            @setting-id-set="setCurrentResearchSetting"
          />
        </template>
        <template #fallback>
          <span class="message">an already existing</span>
        </template>
      </Suspense>
      <span class="message">research setting or</span>
      <ResearchSettingCreate buttonText="Create" />
      <span class="message">new setting</span>
    </div>

    <div v-else class="setting-selected">
      <div class="controls">
        <div class="title">Research setting</div>
        <div class="actions">
          <Suspense>
            <template #default>
              <ResearchSettingSelect
                @setting-id-set="setCurrentResearchSetting"
              />
            </template>
            <template #fallback>
              <Loading />
            </template>
          </Suspense>
          <ResearchSettingCreate />
        </div>
      </div>
      <div class="current-setting">
        <a-descriptions
          size="small"
          :column="5"
          layout="vertical"
          :bordered="true"
        >
          <a-descriptions-item label="Global multiplier">
            <span>{{ currentResearchSetting.globalMultiplier }}</span>
          </a-descriptions-item>
          <a-descriptions-item label="Image #">
            <span>{{ currentResearchSetting.totalAmount }}</span>
          </a-descriptions-item>
          <a-descriptions-item label="Overlapping">
            <span>{{ currentResearchSetting.overlapAmount }}</span>
          </a-descriptions-item>
          <a-descriptions-item label="Gender eq.">
            <span>{{
              currentResearchSetting.equalizeGender ? "Yes" : "No"
            }}</span>
          </a-descriptions-item>
          <a-descriptions-item label="Sl. steps">
            <span>{{ currentResearchSetting.sliderSteps }}</span>
          </a-descriptions-item>
        </a-descriptions>
      </div>
    </div>
  </div>
</template>

<script>
import ResearchSettingCreate from "@/components/shared/modals/researchSetting/ResearchSettingCreate";
import ResearchSettingSelect from "@/components/shared/controls/ResearchSettingSelect";
import Loading from "@/components/shared/display/Loading";

import useResearchSettings from "@/modules/researchSettings";

export default {
  name: "ResearchSettings",

  setup() {
    const {
      currentResearchSetting,
      setCurrentResearchSetting,
    } = useResearchSettings();

    return {
      currentResearchSetting,
      setCurrentResearchSetting,
    };
  },

  components: {
    ResearchSettingCreate,
    ResearchSettingSelect,
    Loading,
  },
};
</script>

<style lang="scss" scoped>
#research-settings {
  padding: 20px 20px;

  & > * {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    align-items: flex-start;
  }

  .no-setting-selected {
    .message {
      font-size: 1.4rem;
      font-weight: bold;
      color: $primary;
      margin: 0 10px;
    }

    .research-setting-select {
      width: 200px;
    }
  }

  .setting-selected {
    .controls {
      flex: 100%;
      display: flex;
      flex-wrap: wrap;
      margin-bottom: 10px;

      .title {
        flex: 100%;
      }

      .actions {
        flex: 100%;
        display: flex;
      }

      .research-setting-select {
        margin-right: 10px;
      }
    }

    .current-setting {
      flex: 100%;
    }
  }
}

@include tablet {
  #research-settings {
    padding: 20px 0;
  }
}

@include sm-desktop {
  #research-settings {
    .setting-selected {
      .controls,
      .current-setting {
        flex: 1;
      }

      .controls {
        margin-bottom: 0;
        margin-right: 10px;
      }
    }
  }
}
</style>