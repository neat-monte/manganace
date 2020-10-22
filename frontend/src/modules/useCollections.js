import { reactive, readonly } from 'vue'
import http from '@/services/http'

const state = reactive({
  collections: {}
});

export default function useCollections() {
  const loadCollections = async () => {
    const collections = await http.collections.getAllWithoutRelations();
    collections.forEach(collection => {
      state.collections[collection.id] = collection;
    })
  }

  return {
    state: readonly(state),
    loadCollections
  }
}

// const storeCollections = (collections) => {
//   collections.forEach(collection => {
//     if (collection.id in state.collections)
//       return;
//     const cl = makeCollection(collection);
//     collection.images.forEach(image => {
//       if (image.id in state.images || image.id in cl.imagesIds)
//         return;
//       const im = makeImage(image);
//       image.tags.forEach(tag => {
//         if (tag.id in state.tags || tag.id in im.tagsIds)
//           return;
//         im.tagsIds.push(tag.id);
//         state.tagsIds.push(tag.id);
//         state.tags[tag.id] = makeTag(tag);
//       });
//       cl.imagesIds.push(image.id);
//       state.imagesIds.push(image.id);
//       state.images[image.id] = im;
//     });
//     state.collectionsIds.push(collection.id);
//     state.collections[collection.id] = cl;
//   });
// }

// function makeCollection(collectionJson) {
//   return {
//     id: collectionJson.id,
//     name: collectionJson.name,
//     description: collectionJson.description,
//     isArchived: collectionJson.isArchived,
//     created: collectionJson.created,
//     updated: collectionJson.updated,
//     imagesIds: []
//   }
// }

// function makeImage(imageJson) {
//   return {
//     id: imageJson.id,
//     seed: imageJson.seed,
//     filename: `${endpoints.baseAddress}${endpoints.static}/${imageJson.filename}`,
//     description: imageJson.description,
//     collectionId: imageJson.collectionId,
//     tagsIds: []
//   }
// }

// function makeTag(tagJson) {
//   return {
//     id: tagJson.id,
//     name: tagJson.name
//   }
// }