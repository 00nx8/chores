<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
const props = defineProps(['title', 'para'])
const emit = defineEmits(['close'])

const popupRef = ref()

function handleClickOutsude(e) {
    if (popupRef.value && !popupRef.value.contains(e.target)) {
        emit('close')
    }
}
</script>
<template>
    <section @click="handleClickOutsude">
        <div  ref="popupRef">
            <h2>{{ props.title }}</h2>
            <p>{{ props.para }}</p>
    
            <slot>
    
            </slot>
        </div>
    </section>
</template>


<style scoped>
section {
    position: fixed;
    top: 0;
    left: 0;
    background-color: rgba(0, 0, 0, 0.61);
    height: 100dvh;
    width: 100dvw;
    display: flex;
    justify-content: center;
    align-items: center;
}

div {
    background-color: white;
    color: black;
    padding: 1rem 2rem;
    border-radius: 2rem;
}


</style>