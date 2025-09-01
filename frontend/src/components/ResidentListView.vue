<script setup lang="ts">
import { useRouter } from 'vue-router';
import { ref } from 'vue';
const props = defineProps(['residents', "user"])
const router = useRouter()

const action = ref('')

function confirmAction() {

}

</script>

<template>
<section>
    <div v-for="resident in props.residents">
        <p>{{ resident.name }}</p>
        <div>
            <button 
                @click="confirmAction"
                v-if="props.user.id !== resident.id"
                >Evict</button>
            <button @click="router.push(`/user/${resident.id}`)">View</button>
        </div>
        <div v-if="action">asd</div>
    </div>

</section>
</template>

<style scoped>
div {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
div>div {
    gap: 1rem;
}

button {
    background-color: transparent;
    cursor: pointer;
}

button:hover {
    background-color: #4caf4f34;
    transition: all .3s ease-in-out;
}
</style>