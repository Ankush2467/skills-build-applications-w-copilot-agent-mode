from django.core.management.base import BaseCommand
from django.conf import settings
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']

        # Clear existing data
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Create unique index on email
        db.users.create_index([('email', 1)], unique=True)

        # Teams
        marvel = {'name': 'Team Marvel', 'description': 'Marvel superheroes'}
        dc = {'name': 'Team DC', 'description': 'DC superheroes'}
        marvel_id = db.teams.insert_one(marvel).inserted_id
        dc_id = db.teams.insert_one(dc).inserted_id

        # Users
        users = [
            {'name': 'Iron Man', 'email': 'ironman@marvel.com', 'team_id': marvel_id},
            {'name': 'Captain America', 'email': 'cap@marvel.com', 'team_id': marvel_id},
            {'name': 'Batman', 'email': 'batman@dc.com', 'team_id': dc_id},
            {'name': 'Wonder Woman', 'email': 'wonderwoman@dc.com', 'team_id': dc_id},
        ]
        user_ids = db.users.insert_many(users).inserted_ids

        # Activities
        activities = [
            {'user_id': user_ids[0], 'type': 'run', 'distance': 5, 'duration': 30},
            {'user_id': user_ids[1], 'type': 'cycle', 'distance': 20, 'duration': 60},
            {'user_id': user_ids[2], 'type': 'swim', 'distance': 2, 'duration': 40},
            {'user_id': user_ids[3], 'type': 'yoga', 'duration': 50},
        ]
        db.activities.insert_many(activities)

        # Leaderboard
        leaderboard = [
            {'user_id': user_ids[0], 'points': 100},
            {'user_id': user_ids[1], 'points': 90},
            {'user_id': user_ids[2], 'points': 110},
            {'user_id': user_ids[3], 'points': 95},
        ]
        db.leaderboard.insert_many(leaderboard)

        # Workouts
        workouts = [
            {'name': 'Full Body Blast', 'suggested_for': 'all'},
            {'name': 'Hero HIIT', 'suggested_for': 'advanced'},
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
