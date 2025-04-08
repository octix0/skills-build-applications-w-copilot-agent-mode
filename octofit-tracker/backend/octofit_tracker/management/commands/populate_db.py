from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from bson import ObjectId
from datetime import timedelta

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activities, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # Clear existing data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Create users
        users = []
        user_data = [
            {'email': 'thundergod@mhigh.edu', 'name': 'Thor', 'age': 30},
            {'email': 'metalgeek@mhigh.edu', 'name': 'Tony Stark', 'age': 35},
            {'email': 'zerocool@mhigh.edu', 'name': 'Steve Rogers', 'age': 32},
            {'email': 'crashoverride@mhigh.edu', 'name': 'Natasha Romanoff', 'age': 28},
            {'email': 'sleeptoken@mhigh.edu', 'name': 'Bruce Banner', 'age': 40},
        ]
        for data in user_data:
            user = User.objects.create(**data)
            users.append(user)

        # Create teams
        team1 = Team(name='Blue Team')
        team2 = Team(name='Gold Team')
        team1.save()
        team2.save()

        # Add members to teams
        team1.members.set([users[0], users[1], users[2]])
        team2.members.set([users[3], users[4]])

        # Create activities
        activities = [
            Activity(user=users[0], type='Cycling', duration=60, date='2025-04-08'),
            Activity(user=users[1], type='Crossfit', duration=120, date='2025-04-07'),
            Activity(user=users[2], type='Running', duration=90, date='2025-04-06'),
            Activity(user=users[3], type='Strength', duration=30, date='2025-04-05'),
            Activity(user=users[4], type='Swimming', duration=75, date='2025-04-04'),
        ]
        Activity.objects.bulk_create(activities)

        # Create leaderboard entries
        leaderboard_entries = [
            Leaderboard(team=team1, points=100),
            Leaderboard(team=team2, points=90),
        ]
        Leaderboard.objects.bulk_create(leaderboard_entries)

        # Create workouts
        workouts = [
            Workout(name='Cycling Training', description='Training for a road cycling event', duration=60),
            Workout(name='Crossfit', description='Training for a crossfit competition', duration=120),
            Workout(name='Running Training', description='Training for a marathon', duration=90),
            Workout(name='Strength Training', description='Training for strength', duration=30),
            Workout(name='Swimming Training', description='Training for a swimming competition', duration=75),
        ]
        Workout.objects.bulk_create(workouts)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))