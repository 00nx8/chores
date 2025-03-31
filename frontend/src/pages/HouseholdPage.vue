<script lang='ts' setup>
import { userRequest } from 'src/components/userRequest';
import { ref } from 'vue'
import GetAHouse from 'src/components/GetAHouse.vue';
import ChoreTable from 'src/components/ChoreTable.vue';

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

const householdRequest = await userRequest('/user/household', {
  method: 'GET',
}).catch(error => console.log(error))

household.value = householdRequest.household
console.log(household.value)
</script>

<template>
  <section class="q-pa-md" v-if="household">
    <h1 class="text-h5">Welcome {{ username }}</h1>
    <div>
      <ChoreTable :rows="[]" :columns="columns"/>

      <div v-if="selected.length" class="q-mt-md">
        <q-btn @click="markAsDone" style="position: fixed; right: 1rem; bottom: 5rem;"  color="teal" icon="done">Done</q-btn>
      </div>
    </div>
  </section>
  <section v-else>
    <GetAHouse />
  </section>
</template>