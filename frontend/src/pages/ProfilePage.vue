<script lang="ts" setup>

import CustomChart from '@/components/CustomChart.vue';
import { userRequest } from '@/components/userRequest';
import { ref } from 'vue';
import type { Household, User } from '@/components/interface';

// TODO:
// for this you need to figure out the deadlines for the chores.
// on time chart

const user = ref<User>({} as User)
const household = ref<Household>({} as Household)
const chores = ref([])

const error =  ref('')

userRequest('/user', {method:"GET"})
.then(res => {
    if (res.error) {
        error.value = res.error
        return
    }
    
    household.value = res.household
    user.value = res.user

    userRequest(`/household/${household.value.id}/done`, {method: "GET"}).then(res => {
        chores.value = res.chores
    })

})


</script>

<template>
    <section>
        <section>
            <section>
                <h1 style="text-align: center;">Hello {{ user.name }}</h1>
                <section v-if="Object.keys(household).length">
                    <h2 style="text-align: center;">{{household.name}}</h2>
                </section>
                <section v-else class="noHouseholdCont">
                    You are not part of a household. <br>Join or create one!
                    <RouterLink :to="{name: 'household'}">
                        <button>
                            Household
                        </button>
                    </RouterLink>
                </section>
            </section>

            <section v-if="chores.length" class="statsCont">
                <CustomChart :chores="chores" />
                
            </section>
        </section>
        
    </section>
</template>

<style scoped>
.noHouseholdCont {
    height: 80dvh;
    display:flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    text-align: center;
    gap: 1rem;
}

a:hover {
    background-color: transparent;
}

fieldset {
    border: 1px solid rgba(128, 128, 128, 0.295);
    padding: .25rem .5rem;
    border-radius: .25rem;
}
fieldset > button {
    padding: .25rem .75rem;
}
</style>