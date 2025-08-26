<script lang="ts" setup>
import { ref } from 'vue';
const props = defineProps(['chore', 'status']);

// chroes to be displayed
const chore = ref(props.chore)
// emit this when ever a chore has its input selected
const emit = defineEmits(['choreSelected'])
// value of the checkbox
const isSelected = ref(false)

// extract the month from the date object
const deadline = new Date(props.chore.deadline).toLocaleDateString('en-GB', {
        day: '2-digit',
        month: 'short'
    })
const doneOn = new Date(props.chore.done_on).toLocaleDateString('en-GB', {
        day: '2-digit',
        month: 'short'
    })
</script>

<template>
    <div class="cardWrapper">
        <div>
            <div class="cardHeader">
                <div class="checkboxContainer">
                    <input @change="emit('choreSelected', [chore, isSelected])" v-model="isSelected" type="checkbox" name="selectedChore" id="">
                </div>
                <div class="choreDetails">
                    <h2>{{ chore.name }}</h2>
                    <section>
                        <p>{{ props.status }}</p>
                    </section>
                </div>
            </div>
            <div class="cardBody">
                <p>{{ chore.description }}</p>
                <p>Assigned to: {{ chore.resident.name }}</p>
                <p v-if="status == 'done'">Done on:{{ doneOn }}</p>
                <p v-else>Deadline: {{ deadline }}</p>
            </div>
        </div>
    </div>
</template>

<style scoped>


.cardWrapper {
    background-color: var(--color-border);
    padding: .5rem;
    margin-bottom: .5rem;
    border-radius: .5rem;

    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.cardHeader {
    background-color: var(--vt-c-black-soft);
    border-radius: .5rem;
    padding-inline: .5rem;
    display: flex;
    align-items: center;
    gap: 1rem;
}

.choreDetails {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.choreDetails > section {
    text-align: right;
}
.choreDetails > section > h3 {
    font-weight: bolder;
    font-size: .8rem;
}

.cardHeader > h2 {
    font-size: 1rem;   
}

.cardBody {
    border: 1px solid var(--color-background);
    padding: .5rem;
    border-radius: .5rem;
}

</style>