import random
from datetime import datetime, timedelta

# TODO:
# create crontab job to run this once every week


def schedule_chores(db, household, chore):
    households = db.session.query(household).all()
    deadline = (datetime.now() + timedelta(days=7)).replace(
        hour=0, minute=0, second=0, microsecond=0
    )

    for house in households:
        residents = house.resident
        chores = db.session.query(chore).filter(chore.household_id == house.id).all()
        
        random.shuffle(chores)

        if not len(chores) or not len(residents):
            continue

        num_residents = len(residents)
        
        for resident, chunk in zip(residents, split_list(chores, num_residents), strict=True):
            for chore_to_assign in chunk:
                chore_to_assign.done_on = None
                chore_to_assign.deadline = deadline
                chore_to_assign.resident_id = resident.id

        db.session.commit()


def split_list(_list, num_chunks):
    n = len(_list)
    base, remainder = divmod(n, num_chunks)
    start = 0
    for i in range(num_chunks):
        # First 'remainder' chunks get 1 extra item
        end = start + base + (1 if i < remainder else 0)
        yield _list[start:end]
        start = end


if __name__ == "__main__":
    pass
