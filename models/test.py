import unittest
import joblib
import numpy as np
from pipeline_generator import train_user_user, train_item_item, predict

class TestUserItemPipelines(unittest.TestCase):
    
    def setUp(self):
        """Train models before testing."""
        self.k = 5
        train_user_user(self.k)
        train_item_item(self.k)
    
    def test_user_user_model_exists(self):
        """Check if the User-User model file is created."""
        model = joblib.load("user_user_model.joblib")
        self.assertIn("cosine", model)
        self.assertIn("pearson", model)
        self.assertIn("jaccard", model)
    
    def test_item_item_model_exists(self):
        """Check if the Item-Item model file is created."""
        model = joblib.load("item_item_model.joblib")
        self.assertIn("cosine", model)
        self.assertIn("pearson", model)
        self.assertIn("jaccard", model)
    
    def test_user_user_prediction(self):
        """Test User-User prediction using Cosine similarity."""
        recommendations = predict("user_user_model.joblib", id_usuario=1, k=self.k, similarity="cosine")
        self.assertEqual(len(recommendations), self.k)
    
    def test_item_item_prediction(self):
        """Test Item-Item prediction using Pearson similarity."""
        recommendations = predict("item_item_model.joblib", id_usuario=1, k=self.k, similarity="pearson")
        self.assertEqual(len(recommendations), self.k)
    
    def test_jaccard_prediction(self):
        """Test Jaccard similarity prediction for User-User model."""
        recommendations = predict("user_user_model.joblib", id_usuario=1, k=self.k, similarity="jaccard")
        self.assertEqual(len(recommendations), self.k)
    
if __name__ == "__main__":
    unittest.main()
