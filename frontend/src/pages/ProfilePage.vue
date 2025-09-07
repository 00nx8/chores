<script lang="ts" setup>
import CustomChart from '@/components/CustomChart.vue';
import { userRequest } from '@/components/userRequest';
import { ref, watch } from 'vue';
import type { Household, User } from '@/components/interface';
import ResidentListView from '@/components/ResidentListView.vue';
import { useRoute, useRouter } from 'vue-router';
import HiddenButtons from '@/components/HiddenButtons.vue';
import Cookies from 'universal-cookie';

const route = useRoute()
const router = useRouter()

const user = ref<User>({} as User)
const household = ref<Household>({} as Household)
const chores = ref([])
const residents = ref([])

const cookies = new Cookies()

const fetchUserData = async () => {
    const url = route.params.id ? `/user/${route.params.id}` : '/user'
    const res = await userRequest(url, {method:"GET"})
    if (res.error) {
        router.push('/user')
        return
    }
    
    console.log('asd')
    household.value = res.household
    user.value = res.user

    const [doneRes, residentRes] = await Promise.all([
            userRequest(`/household/${household.value.id}/done`, {method: "GET"}),
            userRequest(`/household/${household.value.id}/residents`, {method: "GET"})
    ])

    chores.value = doneRes.chores
    residents.value = residentRes.residents
}

watch(
  () => route.params.id,
  () => {
    fetchUserData()
  },
  { immediate: true }
)

function buttonCall( action: string ) {
    switch (action) {
        case('Sign out'):
            cookies.remove('token')
            router.push('/')
        case('Leave household'):

            localStorage.removeItem('household')

            userRequest('/user/household', {
                method: 'PUT',
                body: {
                    household_id: 0
                }
            }).then(res => {
                household.value = null
            })
            router.push('/')
    }
}

</script>

<template>
    <section>
        <section>
            <section>
                <h1 style="text-align: center;">Hello {{ user.name }}</h1>
                <section v-if="Object.keys(household).length">
                    <h2 style="text-align: center;">{{household.name}}</h2>
                    <section v-if="chores.length" class="statsCont">
                        <CustomChart 
                            :title="'Chores done'"
                            :tagLeft="'No. of Chores'"
                            :tagBottom="'Month'"
                            :chores="chores"
                            />
                    </section>
                    <section style="padding-top: 1rem;">
                        <h2>Overview</h2>
                        <section>
                            <h3>Residents</h3>
                            <ResidentListView :residents="residents" :user="user"/>       
                        </section>

                    </section>
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
        <HiddenButtons @action="buttonCall" :buttons="[
            {icon: 'https://api.iconify.design/mdi/logout.svg?color=white', action: 'Sign out'},
            {icon: 'https://api.iconify.design/mdi/home-export-outline.svg?color=white', action: 'Leave household'}
        ]" />
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