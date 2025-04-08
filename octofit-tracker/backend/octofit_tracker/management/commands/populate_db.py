from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from django.conf import settings
from pymongo import MongoClient
from datetime import timedelta
from bson import ObjectId

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activities, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # Connect to MongoDB
        client = MongoClient(settings.DATABASES['default']['HOST'], settings.DATABASES['default']['PORT'])
        db = client[settings.DATABASES['default']['NAME']]

        # Drop existing collections
        db.users.drop()
        db.teams.drop()
        db.activity.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Clear existing User entries to avoid duplicate key errors
        User.objects.all().delete()

        # Save each user individually to ensure proper database association
        users = [
            User(email='thundergod@mhigh.edu', name='Thor Odinson', age=30),
            User(email='metalgeek@mhigh.edu', name='Tony Stark', age=35),
            User(email='zerocool@mhigh.edu', name='Steve Rogers', age=28),
            User(email='crashoverride@mhigh.edu', name='Natasha Romanoff', age=32),
            User(email='sleeptoken@mhigh.edu', name='Bruce Banner', age=40),
        ]
        for user in users:
            user.save()

        # Adjusted team creation to match the actual Team model fields
        team1 = Team(name='Blue Team')
        team2 = Team(name='Gold Team')
        team1.save()
        team2.save()

        # Add members to the teams
        for user in users:
            team1.members.add(user)

        # Adjusted activity creation to match the actual Activity model fields
        activities = [
            Activity(user=users[0], type='Cycling', duration=60, date='2025-04-08'),
            Activity(user=users[1], type='Crossfit', duration=120, date='2025-04-08'),
            Activity(user=users[2], type='Running', duration=90, date='2025-04-08'),
            Activity(user=users[3], type='Strength', duration=30, date='2025-04-08'),
            Activity(user=users[4], type='Swimming', duration=75, date='2025-04-08'),
        ]
        Activity.objects.bulk_create(activities)

        # Adjusted leaderboard creation to match the actual Leaderboard model fields
        leaderboard_entries = [
            Leaderboard(team=team1, points=100),
            Leaderboard(team=team2, points=90),
        ]
        Leaderboard.objects.bulk_create(leaderboard_entries)

        # Adjusted workout creation to match the actual Workout model fields
        workouts = [
            Workout(name='Cycling Training', description='Training for a road cycling event', duration=60),
            Workout(name='Crossfit', description='Training for a crossfit competition', duration=120),
            Workout(name='Running Training', description='Training for a marathon', duration=90),
            Workout(name='Strength Training', description='Training for strength', duration=30),
            Workout(name='Swimming Training', description='Training for a swimming competition', duration=75),
        ]
        Workout.objects.bulk_create(workouts)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))