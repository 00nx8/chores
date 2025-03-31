
<!--
 i cant be bothered for typescript rn
 TODO:get it to shut up

 -->
<script lang="ts" setup>
import { ref } from 'vue'
const props = defineProps({
  rows: [],
})

const selected = ref([])


</script>

<template>
<div>
  <q-table
    flat bordered dense
    title="TODO"
    :rows="props.rows!"
    :columns="props.columns!"
    row-key="id"
    selection="multiple"
    v-model:selected="selected"
    :hide-bottom="true"
  />
</div>
</template>