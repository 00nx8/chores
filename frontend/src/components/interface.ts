export interface Chore {
    id: number,
    description: string,
    name: string,
    is_done: boolean
}

export interface Household {
    id: Number,
    name: string
}

export interface User {
    id: Number,
    name: string,
    household_id: number
}