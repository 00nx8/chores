<script setup lang="ts">

import CustomInput from '@/components/CustomInput.vue';
import { userRequest } from '@/components/userRequest';
import { reactive, ref } from 'vue';
import ErrorText from '@/components/ErrorText.vue';
import { useRouter } from 'vue-router';
const router = useRouter()

const choreInfo = reactive({
    name: '',
    description: '',
    doing_it: 0
})

const errors = ref([])
const residents = ref([])

const household = JSON.parse(localStorage.getItem('household'))

userRequest(`/household/${household.id}/residents`, {
    method: "GET"
}).then(res => {
    residents.value = res.residents
})

function validateForm() {
    console.log('this runs ??')
    errors.value = []
    
    if (!choreInfo.name || !choreInfo.doing_it || !choreInfo.description) {
        errors.value.push('Name, description and user are required')
        return
    }

    userRequest('/chore', {
        method: "POST",
        body: {
            ...choreInfo,
            household_id: household.id
        }
    }).then(res => {
        console.log(res)
        router.push('/')
    })

}

</script>

<template>
    <h1>create Chore</h1>
    <form @submit.prevent="validateForm">
        <CustomInput 
            name="Name"
            type="text"
            v-model="choreInfo.name"
        />
        <CustomInput 
            name="Description"
            type="text"
            v-model="choreInfo.description"
        />
        <label>
            Doing it
            <select name="doing_it" v-model="choreInfo.doing_it">
                <option v-for="resident in residents" :value="resident.id">{{resident.name}}</option>
            </select>
        </label>

        <button type="submit">
            create
        </button>
    </form>
    <ErrorText v-if="errors.length" :errors="errors" />
</template> 