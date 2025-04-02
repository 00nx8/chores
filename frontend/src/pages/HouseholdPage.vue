<script lang='ts' setup>
import { userRequest } from 'src/components/userRequest';
import { onMounted, ref, watch } from 'vue'
import GetAHouse from 'src/components/GetAHouse.vue';
import ChoreTable from 'src/components/ChoreTable.vue';

export interface Chore {
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
const allChores = ref()
const username = ref(localStorage.getItem('username'))

const todos = ref([])
const allDone = ref<Chore[]>([])

const selected = ref<Chore[]>([])

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
  const promises = selected.value.map((chore: Chore) =>
    userRequest(`/chore/${chore.id}`, { method: "POST" })
  );

  Promise.all(promises)
    .then(() => {
      return userRequest(`/household/${household.value.id}/chore/all`, { method: 'GET' })
    })
    .then(response => {
      allChores.value = response.chores;
      todos.value = allChores.value.filter((chore: Chore) => !chore.is_done)
      allDone.value = allChores.value.filter((chore: Chore) => chore.is_done)
      selected.value = []
    })
    .catch(error => console.error('Error updating chores:', error))
}
function fillSelected(newRows: Chore[]) {
  selected.value = newRows
}

onMounted(() => {
  userRequest('/user/household', {
    method: 'GET',
  }).then(response => {
    household.value = response.household
  }).catch(
    error => console.log(error)
  )
})

watch(household, () => {
  const url = `/household/${household.value.id}/chore/all`
  userRequest(url, {
    method: 'GET'
  }).then(response => {
    allChores.value = response.chores
    todos.value = allChores.value.filter((chore: Chore) => chore.is_done !== true)
    allDone.value = allChores.value.filter((chore: Chore) => chore.is_done == true)
  }).catch(err => console.log(err))
})

</script>

<template>
  <section class="q-pa-md" v-if="household">
    <h1 class="text-h5">Welcome {{ username }}</h1>
    <div
        v-if="todos.length || allDone.length"
        class="q-gutter-md"
      >
      <ChoreTable v-on:selected="fillSelected" title="TODO" :rows="todos" :columns="columns"/>
      <ChoreTable title="Done" :rows="allDone" :columns="columns"/>

      <div v-if="selected.length" class="q-mt-md">
        <q-btn @click="markAsDone" style="position: fixed; right: 1rem; bottom: 5rem;"  color="teal" icon="done">Done</q-btn>
      </div>
    </div>
  </section>
  <section v-else>
    <GetAHouse />
  </section>
</template>