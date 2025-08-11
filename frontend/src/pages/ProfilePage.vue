<script lang="ts" setup>

import CustomChart from '@/components/CustomChart.vue';
import { userRequest } from '@/components/userRequest';
import { reactive, ref } from 'vue';
import type { Household, User } from '@/components/interface';
import type { Ref } from 'vue';
// TODO:
// for this you need to figure out the deadlines for the chores.
// on time chart

const userInfo = reactive<{
    household: Household,
    chores: [],
    user: Ref<User>
}>({
    household: {} as Household,
    chores: [],
    user: ref({} as User)
})

const error =  ref('')

userRequest('/user', {method:"GET"})
    .then(res => {
        if (res.error) {
            error.value = res.error
            return
        }
        userInfo.household = res.household
        userInfo.chores = res.chores
        userInfo.user = res.user
    })

</script>

<template>
    <section>
        <section>
            <section>
                <h1 style="text-align: center;">Hello {{ userInfo.user.name }}</h1>
                <section v-if="Object.keys(userInfo.household).length">
                    <h2 style="text-align: center;">{{userInfo.household.name}}</h2>
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

            <section class="statsCont">
                <CustomChart :chores="userInfo.chores" />
                
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