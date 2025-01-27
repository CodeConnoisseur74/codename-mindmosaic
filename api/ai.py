import marvin

from .models import StudyPlanInput, StudyPlanOutput


@marvin.fn
def create_study_plan(input_data: StudyPlanInput) -> StudyPlanOutput:
    """Generate a study plan with daily activities based on the provided input
    data.
    Input:
    - `goals`: A single specific goal for the study plan
    (e.g., "Learn Python OOP concepts").
    - `time_per_day`: The total study time available per day in minutes (e.g., 60).
    - `preferred_topics`: A list of topics preferred for study
    (e.g., ["Python", "OOP"]).
    Output:
    - List of week days, where each day has one or more activities depending on
    time effort per day.
    Ensure:
    - Activities are diverse and derived from `preferred_topics`.
    - The total time for activities in each day does not exceed `time_per_day`.
    - Output is concise and actionable, avoiding redundant information.
        @@ -68,17 +42,17 @@
    """


if __name__ == '__main__':
    plan = create_study_plan(
        StudyPlanInput(
            goals='Learn Python OOP concepts',
            days=7,
            time_per_day=60,
            preferred_topics=['Python', 'OOP'],
        )
    )
    for week_day in plan.study_plan:
        print(f'Day {week_day.day}:')
        for activity in week_day.activities:
            print(f' - {activity.activity} ({activity.time_minutes} minutes)')
        print()
