from flask import Flask,render_template,request,redirect,url_for
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import rader
import bar
import json

app = Flask(__name__)



# Database Integration 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import session
import os
from werkzeug.utils import secure_filename

# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:18272610@localhost:5432/sentinova"
app.config['SQLALCHEMY_DATABASE_URI']="postgresql://avnadmin:AVNS_l6vR94I-x5zEg9OMKSl@sentinova-vedantpatel07756-b10e.d.aivencloud.com:10545/defaultdb?sslmode=require"
app.config['SECRET_KEY'] = 'mini_project'  # Replace with a secret key for form CSRF protection
app.config['UPLOAD_FOLDER'] = './application/static/upload/profileimg'  # Replace with the folder where you want to store uploaded files
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    email = db.Column(db.String(), unique=True)
    password = db.Column(db.String())
    avatar = db.Column(db.String())  # Store path to avatar image
    bio = db.Column(db.String())
    # Define one-to-many relationship with AnotherTable
    another_tables = db.relationship('AnotherTable', backref='user', lazy=True)
    def __repr__(self):
        return f'<User {self.name}>'
    


class AnotherTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    filename = db.Column(db.String())
    type = db.Column(db.String())
    avgno = db.Column(db.Float())
    positive = db.Column(db.Integer())
    negative = db.Column(db.Integer())
    neutral = db.Column(db.Integer())
    dataR = db.Column(db.String())
    dataB = db.Column(db.String())
    # Define foreign key relationship with User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
   

with app.app_context():
    db.create_all()










# Load CSV file containing tweets
# import os
# csv_file_path = os.path.abspath('./application/cooking.csv')
# df = pd.read_csv(csv_file_path)




# Custom dictionary of emojis with sentiment values
emoji_sentiments = {
    "😍": 1,
    "😊": 0.9,
    "😄": 0.8,
    "😐": 0.7,
    "😕": 0.6,
    "😞": 0.5,
    "😠": 0.4,
    "😡": 0.3,
    "😢": 0.2,
    "😭": 0.1
}

def analyze_vader_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_scores = analyzer.polarity_scores(text)
    vader_positive_score = sentiment_scores['pos']
    vader_negative_score = sentiment_scores['neg']
    vader_neutral_score = sentiment_scores['neu']
    vader_sentiment = sentiment_scores['compound']
    return vader_sentiment, vader_positive_score, vader_negative_score, vader_neutral_score

def analyze_emoji_sentiment(text):
    sentiment_score = 0
    emojis = [c for c in text if c in emoji_sentiments]
    for emoji in emojis:
        sentiment_score += emoji_sentiments[emoji]
    if sentiment_score > 0:
        return sentiment_score, "Positive"
    elif sentiment_score < 0:
        return sentiment_score, "Negative"
    else:
        return sentiment_score, "Neutral"


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template('register.html')
    elif request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        bio = request.form['bio']
        
        if 'avatar' not in request.files:
            return 'No file part'
        
        file = request.files['avatar']
        
        if file.filename == '':
            return 'No selected file'
        
        if not allowed_file(file.filename):
            return 'Invalid file type'
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        new_user = User(
            name=name,
            email=email,
            password=password,
            avatar=filepath,
            bio=bio
        )
        db.session.add(new_user)
        db.session.commit()
        print('User registered successfully!')
        return redirect(url_for('login'))
    
@app.route('/')      
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        if user:
            if user.password == password:
                # Store user information in session
                session['user_id'] = user.id
                session['user_name'] = user.name
                session['user_image'] = user.avatar
                # Successful login, redirect to dashboard or another page
                return redirect(url_for('dashboard'))
        
        # If login fails, render login page with error message
        error_message = 'Invalid email or password'
        return render_template('login.html', error_message=error_message)
    
    # Add a default return statement if the function ends without returning
    return render_template('login.html')  # or another appropriate response

    
@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        user_name = session['user_name']
        user_image = session['user_image']
        user_image = user_image.replace('\\', '/')
        user_image = user_image.replace('./application/static', '../static')
        
        # Query records from AnotherTable for the logged-in user
        user_records = AnotherTable.query.filter_by(user_id=user_id).all()

        print(f'User Record ={user_records}')

        return render_template('dashboard.html', user_name=user_name, user_image=user_image, user_records=user_records)
    else:
        # If user is not logged in, redirect to the login page
        return redirect(url_for('login'))


from flask import jsonify

