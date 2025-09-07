// Switch to the "{auth_db}" database
db = db.getSiblingDB("{auth_db}");

// Create a user with readWrite access to that database
db.createUser({
  user: "{username}",
  pwd: "{password}",
  roles: [
    {
      role: "readWrite",
      db: "{auth_db}"
    }
  ]
});
