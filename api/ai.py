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

    Example output:
    {
        1: [
            {"time_minutes": 20, "activity": "Read OOP theory"},
            {"time_minutes": 40, "activity": "Practice coding"},
        ],
        2: [
            {"time_minutes": 30, "activity": "Review OOP patterns"},
            {"time_minutes": 30, "activity": "Work on a small project"},
        ],
        3: [
            {"time_minutes": 20, "activity": "Watch an OOP tutorial"},
            {"time_minutes": 40, "activity": "Apply concepts to a coding challenge"},
        ]
    }
    """


if __name__ == '__main__':
    import sys

    if len(sys.argv) != 5:
        print('Usage: python ai.py <goals> <days> <time_per_day> <preferred_topics>')
        sys.exit(1)
    goals, days, time_per_day = sys.argv[1:4]
    days = int(days)
    time_per_day = int(time_per_day)
    topics = sys.argv[4].split(',')
    plan = create_study_plan(
        StudyPlanInput(
            goals=goals, days=days, time_per_day=time_per_day, preferred_topics=topics
        )
    )
    for week_day in plan.study_plan:
        print(f'Day {week_day.day}:')
        for activity in week_day.activities:
            print(f' - {activity.activity} ({activity.time_minutes} minutes)')
        print()