@app.route('/delete/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    # Retrieve the record from the database
    record = AnotherTable.query.get_or_404(record_id)
    db.session.delete(record)
    db.session.commit()
    return jsonify({'message': 'Record deleted successfully'}), 200
# @app.route('/login')
# def login():
#     # Render the login page
#     return render_template('login.html')



# Render the HTML form for file upload
# @app.route('/')
# def upload_form():
#     return render_template('upload.html')

@app.route('/upload', methods=['POST','GET'])
def display_sentiment_analysis():
    if request.method=='GET':
        return render_template('upload.html')
    if request.method == 'POST':
        file = request.files['file']
        title = request.form['title']
        analysis_type = request.form['type']
        if file:
            # Read the CSV file
            df = pd.read_csv(file)

        # # Initialize variables to store aggregate sentiment scores
        # total_positive = 0
        # total_negative = 0
        # total_neutral = 0
        # total_tweets = len(df)

        # # Perform sentiment analysis for each tweet
        # for tweet in df['tweet']:
        #     vader_sentiment, vader_positive, vader_negative, vader_neutral = analyze_vader_sentiment(tweet)
        #     emoji_sentiment_score, _ = analyze_emoji_sentiment(tweet)
        #     average_sentiment = (vader_sentiment + emoji_sentiment_score) / 2

        #     # Aggregate sentiment scores
        #     total_positive += average_sentiment if average_sentiment > 0 else 0
        #     total_negative += abs(average_sentiment) if average_sentiment < 0 else 0
        #     total_neutral += 1 if average_sentiment == 0 else 0

        # # Calculate average sentiment scores
        # average_positive = total_positive / total_tweets
        # average_negative = total_negative / total_tweets
        # average_neutral = total_neutral / total_tweets
        # avg_all=(average_positive+average_negative+average_neutral)/3
    # Initialize variables to store aggregate sentiment scores
    total_positive = 0
    total_negative = 0
    total_neutral = 0
    total_tweets = len(df)

    # Perform sentiment analysis for each tweet
    for tweet in df['tweet']:
        vader_sentiment, vader_positive, vader_negative, vader_neutral = analyze_vader_sentiment(tweet)
        emoji_sentiment_score, _ = analyze_emoji_sentiment(tweet)
        average_sentiment = (vader_sentiment + emoji_sentiment_score) / 2

        # Aggregate sentiment scores
        total_positive += vader_positive
        total_negative += vader_negative
        total_neutral += vader_neutral

    # Calculate average sentiment scores
    average_positive = total_positive / total_tweets
    average_negative = total_negative / total_tweets
    average_neutral = total_neutral / total_tweets
    # average_positive = total_positive 
    # average_negative = total_negative 
    # average_neutral = total_neutral 
    avg_all=(average_positive+average_negative+average_neutral)/3
    # Render template with sentiment analysis results

    # Rader Data import 
    dataR=rader.raderdata(df)
    dataB=bar.bar_data(df)
    print(round(average_sentiment*100,2))

    user_id = session.get('user_id')
    print(f'User iD = {user_id}')

    # Serialize dictionary data to JSON strings
    dataR_json = json.dumps(dataR)
    dataB_json = json.dumps(dataB)

    print(f'dataR  = {dataR_json}')
    print(f'dataB  = {dataB_json}')
     # Save data to the database
    
    new_data = AnotherTable(
                title=title,
                filename=file.filename,
                type=analysis_type,
                avgno=round(avg_all*100,2),
                positive=total_positive,
                negative=total_negative,
                neutral=total_neutral,
                dataR=dataR_json,  # You need to define 'dataR' and 'dataB' variables
                dataB=dataB_json,
                user_id=user_id  # Assuming you have a current_user object
            )
    db.session.add(new_data)
    db.session.commit()


    return render_template("graph.html",
                           pos=round(average_positive * 100, 2),
                           neg=round(average_negative * 100, 2),
                           neu=round(average_neutral * 100, 2),
                           avg=round(avg_all*100,2),
                           dataR=dataR,
                           dataB=dataB)

if __name__ == "__main__":
    app.run(debug=True)




# # Example usage:
# text = "I hate the Movie and the acting of Super Hero is Bad"   
# text="I love the Movie and the acting of Super Hero is Awesome " 
# text="I love the Movie but the acting of Super Hero is super bad " 
# text="I love the Movie and the acting of Super Hero is Awesome 😍😍" 


# vader_sentiment, vader_positive, vader_negative, vader_neutral = analyze_vader_sentiment(text)
# emoji_sentiment_score, emoji_sentiment_label = analyze_emoji_sentiment(text)
# average_sentiment = (vader_sentiment + emoji_sentiment_score) / 2

# print("Sentiment with emojis (using Vader model):", vader_sentiment)
# print("Vader Positive Score:", vader_positive)
# print("Vader Negative Score:", vader_negative)
# print("Vader Neutral Score:", vader_neutral)
# print("Sentiment with emojis (custom sentiment analysis):", emoji_sentiment_score, emoji_sentiment_label)
# print("Average Sentiment:", average_sentiment*100) 

# @app.route("/")
# def hello_world():
#     return render_template("graph.html",pos=round(vader_positive*100,2),neg=round(vader_negative*100,2),neu=round(vader_neutral*100,2),avg=round(average_sentiment*100,2))



