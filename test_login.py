import requests

# Test login
print("Testing login...")
r = requests.post('http://localhost/api/auth/login', json={'email':'testuser@example.com','password':'TestPass123!'})
print(f"Status: {r.status_code}")
if r.status_code == 200:
    print("LOGIN WORKS!")
else:
    print(f"Failed: {r.json()}")

# Test login again (duplicate token test)
print("\nTesting login again...")
r2 = requests.post('http://localhost/api/auth/login', json={'email':'testuser@example.com','password':'TestPass123!'})
print(f"Status: {r2.status_code}")
if r2.status_code == 200:
    print("LOGIN AGAIN WORKS! No duplicate token error!")
else:
    print(f"Failed: {r2.json()}")
