"""
Restaurant Recommendation Module
Hybrid approach: K-Means (Content-Based) + KNN (Collaborative Filtering)
"""
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from typing import List, Dict, Optional
import os

class RestaurantRecommender:
    """
    Restaurant recommendation system using hybrid approach
    """
    
    def __init__(self, data_path: Optional[str] = None):
        """
        Initialize restaurant recommender
        
        Args:
            data_path: Path to restaurant dataset (Yelp or alternative)
        """
        self.data_path = data_path or 'yelp_dataset/'
        self.restaurants_df = None
        self.kmeans_model = None
        self.knn_model = None
        self.scaler = StandardScaler()
        
    def load_data(self) -> bool:
        """
        Load restaurant data
        Tries Yelp dataset first, falls back to alternative sources
        """
        # Try to load Yelp dataset
        yelp_path = os.path.join(self.data_path, 'yelp_academic_dataset_business.json')
        if os.path.exists(yelp_path):
            try:
                self.restaurants_df = pd.read_json(yelp_path, lines=True)
                # Filter for restaurants
                if 'categories' in self.restaurants_df.columns:
                    self.restaurants_df = self.restaurants_df[
                        self.restaurants_df['categories'].str.contains('Restaurant', case=False, na=False)
                    ]
                print(f"✓ Loaded {len(self.restaurants_df)} restaurants from Yelp dataset")
                return True
            except Exception as e:
                print(f"⚠️  Error loading Yelp data: {e}")
        
        # Fallback: Create sample restaurant data from attractions/hotels data
        print("⚠️  Yelp dataset not found. Creating sample restaurant data...")
        self._create_sample_data()
        return True
    
    def _create_sample_data(self):
        """
        Create sample restaurant data from existing datasets
        This is a fallback when Yelp data is not available
        """
        # Use existing data to create restaurant-like recommendations
        # In a real scenario, you'd have actual restaurant data
        sample_restaurants = []
        
        # Try to extract restaurant-like places from attractions
        try:
            att_df = pd.read_json('etl/attractions.json', orient='records')
            food_related = att_df[att_df['category'].str.contains('food|dining|restaurant', case=False, na=False)]
            
            for _, row in food_related.head(50).iterrows():
                sample_restaurants.append({
                    'name': row.get('name', 'Restaurant'),
                    'latitude': row.get('latitude', 0),
                    'longitude': row.get('longitude', 0),
                    'rating': row.get('rating', 4.0),
                    'price': row.get('price', 50),
                    'category': 'Restaurant',
                    'cuisine': 'Local',
                    'city': row.get('city', 'Unknown')
                })
        except:
            pass
        
        if not sample_restaurants:
            # Create minimal sample data
            sample_restaurants = [
                {'name': f'Restaurant {i}', 'latitude': 49.0 + i*0.1, 'longitude': -123.0 + i*0.1,
                 'rating': 4.0 + (i % 3) * 0.5, 'price': 20 + i*5, 'category': 'Restaurant',
                 'cuisine': ['Italian', 'Chinese', 'Mexican', 'Indian', 'French'][i % 5],
                 'city': 'Vancouver'}
                for i in range(20)
            ]
        
        self.restaurants_df = pd.DataFrame(sample_restaurants)
        print(f"✓ Created {len(self.restaurants_df)} sample restaurants")
    
    def train_models(self):
        """
        Train K-Means and KNN models
        """
        if self.restaurants_df is None or len(self.restaurants_df) == 0:
            print("⚠️  No restaurant data available")
            return
        
        # Prepare features
        features = ['latitude', 'longitude', 'rating', 'price']
        available_features = [f for f in features if f in self.restaurants_df.columns]
        
        if len(available_features) < 2:
            print("⚠️  Insufficient features for training")
            return
        
        X = self.restaurants_df[available_features].fillna(0)
        X_scaled = self.scaler.fit_transform(X)
        
        # Train K-Means for content-based filtering
        n_clusters = min(5, len(self.restaurants_df) // 3)
        if n_clusters > 0:
            self.kmeans_model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            self.restaurants_df['cluster'] = self.kmeans_model.fit_predict(X_scaled)
        
        # Train KNN for collaborative filtering
        if len(self.restaurants_df) > 5:
            self.knn_model = NearestNeighbors(n_neighbors=min(5, len(self.restaurants_df)), 
                                             metric='euclidean')
            self.knn_model.fit(X_scaled)
        
        print("✓ Restaurant models trained")
    
    def recommend_by_meal(self, city: str, meal_type: str, budget: float, 
                         cuisine_preference: Optional[str] = None, 
                         num_recommendations: int = 2) -> List[Dict]:
        """
        Recommend restaurants for a specific meal
        
        Args:
            city: City name
            meal_type: 'breakfast', 'lunch', 'dinner'
            budget: Budget per meal
            cuisine_preference: Preferred cuisine type
            num_recommendations: Number of recommendations
        
        Returns:
            List of restaurant recommendations
        """
        if self.restaurants_df is None:
            self.load_data()
            self.train_models()
        
        if self.restaurants_df is None or len(self.restaurants_df) == 0:
            return []
        
        # Filter by city and budget
        filtered = self.restaurants_df.copy()
        
        if 'city' in filtered.columns:
            filtered = filtered[filtered['city'].str.contains(city, case=False, na=False)]
        
        if 'price' in filtered.columns:
            filtered = filtered[filtered['price'] <= budget]
        
        if cuisine_preference and 'cuisine' in filtered.columns:
            filtered = filtered[filtered['cuisine'].str.contains(cuisine_preference, case=False, na=False)]
        
        if len(filtered) == 0:
            # Fallback to all restaurants
            filtered = self.restaurants_df.copy()
        
        # Sort by rating and price
        if 'rating' in filtered.columns:
            filtered = filtered.sort_values('rating', ascending=False)
        
        # Select top recommendations
        recommendations = filtered.head(num_recommendations)
        
        result = []
        for _, restaurant in recommendations.iterrows():
            result.append({
                'name': restaurant.get('name', 'Restaurant'),
                'latitude': restaurant.get('latitude', 0),
                'longitude': restaurant.get('longitude', 0),
                'rating': restaurant.get('rating', 4.0),
                'price': restaurant.get('price', 50),
                'cuisine': restaurant.get('cuisine', 'Local'),
                'meal_type': meal_type,
                'city': city
            })
        
        return result
    
    def recommend_for_trip(self, city: str, days: int, daily_budget: float,
                          cuisine_preferences: Optional[List[str]] = None) -> Dict:
        """
        Recommend restaurants for entire trip
        
        Args:
            city: City name
            days: Number of days
            daily_budget: Budget per day
            cuisine_preferences: List of preferred cuisines
        
        Returns:
            Dictionary with meal recommendations for each day
        """
        meal_budget = daily_budget / 3  # Divide by 3 meals
        recommendations = {}
        
        meals = ['breakfast', 'lunch', 'dinner']
        cuisines = cuisine_preferences or ['Local', 'Italian', 'Asian', 'American', 'Mexican']
        
        for day in range(1, days + 1):
            day_recommendations = {}
            for meal in meals:
                cuisine = cuisines[day % len(cuisines)]  # Rotate cuisines
                day_recommendations[meal] = self.recommend_by_meal(
                    city, meal, meal_budget, cuisine, num_recommendations=2
                )
            recommendations[f'Day {day}'] = day_recommendations
        
        return recommendations

