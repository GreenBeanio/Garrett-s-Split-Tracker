# Creating the tracker page
@auth_bp.route("/tracker/<string:username>")
def showTracker(username):
    return f"User is {escape(username)}"


# Creating the specific tracked activity page
@auth_bp.route("/tracker/<string:username>/<string:activity>")
def showTrackedActivity(username, activity):
    return f"User is {escape(username)} for the activity {escape(activity)}"
