<script lang="ts" setup>
import { type Chore } from 'src/pages/HouseholdPage.vue';
import { ref, watch, toRef } from 'vue'

interface Column {
  name: string,
  label: string,
  align: 'left' | 'right' | 'center',
  field: string | ((row: Chore) => string)
  sortable?: boolean
}

const emit = defineEmits(['selected'])

const props = defineProps<{
  columns: Column[],
  rows: Chore[],
  title: string
}>()

const rows = toRef(props, 'rows')
const columns = toRef(props, 'columns')

const selected = ref([])

watch(selected, () => {
  emit('selected', selected.value)
})

</script>

<template>
<div>
  <q-table
    class="no-x-scroll"
    style="height: 200px;"
    flat bordered dense
    virtual-scroll
    :title="props.title!"
    :rows="rows"
    :columns="columns"
    row-key="id"
    :selection="props.title == 'TODO' ? 'multiple' : 'none'"
    v-model:selected="selected"
    :hide-bottom="true"
    :no-data-label="props.title == 'TODO' ? 'You\'re done 🫡' : 'what u doin?'"
    :rows-per-page-options="[0]"
  />
</div>
</template>


<style lang="scss">
.no-x-scroll {
  .q-table__middle.q-virtual-scroll.q-virtual-scroll--vertical.scroll {
    overflow-x: hidden;
    table {
      tbody {
        tr {
          td {
            max-width: 50dvw;
            overflow-x: hidden;
            text-wrap: balance;
          }
        }
      }
    }
  }
}
</style>