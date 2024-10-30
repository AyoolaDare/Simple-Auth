# My First Cloud Project: User Login System 🚀

Here is my step on my Simple Authentication system! 

## What Are We Building? 🤔
We're making a simple website where:
- Users can create new accounts
- Log in with their username and password 
- See a welcome page after logging in

It's like making a super basic version of logging into your email!

## The Building Blocks 🏗️

### Frontend (The Stuff We See)
We have three main pages:
1. `login.html` - Where you sign in
2. `index.html` - Where new users create accounts
3. `dashboard.html` - The welcome page you see after logging in

We also have:
- `scripts.js` - Makes buttons work and handles clicking
- `style.css` - Makes everything look pretty!

### Backend (The Magic Behind the Scenes)
We're using AWS (Amazon's cloud) to make everything work:

#### 1. AWS Lambda (Our Little Cloud Helpers)
Think of these as little workers in the cloud:
- One worker handles new sign-ups
- Another worker checks if your password is correct
- A third worker gets your information after you log in

#### 2. DynamoDB (Our Cloud Notebook)
- Like a big spreadsheet that remembers everyone's:
  - Username
  - Email
  - Password

#### 3. API Gateway (Our Traffic Director)
- When someone tries to do something on our website, API Gateway tells them where to go:
  - Want to sign up? → Go to the sign-up worker
  - Want to log in? → Go to the login worker
  - Want your info? → Go to the info worker

## How to Set Everything Up 🛠️

### Before We Start
You'll need:
- An AWS account (like having an Amazon account, but for cloud stuff!)
- Some basic AWS knowledge (we'll learn together!)

### Step-by-Step Guide

1. **Setting Up Our Cloud Workers (AWS Lambda & API Gateway)**
   - Create three Lambda functions (our workers)
   - Set up API Gateway (our traffic director)
   - Save the website address in our code

2. **Creating Our Storage (DynamoDB)**
   - Make a new table called `Users`
   - Make sure `username` is our main way to find users

3. **Getting Our Website Ready**
   - Put our pages together
   - Make sure our code can talk to AWS

## How to Use It 🎮

1. **Creating a New Account**
   - Go to the home page
   - Fill in your username, email, and password
   - Click submit!

2. **Logging In**
   - Go to the login page
   - Type your username and password
   - Click login
   - You should see your dashboard!

3. **Logging Out**
   - Just click the logout button on your dashboard

## Help! Something's Wrong! 🆘

If things aren't working:
- **Getting 404 errors?** Make sure API Gateway is set up right
- **DynamoDB problems?** Check if your table exists
- **Not sure what's wrong?** Look at your browser's console (press F12)

## Learning Notes 📝
- Take it slow! Cloud stuff can be tricky at first
- Don't worry if you make mistakes - we all do!
- Try breaking things on purpose to learn how they work

Remember: Everyone starts somewhere! If you're confused, that's totally normal. Keep experimenting and learning! 🌟
