
<!--
 i cant be bothered for typescript rn
 TODO:get it to shut up

 -->


<script lang="ts" setup>
import { ref } from 'vue'
interface Column {
  name: string,
  label: string,
  align: 'left' | 'right' | 'center',
  field: string | ((row: any) => any)
  sortable?: boolean

}

const props = defineProps<{
  columns: Column[],
  rows: any[]
}>()

const columns = props.columns
const rows = props.rows

const selected = ref([])


</script>

<template>
<div>
  <q-table
    flat bordered dense
    title="TODO"
    :rows="rows"
    :columns="columns"
    row-key="id"
    selection="multiple"
    v-model:selected="selected"
    :hide-bottom="true"
  />
</div>
</template>