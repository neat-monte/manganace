<template>
  <a-button v-if="buttonText" type="primary" @click="showModal()">
    {{ buttonText }}
    <edit-outlined />
  </a-button>

  <a-tooltip v-else placement="top" title="Edit image">
    <a-button type="primary" @click="showModal()">
      <template v-slot:icon>
        <edit-outlined />
      </template>
    </a-button>
  </a-tooltip>

  <a-modal
    v-model:visible="visible"
    title="Edit image description"
    @ok="handleUpdate()"
  >
    <a-form>
      <a-form-item label="Description">
        <a-textarea
          v-model:value="updatedImage.description"
          placeholder="Give picture a short description"
          :rows="2"
        />
      </a-form-item>

      <a-form-item label="Tags">
        <Suspense>
          <template #default>
            <TagSelect v-model="updatedImage.tagsIds" />
          </template>
        </Suspense>
      </a-form-item>
    </a-form>
  </a-modal>
</template>

<script>
import { reactive, ref } from "vue";
import { EditOutlined } from "@ant-design/icons-vue";
import TagSelect from "@/components/shared/controls/TagSelect";
import useImages from "@/modules/images";

export default {
  name: "ImageUpdate",

  props: {
    image: Object,
    buttonText: {
      type: String,
      default: null,
    },
  },

  setup(props) {
    const visible = ref();
    function showModal() {
      visible.value = true;
    }

    const { updateCollectionImageAsync } = useImages();
    const updatedImage = reactive({
      id: props.image.id,
      description: props.image.description,
      collectionId: props.image.collectionId,
      tagsIds: props.image.tagsIds,
    });

    async function handleUpdate() {
      visible.value = false;
      await updateCollectionImageAsync(updatedImage);
    }

    return {
      updatedImage,
      handleUpdate,
      showModal,
      visible,
    };
  },

  components: {
    EditOutlined,
    TagSelect,
  },
};
</script>