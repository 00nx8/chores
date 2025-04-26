<script setup lang="ts">
import CustomInput from '@/components/CustomInput.vue';
import { reactive, ref } from 'vue';
import { RouterLink } from 'vue-router';
import { setUserInfo, userRequest } from '@/components/userRequest';
import ErrorText from '@/components/ErrorText.vue';
import { useRouter } from 'vue-router';

const router = useRouter()

const userInfo = reactive({
    username: '',
    password: '',
    repeatPassword: ''
})

const errors = ref([])

function validateForm() {
    errors.value = []
    if (!userInfo.username || !userInfo.password || !userInfo.repeatPassword) {
        errors.value.push('All fields are required')
        return
    }

    if (userInfo.password !== userInfo.repeatPassword) {
        errors.value.push('Password and Repeat password must match')
        return
    }

    userRequest('/register', {
        method: 'POST',
        body: {
            username: userInfo.username,
            password: userInfo.password
        }
    }).then(res => {
        if (res.error) {
            errors.value.push(res.error) 
            return
        }
        router.push('/login')
    })
}

</script>

<template>
    <h1>register</h1>
    <form @submit.prevent="validateForm">
        <CustomInput 
            name="username" 
            v-model="userInfo.username"
            type='text'/>
        <CustomInput
            name="password" 
            v-model="userInfo.password"
            type='password'/>
        <CustomInput 
            name="repeat Password" 
            v-model="userInfo.repeatPassword"
            type='password'/>
        <section class="gap-md space-evenly">
            <button type="submit">
                submit
            </button>
            <RouterLink :to="{name: 'login'}" class="toAction">
                login
            </RouterLink>
        </section>
        <ErrorText v-if="errors.length" :errors="errors"/>
    </form>


</template>