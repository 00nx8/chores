<script lang="ts" setup>
import { reactive, ref } from 'vue';
import { userRequest } from '@/components/userRequest';
import { RouterLink, useRouter } from 'vue-router';
import { setUserInfo } from '@/components/userRequest';
import CustomInput from '@/components/CustomInput.vue';
import ErrorText from '@/components/ErrorText.vue';
import Cookies from 'universal-cookie';
const router = useRouter()
const cookies = new Cookies()

const userInfo = reactive({
    password: '',
    username: ''
})

const errors = ref([])

function validateForm() {
    errors.value = []
    if (!userInfo.username || !userInfo.password) {
        errors.value.push('Please supply a username and password') 
        return
    }

    userRequest('/login', {
        method: 'POST',
        body: {
            ...userInfo
        }
    }).then(res => {
        if (res.error && !errors.value.includes(res.error)) {
            errors.value.push(res.error)
            return
        }
        cookies.set('token', res.token)
        router.push('/')
    })



}

</script>

<template>
    <section>
        <h1 style="font-size: 2rem; text-transform: capitalize;">login</h1>
        <form @submit.prevent="validateForm">
            <CustomInput 
                type="text"
                name="username"
                v-model="userInfo.username"
            />
            <CustomInput 
                type="password"
                name="password"
                @valueDefined="(inputValue: string) => setUserInfo(userInfo, 'password', inputValue)"
                v-model="userInfo.password"
            />
            <section class="space-evenly flex-wrap gap-md">
                <button type="submit">
                    Submit
                </button>
                <RouterLink class="toAction" :to="{name: 'register'}">Register</RouterLink>
            </section>
        </form>

        <ErrorText v-if="errors.length" :errors="errors" />
    </section>
</template>