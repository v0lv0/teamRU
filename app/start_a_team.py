from app.util import call_validate_endpoint, return_resp, call_auth_endpoint, get_name, format_string
from flask import request
from app.db import users, teams


def create_team(email, token):
    email = email.strip().lower()
    if call_validate_endpoint(email, token) == 200:
        if request.method == 'POST':
            data = request.get_json(silent=True)
            if not data or 'name' not in data or 'desc' not in data or 'skills' not in data or not data['name'] or not data['desc'] or not data['skills']:
                return {"statusCode": 400, "body": "Required info not found"}
            team_name = data['name'].strip().lower()
            team_desc = data['desc'].strip().lower()
            partner_skills = data['skills']
            formatted_skills = format_string(partner_skills)
            formatted_prizes = []
            if 'prizes' in data:
                prizes = data['prizes']
                formatted_prizes = format_string(prizes)
            team_exist = teams.find_one({"_id": str(team_name)})
            user_exists = users.find_one({"_id": email})
            if not user_exists:
                return return_resp(403, "Invalid user")
            if team_exist:
                return return_resp(401, "Invalid name")
            else:
                user_in_a_team = users.find_one({"_id": email, "hasateam": True})
                if user_in_a_team:
                    return return_resp(402, "User in a team")
                else:
                    users.update_one({"_id": email}, {"$set": {"hasateam": True}})
                    teams.insert({"_id": team_name, "members": [email], "desc": team_desc, "partnerskills": formatted_skills, "prizes": formatted_prizes, "complete": False, "interested": []})
                    return return_resp(200, "Success")
    else:
        return return_resp(404, "Invalid request")