<script setup lang="ts">
import { userRequest } from './userRequest';
import { ref } from 'vue';
import { RouterLink } from 'vue-router';
interface Chore {
    id: number,
    description: string,
    name: string,
    is_done: boolean
}

const toDo = ref([])
const done = ref([])

const props = defineProps<{
    household: {[key:string]: string}
}>()

userRequest(`/household/${props.household.id}/chore`, {
    method: 'GET'
}).then(res => {
    console.log(res)
    toDo.value = res.chores.filter((chore: Chore) => chore.is_done == false)
    done.value = res.chores.filter((chore: Chore) => chore.is_done == true)
})

</script>

<template>
    <h2 style="font-size: 1rem; text-align: center;">{{props.household.name}}</h2>
    
    <section class="flex space-evenly" style="margin-bottom: 2rem;">
        <section style="text-align: center;">
            <h4>Outstanding:</h4>
            <h2>{{ toDo.length }}</h2>
        </section>
        <section style="text-align: center;">
            <h4>Done:</h4>
            <h2>{{done.length}}</h2>
        </section>
    </section>

    <h2>todo:</h2>
    <table style="width: 100%; text-align: left; table-layout: fixed;">
        <thead>
            <tr>
            <th>#</th>
            <th>Name</th>
            <th>Description</th>
            <th>Doing it</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="(chore, i) in toDo" :key="i">
            <td>{{ i + 1 }}</td>
            <td>{{ chore.name }}</td>
            <td style="word-wrap: break-word; white-space: normal; vertical-align: top;">
                {{ chore.description }}
            </td>
            <td>{{ chore.doing_it }}</td>
            </tr>
        </tbody>
    </table>

    <RouterLink class="floatingButton toAction center" :to="{ name: 'createChore' }">
        <svg fill='white' viewBox="0 0 24 24">
            <path fill-rule="evenodd" d="M 11 2 L 11 11 L 2 11 L 2 13 L 11 13 L 11 22 L 13 22 L 13 13 L 22 13 L 22 11 L 13 11 L 13 2 Z"></path>
        </svg>
    </RouterLink>
</template>

<style scoped>
tr > th:first-child {
  width: 15px;
}
tr > th:nth-child(2) {
    width: 4rem;
    word-wrap: break-word;
}
tr > th:nth-child(3) {
    width: 40%;
}

@media screen and (max-width: 300px) {
    tr > th:last-child,
    tr > td:last-child {
        display: none;
    }
}

</style>