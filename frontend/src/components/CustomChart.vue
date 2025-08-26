<script setup lang="ts">
import { ref, computed } from 'vue';
import { userRequest } from './userRequest';

const props = defineProps(['chores'])

const chartTextLeft = 'Chores done'
const chartTextBottom = 'Date'

const displayedMonths = ref({
    '01': 4,
    '02': 7,
    '04': 2,
    '05': 2,
    '06': 5,
    '07': 4,
    '08': 2
})

// const displayedMonths = ref({})
// chores is a list of objects with information about when a chore was done. 
// this adds up how many chores were done in a given month
props.chores.forEach(chore => {
    const dateObj = new Date(chore.done_on)

    const monthNumber = (dateObj.getMonth() + 1).toString().padStart(2, '0')

    if (Object.keys(displayedMonths.value).includes(monthNumber)) {
        displayedMonths.value[monthNumber] += 1
    } else {
        displayedMonths.value[monthNumber] = 1
    }
})

// gets the highest amount in the dataset
const maxCount = Math.max(...Object.values(displayedMonths.value) as [number])
// generates a list from 1 to the highest amount
let countRange = Array.from({ length: maxCount }, (_, i) => maxCount - i).reverse()

// if the number keys generated is higher then the allowed amount, it removes the excess from low->high
const MAX_DISPLAYED_KEYS = 8
let excess = 0
if ( countRange.length > MAX_DISPLAYED_KEYS) {
    excess = MAX_DISPLAYED_KEYS - countRange.length
    if (excess < 0){
        countRange.splice(0, excess * -1)
    }
}

const CHART_HEIGHT = 10

// used to determine the height of bars/position of keys on the chart.
const scale = CHART_HEIGHT / countRange.length
// TODO
// if the value in the month is lower than the excess i.e val - excess = <0 then the height will be determined with a negative integer.
// this leads to some funy graphs where 2 is higher than 7
// also if the value displayed on theg graph is lower than the lowest number displayed, how should it be done ?
</script>

<template>
    <section class="container">
        <h2>Chart</h2>  
        <section class="chartBody">
            <div class="bars">
                <div
                    v-for="(month, i) in Object.keys(displayedMonths)"
                    class="bar"
                    :style="{left: `${i * 2}rem`, height: `${(displayedMonths[month] - -excess) * scale}rem`}"
                 >{{displayedMonths[month]}}</div>
            </div>
            <div>
                <div class="labelLeft">
                    {{ chartTextLeft }}
                </div>
            </div>
            <div class="keys">
                <p 
                    :key="i" v-for="val, i in countRange"
                    :style="{position: 'absolute', bottom: `${i * scale}rem`}"
                >{{ val }}</p>
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
    min-height: .5rem;
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