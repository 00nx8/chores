<script setup lang="ts">
import { nextTick, onMounted, ref } from 'vue';

const props = defineProps<{
    buttons: Array<{[key: string]: string}>
}>()

const burgerButton = ref()

const labelRefs = ref([])
const buttonRefs = ref([])
const buttons = ref(props.buttons)
const buttonClass = ref('hiddenButton')

const emit = defineEmits(['action'])

function animateButtons(rect: DOMRect, direction: 'show' | 'hide') {
    for (let i = 0; i < buttonRefs.value.length; i++) {
        const button = buttonRefs.value[i]
        const label = labelRefs.value[i]

        const offset = (i + 1) * -4 * 16
        const fromTop = direction === 'show' ? rect.top : rect.top + offset
        const toTop = direction === 'show' ? rect.top + offset : rect.top

        label.style.top = toTop + 13 + 'px'
        label.style.right = rect.left

        button.animate(
            [
                { top: `${fromTop}px` },
                { top: `${toTop}px` }
            ],
            {
                duration: 400,
                fill: 'forwards',
                easing: direction === 'show' ? 'ease-out' : 'ease-in'
            }
        )
    }
}

function changeButtonStatus() {
    buttonClass.value = buttonClass.value !== 'hiddenButton' ? 'hiddenButton' : 'shownButton'
    const rect = burgerButton.value.getBoundingClientRect()
    if (buttonClass.value !== 'hiddenButton') {
        animateButtons(rect, 'show')
    } else {
        animateButtons(rect, 'hide')
    }
}

function showLabel(i: number) {
    const label = labelRefs.value[i]

    label.animate(
        [
            { right: '0rem', opacity: 0 },
            { right: '5rem', opacity: 100 }
        ],
        {
            duration: 400,
            fill: 'forwards',
            easing: 'ease-in-out'
        }
    )
}

function hideLabel(i: number) {
    const label = labelRefs.value[i]
    
    label.animate(
        [
            { right: '5rem', opacity: 100 },
            { right: '0rem', opacity: 0 }
        ],
        {
            duration: 400,
            fill: 'forwards',
            easing: 'ease-in-out'
        }
    )
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
        @click="emit('action', button.action)"
        @mouseenter="() => showLabel(idx)"
        @mouseleave="() => hideLabel(idx)"
    >
        <img :src="button.icon" :alt="button.action" srcset="">
        <p
            :ref=" el => labelRefs[idx] = el"
            class="burgerButtonText">{{ button.action }}  
        </p>
    </button>
</template>


<style>
.hiddenButton {
    opacity: 0;
    z-index: -100;
    position: fixed;
    bottom: 3rem;
    right: 1rem;
    transition: all 1s ease;
}

.shownButton {
    opacity: 100;
    display: block;
    position: fixed;
    transition: all 1s ease;
    z-index: 200;
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
    z-index: 300;
}

.burgerButtonText {
    padding: .2rem .4rem;
    border-radius: 10px;
    opacity: 0;
    position: fixed;
    transition: all 1s ease;
    background-color: #4CAF50;
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