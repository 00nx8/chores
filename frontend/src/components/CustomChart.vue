<script setup lang="ts">
import { ref, computed } from 'vue';
import { userRequest } from './userRequest';

const props = defineProps(['chores'])

const chartBody = ref()

const chartTextLeft = 'Chores done'
const chartTextBottom = 'Date'

const displayedMonths = ref({})
props.chores.forEach(chore => {
    const dateObj = new Date(chore.done_on)

    const monthNumber = (dateObj.getMonth() + 1).toString().padStart(2, '0')

    if (Object.keys(displayedMonths.value).includes(monthNumber)) {
        displayedMonths.value[monthNumber] += 1
    } else {
        displayedMonths.value[monthNumber] = 1
    }
})

const maxCount = Math.max(...Object.values(displayedMonths.value) as [number])
const countRange = Array.from({ length: maxCount + 1 }, (_, i) => maxCount - i);
const chartHeight = 10

const scale = computed(() => {
  return maxCount > 0 ? chartHeight / maxCount : 0
})

</script>

<template>
    <section class="container">
        <h2>Chart</h2>
        <section ref="chartBody" class="chartBody">
            <div class="bars">
                <div
                    v-for="(month, i) in Object.keys(displayedMonths)"
                    class="bar"
                    :style="{left: `${i * 2}rem`, height: `${displayedMonths[month] * scale}rem`}"
                 >{{displayedMonths[month]}}</div>
            </div>
            <div>
                <div class="labelLeft">
                    {{ chartTextLeft }}
                </div>
            </div>
            <div class="keys">
                <p 
                    :key="i" v-for="i in countRange"
                    :style="{position: 'absolute', bottom: `${i * scale * .85}rem`}"
                >{{ i }}</p>
            </div>
            <div class="labelBottom">
                {{ chartTextBottom }}
            </div>
            <div class="borders">
                <hr class="side">
                <hr class="bottom">
            </div>
        </section>

    </section>
</template>

<style scoped>
.keys {
    position: absolute;
    bottom: 0;
    left: -1rem;
    height: 100%;
    width: 1rem;
}
.bars  {
    position: relative;
    height: 10rem;
}
.bar {
    position: absolute;
    bottom: 0;
    height: 9rem;
    background-color: red;
    width: 1.2rem;
}
.container {
    width: 100%;
    /* background-color: grey; */
}
.borders { 
    position: absolute;
    top:0;
    bottom: 0;
    height:10rem;
    width: 100%;
}
.labelBottom {
    position: absolute;
    bottom: -1.5rem;
    left: 0;
}
.labelLeft {
    position: absolute;
    bottom: 0;
    left: -2.5rem;
    writing-mode: sideways-lr;
}

.bottom {   
    display:block;
    width: 100%;
    height: 1px;
    border: none;
    background-color: white;
}


.side {
    display:block;
    height: 100%;
    width: 1px;
    border: none;
    background-color: white;
}

.chartBody {
    position: relative;
    margin: 1rem;
    min-height: 1rem;
    height: 10rem;
    max-height: 10rem;

}

</style>