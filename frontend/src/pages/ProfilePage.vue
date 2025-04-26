<script lang="ts" setup>

import { userRequest } from '@/components/userRequest';
import { reactive, ref, watch } from 'vue';

const userInfo = reactive({
    household: {},
    chores: [],
    user: ref({})
})

const error =  ref('')
const fileData = ref()
const profilePictureBase64 = ref('')

function uploadPicture() {

    // TODO:
    // sending the profile picture across is too large for the request appearantly
    // find an alternative, myb stream it (god save me)
    
    // More importantly: finish thee overview then u can get started on profile pictures

    error.value = ''
    if (!fileData.value) {
        error.value = "No file data found"
        return
    }
    const reader = new FileReader()
    reader.onload = () => {
        const byteData = reader.result

        const byteArray = new Uint8Array(byteData as ArrayBuffer)
        let binary = ''
        byteArray.forEach(byte => binary += String.fromCharCode(byte))
        const base64String = btoa(binary)

        userRequest('/user/profile_picture', {
            method: "POST",
            body: {
                profile_picture: base64String
            }
        })
        profilePictureBase64.value = base64String
        userInfo.user.profile_picture = base64String
    }

    reader.readAsArrayBuffer(fileData.value)
}

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
    <section v-if="error">
        <h1>Hello, something went wrong : (</h1>
        <p>{{ error }}</p>
    </section>
    <section v-else>
        <section v-if="userInfo.user.profilePicture || profilePictureBase64">
            <img :src="userInfo.user.profilePicture" alt="">
            <section>
                <h1>Hello {{ userInfo.user.name }}</h1>
        
                <h3>You are part of:</h3>
                <h5>{{ userInfo.household.name }}</h5>
            </section>
        </section>
        <section v-else>
            <form class="" @submit.prevent="uploadPicture">
                <fieldset class="flex space-evenly align-center">
                    <input @change="(e: any) => fileData = e.target.files[0]!" type="file">
                    <button>upload</button>
                </fieldset>
            </form>
            <section>
                <h1>Hello {{ userInfo.user.name }}</h1>
        
                <h3>You are part of:</h3>
                <h5>{{ userInfo.household.name }}</h5>
            </section>
        </section>
        
    </section>
</template>

<style scoped>
fieldset {
    border: 1px solid rgba(128, 128, 128, 0.295);
    padding: .25rem .5rem;
    border-radius: .25rem;
}
fieldset > button {
    padding: .25rem .75rem;
}
</style>