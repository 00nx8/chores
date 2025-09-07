<script setup lang="ts">

import ChoreComponent from './ChoreComponent.vue';
import HiddenButtons from './HiddenButtons.vue';
import type { Chore } from './interface';
import { userRequest } from './userRequest';
import { ref } from 'vue';
import { RouterLink } from 'vue-router';
import PopUp from './PopUp.vue';

// TODO: 
// when selecting done chores either present differnet options or not select them.

const popup = ref(false)

const toDo = ref([])
const done = ref([])
const selectedChores = ref([])
const props = defineProps<{
    household: {[key:string]: string}
}>()
const residents = ref([])
const selectedUserId = ref()

Promise.all([
    userRequest(`/household/${props.household.id}/chore`, {method: "GET"}),
    userRequest(`/household/${props.household.id}/done`, {method: "GET"}),
    userRequest(`/household/${props.household.id}/residents`, {method: "GET"})
]).then(([allRes, doneRes, residentsRes]) => {
    const allChores = allRes.chores
    const doneChoresMap = new Map()

    // Store done chores in a Map for quick lookup and access to `done_on`
    doneRes.chores.forEach(completed => {
        doneChoresMap.set(completed.chore_id, completed)
    })

    done.value = allChores
        .filter(chore => doneChoresMap.has(chore.id))
        .map(chore => ({
            ...chore,
            done_on: doneChoresMap.get(chore.id).done_on
        }))

    toDo.value = allChores.filter(chore => !doneChoresMap.has(chore.id))

    residents.value = residentsRes.residents

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

async function buttonCall(action: string) {
    switch (action) {
        case ('delete'):
            selectedChores.value.forEach(chore => {
                userRequest(`/chore`, {
                    method:"DELETE",
                    body: {
                        choreId: chore.id
                    }
                })
                
            })
            toDo.value = toDo.value.filter(chore => !selectedChores.value.includes(chore) ) 
            done.value = done.value.filter(chore => !selectedChores.value.includes(chore) ) 
            selectedChores.value = []
            break
        case ('re-assign'):
            popup.value = true
            break
        case ('complete'):
                const completionPromises = selectedChores.value.map(async (chore) => {
                    const res = await userRequest(`/chore/${chore.id}`, { method: 'POST' })
                        chore.done_on = res.completion.done_on
                        return chore
                })

                const completedChores = await Promise.all(completionPromises)

                done.value.push(...completedChores)

                toDo.value = toDo.value.filter(
                    toDoChore => !selectedChores.value.some(selected => selected.id === toDoChore.id)
                )

                selectedChores.value = []
                break
    }
}

function assign() {

    selectedChores.value.forEach(chore => {
        userRequest(`/chore/${chore.id}/assign`, {
            method: "POST",
            body: {
                user_id: selectedUserId.value
            }
        })
    })
}

</script>

<template>
    <h2 style="font-size: 1.5rem; text-align: center;">{{props.household.name}}</h2>

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
    <section v-if="toDo.length">
        <ChoreComponent @chore-selected="([chore, isSelected]) => updateChore(chore, isSelected) " :key="chore.id" :status="'todo'" v-for="chore in toDo" :chore="chore" />
    </section>
    <section v-else>
        <p
            v-if="done.length"
            style="text-align: center;"
        >
            Nothing for now, <br /> relax
        </p>
        <p v-else>
            Click the + Button to setup some chores!
        </p>
    </section>

    <section v-if="done.length">
        <h2>done:</h2>
        <ChoreComponent @chore-selected="([chore, isSelected]) => updateChore(chore, isSelected) " :key="chore.id" v-for="chore in done" :status="'done'" :chore="chore" />
    </section>

    <section v-if="!selectedChores.length">
        <RouterLink class="floatingButton toAction center" :to="{ name: 'createChore' }">
            <svg fill='white' viewBox="0 0 24 24">
                <path fill-rule="evenodd" d="M 11 2 L 11 11 L 2 11 L 2 13 L 11 13 L 11 22 L 13 22 L 13 13 L 22 13 L 22 11 L 13 11 L 13 2 Z"></path>
            </svg>
        </RouterLink>
    </section>
    <section v-else>
        <HiddenButtons @action="buttonCall" :buttons="[
            {icon: 'https://api.iconify.design/mdi/check.svg?color=white', action: 'complete'},
            {icon: 'https://api.iconify.design/mdi/account.svg?color=white', action: 're-assign'},
            {icon: 'https://api.iconify.design/mdi/delete.svg?color=white', action: 'delete'},
        ]" />

    </section>
    <!-- TODO: add functionality so it re assigns chore, then closes popup. -->
    <PopUp v-if="popup"
        title="Re-assign"
        @close="popup = false"
        @assign=""
        >
        <select v-model="selectedUserId" name="user">
            <option v-for="resident in residents" :value="resident.id">{{ resident.name }}</option>
        </select>
        <button @click="assign">Re-assign</button>
    </PopUp>

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