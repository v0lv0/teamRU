from flask import request

from src.flaskapp.util import format_string
from src.flaskapp.db import coll
from src.flaskapp.schemas import (
    ensure_json,
    ensure_user_logged_in,
    ensure_feature_is_enabled,
)


def create_team(team_name, email, team_desc, formatted_skills, formatted_prizes):
    """initialize team

       User creating a team

       Args:
           team_name: name of the team
           email: the email of the individual (already in a team) that wants other people to join his team recommendation
           team_desc: team description
           formatted_skills: Preferred skills for the team
           formatted_prizes: team goal/prize

       Return:
            response object(403:Invalid user, 401:Invalid name, 402:User In a team, 200: Success)
       """
    team_exist = coll("teams").find_one({"_id": str(team_name)})
    user_exists = coll("users").find_one({"_id": email})

    if not user_exists:
        return {"message": "Invalid user"}, 403
    if team_exist:
        return {"message": "Invalid name"}, 401
    else:
        user_in_a_team = coll("users").find_one({"_id": email, "hasateam": True})
        if user_in_a_team:
            return {"message": "User in a team"}, 402
        else:
            coll("users").update_one({"_id": email}, {"$set": {"hasateam": True}})
            coll("teams").insert(
                {
                    "_id": team_name,
                    "members": [email],
                    "desc": team_desc,
                    "partnerskills": formatted_skills,
                    "prizes": formatted_prizes,
                    "complete": False,
                    "incoming_inv": [],
                    "outgoing_inv": [],
                }
            )
            return {"message": "Success"}, 200