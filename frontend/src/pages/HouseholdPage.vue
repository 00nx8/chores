<script lang='ts' setup>
import { userRequest } from 'src/components/userRequest';
import { ref, onMounted } from 'vue'
import GetAHouse from 'src/components/GetAHouse.vue';

const lineChart = ref(null)

interface Chore {
  id: number,
  desc: string,
  deadline?: Date,
  done_on?: Date,
  is_big_job: boolean,
  is_done: boolean,
  resident_id?: number,
  household_id: number
}

const household = ref()
const username = ref(localStorage.getItem('username'))

const selected = ref([])
const rows = ref([])

function getSelectedString () {
  return selected.value.length === 0 ? '' : `${selected.value.length} record${selected.value.length > 1 ? 's' : ''} selected of ${rows.value.length}`
}
const columns = [
  {
    name: 'desc',
    label: 'Name',
    align: "left" as const,
    field:(row: Chore) => row.desc,
    sortable: true
  },
  {
    name: 'deadline',
    label: 'Deadline',
    align: "center" as const,
    field: (row: Chore) => row.deadline ? row.deadline.toLocaleString() : 'N/A',  // Formatting Date
    sortable: true
  },
];


function markAsDone() {
  selected.value.forEach((chore: Chore) => {
    userRequest(`/chore/${chore.id}`, {
      method: "POST"
    })
  })
}

userRequest('/user/household', {
  method: 'GET',
}).then(data => {
  if (data.household) {
    household.value = data.household
    userRequest(`/household/${household.value.id}/chore/todo`, {
      method: "GET",
    }).then(rowsData => {
      console.log(rowsData)
      rows.value = rowsData.chores
    })
    console.log(rows.value)
  }
})

console.log(rows)

</script>

<template>
  <section class="q-pa-md" v-if="household">
    <h1 class="text-h5">Welcome {{ username }}</h1>
    <div>

      <q-table
        flat bordered dense
        title="TODO"
        :rows="rows"
        :columns="columns"
        row-key="id"
        :selected-rows-label="getSelectedString"
        selection="multiple"
        v-model:selected="selected"
        :hide-bottom="true"
      />

      <div v-if="selected.length" class="q-mt-md">
        <q-btn @click="markAsDone" style="position: fixed; right: 1rem; bottom: 5rem;"  color="teal" icon="done">Done</q-btn>
      </div>
    </div>



  </section>
  <section v-else>
    <GetAHouse />
  </section>
</template>