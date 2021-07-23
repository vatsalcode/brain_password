USER_RETRIEVED = "User retrieved successfully"
USER_CREATED = "User registered successfully"
USER_UPDATED = "User updated successfully"
USER_NOT_RECOGNIZED = "User not recognized"
USER_RECOGNIZED = "User recognized successfully"
USER_DELETED = lambda email: "User with email: {} deleted successfully".format(email)
USER_NOT_FOUND = lambda user_id: "User with UserID: {} does not exist".format(user_id)
USER_ALREADY_EXISTS = lambda email: "User with email: {} already exists".format(email)


EEG_RECORDINGS_RETRIEVED = lambda user_id: "EEG Recordings for UserID: {} retrieved successfully".format(user_id)
EEG_RECORDINGS_CREATED = lambda user_id: "EEG Recordings for UserID: {} registered successfully".format(user_id)
EEG_RECORDINGS_UPDATED = lambda user_id: "EEG Recordings for UserID: {} updated successfully".format(user_id)
EEG_RECORDINGS_DELETED = lambda user_id: "EEG Recordings for UserID: {} deleted successfully".format(user_id)


INTERNAL_SERVER_ERROR = "Internal Server Error"