<script lang="ts" setup>

import { userRequest } from '@/components/userRequest';
import { reactive, ref, watch } from 'vue';
import type { Household, Chore, User } from '@/components/interface';
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

userRequest('/database', {method:'GET'})

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
                <h1>Hello {{ userInfo.user.name }}</h1>
                <section v-if="Object.keys(userInfo.household).length">
                    <p>hi, youre not homeless</p>
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