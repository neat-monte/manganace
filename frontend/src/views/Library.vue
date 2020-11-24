<template>
  <div id="library" class="content">
    <Suspense>
      <template #default>
        <Tags />
      </template>
      <template #fallback>
        <Loading id="tags" />
      </template>
    </Suspense>

    <Suspense>
      <template #default>
        <Collections :collectionId="collectionId" />
      </template>
      <template #fallback>
        <Loading id="collections" />
      </template>
    </Suspense>
  </div>
</template>

<script>
import Collections from "@/components/library/Collections";
import Tags from "@/components/library/Tags";
import Loading from "@/components/shared/Loading";

export default {
  name: "Library",

  components: {
    Collections,
    Tags,
    Loading,
  },
};
</script>

<style lang="scss" scoped>
#library {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;

  #tags,
  #collections {
    flex: 1 100%;
  }

  #collections {
    order: -1;
  }
}

@include tablet {
  #library {
    #tags {
      flex: 0 200px;
    }

    #collections {
      flex: 1;
      order: initial;
    }
  }
}
</style>