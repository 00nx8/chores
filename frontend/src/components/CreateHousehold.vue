<script setup lang="ts">
import { reactive, ref } from 'vue';
import CustomInput from './CustomInput.vue';
import { setUserInfo, userRequest } from './userRequest';
import ErrorText from './ErrorText.vue';

const emit = defineEmits(['receivedHousehold'])

const creating = ref(false)

const errors = ref([])
const householdInformation = reactive({
    name: '',
    password: '',
    repeatPassword: ''
})

function makeRequest(url: string) {
    userRequest(url, {
        method: 'POST',
        body: {
            ...householdInformation
        }
    }).then(res => {
        if (res.error) {
            errors.value.push(res.error)
            return
        }
        emit('receivedHousehold', res.household)
    })
}

function createHousehold() {
    console.log(householdInformation)
    errors.value = []
    if (!householdInformation.name || !householdInformation.password || !householdInformation.repeatPassword) {
        errors.value.push('All fields are required.')
    }

    if (householdInformation.password != householdInformation.repeatPassword) {
        errors.value.push('Password and repeat password must be the same.')
    }

    if (errors.value.length) {
        return
    }

    makeRequest('/household')
}

function joinHousehold() {
    if (!householdInformation.name || !householdInformation.password ) {
        errors.value.push('All fields are required.')
        return
    }
    makeRequest('/user/household')

}


</script>

<template>
    <section class="space-evenly gap-md">
        <button 
            @click="() => creating = true"
            :class="creating ? 'selected' : ''"
        >
            Create
        </button>
        <button 
            @click="() => creating = false"
            :class="!creating ? 'selected' : ''"
        >
            Join
        </button>
    </section>

    <section v-if="creating">
        <form @submit.prevent="createHousehold">
            <CustomInput
                name="name"
                type="text"
                v-model="householdInformation.name"  
            />
            <CustomInput
                name="password"
                type="password"
                v-model="householdInformation.password"
            />
            <CustomInput
                name="repeat Password"
                type="password"
                v-model="householdInformation.repeatPassword"
            />
            <button type="submit">
                create
            </button>
        </form>
    </section>
    <section v-else>
        <form @submit.prevent="joinHousehold">
            <CustomInput
                name="name"
                type="text"
                v-model="householdInformation.name"
            />
            <CustomInput
                name="password"
                type="password"
                v-model="householdInformation.password"
            />
            <button>
                join
            </button>
        </form>
    </section>
    <ErrorText v-if="errors.length" :errors="errors"/>
</template>