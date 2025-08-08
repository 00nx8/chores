<script setup lang="ts">

import ChoreComponent from './ChoreComponent.vue';
import HiddenButtons from './HiddenButtons.vue';

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
const selectedChores = ref([])
const props = defineProps<{
    household: {[key:string]: string}
}>()

userRequest(`/household/${props.household.id}/chore`, {
    method: 'GET'
}).then(res => {
    toDo.value = res.chores.filter((chore: Chore) => chore.is_done == false)
    done.value = res.chores.filter((chore: Chore) => chore.is_done == true)
})

function updateChore(chore: Chore, isSelected: boolean) {
    if (isSelected) {
        selectedChores.value.push(chore)
    } else {
        if (selectedChores.value.includes(chore)) {
            selectedChores.value.splice(selectedChores.value.indexOf(chore), 1)
        }
    }
}

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
    <section>
        <ChoreComponent @chore-selected="([chore, isSelected]) => updateChore(chore, isSelected) " v-for="chore in toDo" :chore="chore" />
    </section>

    <section v-if="!selectedChores.length">
        <RouterLink class="floatingButton toAction center" :to="{ name: 'createChore' }">
            <svg fill='white' viewBox="0 0 24 24">
                <path fill-rule="evenodd" d="M 11 2 L 11 11 L 2 11 L 2 13 L 11 13 L 11 22 L 13 22 L 13 13 L 22 13 L 22 11 L 13 11 L 13 2 Z"></path>
            </svg>
        </RouterLink>
    </section>
    <section v-else>
        <HiddenButtons :buttons="[{icon: 'complete', action: 'complete'}, {icon: 'person', action: 're-assign'}, {icon: 'delete', action: 'delete'}]" />
    </section>
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