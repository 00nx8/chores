<script setup lang="ts">
import { reactive, ref } from 'vue';
import CustomInput from './CustomInput.vue';
import { userRequest } from './userRequest';
import ErrorText from './ErrorText.vue';

// send household object back to parent component when ever it was recieved from backend
const emit = defineEmits(['receivedHousehold'])

// switch between creating/joining household
const creating = ref(null)

// used to display multiple errors at the same time.
const errors = ref([])

const householdInformation = reactive({
    name: '',
    password: '',
    repeatPassword: ''
})

function makeRequest(url: string) {
    // send a request to the given url with the filled in information about household
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
    // checks if all information for the household is provided/correct then sends the request.
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
    // checks if all information for the household is provided/correct then sends the request.

    if (!householdInformation.name || !householdInformation.password ) {
        errors.value.push('All fields are required.')
        return
    }
    makeRequest('/user/household')

}


</script>

<template>
    <section :class="creating == null ? 'introContUndecided': ''">
        <p v-if="creating == null">Would you like to join or create a household?</p>
        <section class="buttons">
            <button
                @click="() => creating = true"
            >
                Create
            </button>
            <button 
                @click="() => creating = false"
            >
                Join
            </button>
        </section>

    </section>

    <section v-if="creating !== null">
        <section v-if="creating">
            <form @submit.prevent="createHousehold">
                <CustomInput
                    name="Choose a name"
                    type="text"
                    v-model="householdInformation.name"  
                />
                <CustomInput
                    name="set a password"
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
    </section>
    <ErrorText v-if="errors.length" :errors="errors"/>
</template>


<style scoped>
.introContUndecided {
    display: flex;
    height: 80dvh;
    flex-direction: column;
    text-align: center;
    gap:1rem;
    justify-content: center;
    align-items: center;
}

.buttons {
    display: flex;
    justify-content: center;
}
.buttons > button:last-child {
    margin-left: 1rem;
}
</style>