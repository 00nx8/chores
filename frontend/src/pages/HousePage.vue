<script setup lang="ts">
import { userRequest } from '@/components/userRequest';
import HouseholdView from '@/components/HouseholdView.vue';
import CreateHousehold from '@/components/CreateHousehold.vue';
import { ref } from 'vue';

const loading = ref(true)

const userHousehold = ref()
const loadingProgress = ref(0)

loadingProgress.value += 10

userRequest("/user/household", {
    method:"GET"
}).then(res => {
    loadingProgress.value = 90
    loading.value = false
    associateHousehold(res.household)
})

function associateHousehold(household: object) {
    userHousehold.value = household
    localStorage.setItem('household', JSON.stringify(household))
}

</script>

<template>
    <h1 style="text-align: center; font-size: 1rem;">Household</h1>
    <section v-if="loading">
        <span class="loading">
            Loading...
            <hr :style="{width: `${loadingProgress}%`}">
        </span>
    </section>

    <section v-else>
        <section v-if="userHousehold">
            <HouseholdView :household="userHousehold" />
        </section>
        <section v-else>
            <CreateHousehold @receivedHousehold="(household) => associateHousehold(household)" />
        </section>
    </section>
</template>