<script setup lang="ts">
import { onMounted, ref } from 'vue';

const props = defineProps<{
    buttons: Array<{[key: string]: string}>
}>()

const burgerButton = ref()

const buttonRefs = ref([])
const buttons = ref(props.buttons)
const buttonClass = ref('hiddenButton')

onMounted(() => {
    // get the height + 1rem for gap 
    // and then use those positions to position the rest of the buttons.
    const rect = burgerButton.value.getBoundingClientRect();
});
function changeButtonStatus() {
    buttonClass.value = buttonClass.value !== 'hiddenButton' ? 'hiddenButton' : 'shownButton'

    const rect = burgerButton.value.getBoundingClientRect()
    

    buttonRefs.value.forEach(button => {
        button.style.left = `${rect.left}px`;
        button.style.top = `${rect.top}px`;
    })


    for (let i = 0; i < buttonRefs.value.length; i++) {
        const button = buttonRefs.value[i]
        
        const offset = (i + 1) * -4;
// figure out a way to reverse this animation,
// at the moment the buttons just dissapear onnce the burger is pressed again
// coZ the hiddenBUtton class has display None, prolly all css has to go thru js
// gn <3
        button.animate(
            [
                { top: `${rect.top}px` },
                { top: `${rect.top + offset * 16}px` }
            ],
            {
                duration: 400,
                fill: 'forwards',
                easing: 'ease-out'
            }
        );
    }
}

</script>

<template>
    <section class="buttonContainer" >
        <button
            @click="changeButtonStatus"
            ref="burgerButton"
            class="mainBurger toAction center"
            >
            <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path fill-rule="evenodd" clip-rule="evenodd" d="M4 5C3.44772 5 3 5.44772 3 6C3 6.55228 3.44772 7 4 7H20C20.5523 7 21 6.55228 21 6C21 5.44772 20.5523 5 20 5H4ZM7 12C7 11.4477 7.44772 11 8 11H20C20.5523 11 21 11.4477 21 12C21 12.5523 20.5523 13 20 13H8C7.44772 13 7 12.5523 7 12ZM13 18C13 17.4477 13.4477 17 14 17H20C20.5523 17 21 17.4477 21 18C21 18.5523 20.5523 19 20 19H14C13.4477 19 13 18.5523 13 18Z" fill="#fff"/>
            </svg>
        </button>
        <p class="burgerButtonText">Options</p>
    </section>

    <button
        v-for="(button, idx) in buttons"
        :key="idx"
        :class="buttonClass"
        :ref="el => buttonRefs[idx] = el"
    >
        <img :src="button.icon" :alt="button.action" srcset="">
        <p class="burgerButtonText">{{ button.action }}</p>
    </button>
</template>


<style>
.hiddenButton {
    display: None;
    position: fixed;
    bottom: 3rem;
    right: 1rem;
    transition: all 1s ease;
}

.shownButton {
    display: block;
    position: fixed;
    transition: all 1s ease;
}

button {
    border-radius: 50%;
    height: 3rem;
    width: 3rem;
    position: fixed;
    bottom: 3rem;
    right: 1rem;
    transition: all 1s ease;
}

.mainBurger {
    border-radius: 50%;

    animation: spinZoom 1s ;
}

.burgerButtonText {
    opacity: 0;
    position: absolute;
    transition: all 1s ease;
}

@keyframes spinZoom {
    0% {
        transform: rotate(0deg) scale(1);
    } 50% {
        transform: rotate(360deg) scale(1.5);
    } 100% {
        transform: rotate(720deg) scale(1);
    }
}

</style>