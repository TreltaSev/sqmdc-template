// Switch to the "fbla" database
db = db.getSiblingDB("fbla");

// Create a user with readWrite access to that database
db.createUser({
  user: "{username}",
  pwd: "{password}",
  roles: [
    {
      role: "readWrite",
      db: "fbla"
    }
  ]
});
