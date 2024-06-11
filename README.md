This project looks into some of the factors that affect weightlifting performance.

Using data stored in an SQLAlchemy database via a REST API, I'm looking into how:
- body weight
- sleep duration
- workout timing (morning or evening)
- performance supplement dosage and timing (pre or post-workout)
- 
impact power production during weightlifting sessions.

To ensure accuracy, I'm only analyzing exercises that fall within the hypertrophy and strength rep range (1 to 15), with both concentric and eccentric phases. 
This means no static holds or endurance exercises are included in my measurements.
To gauge the effectiveness of each exercise series, I'm using the Matt Brzycki formula, **weight / ( 1.0278 – 0.0278 × reps )**, to calculate the 1 rep max for each set and then finding the mean 1 rep max for the entire set.

For visualization, I'm employing Pandas and Matplotlib to plot each exercise series against the selected factors, allowing me to identify correlations and patterns that can inform better training strategies.
